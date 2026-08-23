# v381 Sabotage-first attacker ordering — rejected

## Objective

Starting from immutable v0046, test whether the fixed attacker should interrupt
the enemy logistics before constructing the cheap enemy-Core Barrier cage.  The
current code's comments described logistics-first pressure, but its actual
priority built the cage first.  This candidate changed only that ordering.

## Scope and non-goals

Production scope was limited to `bots/candidate/bot/attacker.py`, with one
focused ordering test in `tests/test_candidate_nearest_defense.py`.  Route
construction, Store schema, Sentinel pool, Launcher policy, dynamic-worker
tasks, baseline snapshots, and live files were not changed.

## Validation

- Focused coverage passed **27/27**; compileall passed; `make smoke` passed
  **4/4**.  `make static` retained only the inherited 15 obsolete-module
  imports and two navigation fast-path assertions.
- The rotated all-15-map/30-game screen (`screen_seed=559`) was command- and
  delivery-clean: **16–14**, 30/30 first deliveries, zero TLE/suspicious rows,
  candidate collection **111,230 Ti**, maximum p99/peak **1,590/3,081 us**.
- The first-screen promotion floor was not met.  No second screen, release
  matrix, package, upload, activation, or live transition ran.

## Rollback and decision

The ordering change and focused test were removed.  Rollback focused coverage
passed **27/27**, compileall passed, rollback smoke passed **4/4** at
`reports/local-20260820T221702Z`, and recursive candidate production parity with
v0046 is empty in
`reports/iter-v381-sabotage-first/rollback-source-parity.diff`.

**Reject v381.**  Immutable v0046 remains the best local baseline.

Evidence: `reports/iter-v381-sabotage-first/` and
`reports/local-20260820T221235Z/`.
