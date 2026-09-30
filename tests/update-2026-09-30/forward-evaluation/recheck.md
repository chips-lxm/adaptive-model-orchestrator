# Targeted independent recheck — 2026-09-30

Only the changed freezing behavior and deep README role wording were rechecked. No eight-scenario rerun, source modification, child agents, actual project review, historical validation or HANDOFF reads. Original `report.md` preserved byte-for-byte: SHA-256 `2e02e34d64c80e446ce3f2bf82eb3d441533efb7f938d2e5590583d7a223ff19`.

## Result

The requested changes pass the targeted checks for both helpers. The prior plugin-directory finding is closed for the demonstrated plugin-cache and custom CODEX_HOME paths. The README reviewer/verifier ambiguity is resolved.

Each freshly constructed synthetic source explicitly ran `--seal` once after intentional fixture creation. Normal `--output` paths never called seal or repaired a missing/stale manifest. Fixtures and test temporary output remained under this report directory; source suites ran with `-B`, `PYTHONDONTWRITEBYTECODE=1` and isolated TMPDIR values.

| Check for each helper | Actual result |
| --- | --- |
| Missing runtime-manifest.json, before explicit sealing | CLI exit 1; neither output directory nor release manifest created |
| One explicit fixture `--seal` | Exit 0; release manifest produced |
| `.codex/plugins/cache/plugin/skills/snapshot` destination | Exit 1: non-discoverable destination required; output absent |
| Custom CODEX_HOME `plugins/cache/plugin/skills/snapshot` destination | Exit 1 with same rejection; output absent |
| Stable partial source update, unchanged release manifest | Exit 1: `Runtime content differs from its manifest`; output absent, manifest unchanged |
| Completed sealed source | Freeze exit 0; release manifest copied byte-for-byte; snapshot verify true |
| Installation source changed after successful freeze | Verify exit 0; same snapshot digest and original content retained |
| Pre-existing empty output | Exit 1, directory preserved |
| Pre-existing nonempty output | Exit 1, sentinel preserved |
| Source tests/test_freeze_run.py suite | Exit 0; 10 tests OK for each skill (20 total) |

Actual executable: `/Users/lxm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

Harness command:

```sh
/Users/lxm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /private/tmp/skill-forward-20260930/run-recheck.py
```

The harness exited 0. `recheck-results.json` records exact per-case CLI commands, exits, stdout, stderr and test-suite commands/TMPDIR. `run-recheck.py` contains the assertions and synthetic setup.

A separate read-only check loaded each current helper with bytecode disabled and ran `inventory(root)` plus `release_bytes(root, files)`. Both distributed release manifests matched actual runtime bytes at check time:

- adaptive-model-orchestrator: 8 runtime files, digest `20822d2ce4f764eae3ea3a2fdb8b2c7fa51cb8943521a4a42d2f6493f4f940ad`.
- deep-project-review: 11 runtime files, digest `a4768b6532161201f29ab6b8dbec5a0932acb9f690382f40eb4c461b117ee6b8`.
- Updated helpers remain byte-identical, SHA-256 `bf77bde05bd4f355d4f846ed3b851a2ac0e43300bed6d47fdb76d8384311760a`.

## Wording and remaining limits

Deep README line 59 now explicitly says that a verifier must not have made the fix and that a reviewer who did not fix it may be reused. It aligns with the operational rule.

Both runtime references expressly describe common installation-path interception, require callers to avoid additional host discovery roots, reserve `--seal` for intentional maintainer edits, prohibit normal-run resealing, and identify digests as consistency checks rather than adversarial authentication or permission isolation. No remaining contradiction was observed in these changed areas. A sealed manifest certifies consistency with the chosen bytes, not their semantic correctness; maintainer-only is a documented use constraint, not operating-system access enforcement. Those limits do not block the tested workflow.

This targeted recheck does not establish fresh-session skill discovery, effective model/effort configuration, actual multi-agent review quality, universal installation-root detection or token savings.
