# v379 occupied chain-frontier repoint — rejected

## Objective and scope

Starting from immutable v0046, v379 let a route in `MODE_CHAIN` repair an
already occupied friendly Conveyor at its pending frontier when that Conveyor
was visibly facing the wrong way.  The Builder verified ownership, dynamic
price, adjacency, destroy legality, and rebuild legality; foreign buildings,
other structures, and arbitrary joins remained blockers.  Production scope was
`bots/candidate/bot/defender.py`, with temporary focused coverage in
`tests/test_candidate_nearest_defense.py`.

## Validation

- Focused coverage passed **27/27**, compileall passed, `make smoke` was **4/4**
  at `reports/local-20260820T215202Z`, and static retained only the inherited
  workspace failures (15 obsolete imports and two navigation assertions).
- The first rotated all-15-map/30-game screen (`screen_seed=533`) was
  command-clean but **15–15**, with 30/30 deliveries and zero TLE/suspicious
  rows.  Candidate collection was **163,420 Ti**, first delivery averaged
  **27.47** rounds, and average surviving units were 6.73 Harvesters, 0.93
  Sentinels, 2.30 Gunners, and 8.43 Builders.  Raw games are under
  `reports/local-20260820T215233Z`; diagnostics are in
  `reports/iter-v379-chain-repoint/analysis.json`.

The first-screen floor failed, so no second screen or release matrix was
justified.

## Rollback and decision

The temporary repoint branch, focused test, and screen config were removed.
Candidate production is recursively byte-identical to immutable v0046; the
empty proof is at `reports/iter-v379-chain-repoint/rollback-source-parity.diff`.
Rollback focused coverage was **26/26**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260820T215714Z`.  No baseline, package, upload,
activation, promotion, or live-state transition occurred.

Reject v379.  The local repoint repaired a legal defect but did not create a
repeatable win-rate edge; keep the verified route sink and choose a distinct
resource-conversion mechanism next.
