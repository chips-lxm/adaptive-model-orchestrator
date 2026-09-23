# Independent review: parcel quote fixture

**Scope and baseline.** I reviewed only `<migration-dir>/fixture/requirements.md` and `pricing.py` for `quote` API behavior, strict input validation and numerical correctness. The requirement and code SHA-256 hashes matched `evidence/baseline.json` before and after testing: `a3bba47f…a9b20d4fc8fc` and `fb6a3808…d4c00a9c5`, respectively. The source fixture was not modified. I did **not** read `metadata.json`, as assigned; its currency/unit/mode requirement remains **not checked** by this reviewer. No other project was reviewed.

**Execution.** Python 3.9.6. I copied `pricing.py` to this output directory before executing it, so the fixture source did not receive bytecode or test effects. Reproduce with:

```text
python3 <migration-dir>/review-sol/check_behavior.py
```

The script exits 1 because five assertions expose two confirmed validation defects. Full output is `probe.log`. The same run executed W01 from the candidate skill's case file; all seven W01 assertions passed. No test process or command failed to start; the nonzero exit represents the five observed fixture requirement failures. The supplied baseline hashes were rechecked after execution and remained unchanged.

## Confirmed findings

**RS-01 — P1 — `bool` and `int` subclasses accepted as quantities.** `pricing.py:2` uses `isinstance(quantity, int)`, which admits `bool` and user-defined `int` subclasses even though `requirements.md` says quantity must be an **exact** non-negative `int`, explicitly excluding `bool`. `quote(True)` returned `125`, `quote(False)` returned `0`, and `quote(IntChild(2))` returned `250`; all three should raise `ValueError`. This violates the core order-quantity contract and can turn invalid inputs into chargeable quotes. The minimal fix is exact-type validation (`type(quantity) is int`) followed by the existing nonnegative check. Recheck zero, positive, negative, both booleans, a subclass, float and string after repair.

**RS-02 — P2 — invalid delivery objects can be accepted or leak the wrong exception.** `pricing.py:4-6` validates with membership and then compares delivery again; both operations allow an arbitrary object's equality method to control the result. A `DeliverySpoof` object whose equality returns true for `"express"` produced `625` for `quote(1, DeliverySpoof())`, while requirements say **any other value** raises `ValueError`. A `DeliveryRaiser` whose equality raises `RuntimeError` leaked that exception instead of `ValueError`. This can admit unsupported delivery modes and breaks the documented error contract for non-string inputs. Validate a delivery string and its allowed literal value before using it in pricing, without invoking arbitrary non-string equality methods; then recheck standard/express, unknown strings, `None`, and objects with custom equality. Whether a `str` subclass equal to an allowed literal should be accepted is not made explicit by the requirement; choose and document that exact-type policy during repair.

## Checked coverage and limits

| Requirement / area | Actual check and result | Status |
| --- | --- | --- |
| Default standard rate and integer cents | `quote(0)=0`, `quote(1)=125`, `quote(3)=375`; results compared with exact Python `int` | **Checked, passed** |
| Express surcharge, including zero quantity | `quote(0, "express")=500`, `quote(3, "express")=875` | **Checked, passed** |
| Large integer arithmetic | `quote(10**30, "express") = 125*10**30+500` exactly | **Checked, passed** for sampled large value; no formal proof of every magnitude |
| Invalid quantity | Negative, float, string and `None` raised `ValueError`; `True`, `False`, and `int` subclass failed required rejection | **Checked, failed** in RS-01 |
| Invalid delivery | Unknown string and `None` raised `ValueError`; spoofed equality was admitted and raised comparison error leaked `RuntimeError` | **Checked, failed** in RS-02 |
| Metadata content | Assignment expressly excludes reading `metadata.json` | **Not checked** |
| Integration with callers, broader environment, every possible custom Python object | No caller or integration material was in this assigned scope | **Not checked** |

The valid arithmetic path matches the stated formula for the tested inputs and visibly uses Python integer multiplication/addition. The review makes no full-project acceptance claim: these two defects remain in the source, and the metadata portion belongs to another review scope. No fix was applied to the fixture.
