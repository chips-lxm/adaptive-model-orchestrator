"""Check actual local skill discovery without starting a model turn."""
import argparse
import json
from pathlib import Path
import queue
import subprocess
import tempfile
import threading
import time

NAMES = ('adaptive-model-orchestrator', 'deep-project-review')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cwd', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--codex', default='/Users/lxm/.local/bin/codex')
    args = parser.parse_args()
    cwd = str(Path(args.cwd).resolve(strict=True))
    stderr = tempfile.TemporaryFile(mode='w+t')
    proc = subprocess.Popen([args.codex, 'app-server', '--stdio'], cwd=cwd,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=stderr, text=True)
    replies = queue.Queue()

    def read():
        for line in proc.stdout:
            try:
                replies.put(json.loads(line))
            except json.JSONDecodeError:
                continue

    threading.Thread(target=read, daemon=True).start()

    def send(message):
        proc.stdin.write(json.dumps(message) + '\n')
        proc.stdin.flush()

    def response(request_id):
        end = time.monotonic() + 20
        while True:
            remaining = end - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('No app-server response within 20 seconds')
            try:
                message = replies.get(timeout=remaining)
            except queue.Empty as exc:
                raise TimeoutError(f'No app-server response in 20 seconds; child exit={proc.poll()}') from exc
            if message.get('id') == request_id:
                if 'error' in message:
                    raise RuntimeError(message['error'])
                return message['result']

    try:
        send({'id': 1, 'method': 'initialize', 'params': {
            'clientInfo': {'name': 'skill_update_discovery_check', 'version': '2026.09.30'}
        }})
        response(1)
        send({'method': 'initialized'})
        send({'id': 2, 'method': 'skills/list', 'params': {'cwds': [cwd], 'forceReload': True}})
        result = response(2)
        matches = [s for entry in result['data'] for s in entry['skills'] if s['name'] in NAMES]
        errors = [e for entry in result['data'] for e in entry['errors']
                  if any(n in e.get('path', '') for n in NAMES)]
        evidence = {'test': 'Actual local Codex app-server skills/list with forceReload; no model turn started',
                    'cwd': cwd, 'matches': matches, 'errors': errors,
                    'limits': 'Confirms discovery, enabled entries and installed paths. Does not establish fresh-session invocation routing, effective implicit policy or model configuration.'}
        Path(args.output).write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + '\n')
        assert not errors, errors
        for name in NAMES:
            found = [s for s in matches if s['name'] == name]
            assert len(found) == 1 and found[0]['enabled'], found
            assert Path(found[0]['path']).resolve() == Path('/Users/lxm/.codex/skills', name, 'SKILL.md'), found
        print('PASS: Both installed skills uniquely discovered and enabled; no loading errors')
    except Exception:
        stderr.seek(0)
        diagnostic = stderr.read()
        Path(args.output).with_suffix('.stderr.log').write_text(diagnostic)
        print('Diagnostic stderr saved next to discovery output')
        raise
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        stderr.close()


if __name__ == '__main__':
    main()
