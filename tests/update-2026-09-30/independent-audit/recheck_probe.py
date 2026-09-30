"""Focused independent check of the expected-runtime-manifest changes."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
from unittest import mock

ROOT = Path('/private/tmp/skill-astra-20260930')
PYTHON = '/Users/lxm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
results = {}

def rejected(call, kind=(ValueError, FileNotFoundError)):
    try:
        call()
    except kind as error:
        return type(error).__name__ + ': ' + str(error)
    raise AssertionError('Expected rejection, but call succeeded')

for name in ('adaptive-model-orchestrator', 'deep-project-review'):
    source = Path('/Users/lxm/app1/github-preview') / name
    spec = importlib.util.spec_from_file_location(name, source / 'scripts/freeze_run.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    before = module.inventory(source)
    release_before = (source / module.RELEASE).read_bytes()
    with tempfile.TemporaryDirectory(dir=ROOT / 'tmp') as temporary:
        temporary = Path(temporary)
        real = module.freeze(source, temporary / 'real')
        copied_verify = subprocess.run([PYTHON, '-B', str(temporary / 'real/scripts/freeze_run.py'), '--verify', str(temporary / 'real')], capture_output=True, text=True)
        assert copied_verify.returncode == 0, copied_verify.stderr
        assert (temporary / 'real' / module.RELEASE).read_bytes() == release_before

        fixture = temporary / 'fixture'
        fixture.mkdir()
        (fixture / 'references').mkdir()
        (fixture / 'SKILL.md').write_text('v1 rules')
        (fixture / 'references/rules.md').write_text('v1 reference')
        module.seal(fixture)
        old_release = (fixture / module.RELEASE).read_bytes()
        (fixture / 'SKILL.md').write_text('v2 rules')
        partial = rejected(lambda: module.freeze(fixture, temporary / 'partial'))
        assert not (temporary / 'partial').exists()
        assert (fixture / module.RELEASE).read_bytes() == old_release
        (fixture / module.RELEASE).unlink()
        missing = rejected(lambda: module.freeze(fixture, temporary / 'missing'))
        assert not (fixture / module.RELEASE).exists()
        (fixture / 'references/rules.md').write_text('v2 reference')
        module.seal(fixture)
        complete = module.freeze(fixture, temporary / 'complete')
        (temporary / 'complete' / module.RELEASE).write_text('{}')
        frozen_release = rejected(lambda: module.verify(temporary / 'complete'))

        original_copy = module.shutil.copy2
        def copying(src, dst):
            result = original_copy(src, dst)
            if Path(src).name == 'SKILL.md':
                release_path = fixture / module.RELEASE
                release_path.write_bytes(release_path.read_bytes() + b'\n')
            return result
        with mock.patch.object(module.shutil, 'copy2', side_effect=copying):
            manifest_changed = rejected(lambda: module.freeze(fixture, temporary / 'manifest-drift'))
        assert not (temporary / 'manifest-drift').exists()

        plugin = rejected(lambda: module.freeze(source, temporary / '.codex/plugins/cache/example/1.0/skills/copy'))
        with mock.patch.dict(os.environ, {'CODEX_HOME': str(temporary / 'custom')}):
            custom = rejected(lambda: module.freeze(source, temporary / 'custom/plugins/cache/example/1.0/skills/copy'))
        results[name] = {
            'runtime_digest': module.digest(before),
            'release_sha256': hashlib.sha256(release_before).hexdigest(),
            'real_snapshot_verified': real['verified'],
            'copied_verifier_exit': copied_verify.returncode,
            'partial_install_rejection': partial,
            'missing_manifest_rejection': missing,
            'explicitly_sealed_complete_update_accepted': complete['verified'],
            'corrupted_frozen_release_rejection': frozen_release,
            'manifest_change_during_copy_rejection': manifest_changed,
            'plugin_destination_rejection': plugin,
            'custom_codex_home_plugin_rejection': custom,
            'source_runtime_unchanged': module.inventory(source) == before,
            'source_release_unchanged': (source / module.RELEASE).read_bytes() == release_before,
        }
(ROOT / 'recheck-results.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
