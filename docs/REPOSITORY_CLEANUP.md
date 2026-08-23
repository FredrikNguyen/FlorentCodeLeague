# Repository cleanup — 2026-08-23

This checkpoint records the repository-only cleanup after v411 was rejected.
It does not promote, package, upload, activate, or otherwise change a bot.

## Release of record

- Immutable snapshot: `bots/versions/v0047_pressure-economy-steward_20260821-0200_eeafad8f`
- Mutable upload tree: `bots/candidate/`
- Comparator state: `state/project_state.json` (`baseline_path` points to v0047)
- The candidate and v0047 snapshot have empty recursive production diffs.

Only v0047 remains under `bots/versions/`. The v0001–v0046 directories were
superseded snapshots, not unique source of truth; their hypotheses, outcomes,
and report references remain in `experiments/`, `UPDATES.md`, and `reports/`.

## Removed from the checkout

- Obsolete root starter/planning ZIP archives and generated ChatGPT handoff
  outputs. Packets are rebuilt on demand from tracked source and state.
- v0001–v0046 immutable snapshot directories.
- Root and replay-directory `.replay26` payloads, the old v73 replay-diagnosis
  bundle, Python/test/tool caches, and experiment `.tmp-*` run artifacts.
- Pre-v0047 tests and the starter benchmark that imported modules removed by the
  current `bot/` package layout. The v0047-focused tests remain under `tests/`.
- The obsolete root starter `main.py`, stale v0001 submission payload, generated
  package metadata, accumulated rejected plans, and superseded iteration packet.
- Ignored historical submission/platform packages were moved to a recoverable
  temporary quarantine; only the v0047 ZIP and manifest remain locally.

The removed generated files were moved to a temporary quarantine during this
session rather than irreversibly erased. They are not part of the repository or
the publish commit.

## Retained evidence

All durable experiment Markdown records, `UPDATES.md`, state files, source,
tests, scripts, and ignored `reports/` evidence remain available. Historical
references to superseded snapshot names are intentional provenance, not active
evaluation paths.

`.gitignore` now keeps caches, replay payloads, temporary experiment entries,
root archives, and generated handoff ZIPs out of future commits while explicitly
allowing the retained v0047 snapshot.

## Verification

- Current v0047-focused unit tests: **36/36**.
- `make static`: **67/67** tests and compileall passed.
- `make smoke`: **4/4** command-clean games; report
  `reports/local-20260823T073457Z`.
- Static and smoke logs are retained under the ignored `reports/` directory.
