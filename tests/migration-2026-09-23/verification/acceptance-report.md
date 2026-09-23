# Independent fixture acceptance — round 1

Date: 2026-09-23. Verifier: `/root/independent_acceptance`, separate from the repair owner. **Decision: accept this exact repaired fixture revision** for A-01, A-02, and A-03 under the original requirements. This is one bounded repair and verification round, not a claim about other projects or arbitrary Python objects.

## Version and isolation

I read the original `fixture/requirements.md`, current `pricing.py` and `metadata.json`, the complete adjudication, the baseline hashes, and the three `fixture-before/` files. I used the repair report and diffs for navigation, then compared the actual files and independently ran the checks. The verified source hashes before and after verification were identical:

| File | Before and after SHA-256 | Original baseline |
|---|---|---|
| `requirements.md` | `a3bba47f2f277b8d0d0f6bb163320f96e0cf97d5619d196b9771a9b20d4fc8fc` | same |
| `pricing.py` | `a4f3f019e8d21f121200d57313e6d5716f892bc15c7ab6cef6a27084992bfd1b` | `fb6a3808b896346f31dc835ca625066012f306b8ac4921b136f4042d0c00a9c5` |
| `metadata.json` | `4f8465268bfd0902e0845c7470aaa55f76589a3a99c22410ca7ba3e3e5867cce` | `656fbaea94d8189f2beab938f803ea0bb59e794a3e5a65206a5bb344a497bef0` |

The original `fixture-before/` hashes match `evidence/baseline.json` for all three files. The verification copy in `verification/test-copy/` matched the source before and after running tests. The unchanged requirements had an empty original-versus-current diff. Detailed machine-readable evidence is in [source-hashes.json](source-hashes.json) and [executions.json](executions.json). During verification, I observed a truncated metadata digest in the repair report's summary table. The coordinator has since corrected that transcription issue and appended a correction note; the corrected table, `after-hashes.txt`, and actual file now all agree with the full digest above. Fixture content and test results did not change.

## Commands and results

All commands were run by [run_verification.py](run_verification.py) with working directory `verification/`; exact argument arrays, Python version, output paths, and exit codes are in `executions.json`. The two test commands used `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B` and pointed at `verification/test-copy/`:

| Command | Exit | Result |
|---|---:|---|
| `python3 -B verify_fixture.py verification/test-copy` | 0 | 22/22 passed ([output](root_contract.stdout.txt)) |
| `python3 -B verification/independent_checks.py verification/test-copy` | 0 | 59/59 passed ([script](independent_checks.py), [output](independent.stdout.txt)) |
| `diff -u fixture-before/pricing.py fixture/pricing.py` | 1 | Expected difference: exact-int type check, string guard, and underlying string normalization ([diff](pricing_diff.stdout.txt)) |
| `diff -u fixture-before/metadata.json fixture/metadata.json` | 1 | Expected difference: `USD` to `AUD` only ([diff](metadata_diff.stdout.txt)) |
| `diff -u fixture-before/requirements.md fixture/requirements.md` | 0 | No difference |

The verification runner itself exited 0. The two `diff` exit codes of 1 mean files differ; they are not test failures. Both test stderr files are empty.

## Acceptance coverage

- **A-01, exact quantity:** built-in integers 0, 1, 3, and `10**30` returned exact integer totals with standard, express, and default delivery. Negative integers, booleans, float, string, `None`, list, dict, object, and `int` subclasses raised `ValueError`. The type guard precedes the negative comparison.
- **A-02, delivery:** ordinary strings and ordinary `str` subclasses containing `standard` or `express` returned the same totals, including `quote(0, "express") == 500`. Unsupported text and empty text, at quantity zero and one, raised `ValueError`. Non-string values including bytes, list, dict, an equality spoofer, and an equality raiser raised `ValueError`. String subclasses whose underlying text was `overnight` also raised `ValueError` when their equality method spoofed `express` or raised `RuntimeError`. The implementation validates and prices from the same normalized underlying string value.
- **A-03, metadata:** parsed `currency` is `AUD`, `unit` is `cents`, and ordered `delivery_modes` is `["standard", "express"]`. The actual diff changes only currency.

The independent suite has 20 valid pricing checks, 12 invalid quantity checks, 24 invalid delivery checks, and 3 metadata checks. Together with the separate root contract suite, **81/81 checks passed**. This is a count of executed checks, not a proof over all possible objects.

I did not test external callers, other projects, external services, or exhaustive behavior of hostile Python subclasses. Those are outside this fixture's requirements and are not marked passed. I did not edit the fixture, publish a skill, or start another repair round. Host record validation of the agent's effective model and effort belongs to the root task.
