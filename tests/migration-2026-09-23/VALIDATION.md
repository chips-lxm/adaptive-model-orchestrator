# GPT-6 migration validation · 2026-09-23

## Result and scope

The approved active routes are GPT-6 Astra, GPT-6 Sol at medium/high (xhigh when justified), and GPT-6 Luna fixed at high for bounded low-risk work. Sol takes the former Sol/Terra responsibilities. The lead retains its selected model. Required review independence, permissions, dependency readiness, single-editor ownership, and stopping rules remain intact.

**Result: the bounded migration checks and one isolated review–adjudication–repair–independent-verification run completed.** This is not a universal no-regression guarantee, a statistical model benchmark, or a host skill-loading test.

## Behavior checks

- The [original 18 trigger and 12 workflow cases](legacy-cases.json) were evaluated independently by new Sol/high. W01 was actually executed; other case actions were hypothetical. [First-pass decisions](review-sol/behavior-decisions.md) remain unedited.
- First-pass W05 correctly rejected acceptance but called the failing new API test a new regression without a comparable pre-change result. This evidence-attribution error was confirmed by [independent Astra QA](adjudication/migration-qa.md).
- A narrow clarification was added to deep review stage 5 and the acceptance template: a new failing test alone does not prove a newly introduced regression. An independent fresh Sol/high evaluator then passed the targeted W05/W07/W10/W11/W12 decision checks. [Retest](retest-acceptance/decisions.md). The Astra report's “retest pending” records its earlier review stage; this later retest closes that item.
- All [12 new migration scenarios](migration-cases.json) were evaluated separately by [Sol](review-sol/behavior-decisions.md) and [Luna](review-luna/migration-decisions.md): fixed Luna high, ordinary Sol medium, risk-based escalation, no duplicate requirements branch, stale cache, runtime failures, fork compatibility, requested/effective evidence, independent verification, waiting, inheritance-only hosts, and environment errors. Their decisions were supported by Astra's review. These are 12 unique cases with two observations each, not 24 unique executed workflows.
- Total distinct decision scenarios: 42. The initial error and its correction are retained; they are not retrospectively labeled a first-pass success. T02/T03 assume a configured entry; W10 tests write permission after the supplied adjudication premise, not host loading.

## Actual isolated workflow

1. The [original requirements and fixture](fixture-before/requirements.md) were frozen with [baseline hashes](evidence/baseline.json).
2. Separate Sol/high and Luna/high agents reviewed [pricing logic](review-sol/fixture-review.md) and [metadata](review-luna/fixture-review.md) without reading each other's reports.
3. A separate Astra/xhigh agent read both complete reports, traced actual material, and [confirmed three scoped repairs](adjudication/adjudication.md).
4. A different Sol/medium agent repaired exact-int validation, delivery-value validation, and currency metadata in round 1. [Repair report and diff links](repair/repair-report.md). The source requirement was unchanged.
5. A separate Sol/high non-fixer independently checked the repaired revision on an isolated copy: **22/22 contract checks and 59/59 independent checks passed (81/81, both exit 0)**. Ordinary string-subclass compatibility, invalid comparison objects, zero express delivery, arithmetic, and metadata were covered. [Acceptance report](verification/acceptance-report.md), [execution evidence](verification/executions.json), [source hashes](verification/source-hashes.json).

The original contract run was 16/20. After delivery defect coverage was expanded before repair, the baseline was 16/22. The fixer's own 22/22 and 36/36 checks are recorded separately and are not substituted for independent acceptance. One repair–verification round was used; no second or third round was started. A transcribed digest in the repair summary was corrected from machine evidence and acknowledged in the acceptance report; source content and test results did not change.

## Before/after comparison and runtime evidence

A separate GPT-5.6 Sol/high evaluated the same 42 decision scenarios using the untouched pre-migration skills, and reviewed the same before-repair pricing fixture. [Baseline decisions](baseline-old-sol/behavior-decisions.md), [baseline fixture report](baseline-old-sol/fixture-review.md), [comparison limits](evidence/comparison.json). Both Sol versions identified the exact-int and non-string equality validation defects, preserved sampled valid arithmetic, and rejected the W01 false positive. Both model and skill text changed, so this comparison does not isolate model capability from prompt changes. No matched old/new Luna benchmark was run.

[Runtime evidence](runtime-evidence.json) records eight actual tasks' requested configurations and effective host metadata/turn_context: new Sol medium/high, new Luna high, Astra xhigh, and the old Sol/high baseline. No model identity was accepted from an agent's self-description. Scenario-proposed model calls were not actually executed and are not counted as runtime proof.

## Static and packaging checks

[Final static and portability checks](final-checks.json) passed. Both skills pass the official skill-creator format validator. YAML/TOML parsing confirms the original implicit-invocation policies and Astra/xhigh example. Active skill/reference routes contain no GPT-5.6 defaults. Relative Markdown references and Git whitespace checks are checked before publication. The historical validation records, initial test cases, and old release notes are preserved.

Public evidence normalizes local paths and removes runtime IDs; scripts needed for reproduction use relative paths. SHA-256 values in reviewed-material records refer to the originally inspected bytes, including the pre-normalization scripts. Private original evidence and installed-skill backups remain local. The repository baselines are [recorded here](evidence/repository-baselines.json).

## Reproduce the fixture acceptance

Run from a disposable copy of this evidence directory, using Python 3.9 or later:

```sh
python3 -B verification/run_verification.py
```

This writes test copies and logs only inside that copied evidence directory. It expects the before snapshot to differ from the repaired source in two files, and expects requirements to be unchanged. It does not start model agents. The historical review probes in review-sol/ and adjudication/ target fixture-before; they intentionally expose the original defects.

## Limits

- The current session orchestrated the live isolated workflow using the skills' rules. Fresh-session skill-picker injection and optional natural-language loading were not exercised.
- Synthetic unavailable-model, conflict, drift, and exhausted-budget decisions do not prove those failure branches were executed live.
- One old/new Sol run and one small fixture do not establish universal quality equivalence, performance, production readiness, billing, latency, or token savings.
- Actual Sol/xhigh execution was not needed in this sample; its declared host support is distinct from the tested medium/high configurations.
- Future runs still need their own permissions, baseline, current model availability, effective-configuration evidence, and relevant acceptance checks.
