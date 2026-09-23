# Isolated fixture repair, round 1

Date: 2026-09-23. Owner: `/root/fixture_repair`. Scope: `fixture/pricing.py` and `fixture/metadata.json` only. This report records the repair and local checks; independent acceptance belongs to a different agent.

## Changes

- A-01: quantity now requires `type(quantity) is int`, followed by the existing nonnegative check. Booleans and `int` subclasses raise `ValueError`.
- A-02: delivery must be a string. `str.__str__(delivery)` provides the underlying text for both validation and pricing, retaining ordinary `str` subclass support while avoiding overridden equality on unsupported subclass content.
- A-03: metadata currency changed from `USD` to `AUD`. Unit and ordered delivery modes remain unchanged.

The complete source changes are in [pricing.diff](pricing.diff) and [metadata.diff](metadata.diff). No features, dependencies, or other fixture edits were added.

## Version and checks

The three fixture files matched `evidence/baseline.json` before the edit:

| File | Before SHA-256 | After SHA-256 |
|---|---|---|
| `requirements.md` | `a3bba47f2f277b8d0d0f6bb163320f96e0cf97d5619d196b9771a9b20d4fc8fc` | `a3bba47f2f277b8d0d0f6bb163320f96e0cf97d5619d196b9771a9b20d4fc8fc` |
| `pricing.py` | `fb6a3808b896346f31dc835ca625066012f306b8ac4921b136f4042d0c00a9c5` | `a4f3f019e8d21f121200d57313e6d5716f892bc15c7ab6cef6a27084992bfd1b` |
| `metadata.json` | `656fbaea94d8189f2beab938f803ea0bb59e794a3e5a65206a5bb344a497bef0` | `4f8465268bfd0902e0845c7470aaa55f76589a3a99c22410ca7ba3e3e5867cce` |

The test copy in `repair/test-copy/` has the same repaired hashes, recorded in [after-hashes.txt](after-hashes.txt). Both test programs ran against that copy, with `sys.dont_write_bytecode = True`:

| Check | Result | Exit code | Evidence |
|---|---:|---:|---|
| Root's current `verify_fixture.py` | 22/22 passed | 0 | [root-contract-results.json](root-contract-results.json) |
| Targeted delivery checks | 36/36 passed | 0 | [delivery-results.json](delivery-results.json), [check_delivery.py](check_delivery.py) |

The root's expanded baseline before repair was 16/22, with failures in boolean and `int` subclass quantity validation, spoofed/raising delivery comparisons, and currency. The targeted checks cover plain and ordinary string subclass modes at zero and positive quantities; unsupported plain and subclass text; non-string values; and spoofed or raising equality on non-string objects and unsupported string subclasses. They check actual `ValueError` results, including at zero quantity.

The diff commands returned exit code 1 because each file differs from its before snapshot. Hash capture returned 0. No `__pycache__` or bytecode file appeared under the fixture or repair directories after these tests.

## Remaining verification

This owner has not independently accepted the repaired fixture. A separate non-fixer must inspect the final two-file diff, rerun the contract and targeted behavior against the repaired version, confirm the requirements hash and source hashes, and record its own input/version evidence and exit codes. No second repair round has been started.

Coordinator evidence correction: the metadata after-hash above was corrected from a transcription omission using the actual file digest and `after-hashes.txt`; fixture content and test results were unchanged.
