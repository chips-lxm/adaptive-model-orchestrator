# Independent fixture adjudication

Date: 2026-09-23. Task: `/root/astra_adjudication`. This is a separate adjudication of the actual isolated fixture, not a simulated set of reviewer roles. The root owns host-record verification of this task's effective model and effort; this report does not use the task name or a self-assertion as configuration evidence.

**Decision: three confirmed repairs.** The fixture has not been repaired or accepted by this task. Both complete independent fixture reports were read, all reported findings were traced to original material, and targeted probes reproduced the disputed validation behavior. Source hashes matched the supplied baseline before and after the probes. The root can now schedule the three scoped repairs under the fixture's existing authorization, followed by a different agent's independent acceptance. Maximum authorized repair–verification rounds: two; this review/adjudication is not a repair round.

## Materials and evidence actually read

- Original [requirements](../fixture/requirements.md), [implementation](../fixture/pricing.py), [metadata](../fixture/metadata.json), and [baseline hashes](../evidence/baseline.json).
- Complete [Sol fixture report](../review-sol/fixture-review.md), its complete [probe script](../review-sol/check_behavior.py), and [probe output](../review-sol/probe.log).
- Complete [Luna fixture report](../review-luna/fixture-review.md). This report is a source/JSON comparison, with no executable test claim to infer.
- Root's [contract tests](../verify_fixture.py) and [before results](../evidence/before-tests.json): 16/20, failing True, False, int-subclass rejection and currency.
- New independent [trace script](trace_evidence.py) and [trace evidence](trace-evidence.json). Executed with Python 3.9.6; process exit 0 means evidence collection completed, **not** that the unrepaired fixture passed. Source was compiled from read-only text in memory, so no fixture bytecode was written. The output preserves actual returns and exceptions.

No unlisted agent reports, external sources or unrelated projects were inspected. This task wrote only within `adjudication/` and did not spawn agents.

## ID mapping and four-way classification

| Unified ID | Original report ID | Classification | Severity | Adjudication |
|---|---|---|---|---|
| A-01 | RS-01 | Confirmed repair | P1 within this fixture's strict quantity contract | Exact-int requirement is explicit. `isinstance` accepts both booleans and int subclasses. Preserve the finding; no production financial-loss claim has been demonstrated. |
| A-02 | RS-02 | Confirmed repair | P2 | Non-string objects can impersonate an allowed mode or leak RuntimeError through equality. Both symptoms share the delivery-validation root cause. Repair together. The string-subclass policy caveat is bounded below. |
| A-03 | F-01 | Confirmed repair | P2 | Required `AUD` is stored as `USD`. The other required metadata values match. |

**Suggested improvements:** none needed for this bounded task. Extra features, dependencies, integration architecture, or general hardening are not repair work here.

**Evidence insufficient:** no reported fixture defect remains in this category. Actual downstream monetary impact, caller compatibility outside this fixture, and exhaustive behavior of arbitrary Python objects were not established and are not claimed. The requirements do not establish an exact-`str` type restriction for delivery; that restriction must not be inferred from the exact-`int` quantity rule.

**Invalid or duplicate:** no complete reported finding is rejected and none duplicates another report. Within RS-02, treating “choose an exact-type policy” as permission to reject every string subclass would be an unsupported tightening; it is not an additional required repair. The spoof and exception examples are two reproductions of A-02, not separate repair tasks.

## A-01: exact quantity validation

Location: `fixture/pricing.py:2`. The requirement says quantity must be an **exact non-negative int**, expressly excluding bool. Independent actual results are `quote(True) == 125`, `quote(False) == 0`, and `quote(IntChild(2)) == 250`. These match the reviewer script and explain three of the four root contract failures.

Minimal boundary: replace the permissive integer type test with an exact-type check and retain the nonnegative check. Do not change the public signature, unit price, valid arithmetic, exception message contract (none was specified), or other files. A check equivalent to `type(quantity) is not int or quantity < 0` is sufficient. Short-circuit the type check before numeric comparison so invalid objects are rejected without calling their comparison methods.

Independent acceptance: exact built-in ints 0, 1, 3 and a large positive int produce integer cent totals for both modes; -1, True, False, 1.0, `"1"`, None, list, and an int subclass raise ValueError. Default delivery remains standard. Do not add a finite maximum, rounding, coercion, or bool-to-int conversion.

## A-02: delivery value and comparison behavior

Location: `fixture/pricing.py:4-6`. The requirement accepts `"standard"` and `"express"`, with any other value raising ValueError. Independent probes reproduced:

| Input at quantity 1 | Actual baseline | Required result |
|---|---|---|
| Non-string object whose equality returns true for `"express"` | 625 | ValueError |
| Non-string object whose equality raises RuntimeError | RuntimeError | ValueError |
| String subclass with underlying `"overnight"` but spoofed equality | 625 | ValueError |
| String subclass with underlying `"overnight"` and raising equality | RuntimeError | ValueError |

The last two targeted checks establish that a string type guard alone would leave the same root cause for unsupported string content. They do not justify banning string subclasses. Ordinary subclasses with inherited string behavior already return 125 for `"standard"`, 625 for `"express"`, and ValueError for `"overnight"`.

**Delivery subclass boundary:** unlike quantity, delivery is not specified as an *exact* built-in type. Preserve ordinary string-subclass compatibility for the two allowed text values. No new caller-selectable policy is required. The smallest robust approach is to reject non-strings, derive an ordinary string from the underlying string value without invoking the object's overridden equality or conversion methods, then validate and price from that same value. For this Python fixture, `isinstance(delivery, str)` followed by `str.__str__(delivery)` is one concrete local option; the independent probe confirms that the latter preserves the underlying `"overnight"` value rather than the spoofed equality. Avoid general `str(delivery)` coercion of arbitrary objects, a blanket exact-str restriction, case folding, trimming, or new delivery modes.

Independent acceptance must add checks beyond the root's 20 tests:

1. Valid ordinary strings retain standard/express totals at zero and positive quantity, with exact integer results. In particular `quote(0, "express") == 500`.
2. Unknown/empty strings, None, an integer, bytes, a list, and a dict raise ValueError. Validate delivery at zero quantity as well; zero must not bypass the mode contract.
3. The two non-string spoof/raiser objects in the original Sol probe raise ValueError. Their equality methods need not run. Acceptance must observe actual exceptions, not only returned values.
4. Ordinary `str` subclasses containing the two supported texts retain the same totals. An ordinary subclass containing unsupported text raises ValueError.
5. Subclasses with unsupported underlying text cannot gain acceptance through overridden equality or leak its exception. If normalization is used, ensure pricing reads that normalized value too; validating one representation and pricing from another would leave the defect open.

These are local tests of the reported cause and existing compatibility. No security claim about executing arbitrary hostile Python code or integrations is made.

## A-03: currency metadata

Location: `fixture/metadata.json:2`. The original requirement is exactly `currency: "AUD"`; the parsed baseline and independent trace show `"USD"`. Change that value only. Keep `unit: "cents"` and `delivery_modes: ["standard", "express"]` in that order. No exchange-rate conversion or price change follows from this metadata correction.

Independent acceptance: parse the final JSON and compare all three required values. Do not require an invented “no additional keys” rule: the requirements name the required fields, not a closed schema. Record the actual diff.

## Coverage, repair ownership, and exit requirements

| Requirement | Review coverage and adjudication evidence | Remaining work |
|---|---|---|
| Exact nonnegative quantity | Sol, root before tests, independent targeted reproduction | Repair A-01 and independently rerun valid/invalid cases |
| Unit cost, default mode, integer cents | Sol numeric checks, root before tests, independent 0/1/3/large cases and source arithmetic | Preserve and independently regress after validation edits |
| Standard/express surcharge, express zero | Both reviewed code evidence sets; independent trace | Preserve, including zero and subclass compatibility |
| Invalid delivery ValueError contract | Sol spoof/raiser traces; independent reproduction plus same-root subtype probe | Repair A-02; root's current 20-test set alone cannot accept it |
| Metadata currency/unit/modes order | Luna, root before tests, parsed original file | Repair A-03 and compare all three fields |
| Baseline isolation | All three current source hashes equal baseline before/after adjudication | Capture repaired version and test copies; preserve requirements |
| Independent final acceptance | Not yet run | Must be a different actual agent from the fixer |

Use one active owner for `pricing.py`; A-01 and A-02 should be integrated in one small edit. `metadata.json` is separable, but its small size does not require another branch. This report grants no broader write permission; the original fixture requirement already authorizes these local repairs. Do not edit `requirements.md`, other projects, or published skills as part of fixture repair.

For round 1, capture the source diff and revised hashes, run the existing 20 tests plus A-02's targeted cases on an isolated copy, and have a non-fixer independently check the same repaired version. The verifier must record actual test results, exit codes, input/version evidence, and untouched source hashes. One grouped repair followed by its independent acceptance counts as one round, regardless of file or agent count. If verification fails, attribute the failure using evidence and either undertake the second authorized round or report the remaining blocker. No third automatic repair round. This adjudication is complete; fixture delivery remains pending repair and independent acceptance.
