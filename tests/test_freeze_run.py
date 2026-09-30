"""Behavioral checks for stable snapshots, drift, and existing-user-data preservation."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SPEC = importlib.util.spec_from_file_location("freeze_run", Path(__file__).resolve().parents[1] / "scripts" / "freeze_run.py")
snapshot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(snapshot)


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text("original rules", encoding="utf-8")
        (self.source / "references").mkdir()
        (self.source / "references" / "rules.md").write_text("original reference", encoding="utf-8")
        snapshot.seal(self.source)
        self.output = self.root / "run" / "frozen"

    def test_snapshot_stays_on_old_version_and_excludes_history(self):
        for name in ("tests", ".git"):
            (self.source / name).mkdir()
            (self.source / name / "private.txt").write_text("not runtime")
        first = snapshot.freeze(self.source, self.output)
        (self.source / "SKILL.md").write_text("new rules")
        self.assertEqual(snapshot.verify(self.output)["digest"], first["digest"])
        self.assertEqual((self.output / "SKILL.md").read_text(), "original rules")
        self.assertFalse((self.output / "tests").exists())
        self.assertFalse((self.output / ".git").exists())

    def test_existing_output_is_never_overwritten(self):
        self.output.mkdir(parents=True)
        sentinel = self.output / "user-data"
        sentinel.write_text("keep")
        with self.assertRaises(FileExistsError):
            snapshot.freeze(self.source, self.output)
        self.assertEqual(sentinel.read_text(), "keep")

    def test_changed_added_or_missing_reference_invalidates_snapshot(self):
        snapshot.freeze(self.source, self.output)
        reference = self.output / "references" / "rules.md"
        for operation in ("change", "delete", "add"):
            with self.subTest(operation=operation):
                reference.write_text("original reference")
                extra = self.output / "references" / "extra.md"
                extra.unlink(missing_ok=True)
                if operation == "change":
                    reference.write_text("altered")
                elif operation == "delete":
                    reference.unlink()
                else:
                    extra.write_text("extra rules")
                with self.assertRaises(ValueError):
                    snapshot.verify(self.output)

    def test_runtime_symlinks_are_not_followed(self):
        (self.source / "references" / "outside").symlink_to(self.root)
        with self.assertRaises(ValueError):
            snapshot.freeze(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_discoverable_and_recursive_destinations_are_rejected(self):
        for target in (self.source / "nested", self.root / ".codex" / "skills" / "new", self.root / ".agents" / "skills" / "new", self.root / ".codex" / "plugins" / "cache" / "plugin" / "skills" / "new"):
            with self.subTest(target=target), self.assertRaises(ValueError):
                snapshot.freeze(self.source, target)
        with mock.patch.dict("os.environ", {"CODEX_HOME": str(self.root / "custom")}):
            for target in (self.root / "custom" / "skills" / "new", self.root / "custom" / "plugins" / "cache" / "plugin" / "skills" / "new"):
                with self.subTest(target=target), self.assertRaises(ValueError):
                    snapshot.freeze(self.source, target)

    def test_concurrent_source_change_rejects_mixed_snapshot(self):
        original_copy = snapshot.shutil.copy2
        def copying(source, target):
            result = original_copy(source, target)
            if Path(source).name == "SKILL.md":
                (self.source / "references" / "rules.md").write_text("changed concurrently")
            return result
        with mock.patch.object(snapshot.shutil, "copy2", side_effect=copying):
            with self.assertRaises(ValueError):
                snapshot.freeze(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_manifest_digest_is_checked(self):
        snapshot.freeze(self.source, self.output)
        path = self.output / snapshot.MANIFEST
        record = json.loads(path.read_text())
        record["digest"] = "wrong"
        path.write_text(json.dumps(record))
        with self.assertRaises(ValueError):
            snapshot.verify(self.output)

    def test_stable_partial_install_is_rejected(self):
        (self.source / "SKILL.md").write_text("new entrypoint with old reference")
        with self.assertRaises(ValueError):
            snapshot.freeze(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_missing_release_manifest_is_not_silently_rebuilt(self):
        (self.source / snapshot.RELEASE).unlink()
        with self.assertRaises(FileNotFoundError):
            snapshot.freeze(self.source, self.output)
        self.assertFalse((self.source / snapshot.RELEASE).exists())

    def test_invalid_manifest_shape_fails_cleanly(self):
        snapshot.freeze(self.source, self.output)
        (self.output / snapshot.MANIFEST).write_text('[]')
        with self.assertRaises(ValueError):
            snapshot.verify(self.output)


if __name__ == "__main__":
    unittest.main()
