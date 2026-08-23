# v179 pre-route Core-ring deferral

## Objective

Improve the recurring low-Harvester loss pattern by deferring opportunistic
Core conveyor-ring maintenance until the first completed route has proved the
economy. The route FSM itself, workforce counts, combat roles, and Store policy
were unchanged. A later repair restored dynamic ring-gap ownership and then
tested a cramped-map exception.

## Allowed files

- `bots/candidate/bot/defender.py`
- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and durable project state

## Non-goals

No workforce/role target, Harvester cost or route geometry, combat/Sentinel/
Gunner/Barrier/Launcher policy, Store schema, map-specific coordinates,
baseline/archive, package, upload, activation, or live-state change.

## Evidence

- Initial v179 deferred both defender ring builds and dynamic ring-gap tasks
  before the first route. Focused checks passed **21/21**, compileall passed,
  smoke **4/4**, and static retained the inherited 15 obsolete-import errors
  plus two navigation assertions. The 21-game all-map screen regressed to
  **7-14**, collection **79,270 vs 88,410** (0.8966x), with one candidate
  no-delivery row; candidate placed **136 vs 187** Harvesters. Reports:
  `reports/local-20260818T054730Z` and
  `reports/iter-v179-pre-route-ring-screen-replay-analysis.json`.
- Repair 1 restored dynamic ring-gap tasks while retaining only the defender
  opportunistic deferral. Focused checks stayed **21/21**, compileall passed,
  smoke **4/4**, and the 21-game screen improved to **12-9**, collection
  **104,890 vs 99,730** (1.0517x), with zero no-delivery rows. Reports:
  `reports/local-20260818T055026Z` and
  `reports/iter-v179-pre-route-ring-repair1-screen-replay-analysis.json`.
- The repair-1 release matrix was command-clean and scored **32-28**, with
  collection **268,070 vs 264,930** (1.0119x), candidate/comparator
  no-delivery **2/0**, zero TLE/suspicious-output rows, and max p99/peak
  **1,496/5,849 us**. Protected map floors were weak (Auroraveil **1/4**,
  Drumlin/Midgard/Ragnarok/Valkyrie/Yulerune **1/4**); report:
  `reports/local-20260818T055306Z`, analysis
  `reports/iter-v179-pre-route-ring-repair1-release60-replay-analysis.json`.
- Repair 2 allowed pre-route ring maintenance only when the map's mirrored
  Core distance was within `CRAMPED_CORE_DIST`. Focused checks stayed **21/21**,
  compileall passed, smoke **4/4**, but the screen fell to **6-15**, collection
  **68,200 vs 91,450** (0.7458x), with one candidate no-delivery row. Reports:
  `reports/local-20260818T060050Z` and
  `reports/iter-v179-pre-route-ring-repair2-screen-replay-analysis.json`.

## Decision and rollback

v179 is **rejected** after both bounded repairs. Repair 1's release edge was
not material enough to justify its two candidate no-delivery rows and weak
map floors; repair 2 failed the screen decisively. The temporary defender,
dynamic, and test changes were removed with `apply_patch`; recursive
candidate-v0040 source parity is **0 diff lines** at
`reports/iter-v179-rollback-source-diff.txt`. Rollback focused checks passed
**20/20**, compileall passed, and rollback smoke was **4/4**
(`reports/local-20260818T060334Z`). No remote gate, package, upload,
activation, or baseline transition occurred.
