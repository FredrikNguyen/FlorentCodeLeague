# v383 post-ramp five-Builder replenishment — rejected

## Objective and scope

The v0046-pinned screen and fresh live review showed losses ending with only
two-to-four Harvesters and a depleted Builder workforce.  v383 tested one
bounded recovery contract: after the initial workforce ramp, the Core could
waive its normal spawn reserve while living Builders were below a five-Builder
floor.  The initial ramp target, normal stage targets, route FSM, economy
phase, combat, Store, and unit policy otherwise stayed unchanged.

Allowed production files were `bots/candidate/bot/core_role.py` and
`bots/candidate/bot/constants.py`; focused coverage was in
`tests/test_candidate_nearest_defense.py`.  Baseline snapshots, package,
upload, activation, and live state were non-goals.

## Validation

- Focused nearest-defense coverage was **27/27**, economy-phase coverage was
  **5/5**, and compileall passed.
- `make static` retained the inherited 15 obsolete-module import errors and
  two navigation fast-path assertions; smoke was **4/4** at
  `reports/local-20260820T224510Z`.
- The rotated all-15-map/30-game paired screen (`screen_seed=583`) was
  command-clean but only **13–17**.  Candidate delivered **29/30** versus
  **30/30**, collected **121,170 vs 151,160 Ti**, and ended with placed/alive
  workforce totals below the comparator (**235/172 Builders/Harvesters vs
  265/212**).  TLE and suspicious-output rows were zero; max p99/peak was
  **1,432/3,732 us**.  Evidence is in
  `reports/iter-v383-replenishment/analysis.json` and
  `reports/local-20260820T224541Z`.

The screen failed both win-rate and conversion floors, so no second screen,
release gate, package, upload, activation, or live operation was justified.

## Rollback and decision

The temporary constant, Core reserve branch, focused test, and screen config
were removed.  Rollback focused coverage passed **27/27**, compileall passed,
rollback smoke was **4/4** at `reports/local-20260820T224918Z`, and recursive
candidate parity with immutable v0046 is empty at
`reports/iter-v383-replenishment/rollback-source-parity.diff`.

Reject v383.  Immutable v0046 remains the baseline; the next hypothesis must
address resource conversion without simply spawning more workforce.
