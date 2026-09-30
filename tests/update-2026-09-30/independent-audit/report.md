# Independent audit — 2026-09-30 skill update

## Conclusion

No blocking execution defect or lost deep-review invariant was found in the inspected revision. Both snapshot test suites pass (7 tests each), and both real skill trees can be frozen and verified using the script inside their own snapshots. The main execution instructions preserve the required model choices and independence boundaries. Two README passages should be aligned with the new operational routing. The snapshot helper has a demonstrated release-coherence limitation, but the reproduction does **not** show a failure of its byte-stability check.

This was a source/behavior audit under skill-creator, not invocation of deep-project-review against a live project. No children were created. No repository or installed skill files were changed. I did not read evaluation reports or any contents of `tests/update-2026-09-30`.

## Scope and evidence

Inspected both repositories' `AGENTS.md`, `REQUIREMENTS.md`, `SKILL.md`, `agents/openai.yaml`, applicable references, `scripts/freeze_run.py`, `tests/test_freeze_run.py`, and both READMEs. Also inspected deep-review's entry/config examples. Compared the changed operational rules and templates with the local `before-6-1-sol-2026-09-30` tag. Historical test reports were not used as evidence.

Commands executed with the supplied bundled Python:

```text
TMPDIR=/private/tmp/skill-astra-20260930/tmp python3 -B tests/test_freeze_run.py
```

Executed once in each repository: exit 0, 7 tests passed per repository. These test stable snapshots, preserved existing destinations, reference drift, rejected symlinks, basic discovery paths, copy-time source mutation, and manifest digest mismatch.

Additional reproducible probes are in `probe.py`; results and the exact runtime source hashes are in `probe-results.json`, both alongside this report. The probe copies only into its temporary directory and imports with `-B`. It verified real source snapshots, ran each copied script's `--verify`, and checked that each source inventory remained unchanged. Temporary snapshot directories are intentionally cleaned up; the reproducer and result evidence remain.

Inspected runtime digests:

- adaptive-model-orchestrator: `0bf3b95ad9aa8c7d96d6d3d00555a68cb582e7e094da85121278bce6621ba7e5` (8 runtime files).
- deep-project-review: `aa793ac115500e97dd048f99c3a7dcc8295312dc94265f903571e308b24e24ff` (11 runtime files).

## Actionable documentation drift

### D1 — P3: README still routes coordination to a new Sol role

Locations: adaptive-model-orchestrator `README.md:8`, `README.md:43`, `README.md:63`; analogous diagram and “协调与集成” entry in `README.zh-CN.md`.

The operational `references/collaboration-and-validation.md` now says progress coordination belongs to the current session and explicitly forbids an idle branch created just to coordinate. `SKILL.md` retains the user's chosen lead model. The README diagram/shortcut still presents coordination as `6.1 Sol · high/xhigh/max`, and its English default-role paragraph includes coordination. Although later README qualifications allow combined roles and prevent a mandatory branch, the prominent shortcut is stale and encourages the exact unnecessary handoff the revision is trying to remove.

Minimal correction: label coordination as the current lead; label Sol as implementation/integration/review. Preserve the lead's ability to delegate useful independent work. This is a documentation inconsistency, not evidence that the operational skill will invariably spawn an unnecessary branch.

### D2 — Optional alignment: the indivisible-problem row is narrower than the new route

Locations: adaptive-model-orchestrator `README.md:58` and the equivalent Chinese task-shape row.

The README says an indivisible difficult reasoning problem goes to Astra. The revised operational rules allow a suitable strong configuration and explicitly permit 6.1 Sol `xhigh` or `max` directly for difficult reasoning. Astra remains valid and is still preferable for the stated uncertainty/risk cases, so this is not a forbidden route or a lost capability. It is nevertheless easy to read the table as an unconditional Astra requirement.

Optional correction: say to choose a suitable strong configuration (6.1 Sol `xhigh/max` or Astra as warranted), with an independent reviewer when needed. Do not imply that Sol max replaces deep-review's mandatory separate Astra xhigh adjudicator.

## Demonstrated snapshot limitation, not a copy-stability bug

### L1 — Stable partial installs are accepted

Location in both copies: `scripts/freeze_run.py:68–82`; creation guidance in adaptive's collaboration reference and deep-review's runtime reference.

Reproduction: create a synthetic source whose `SKILL.md` is already version 2 while `references/rules.md` is still version 1; leave that source unchanged during the copy. Both helpers return `verified: true`. The probe records `stable_partial_install_accepted: true` for both repositories. This models a file-by-file installer paused or failed between two updates. No concurrent source mutation is necessary.

The code compares the source inventory before and after copying and validates the copied bytes against that inventory. It correctly catches changes during the operation. It has no independently established expected release manifest and therefore cannot know whether the initial inventory represents one published revision or an already mixed installation. The generated `snapshot.json` proves self-consistency, not release provenance.

Impact: if freezing is allowed while an installation is partially updated, all branches consistently read a hybrid version. This defeats the broader intention of avoiding old/new rule mixing, even though snapshot immutability works. Existing documentation already says to finish active runs or arrange a version boundary before replacing an installation, so this reproduction alone does **not** establish that the documented intended workflow is broken.

Recommended proportional response: make the creation precondition explicit beside the freeze command: finish/verify a complete installation first; do not create a snapshot while installation is in progress; perform installation from a complete staged version or under an update/snapshot exclusion boundary. Continue using snapshots for existing active runs. A real enforced installation boundary is sufficient for the current requirement; a vague statement that a directory “looked stable” is not sufficient.

A shipped expected-runtime manifest would provide a stronger, independently checkable guarantee and detect an interrupted partial install even after the installer has stopped. My evidence warrants considering it if unattended installation/snapshot concurrency or recovery from interrupted installs is in scope. It does **not** require adding this machinery to make byte pinning correct. If adopted, regeneration must be explicit after intentional maintainer edits; `freeze` must not silently regenerate the expected manifest from whatever files happen to exist, because that would reproduce the same limitation. Keep the shipped expected manifest distinct from the per-run snapshot manifest. Account for the maintenance cost and avoid making legitimate local skill edits unusable without a clear refresh path.

## Preserved behavior and overhead assessment

Source-level scenario checks confirm:

- Simple/local work can remain in the current session; multi-agent work still requires an explicit benefit and ready, nonconflicting boundaries.
- 6.1 Sol defaults to high, may go directly to xhigh/max, and need not fail through a tier ladder. 6 Sol remains available for evidence-backed paths. Luna stays high and bounded.
- Discussing or modifying deep-project-review does not invoke it. Its explicit gate and `allow_implicit_invocation: false` remain intact.
- An authorized deep review still requires multiple real independent reviewers and a separate Astra xhigh adjudicator, including when all reports are clean or the user requests review only.
- Review-only authorization does not authorize repairs. Necessary authorized repairs may proceed without repeated permission prompts.
- Independent acceptance uses a real agent uninvolved in that repair and requires personal execution of key checks. Reuse of applicable evidence cannot replace these checks.
- Model escalation, extra tasks, and supplemental investigation do not reset the two repair–verification rounds.
- Actual failures, unrun checks, and unverifiable results remain distinct from passes. Added-test failures alone still cannot establish a newly introduced regression.

The shared record, focused reports, evidence reuse with invalidation, targeted Astra checks, and no mandatory model ladder are plausible reductions in unnecessary cost. No quantitative token/latency improvement was measured or inferred. The new snapshot adds small deterministic work and seems proportionate to the requested version-consistency requirement. No extra mandatory coordination branch or unconditional full-project rerun was introduced.

## Limits

This audit did not run a full real multi-agent review/repair workflow, exercise remote model availability, test fresh-session host discovery, or measure performance. The desk-checked scenarios above are reasoned evaluations of the instructions, not claims that those full workflows executed. The report does not independently confirm installer safety outside the inspected guidance.
