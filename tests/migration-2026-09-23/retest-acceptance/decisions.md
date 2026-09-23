# Independent acceptance decisions

These are decisions about the **synthetic cases** in `github-preview/deep-project-review/tests/cases.json`, interpreted using the current `SKILL.md`, `references/templates.md`, and `references/runtime.md`. I did not execute a project review, start an agent, run any case test, or modify a reviewed project. Case descriptions are supplied facts for reasoning, not events I observed.

## W05 — Failed and unrun checks

- **Next action:** Record each check separately. Investigate the new API failure and obtain comparable before/after evidence (or another traceable cause) before assigning regression origin. Run the export check if its environment and scope permit. Do not close acceptance while required checks fail or remain unrun.
- **Claim:** The legacy fixture test **failed** before and after with the same reported assertion; it is an existing baseline failure in the case data. The new API test **failed** after the change. The export check is **not run**. Overall acceptance cannot be marked passed.
- **Evidence limit:** The new test has no comparable prechange result. Its failure alone cannot establish that this round introduced the API problem. The identical legacy assertion supports classifying that particular failure as pre-existing, but it does not establish that all other behavior is unchanged. No export result can be inferred.

## W07 — Review only

- **Next action:** Finish and deliver the review with the confirmed P1 finding, concrete repair plan, and acceptance criteria; stop before modifying the project. A later repair requires separate write authorization.
- **Claim:** On the supplied case facts, Astra has confirmed a P1 issue and its proposed repair and acceptance criteria are clear. This round can be reported as **review complete**, with the issue outstanding and **no repair performed**.
- **Evidence limit:** The stated Astra result is a case premise, not an actual review result I verified. A repair plan is neither an implemented fix nor independently accepted behavior. The user's instruction expressly forbids edits.

## W10 — No write authorization

- **Next action:** Continue all authorized read-only review work, including evidence assessment and a precise repair plan. Stop before assigning or applying the local fix. Present the proposed change and acceptance criteria to obtain write authorization as the final gate.
- **Claim:** The user authorized an in-depth independent review. The supplied Astra result supports reporting a confirmed local error and a proposed scope, but not that it was repaired or accepted.
- **Evidence limit:** Review authorization does not imply project write authorization. The case does not give the underlying evidence or actual implementation result; those cannot be claimed from the one-line premise.

## W11 — Model and scheduling choices

| Synthetic task | Model and effort if dispatched | Scheduling and stop decision | Claim and evidence limit |
| --- | --- | --- | --- |
| Two clear, low-risk omissions under an existing naming rule, with a direct check | `gpt-6-luna`, `high` | Appropriate for a narrow repair task, followed by independent verification. | This is a routing choice from the case description; no edit, test, or effective model configuration has been observed. |
| Cross-module interface mismatch with an unknown root cause and data-consistency impact | `gpt-6-sol`, `high` initially; `xhigh` only if genuinely deeper reasoning is needed | Give one owner responsibility for the shared interface and sequence dependent changes. Locate the cause before prescribing a patch; stop retries if failures expose a deeper cause. | The route reflects complexity and impact. The case does not identify the cause or prove any fix. |
| High-uncertainty system design conflict after two failed fix/verification rounds | `gpt-6-astra`, `xhigh` for a future authorized, targeted analysis or repair; **no new automatic repair dispatch now** | The default two-round limit has been reached. Stop the automatic fix loop, report the unresolved conflict and evidence, and obtain an explicit budget change before another repair round. | Astra is the suitable route for the systemic uncertainty, but model selection does not override the round cap. Neither success nor the cause is established by the description. |

If any task is actually dispatched later, use structured `model` and `reasoning_effort` parameters and record requested versus effective configuration. The model IDs above are proposed routes, not claims of actual calls.

## W12 — Repairer self-verification

- **Next action:** Assign a real verifier who did not perform the repair to inspect the changed version. Have them reproduce the original issue, check associated behavior and suitable regressions, and record tests and evidence, including any failures or unrun checks. Add targeted Astra `xhigh` review if the actual change is major, complex, or disputed.
- **Claim:** The repairer reports success and passing tests. Independent acceptance is **pending**; the project cannot yet be delivered as acceptance passed.
- **Evidence limit:** The case supplies no changed version, diff, test command/output, or independent verifier. The repairer's statement is not independent evidence, and no test result was observed in this exercise.
