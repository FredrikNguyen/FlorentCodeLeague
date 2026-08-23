# v384 liquidity-backed late workforce expansion — rejected

## Objective and scope

Starting from immutable local baseline
`bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`,
v384 tested whether the existing late Builder target could unlock earlier when
five completed routes and a fresh Core income heartbeat proved that the
economy was paying.  The initial variant used a 250-Ti bank floor; one bounded
repair raised it to 350 Ti.  The opening targets, route FSM, dynamic tasks,
combat policy, Store layout, and platform state were unchanged.

Allowed production files were `bots/candidate/bot/core_role.py` and
`bots/candidate/bot/constants.py`, with temporary workforce coverage in
`tests/test_candidate_nearest_defense.py`.  Temporary screen/release configs,
this record, reports, `UPDATES.md`, `docs/CURRENT_PLAN.md`, and durable state
were bookkeeping only.  Baseline snapshots, navigation, routes, turrets,
Sentinels, Launchers, Barriers, package, upload, activation, and live state
were non-goals.

## Validation

- Initial focused coverage was **32/32**; compileall passed; `make smoke` was
  **4/4** at `reports/local-20260820T225909Z`.  `make static` retained the
  inherited 15 obsolete-module imports and two navigation assertions.
- Rotated screen 1 (`screen_seed=599`) was **19–11** for the candidate,
  command/reliability-clean with **30/30** deliveries for both sides.
  Collection was **153,640 vs 128,480 Ti**; max p99/peak was **1,378/4,127
  us**.  Replay analysis is
  `reports/iter-v384-late-workforce/replay-analysis.json` and the raw matrix
  is `reports/local-20260820T225934Z`.
- Rotated screen 2 (`screen_seed=613`) was **20–10**, also **30/30** delivery
  clean, with **160,350 vs 150,150 Ti** and max p99/peak **1,398/5,166 us**.
  Analysis is `reports/iter-v384-late-workforce/replay-analysis2.json`; raw
  matrix is `reports/local-20260820T230318Z`.
- The required 60-game endpoint-seed release matrix was **29–31**.  Candidate
  delivery was **60/60** versus baseline **58/60**, but collection was
  **312,030 vs 320,120 Ti** and surviving Harvesters/Sentinels were lower
  (**398/63 vs 423/81**).  Runtime was command-clean with zero TLE/suspicious
  rows; max p99/peak was **1,542/5,867 us**.  Analysis is
  `reports/iter-v384-late-workforce/release-analysis.json`; raw matrix is
  `reports/local-20260820T230731Z`.
- Repair focused coverage remained **32/32**, compileall passed, static kept
  the same inherited profile, and smoke was **4/4** at
  `reports/local-20260820T231515Z`.  The 350-Ti repair screen
  (`screen_seed=631`) tied **15–15**, delivered **30/30** on both sides, and
  collected **127,220 vs 141,240 Ti**.  Analysis is
  `reports/iter-v384-late-workforce/repair-analysis.json`; raw matrix is
  `reports/local-20260820T231547Z`.

## Decision and rollback

Reject v384.  The 250-Ti variant's attractive 39–21 two-screen result did not
  transfer to the complete endpoint matrix, and the 350-Ti repair was neutral
  with lower collection.  Remove the temporary gate, threshold, focused test,
  and configs; restore exact recursive candidate parity with immutable v0046.
The parity proof is the empty
`reports/iter-v384-late-workforce/rollback-source-parity.diff`.

Rollback focused coverage was **31/31**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260820T231949Z`.  No promotion, package,
remote gate, upload, activation, or live transition was justified.  The local
baseline remains immutable v0046.

## Follow-up

Do not retry another 250/350-Ti late-target threshold or a broad workforce
expansion.  The release losses concentrate on resource-conversion races on
Drakkarfjord, Glacierkeep, Icefloe, Nordkap, and long Auroraveil rows despite
reliable delivery.  The next hypothesis must use a distinct replay-backed
action or topology mechanism and preserve the delivery, reliability, and
protected-map floors.
