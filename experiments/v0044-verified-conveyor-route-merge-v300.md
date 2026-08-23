# v300 — verified conveyor-route merge

Date: 2026-08-19

## Hypothesis and scope

Fresh v107 losses showed a route-conversion gap: several matches built many
Conveyors but delivered late after a link was removed.  v300 tested one
conservative merge in `bots/candidate/bot/defender.py`: when a pending chain
tile was adjacent to a friendly Conveyor, the Builder could face into that
Conveyor only after a visible, cycle-bounded fixed-output walk proved that the
whole path reached a friendly Core.  Unknown vision, enemy buildings, cycles,
and Splitter branches were rejected.  Scope also included one temporary
`tests/test_candidate_route_merge.py` module; no role, economy, combat, Store,
navigation, baseline, package, platform, or live-state change was allowed.

## Validation and evidence

- The four focused merge tests passed, and the existing nearest-defense,
  seeded-route, and economy-phase subset passed **38/38**.  Compileall passed.
- `make static` retained the inherited exit-2 profile: 15 obsolete removed
  module imports and two navigation fast-path assertions; no v300-specific
  failure appeared.  `make smoke` was **4/4** command-clean at
  `reports/local-20260819T194050Z`.
- The configured 15-map screen against immutable v0044 was command- and
  delivery-clean but negative: candidate-A finished **6-9**, collected
  **49,920 vs 50,550 Ti**, and first delivery averaged **30.33 vs 21.53**
  turns.  There were zero no-delivery rows, TLEs, or suspicious outputs; max
  p99/peak callback time was **1,465/5,278 us**.  Evidence is
  `reports/local-20260819T194119Z` and
  `reports/iter-v300-route-merge/replay-analysis.log`.

## Decision and rollback

Reject v300 at the first screen without repair or release.  The temporary
merge helper and focused test were removed; candidate `defender.py` is
byte-identical to immutable v0044 (SHA-256
`99c9a0154174b272c8a3d249a9776f1554fd35161953b28a162bfaee81ae133c`), proven
by the empty `reports/iter-v300-route-merge/rollback-source-parity.diff`.
Rollback focused coverage was **34/34**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260819T194550Z`.  No 60-game gate, package,
upload, activation, or live transition occurred.  v105 remains the
operational rollback target and live v107 remains `active_observing`.
