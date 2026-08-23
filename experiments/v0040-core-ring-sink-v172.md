# v0040 Core-ring sink merge — v172

## Objective

Recover Harvester routes that reach the Core neighbourhood but cannot finish
because the direct Core-facing tile is occupied by an existing friendly
conveyor ring. Permit exactly one additional verified sink: a pending chain
conveyor may face a visible friendly Conveyor whose own facing is directly into
our Core. Do not enable arbitrary conveyor-to-conveyor merges.

## Comparator and allowed files

- Comparator: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Source: `bots/candidate/bot/defender.py`.
- Focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, `UPDATES.md`, and durable project state.

## Non-goals

No route geometry, workforce/role/task policy, idle fallback, combat, ammo,
turret/Sentinel/Launcher/Barrier behavior, Store schema, map branch, baseline,
archive, package, upload, activation, or live-state change.

## Hypothesis and implementation

Add a small helper beside `_best_feed_direction` that scans only the four
cardinal output tiles. It returns a direction only when the output is a
friendly Conveyor, that Conveyor is visible, and its actual facing equals the
direction from the ring tile into a visible friendly Core footprint. The
existing direct-Core check remains first; all other Conveyor tails remain
unverified and are rejected exactly as in v0040. Use the returned direction in
the pending-chain completion path, so a successful build records one completed
route through the verified ring sink.

## Done criteria

- Focused tests prove a Core-facing ring conveyor is accepted, an arbitrary
  conveyor is rejected, and direct Core behavior is unchanged.
- Candidate compileall passes; `make static` is checked and inherited failures
  are recorded; smoke is command-clean.
- The 21-game all-map screen materially improves paired win rate over v0040
  with no candidate no-delivery, command, TLE, or suspicious-output regression.
- Only a materially positive screen advances to the 60-game release gate. A
  tie/regression or delivery/reliability failure requires exact v0040 rollback
  and no platform operation.

## Evidence and decision

- Initial implementation passed focused checks **21/21**, compileall, and
  command-clean smoke (**4/4**, `reports/local-20260818T032158Z`). Static
  retained the inherited 15 obsolete-import errors and two navigation
  assertions. Its 21-game all-map screen was command-clean and scored
  **11-10** versus v0040, with mean first delivery **21.9 vs 29.6** and mean
  final resources **4,051 vs 3,556**; the one-game edge was not material
  (`reports/local-20260818T032223Z` and
  `reports/iter-v172-core-ring-sink-screen-replay-analysis.json`).
- Bounded repair 1 gated ring recognition on at least one completed route.
  Focused checks remained **21/21**, compileall passed, smoke was **4/4**, and
  static was unchanged. The screen fell to **9-12**, despite resources
  **5,069 vs 4,931** and first delivery **22.3 vs 24.9**
  (`reports/local-20260818T032533Z` and
  `reports/iter-v172-core-ring-sink-repair1-screen-replay-analysis.json`).
- v172 is rejected after the bounded repair budget. Both source and focused
  test changes were removed; recursive v0040 parity is **0 diff lines** in
  `reports/iter-v172-core-ring-sink-rollback-source-diff.txt`. Rollback focused
  checks passed **20/20**, compileall passed, and rollback smoke was **4/4**.
  No 60-game gate, package, release, remote match, upload, activation, or
  baseline transition occurred.
