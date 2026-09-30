"""Capture bounded source validation; run with the prepared Python/PyYAML environment."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib
from urllib.parse import unquote, urlsplit
import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--validator', type=Path, required=True)
    parser.add_argument('--git', required=True)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    out = root / 'tests/update-2026-09-30'
    out.mkdir(parents=True, exist_ok=True)
    commands = []

    def run(command):
        result = subprocess.run(command, cwd=root, capture_output=True, text=True)
        record = {'command': command, 'cwd': str(root), 'exit_code': result.returncode,
                  'stdout': result.stdout, 'stderr': result.stderr}
        commands.append(record)
        if result.returncode:
            (out / 'validation-commands.json').write_text(json.dumps(commands, indent=2) + '\n')
            raise RuntimeError(record)
        return result

    run([sys.executable, '-B', str(args.validator), str(root)])
    tests = run([sys.executable, '-B', 'tests/test_freeze_run.py'])
    count = int(re.search(r'Ran (\d+) tests', tests.stderr).group(1))
    frontmatter = (root / 'SKILL.md').read_text().split('---', 2)[1]
    skill = yaml.safe_load(frontmatter)
    ui = yaml.safe_load((root / 'agents/openai.yaml').read_text())
    assert skill['name'] == root.name
    assert skill['metadata']['revision'] == '2026-09-30'
    expected_policy = root.name == 'adaptive-model-orchestrator'
    assert ui['policy']['allow_implicit_invocation'] is expected_policy
    assert 25 <= len(ui['interface']['short_description']) <= 64
    config = root / 'examples/astra-reviewer.toml'
    if config.exists():
        agent = tomllib.loads(config.read_text())
        assert agent['model'] == 'gpt-6-astra'
        assert agent['model_reasoning_effort'] == 'xhigh'

    checked, errors = [], []
    docs = list(root.glob('*.md'))
    for folder in ('references', 'docs', 'examples'):
        docs.extend((root / folder).rglob('*.md'))
    for path in sorted(docs):
        text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            target = target.strip('<>')
            if urlsplit(target).scheme or target.startswith('#'):
                continue
            local = unquote(target.split('#', 1)[0])
            if not local:
                continue
            checked.append({'file': str(path.relative_to(root)), 'target': target})
            if not (path.parent / local).exists():
                errors.append(checked[-1])
    assert not errors, errors

    spec = importlib.util.spec_from_file_location('freeze_run', root / 'scripts/freeze_run.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    inventory = helper.inventory(root)
    helper.release_bytes(root, inventory)
    with tempfile.TemporaryDirectory(prefix='skill-final-20260930-') as temp:
        destination = Path(temp) / 'snapshot'
        created = run([sys.executable, '-B', 'scripts/freeze_run.py', '--output', str(destination)])
        verified = run([sys.executable, '-B', str(destination / 'scripts/freeze_run.py'), '--verify', str(destination)])
        actual = json.loads(verified.stdout)
        assert actual['digest'] == helper.digest(inventory)
        smoke = {'create_exit': created.returncode, 'verify_exit': verified.returncode,
                 'files': actual['files'], 'digest': actual['digest'],
                 'copied_script_verified_snapshot': True,
                 'release_manifest_copied_exactly': (root / helper.RELEASE).read_bytes() == (destination / helper.RELEASE).read_bytes(),
                 'snapshot_location': 'temporary directory, removed after test'}
    run([args.git, 'diff', '--check'])
    static = {'format_validator': 'passed', 'yaml_policy': expected_policy,
              'yaml_and_toml': 'passed', 'local_links_checked': len(checked),
              'local_link_scope': 'Current root, reference, documentation and example Markdown; file targets only, no external URLs or anchors',
              'link_errors': errors, 'snapshot_unit_tests': {'tests': count, 'exit_code': 0},
              'runtime_digest': helper.digest(inventory), 'runtime_file_hashes': inventory,
              'release_manifest_sha256': hashlib.sha256((root / helper.RELEASE).read_bytes()).hexdigest()}
    for name, data in [('static-checks.json', static), ('snapshot-smoke.json', smoke),
                       ('validation-commands.json', commands)]:
        (out / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'skill': root.name, 'format': 'passed', 'tests': count,
                      'links': len(checked), 'snapshot': 'passed', 'digest': helper.digest(inventory)}))


if __name__ == '__main__':
    main()
