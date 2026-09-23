# Synthetic fixture review

## Scope and method

This was a read-only review of exactly these two files, as requested:

- `<migration-dir>/fixture/requirements.md`
- `<migration-dir>/fixture/metadata.json`

I compared them against `<migration-dir>/evidence/baseline.json`. SHA-256 checks for the two inspected files match the baseline:

- `requirements.md`: `a3bba47f2f277b8d0d0f6bb163320f96e0cf97d5619d196b9771a9b20d4fc8fc` — match.
- `metadata.json`: `656fbaea94d8189f2beab938f803ea0bb59e794a3e5a65206a5bb344a497bef0` — match.

## Exact requirements observed

`requirements.md` specifies that `quote(quantity, delivery="standard")` returns an integer total in cents. `quantity` must be an exact non-negative `int`; booleans and non-integers are invalid and raise `ValueError`. Unit cost is 125 cents. Delivery accepts only `"standard"` or `"express"`; any other value raises `ValueError`. Standard adds zero; express adds 500 cents, including when quantity is zero.

The exact metadata requirements are `currency: "AUD"`, `unit: "cents"`, and `delivery_modes: ["standard", "express"]` in that order. The requirements also limit repair to this isolated synthetic project, prohibit new features, dependencies, and external services, and authorize at most two repair/verification rounds.

## Finding

**F-01 — Metadata currency does not match the requirement (severity: P2 / moderate).**

- Location: `fixture/metadata.json`, field `currency`.
- Requirement: exact value `"AUD"`.
- Actual inspected value: `"USD"`.
- Evidence: the parsed file content shows `"currency": "USD"`; the file hash matches the recorded baseline, so this is the baseline state reviewed.
- Impact: consumers relying on the declared currency can interpret cent amounts under the wrong currency. The other two required metadata values match exactly: `unit` is `"cents"`, and `delivery_modes` is `["standard", "express"]` in the specified order.
- Minimal fix direction: change only the `currency` value to `"AUD"`, then check the resulting metadata against all three exact required fields. No edit was made in this review.

## Unexamined scope and limits

I did not read or inspect `pricing.py`, execute the quote implementation, or evaluate behavior such as exact-int validation, bool rejection, arithmetic, delivery validation, or return type. Its hash is present in the supplied baseline, but that is not evidence of its contents or correctness. No code-level conclusion is made. This report is limited to the two authorized files and the baseline hashes for those same files.
