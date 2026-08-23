# v206 — coordinated forward assault lane

## Objective

Replace the isolated forward-shell task with an explicit phase handoff: one
dynamic Builder already near a fixed attacker and a confirmed enemy Core could
alternate a legal Barrier and Sentinel support action while preserving route
liquidity. The support Builder never owned the approach.

## Scope and non-goals

- Temporary source: `bots/candidate/bot/constants.py` and
  `bots/candidate/bot/dynamic.py`.
- Temporary focused coverage: `tests/test_candidate_forward_assault.py`.
- Regression schedule: `configs/eval_regression.toml`, rotated seed 171.
- No opening route/ore policy, failed-chain cleanup, long-range dynamic travel,
  Launcher fleet, Store schema, map branch, home-Gunner/ammo, sabotage target
  ranking, baseline, package, upload, activation, or live-state change.

## Validation and replay evidence

- Initial focused coverage was **27/27**, compileall passed, static retained
  inherited failures, and smoke was **4/4**. The seed-171 screen was **6-9**,
  command-clean with zero TLE/suspicious output/no-delivery rows. Candidate
  first delivery improved to **24.0** versus **36.4** for v0042 and Harvesters
  increased to **142 vs 119**, but candidate converted less into forward
  pressure: **58 vs 67 Barriers** and **36 vs 46 Sentinels**. Collection was
  **74,750 vs 85,530 Ti**. Reports: `reports/local-20260818T142738Z` and
  `reports/iter-v206-forward-assault-replay-analysis.json`.
- One bounded repair front-loaded a legal Sentinel whenever the lane had no
  damage source. Focused coverage was **28/28**, compileall passed, static
  retained exit 2, and smoke was **4/4**. The same screen remained **6-9** and
  introduced a candidate no-delivery Icefloe row; first delivery was
  **29.5 vs 29.67**, collection **63,850 vs 61,410 Ti**, and pressure was
  **54 vs 67 Barriers**, **53 vs 65 Sentinels**. Reports:
  `reports/local-20260818T143031Z` and
  `reports/iter-v206-forward-assault-repair-replay-analysis.json`.

## Decision and rollback

Reject v206 after the permitted repair: coordination changed the phase and
improved some delivery rows, but did not create a paired win-rate edge and the
repair introduced a reliability regression. Temporary source and tests were
removed; candidate production files are recursively byte-identical to
immutable v0042. Rollback nearest-defense was **23/23**, compileall passed,
static retained the inherited exit 2, and smoke was **4/4**. Logs are under
`reports/iter-v206-forward-assault-rollback-*`. No release gate, package,
upload, activation, or live transition was justified.

## Replay follow-up

The top-team pattern is broader than a Builder support task: their Launchers
reposition units and their forward shell remains fed by a larger, coordinated
workforce. v206's fixed-attacker visibility contract was too brittle and did
not produce enough durable pressure. The next hypothesis must inspect actual
Launcher action timing and unit-cap/workforce conversion, then change the
unit-control architecture rather than add another task-priority branch.
