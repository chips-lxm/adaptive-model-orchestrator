# Independent forward check — 2026-09-30

Scope: read-only skill-maintenance evaluation of `/Users/lxm/app1/github-preview/adaptive-model-orchestrator` and `/Users/lxm/app1/github-preview/deep-project-review`; synthetic writes only under `/private/tmp/skill-forward-20260930`. No project review, source edits, children, prior validation reports or HANDOFF files were used. Read skill-creator's independent-forward-testing instructions, both SKILL.md files, adaptive collaboration reference, deep runtime/templates/entry example/README/UI policy, and both freeze helpers. Scenario outcomes below are decisions implied by the rules, not claimed end-to-end executions.

## Scenario decisions

1. **One clear low-risk wording correction.** Current session reads the target/context, changes the wording and checks the affected meaning/diff. No branch merely to obtain a cheaper model; no deep review. A justified already-separated mechanical job could use Luna high, but this one does not justify delegation. Claim only that the requested wording and relevant checks are complete. If the target or intended wording is missing, obtain that material; do not invent it.

2. **Feature: two independent modules, shared interface unstable.** Lead defines requirements/acceptance and assigns one owner to stabilize the minimal interface. Module execution that depends on it waits; independent preparations can proceed. After the interface is versioned and checked, dispatch disjoint module work concurrently within host limits, normally gpt-6.1-sol high, directly xhigh/max only for actual difficulty. Lead proceeds with integration/acceptance work that does not duplicate branches. Freeze common rules and maintain one shared baseline/requirements record. Module reports alone do not establish feature completion; integrate and check the combined behavior. Interface instability blocks dependent implementation, not all useful work.

3. **Difficult tightly coupled root cause, ambiguous evidence.** Concentrate the core investigation, gather reproducible raw evidence and distinguish environment/tool failure from reasoning difficulty. Difficulty alone does not justify parallel implementation. Keep the user's lead model; if a separate substantial reasoning task is warranted, Astra high/xhigh is suitable for ambiguous systemic judgments, or 6.1 Sol xhigh/max for a concrete difficult derivation. An independent verification task can be added only when its benefit justifies it. Do not mechanically exhaust all models. Claim a confirmed cause only with causal evidence; otherwise report hypotheses, missing evidence and next discriminating check.

4. **Discuss improving deep-project-review, no project-review request.** Exit the review workflow and work on the requested discussion/skill-maintenance scope. Do not read a project or create reviewers/Astra merely because the skill was named or loaded. No review configuration is required. Claim discussion findings or actual skill edits only; no project review was authorized.

5. **Explicit deep-project-review, synthetic project, review only; two first reviewers find nothing.** Establish the exact current baseline including relevant untracked/uncommitted material and original requirements. Use real isolated reviewers, normally 6.1 Sol high; no sharing first-review conclusions. After complete reports return, a separate verified gpt-6-astra xhigh adjudicator remains mandatory even with zero findings and review-only permission. Supply full reports, coverage matrix and raw artifacts; Astra forms checks from requirements before assessing reports and checks unreported high-risk paths. Deliver review conclusions and any concrete repair plan without source modification. “No issues found in checked scope” and “review-only completed” are legitimate after the mandatory stage, not universal project approval. Missing/unverifiable Astra blocks completion. Independent post-fix acceptance is not required if nothing was changed. This evaluation did not instantiate these agents.

6. **Authorized repairs; fixer says tests passed, public interface and input data changed.** Record and compare the changed version/input with the baseline; determine whether the interface change stays inside authorized repairs and the original requirements. Stop affected writes if ownership/scope is uncertain. Do not reuse prior tests whose version/input/dependencies no longer apply. Assign a real non-fixing verifier, normally 6.1 Sol high, with xhigh/max for justified complex verification. Verifier personally executes key checks; enlarge necessary regression to interface consumers and affected data paths, not just edited lines. Major/complex/disputed changes need Astra xhigh targeted review. Fixer logs are useful raw evidence but not independent acceptance. Claim only independently verified scope. Failed new tests are not automatically newly introduced regressions without comparable before/after or other causal evidence. Preserve the two repair–verification-round counter; changed baseline or upgraded tasks cannot reset it.

7. **Long run has a snapshot; global installation changes.** Continue from that snapshot and its relative resources, record its digest and verify integrity; future branches/continuations do not silently load the updated installation. Snapshot pins skill rules, not project input/environment. If the snapshot is missing or inconsistent, restore it or explicitly establish a new version boundary, assess affected decisions/evidence and preserve authorization/round counts. A global update alone does not invalidate an intact old snapshot. Legitimate claim: this run used the recorded frozen rule version, not the latest global version.

8. **Host declares 6.1 Sol high/xhigh/max; cache stale; later Astra xhigh fails.** Do not veto the tool-supported 6.1 configuration solely for absent cache entries. Use structured model/effort parameters and an isolated/finite-history fork as required by the host; record tool contract, requested configuration, agent/return and available effective metadata separately. Success without trusted effective evidence must be qualified; an agent's self-identification is insufficient. For later Astra failure, inspect actual error/input/permissions/dependencies, retain reports and stop dependent adjudication/acceptance until the required configuration is restored. No silent old-Sol fallback or claim of completed deep review; do not retry indefinitely. Adaptive-only independent work can continue with an explicit justified alternative and stated limitation. No real model invocations or effective-configuration claims were made in this evaluation.

## Executed helper evidence

Both source helpers are byte-identical: SHA-256 `227838b079d8154b03a87ec45253533e52e2c28338dc80b512896ff3eb523f8a`.

Initial system `python3` failed before executing the harness (exit 69: Xcode license agreement). Used `/Users/lxm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` instead. Actual harness command:

```sh
/Users/lxm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /private/tmp/skill-forward-20260930/run-fixtures.py
```

Exit 0. Full commands, stdout, stderr and cases are retained in `results.json`. The harness copied each unchanged helper into a tiny synthetic source and exercised its CLI plus a controlled copy-time source mutation.

| Case, independently run for each helper | Observed result |
| --- | --- |
| Fresh `--output`, then `--verify` | Both exit 0, four runtime files, verified true |
| Source SKILL.md changes after freezing | Snapshot still contains version A while source contains B; old snapshot verify exits 0 |
| Snapshot reference tampered | Verify exits 1: `Snapshot content differs from its manifest` |
| Pre-existing nonempty output | Exit 1 (`File exists`); sentinel preserved |
| Pre-existing empty output | Exit 1; existing directory preserved |
| Source changes during copying | Raises `Source changed during snapshot creation; retry from a stable version`; incomplete output removed |
| Synthetic history under tests and maintenance under docs | Not copied |
| Extra root file outside runtime allowlist | Verify still exits 0; verification covers the inventoried runtime set, not all arbitrary files |

Additional actual CLI commands used the fixture-0 helper with `--output`:

- `/private/tmp/skill-forward-20260930/discovery-check/.codex/plugins/cache/plugin/skills/snapshot`: exit 0, verified true.
- `/private/tmp/skill-forward-20260930/discovery-check/.codex/skills/snapshot`: exit 1, `Use a non-discoverable output directory outside the source skill`.

## Findings and limits

- **Concrete guard gap:** instructions prohibit snapshots in *any* Codex skills installation directory; `is_discovery_path` only recognizes adjacent `.codex/skills`, `.agents/skills` and `$CODEX_HOME/skills`. It accepts a plugin-cache-style skills path, demonstrated with an isolated analogous path. Actual host discovery of this synthetic path was not tested. Either broaden the recognizable installation roots or state that the caller must validate additional host/plugin roots; the helper alone does not enforce the universal rule.
- **Possible role-separation ambiguity:** deep README says consolidating model routes “never combines independent reviewer, adjudicator, fixer, or verifier responsibilities,” while SKILL.md §5 expressly permits reusing a reviewer as verifier when that reviewer did not perform the fix. The core's concrete non-fixer rule is clear; README wording could wrongly forbid the explicitly permitted reuse. Clarify independence for each judgment/repair rather than implying four permanently distinct individuals.
- **Integrity scope:** the manifest detects changes to its included runtime files, not unexpected root files, and its plain digest is not adversarial authentication. This is adequate as a content-consistency check with a trusted manifest but should not be called cryptographic protection against coordinated manifest/content replacement.
- Scenarios otherwise provide actionable routing and stop conditions: no automatic deep review; no implementation on unstable shared dependencies; mandatory Astra despite no findings; personal independent checking after repairs; version/input drift invalidates affected evidence; old snapshot remains the run's rule source; stale cache alone does not block valid calls.
- End-to-end host loading, actual model/effort effectiveness, multi-agent review outcomes, quality, latency and token savings were not measured. No numerical savings are inferred.
