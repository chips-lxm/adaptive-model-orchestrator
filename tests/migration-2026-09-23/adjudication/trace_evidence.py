"""Independent adjudication probes. Only writes inside adjudication/."""
import hashlib
import json
from pathlib import Path
import platform

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'adjudication'
FIXTURE = ROOT / 'fixture-before'
CANDIDATE = ROOT.parent / 'github-preview'
baseline = json.loads((ROOT / 'evidence/baseline.json').read_text())

def hashes():
    return {name: hashlib.sha256((FIXTURE / name).read_bytes()).hexdigest()
            for name in baseline}

before = hashes()
assert before == baseline, 'Fixture drift before adjudication'
ns = {}
# Compile source text in memory: no import or bytecode write in the fixture.
exec(compile((FIXTURE / 'pricing.py').read_text(), str(FIXTURE / 'pricing.py'), 'exec'), ns)
quote = ns['quote']
observations = []

def record(name, fn, expected, purpose):
    try:
        value = fn()
        actual = {'type': type(value).__name__, 'value': repr(value)}
    except Exception as exc:
        actual = {'exception': type(exc).__name__, 'message': str(exc)}
    observations.append({'name': name, 'expected': expected,
                         'actual': actual, 'purpose': purpose})

class IntChild(int):
    pass

class DeliverySpoof:
    def __eq__(self, other):
        return other == 'express'

class DeliveryRaiser:
    def __eq__(self, other):
        raise RuntimeError('custom comparison failed')

class PlainDelivery(str):
    pass

class LyingDelivery(str):
    def __eq__(self, other):
        return other == 'express'

class RaisingDelivery(str):
    def __eq__(self, other):
        raise RuntimeError('custom string comparison failed')

for q in [True, False, IntChild(2)]:
    record('RS-01 quantity ' + type(q).__name__ + ':' + repr(q),
           lambda q=q: quote(q), 'ValueError', 'Confirm reported exact-int defect')
for name, d in [('non-string spoof', DeliverySpoof()),
                ('non-string comparison error', DeliveryRaiser())]:
    record('RS-02 ' + name, lambda d=d: quote(1, d), 'ValueError',
           'Trace reported non-string delivery defect')
for q, d, total in [(0, 'standard', 0), (1, 'standard', 125),
                    (0, 'express', 500), (3, 'express', 875),
                    (10**30, 'express', 125 * 10**30 + 500)]:
    record('valid ' + repr(q) + ' ' + d, lambda q=q, d=d: quote(q, d),
           {'type': 'int', 'value': repr(total)}, 'Targeted related regression baseline')
for text, expected in [('standard', 125), ('express', 625), ('overnight', 'ValueError')]:
    record('ordinary str subclass ' + text, lambda text=text: quote(1, PlainDelivery(text)),
           expected, 'Existing compatibility; requirements do not require exact str')
record('str subclass invalid underlying text with spoofed equality',
       lambda: quote(1, LyingDelivery('overnight')), 'ValueError',
       'Determine whether equality issue extends to string content; no blanket subtype ban')
record('str subclass invalid underlying text with raising equality',
       lambda: quote(1, RaisingDelivery('overnight')), 'ValueError',
       'Determine whether equality issue extends to string content; no blanket subtype ban')
record('base str normalization preserves underlying value',
       lambda: str.__str__(LyingDelivery('overnight')), "'overnight'",
       'Evaluate optional minimal implementation direction, without editing fixture')
metadata = json.loads((FIXTURE / 'metadata.json').read_text())
cases = json.loads((ROOT / 'legacy-cases.json').read_text())
w01 = next(c for c in cases['workflow_cases'] if c['id'] == 'W01')
w01ns = {}
exec(compile(w01['artifact'], '<W01 artifact>', 'exec'), w01ns)
for q in [0, 1, -1, True, False, 1.0, IntChild(2)]:
    record('W01 ' + type(q).__name__ + ':' + repr(q), lambda q=q: w01ns['total'](q),
           q * 10 if type(q) is int and q >= 0 else 'ValueError',
           'Independently verify conflict and report evidence')
after = hashes()
assert before == after == baseline, 'Fixture drift after adjudication'
evidence = {'python': platform.python_version(), 'baseline_match_before': before == baseline,
            'baseline_match_after': after == baseline, 'fixture_hashes': after,
            'metadata': metadata, 'observations': observations,
            'raw_workflow_cases': [c for c in cases['workflow_cases'] if c['id'] in ('W05','W10','W11')],
            'execution_status': 'completed; observations include expected unrepaired contract failures'}
(OUT / 'trace-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(evidence, ensure_ascii=False, indent=2))
