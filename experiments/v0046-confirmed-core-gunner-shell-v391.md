# v391 confirmed-enemy-Core home-Gunner shell — rejected

Date: 2026-08-21

## Objective and replay basis

Recent live/top-team rows showed winners commonly retaining a three-Gunner
home shell while the v0046 side often had one or none, even when the first
logistics delivery succeeded.  v391 tested whether a confirmed enemy-Core
signal should authorize that shell earlier: after one completed route and
round 36, the Core could raise the home-Gunner cap to three.  The Core's
dynamic cost/reserve, tile legality, lifetime placement guard, and existing
cramped/threat policy remained in force.

## Scope

Temporary production changes were limited to `bots/candidate/bot/constants.py`
and `bots/candidate/bot/core_role.py`; focused coverage was added temporarily
to `tests/test_candidate_nearest_defense.py`.  The temporary screen config was
`configs/.tmp-v391-confirmed-core-shell.toml`.  No baseline snapshot, route
FSM, Store schema, attacker/sentinel policy, package, upload, activation, or
live state was changed.

## Validation and bounded repairs

- Initial focused coverage was **28/28**, compileall passed, and smoke was
  **4/4** (`reports/local-20260821T011617Z`).  The first screen was invalid:
  the new policy referenced an undefined `_update_defense` local, so the
  candidate Core exited on every turn and lost **0–30** with zero candidate
  deliveries.  This was a wiring defect, not strategy evidence; the raw run is
  `reports/local-20260821T011637Z`.
- Repair 1 supplied the route-count local.  Focused coverage stayed **28/28**,
  compileall passed, smoke was **4/4** at
  `reports/local-20260821T011945Z`, and the rotated all-map 30-game screen
  (seed 787) was delivery/reliability-clean but only **13–17**.  Collection
  was **159,840/191,320 Ti**, deliveries **30/30**, and max p99/peak was
  **1,436/5,733 us**, with zero TLE/suspicious rows.
- Repair 2 excluded both fixed attackers from Core home-defense designation,
  because attackers never execute the Gunner builder path.  Focused coverage
  was **29/29**, compileall passed, smoke was **4/4** at
  `reports/local-20260821T012507Z`, and the fresh screen remained below the
  floor at **12–18**.  Collection was **160,370/157,040 Ti**, deliveries
  **30/30**, max p99/peak **1,380/4,598 us**, and zero TLE/suspicious rows.

## Decision and rollback

Reject v391 after the two permitted repairs: neither valid screen met the
**9–6** first-screen floor, and neither justified a long gate.  All temporary
source, tests, and config were removed.  Candidate source is recursively
byte-identical to immutable v0046 (empty proof at
`reports/iter-v391-confirmed-core-shell/rollback-source-parity.diff`).
Rollback focused coverage was **26/26**, compileall passed, static retained the
known inherited exit-2 profile, and rollback smoke was **4/4** at
`reports/local-20260821T013135Z`.  Reports and raw matrices are under
`reports/iter-v391-confirmed-core-shell/`,
`reports/local-20260821T011637Z`, `reports/local-20260821T012012Z`, and
`reports/local-20260821T012525Z`.  No promotion, package, upload, activation,
or live transition occurred; immutable v0046 remains the best local baseline.

## Remaining risk

The shell gap is correlated with losses but is not fixed by an earlier cap or
designation-only change.  Future work must use a distinct pressure-conversion
mechanism and preserve the v0046 opening economy.
