# Fixture review (read-only Sol baseline)

## Result

The quoted arithmetic is correct for ordinary valid inputs, but the API violates its explicit strict quantity contract. It accepts both booleans and subclasses of `int` because `isinstance(quantity, int)` is broader than “exact int.” It also accepts a non-string delivery object that merely compares equal to `"standard"`, despite the requirement that every other delivery value raise `ValueError`.

This was a read-only review of only `fixture/requirements.md` and `fixture/pricing.py`. After the initial check, the coordinator supplied an unchanged before-repair snapshot at `fixture-before`; its requirements and pricing hashes match the initial files, and focused reproductions there returned the same results. `metadata.json` was intentionally not read from either location, so its required fields are **not checked**. No fixture or snapshot file was modified. Hash evidence is in `tests/logs/source-hashes.txt`.

## Findings

### F-001 — P1 — exact quantity validation is not enforced

- **Location:** `fixture/pricing.py:2`
- **Requirement:** quantity must be an **exact** non-negative `int`; booleans and non-integers must raise `ValueError`.
- **Observed:** `quote(True)` returned `125`, `quote(False)` returned `0`, and `quote(IntChild(2))` returned `250`.
- **Cause:** `bool` and user-defined `int` subclasses satisfy `isinstance(value, int)`.
- **Impact:** explicitly invalid inputs are priced as parcels, so callers can receive a normal-looking total instead of the required validation error.
- **Minimum repair:** replace the broad type test with an exact-type test, e.g. `type(quantity) is not int`, while retaining the negative check.
- **Acceptance:** exact built-in integers `0` and positive values price correctly; negative built-in integers, both booleans, floats, strings, `None`, and an `int` subclass all raise `ValueError("quantity")`.

### F-002 — P2 — delivery validation accepts a non-string equality spoof

- **Location:** `fixture/pricing.py:4-6`
- **Requirement:** delivery must be `"standard"` or `"express"`; any other value raises `ValueError`.
- **Observed:** a `PretendsStandard` object whose equality method returns true only for `"standard"` was accepted and `quote(1, object)` returned `125`.
- **Cause:** tuple membership relies on equality without first requiring a string delivery value.
- **Impact:** arbitrary objects can bypass the documented delivery-mode validation. For ordinary built-in invalid values (`None`, integers, booleans, and unknown strings), validation worked.
- **Minimum repair:** require a string before membership, for example `if not isinstance(delivery, str) or delivery not in ("standard", "express"):`. The requirements do not explicitly define treatment of `str` subclasses, so exact-string-type rejection should not be added without a product decision.
- **Acceptance:** the two documented strings work; unknown strings and non-string values, including an equality-spoofing object, raise `ValueError("delivery")`.

## Numerical and API checks actually run

Python 3.9.6 was used with bytecode generation disabled. The complete initial output and the later unchanged-snapshot confirmation are in `tests/logs/fixture-runtime.txt`.

| Check | Actual result | Status |
|---|---:|---|
| `quote(0)` | `0` (`int`) | Pass |
| `quote(0, "express")` | `500` (`int`) | Pass |
| `quote(1)` | `125` (`int`) | Pass |
| `quote(2, "express")` | `750` (`int`) | Pass |
| `quote(10**30)` | `125 * 10**30` (`int`) | Pass |
| `quote(-1)` | `ValueError("quantity")` | Pass |
| float, string, and `None` quantities | `ValueError("quantity")` | Pass |
| `True`, `False`, and an `int` subclass | accepted and priced | Fail (F-001) |
| unknown string, `None`, integer, and boolean delivery | `ValueError("delivery")` | Pass |
| equality-spoofing non-string delivery | accepted as standard | Fail (F-002) |

The multiplication and express surcharge are numerically correct for the tested valid inputs, including zero quantity and a very large integer; Python's unbounded integers avoid overflow here. The review did not infer behavior from `metadata.json`, install dependencies, use external services, or execute any repair/verification round.

## Suggested scoped patch (not applied)

```python
def quote(quantity, delivery="standard"):
    if type(quantity) is not int or quantity < 0:
        raise ValueError("quantity")
    if not isinstance(delivery, str) or delivery not in ("standard", "express"):
        raise ValueError("delivery")
    return quantity * 125 + (500 if delivery == "express" else 0)
```

After applying a repair under the authorized fixture-only scope, a different reviewer should rerun F-001/F-002 reproductions plus the valid arithmetic table. This baseline did not perform that repair or independent post-repair verification.
