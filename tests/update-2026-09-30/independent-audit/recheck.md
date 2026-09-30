# Bounded final recheck — 2026-09-30

**Result: the targeted issues are closed. No remaining actionable problem was found within this recheck's scope.** The original `report.md` is preserved.

## Changes reviewed

- Adaptive README diagrams, coordination shortcuts, and English default-role text now retain coordination in the current lead. The difficult indivisible-problem row permits 6.1 Sol xhigh/max or Astra according to the difficulty. This closes D1 and the optional D2 alignment from the original report.
- Both packages now require a bundled `runtime-manifest.json` before freezing. Its expected runtime inventory is compared against actual bytes, copied to the snapshot, and checked again by snapshot verification. This closes the demonstrated stable-partial-install gap, provided the bundled manifest represents an intentionally prepared complete package.
- `--seal` is a separate explicit operation. Neither `freeze` nor `verify` invokes it automatically. AGENTS, README, and the runtime references distinguish maintainer edits from normal runs and prohibit using resealing to conceal partial installation or drift.
- Known `.codex`/`.agents` and custom `CODEX_HOME` plugin-cache skill destinations are rejected. The documentation accurately leaves additional host-specific discovery roots to the caller; it no longer needs to imply exhaustive discovery-root knowledge.
- Deep-review README wording permits a reviewer to perform acceptance only when that reviewer did not make the relevant repair. Separate first-round judgments and Astra adjudication remain explicit. This agrees with the operational independence rule without requiring unnecessary fresh agents.

## Executed validation

Both repositories' `tests/test_freeze_run.py` ran with bundled Python and a temporary root under this audit directory: **10/10 passed per repository, exit 0**. The two helper implementations and their tests were also byte-identical when compared.

Independent focused reproductions are retained in `recheck_probe.py`, with outputs in `recheck-results.json`. In each package they confirmed:

1. The actual current source package matches its bundled manifest and can create a verified snapshot.
2. The script inside that snapshot verifies it successfully, exit 0; the copied release manifest matches the source manifest bytes.
3. A sealed v1 fixture changed to v2 SKILL plus v1 reference is rejected before creating a destination. The stale source manifest is preserved.
4. A missing source manifest is rejected and is not recreated automatically.
5. A complete v2 fixture explicitly sealed by the maintainer operation can be frozen.
6. Corrupting the frozen release manifest causes verification failure.
7. Changing even the release-manifest bytes during copying is rejected, and the incomplete destination is removed.
8. Ordinary and custom `CODEX_HOME` plugin-cache skill destinations are rejected.
9. The real source runtime files and bundled manifests remain unchanged after the probes.

Verified runtime digests:

- adaptive-model-orchestrator: `20822d2ce4f764eae3ea3a2fdb8b2c7fa51cb8943521a4a42d2f6493f4f940ad`.
- deep-project-review: `a4768b6532161201f29ab6b8dbec5a0932acb9f690382f40eb4c461b117ee6b8`.

## Practical limit

The expected manifest validates package completeness against an explicitly maintained baseline. It is not a cryptographic authenticity or permission mechanism, and the updated references correctly say so. A maintainer can intentionally seal arbitrary content; requiring intentional maintenance and prohibiting automatic runtime resealing is the appropriate boundary here. No extra authentication mechanism is needed for the stated task.

This was a read-only, bounded recheck of the named changes. No subagents, remote model calls, global-install changes, or full project-review workflow were performed. No evaluation reports or `tests/update-2026-09-30` contents were read.
