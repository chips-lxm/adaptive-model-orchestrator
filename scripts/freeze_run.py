#!/usr/bin/env python3
"""Pin the runtime resources of one skill without modifying its installation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil

RUNTIME = ("SKILL.md", "README.md", "README.zh-CN.md", "LICENSE",
           "agents", "references", "scripts", "examples", "assets")
MANIFEST = "snapshot.json"
RELEASE = "runtime-manifest.json"


def inventory(root):
    root = Path(root).resolve()
    files = {}
    for name in RUNTIME:
        entry = root / name
        if not entry.exists() and not entry.is_symlink():
            continue
        pending = [entry]
        while pending:
            path = pending.pop()
            if path.name in ("__pycache__", ".DS_Store") or path.suffix in (".pyc", ".pyo"):
                continue
            if path.is_symlink():
                raise ValueError(f"Runtime symlinks must be resolved explicitly: {path}")
            if path.is_dir():
                pending.extend(path.iterdir())
            elif path.is_file():
                files[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
            else:
                raise ValueError(f"Unsupported runtime resource: {path}")
    if "SKILL.md" not in files:
        raise ValueError("Missing SKILL.md")
    return dict(sorted(files.items()))


def digest(files):
    data = json.dumps(files, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def is_discovery_path(path):
    parts = path.parts
    if any(part in (".codex", ".agents") and "skills" in parts[index + 1:]
           for index, part in enumerate(parts)):
        return True
    codex_root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).resolve()
    if path == codex_root or codex_root in path.parents:
        return "skills" in path.relative_to(codex_root).parts
    return False


def check_record(record, files):
    if not isinstance(record, dict) or record.get("format") != 1 or record.get("files") != files or record.get("digest") != digest(files):
        raise ValueError("Runtime content differs from its manifest")


def seal(source):
    """Maintainer operation after intentional edits; never an automatic repair."""
    source = Path(source).resolve()
    files = inventory(source)
    record = {"format": 1, "digest": digest(files), "files": files}
    (source / RELEASE).write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"release_manifest": str(source / RELEASE), "digest": record["digest"]}


def release_bytes(root, files):
    raw = (Path(root) / RELEASE).read_bytes()
    check_record(json.loads(raw), files)
    return raw


def verify(destination):
    destination = Path(destination).resolve()
    record = json.loads((destination / MANIFEST).read_text(encoding="utf-8"))
    actual = inventory(destination)
    check_record(record, actual)
    release_bytes(destination, actual)
    return {"skill_file": str(destination / "SKILL.md"), "digest": record["digest"],
            "files": len(actual), "verified": True}


def freeze(source, destination):
    source = Path(source).resolve()
    destination = Path(destination).expanduser().resolve()
    if destination == source or source in destination.parents or is_discovery_path(destination):
        raise ValueError("Use a non-discoverable output directory outside the source skill")
    before = inventory(source)
    release = release_bytes(source, before)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation protects any existing snapshot, even an empty directory.
    destination.mkdir()
    try:
        for name in before:
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, target)
        if inventory(destination) != before or inventory(source) != before:
            raise ValueError("Source changed during snapshot creation; retry from a stable version")
        if release_bytes(source, before) != release:
            raise ValueError("Release manifest changed during snapshot creation")
        (destination / RELEASE).write_bytes(release)
        record = {"format": 1, "digest": digest(before), "files": before,
                  "excluded": "Git, project-maintenance documents, historical tests and caches"}
        (destination / MANIFEST).write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return verify(destination)
    except Exception:
        shutil.rmtree(destination)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--output", type=Path, help="New directory outside skill discovery roots")
    action.add_argument("--verify", type=Path, help="Existing frozen skill directory")
    action.add_argument("--seal", action="store_true", help="Maintainer only: rebuild runtime manifest after intentional edits")
    args = parser.parse_args()
    try:
        source = Path(__file__).resolve().parents[1]
        if args.seal:
            result = seal(source)
        else:
            result = verify(args.verify) if args.verify else freeze(source, args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Snapshot failed: {exc}\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
