# v0047 pressure-phase economy steward (v392)

Date: 2026-08-21

## Objective and scope

Starting from immutable v0046, preserve one local dynamic Builder on the
SCOUT/CHAIN economy loop after the Core reports healthy `PRESSURE`.  The
existing permanent Defender is still the economy floor, but it can be dead,
under siege, or committed to a long chain.  The new steward is selected by the
existing nearest-home lease: only a non-fixed Builder inside the home response
radius can claim it, and a closer local Builder wins.  Forward dynamic
Builders keep the existing raid/denial/advance behavior.

Production scope was `bots/candidate/bot/dynamic.py`; focused coverage added
one pressure-steward ownership test in
`tests/test_candidate_economy_phase.py`.  Route geometry, Store layout,
spawning, ammo, turrets, Sentinels, Launchers, Barriers, fixed attackers,
baseline snapshots, and live state were non-goals.

## Validation

- Focused phase/defense coverage: **32/32** (`reports/iter-v392-pressure-steward/focused.log` was run as the two focused unittest modules).
- Candidate compileall passed (`reports/iter-v392-pressure-steward/compileall.log`).
- `make static` retained the inherited exit 2 only: 15 obsolete-module import
  errors and two navigation fast-path assertions; the v392 tests themselves
  passed (`reports/iter-v392-pressure-steward/static.log`).
- `make smoke` was **4/4** command-clean at
  `reports/local-20260821T014245Z` (`reports/iter-v392-pressure-steward/smoke.log`).
- Rotated screen 1 (`screen_seed=797`) was **19–11** against v0046, with
  **30/30** deliveries, zero command/TLE/suspicious rows, and
  **132,690/119,950 Ti** collection.  Raw games and analysis are under
  `reports/local-20260821T014408Z` and
  `reports/iter-v392-pressure-steward/replay-analysis.json`.
- Rotated screen 2 (`screen_seed=809`) was **15–15**, with **30/30**
  deliveries, zero command/TLE/suspicious rows, and **177,570/135,530 Ti**
  collection.  Raw games and analysis are under
  `reports/local-20260821T014723Z` and
  `reports/iter-v392-pressure-steward/replay-analysis-2.json`.
- Combined screen result: **34–26**, meeting the 19–11 paired floor.
- Pinned 60-game release gate: **35–25**, **59/60** candidate deliveries vs
  **60/60** baseline, zero command failures/TLE/suspicious rows, max
  p99/peak **1,310/3,361 us**, and **324,040/237,410 Ti** collection.  The
  sole no-delivery row was Glacierkeep seed 1 side B; this remains a risk but
  was not a protected-map collapse.  Evidence is under
  `reports/local-20260821T015046Z` and
  `reports/iter-v392-pressure-steward/release-analysis.json`.
- Server gate `dbe3b194-6997-4ade-920e-3a211b9a666e` completed **3–2** for
  candidate across sprint/bridge/crossfire/vault/aurora; final JSON is
  `reports/iter-v392-pressure-steward/remote-info-final.json`.

## Decision

Promote v392 to the new local baseline.  The candidate clears the paired
screen, local release, and server gates with a substantial aggregate edge.
Retain the Glacierkeep no-delivery replay as the first follow-up risk; do not
change the steward rule during this promotion checkpoint.
