# v169 staged workforce expansion

## Objective

After v0040's first completed Harvester route unlocks the existing stage-2
workforce, raise only that staged living-Builder target from 8 to 10. The
additional Builders should stay in the existing Defender/Dynamic policy and
convert into more Harvesters and path construction rather than introducing a
new attack role.

The hypothesis is motivated by the v0040 pressure-loss audit: several losses
delivered early but ended with only 3–4 candidate Harvesters against 8–15 for
the winner. The current stage-2 target of 8 can therefore leave the economy
understaffed even when the first route has already paid for expansion.

## Comparator and allowed files

- Comparator: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Source: `bots/candidate/bot/constants.py`.
- Focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, `UPDATES.md`, and durable project state.

## Non-goals

No route geometry or chain FSM, task ordering, role assignment, Sentinel or
Gunner policy, ammo conversion, map branch, Store schema, cost/reserve rule,
baseline/archive, package, upload, activation, or live-state change.

## Implementation

- Change `REINFORCEMENT_BUILDER_TARGET` from 8 to 10.
- Keep `HARVESTER_MILESTONE`, `STAGE2_FALLBACK_ROUND`, `SPAWN_RESERVE`, and the
  late five-route target unchanged.
- Add a focused spawn-target test proving the stage-2 target reaches 10 while
  the pre-stage target remains the initial roster.

## Done criteria

- Focused tests and compileall pass; `make static` is checked and any inherited
  failures are recorded; smoke is command-clean.
- The 21-game all-map screen improves aggregate paired win rate over v0040
  without candidate no-delivery, command, TLE, or suspicious-output failures.
- Only a materially positive screen advances to the 60-game release gate. A
  tie/regression or a delivery/reliability failure requires exact v0040
  rollback, with no package, upload, activation, or baseline transition.
- Self-review confirms only the scoped constant/test/metadata changes remain.

## Evidence and decision

The initial expansion passed focused checks **21/21**, compileall, and smoke
**4/4**. Its 21-game all-map screen was **7-14** against v0040, with one
candidate no-delivery game versus zero for the comparator. Candidate mean
Harvester placements were **6.86 vs 9.48**, mean first delivery **24.4 vs
46.9**, and Sentinel placements **3.14 vs 4.33**; all commands were clean,
with max p99/peak **1,494/3,180 us**. Evidence:
`reports/local-20260818T025040Z` and
`reports/iter-v169-stage2-workforce-screen-replay-analysis.json`.

Repair 1 kept the shipped eight-Builder wave after route 1 and unlocked ten
only after route 2. Focused checks passed **22/22**, compileall passed, static
retained only inherited failures, and smoke was **4/4**. The screen recovered
to **12-9**, but still had one candidate no-delivery game versus zero for
v0040; mean Harvesters were **7.38 vs 8.05** and Sentinels **3.43 vs 3.14**.
Replay execution remained clean with max p99/peak **1,437/5,631 us**.
Evidence: `reports/local-20260818T025446Z` and
`reports/iter-v169-stage2-workforce-repair1-screen-replay-analysis.json`.

v169 is rejected after the bounded repair: the aggregate edge did not meet
the delivery/reliability criterion, so no 60-game gate, remote test, package,
upload, activation, or baseline transition was attempted. The constant,
Core guard, and focused tests were removed; candidate source is exact
recursive v0040 parity (**0 diff lines** in
`reports/iter-v169-stage2-workforce-rollback-source-diff.txt`). Rollback
focused checks passed **20/20**, compileall passed, and rollback smoke was
**4/4** (`reports/local-20260818T025809Z`).
