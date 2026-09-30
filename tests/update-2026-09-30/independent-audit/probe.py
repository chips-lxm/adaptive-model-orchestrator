"""Independent snapshot probes; no repository or installed-file writes."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path('/private/tmp/skill-astra-20260930')
PYTHON = '/Users/lxm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
results = {}
for name in ('adaptive-model-orchestrator', 'deep-project-review'):
    source = Path('/Users/lxm/app1/github-preview') / name
    spec = importlib.util.spec_from_file_location(name, source / 'scripts/freeze_run.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    baseline = module.inventory(source)
    with tempfile.TemporaryDirectory(dir=ROOT / 'tmp') as tmp:
        tmp = Path(tmp)
        real = module.freeze(source, tmp / 'real-snapshot')
        subprocess_result = subprocess.run(
            [PYTHON, '-B', str(tmp / 'real-snapshot/scripts/freeze_run.py'), '--verify', str(tmp / 'real-snapshot')],
            text=True, capture_output=True, check=False)
        fixture = tmp / 'partially-installed'
        fixture.mkdir()
        (fixture / 'references').mkdir()
        (fixture / 'SKILL.md').write_text('version 2 rules; see references/rules.md\n')
        (fixture / 'references/rules.md').write_text('version 1 reference\n')
        hybrid = module.freeze(fixture, tmp / 'hybrid-snapshot')
        results[name] = {
            'source_digest': module.digest(baseline),
            'source_files': baseline,
            'real_snapshot': real,
            'frozen_script_verify_exit': subprocess_result.returncode,
            'frozen_script_verify_stdout': subprocess_result.stdout.strip(),
            'source_unchanged_after': module.inventory(source) == baseline,
            'stable_partial_install_accepted': hybrid['verified'],
            'partial_install_explanation': 'v2 SKILL plus v1 reference already present before freeze. This tests release coherence, not copy-time byte stability.',
        }

(ROOT / 'probe-results.json').write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({k: {a: b for a, b in v.items() if a not in ('source_files',)} for k, v in results.items()}, indent=2))
