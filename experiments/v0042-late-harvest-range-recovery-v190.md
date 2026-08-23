# v190 late no-delivery harvest-range recovery

## Objective

Recover maps where the early short-radius ore contract has produced no
completed Harvester route by round 80. After that bounded failure signal, admit
the normal map-scaled harvest range only when the bank can fund an estimated
Harvester-plus-conveyor route and one replacement Harvester reserve.

## Scope and non-goals

- Temporary source: `bots/candidate/bot/constants.py` and
  `bots/candidate/bot/defender.py`.
- Focused coverage: `tests/test_candidate_harvest_range_recovery.py`.
- Screen schedule: `configs/eval_regression.toml` rotated to seed 159; the
  quick gate remains 15 games covering every configured map once.
- No changes to route construction, combat, workforce, ammo, turrets,
  Launcher/Splitter behavior, baseline snapshots, package, or live state.

## Validation

- Initial focused checks: **31/31**, compileall passed, smoke **4/4**, and
  static retained only the inherited 15 obsolete-module imports and two
  navigation assertions (`reports/iter-v190-harvest-recovery/focused.log`,
  `compileall.log`, `static.log`, `smoke.log`).
- Initial seed-158 screen: **6-9** candidate wins, 15/15 command-clean, no
  TLE or suspicious output (`reports/local-20260818T095623Z`; replay analysis
  in `reports/iter-v190-harvest-recovery/replay-analysis.json`). Replay review
  showed late delivery and low liquidity on the recovery path.
- Repair 1 required an estimated route bank before relaxing the radius.
  Focused checks remained **31/31**, compileall and smoke were clean, static
  retained inherited failures, and seed-158 recovered to **8-7**
  (`reports/local-20260818T095905Z`).
- Independent seed-159 rotation then scored **7-8**, 15/15 command-clean, with
  no TLE or suspicious output (`reports/local-20260818T100048Z`).

## Decision and rollback

The repaired edge reversed on the independent rotation, so v190 did not show
a reliable aggregate improvement and did not earn the 60-game release gate.
The temporary constants/defender/test changes were removed; both production
files are byte-identical to immutable v0042 and the candidate tree has no
source difference. Rollback focused checks passed, compileall passed, static
retained only the known inherited failures, and rollback smoke was **4/4**:

- `reports/iter-v190-harvest-recovery/rollback-focused.log`
- `reports/iter-v190-harvest-recovery/rollback-compileall.log`
- `reports/iter-v190-harvest-recovery/rollback-static.log`
- `reports/iter-v190-harvest-recovery/rollback-smoke.log`

No release matrix, package, remote gate, upload, activation, or baseline
transition was performed.
