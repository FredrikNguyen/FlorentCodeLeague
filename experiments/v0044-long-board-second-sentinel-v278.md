# v278 long-board income-backed second Sentinel — rejected

Date: 2026-08-19

## Objective and scope

The latest live v105 loss against Well had no forward Sentinel, while its
winner reached three Sentinels with four Harvesters.  v278 tested one narrow
pressure handoff: after one completed route and a Core-published converting or
pressure phase, a board with width plus height at least 60 could raise the
early Sentinel pool from one to two.  Confirmed-Core intel, range, dynamic
prices, site memory, legality, and the mature three-Sentinel pool stayed
unchanged.  Only `bots/candidate/bot/attacker.py`,
`bots/candidate/bot/constants.py`, and focused tests were implementation scope.

## Evidence

- Focused coverage passed **34/34**, compileall passed, `make static` retained
  inherited exit 2, and smoke was **4/4**.  All artifacts are under
  `reports/iter-v278-long-board-sentinel/`.
- Seed-172 report `reports/local-20260819T133716Z` was **7-8**.  Candidate /
  comparator collection was **68,900/76,640 Ti**, delivery **15/15 vs 15/15**,
  and Sentinel placements **46/44**; candidate reliability had zero TLE or
  suspicious rows.  Candidate placed **92 vs 150 Harvesters**.
- Seed-175 report `reports/local-20260819T133920Z` was **7-8**.  Collection
  was **43,120/51,100 Ti**, delivery **14/15 vs 15/15**, and Sentinel
  placements **39/50**; there was one candidate no-delivery row but zero TLE
  or suspicious rows.  Candidate placed **100 vs 113 Harvesters**.
- The paired result was **14-16**, collection **112,020/127,740 Ti**, and
  delivery **29/30 vs 30/30**.  The extra early Sentinel did not create a
  pressure edge and coincided with route-conversion loss, so no repair or
  longer gate was justified.

## Rollback and risks

The candidate source was restored recursively byte-identically to immutable
`bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`;
`reports/iter-v278-long-board-sentinel/rollback-source-parity.diff` is zero
bytes.  Rollback focused coverage was **31/31**, compileall passed, smoke was
**4/4**, and static retained exit 2.  No release gate, promotion, package,
upload, activation, or live transition occurred.  v0044 remains the local
baseline.  v105 remains the requested historical rollback reference only;
v101 remains the guarded operational fallback because v105's recorded live
result is 142/275 (51.64%).
