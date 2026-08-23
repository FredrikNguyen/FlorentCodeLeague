# v256 first-route Gunner-ray shield — rejected after bounded repair

## Replay basis and objective

The fresh v106 SmartFridge series (`3df91a25-a3b7-4386-90b4-d0f03c98f3c3`)
contained a direct route-conversion failure: our game-1 side built two
Harvesters and 30 Conveyors but delivered no titanium. Its first route ended
at `(6,1)` after 14 links, while the opponent had a Gunner at `(8,3)` from
round 20 and delivered at round 24. The same audit found no opponent Conveyor
adjacent to one of our Harvesters, so this was not evidence for a new
anti-infiltrator or hijack selector.

v256 tested one defensive topology response. During only an ordinary first
Harvester CHAIN, the route owner could build at most one dynamic-price Barrier
on an adjacent empty tile of a visible enemy Gunner ray when the immediate
next route tile was itself dangerous. The gate retained a Harvester, two
Conveyors, and the existing economy reserve, rejected ore/Core-ring/belt
severing/no-exit sites, and left seeded hijack routes and Sentinel danger
unchanged. Navigation treated the first friendly Barrier on a Gunner ray as
the line-of-sight stop.

## Scope

Temporary production files were `bots/candidate/main.py`,
`bots/candidate/bot/defender.py`, and `bots/candidate/bot/navigation.py`.
Focused additions were in `tests/test_candidate_nearest_defense.py`. The
immutable comparator was
`bots/versions/v0043_liquidity-backed-dynamic-floor_20260819-0415_eeafad8f`.
No baseline/archive, package, upload, activation, or live-state write was
allowed.

## Validation

- Initial focused coverage: **30/30**; compileall passed; `make smoke` was
  **4/4**; `make static` retained the inherited 15 obsolete imports and two
  navigation fast-path assertions. Logs are under
  `reports/iter-v256-gunner-ray-shield/`.
- Initial 15-map screen (seed 172): **9-6** candidate-A, all deliveries,
  **96,940 vs 82,650 Ti**, zero TLE/suspicious rows, max p99/peak
  **1,305/5,309 us**. Raw report:
  `reports/local-20260819T062009Z`; parsed metrics:
  `reports/local-20260819T062009Z/analysis.json`.
- Independent side-swapped 30-game screen (seed 173): **12-18**, one
  candidate no-delivery row, **89,420 vs 93,580 Ti**, zero TLE/suspicious,
  max p99/peak **1,399/5,131 us**. This failed the paired edge.
- Bounded repair required the immediate next route tile to be in the danger
  set. Focused coverage remained **30/30**, compileall passed, static kept the
  inherited failures, and smoke was **4/4**. The repair screen was
  **17-13**, all deliveries, **120,840 vs 109,970 Ti**, zero TLE/suspicious,
  max p99/peak **1,532/2,855 us**, but collapsed protected maps
  Archipelago, Auroraveil, Drakkarfjord, and Yulerune to **0-2** each. Raw
  report: `reports/local-20260819T062730Z`; parsed metrics:
  `reports/local-20260819T062730Z/analysis.json`.

## Decision and rollback

Reject v256. The aggregate repair edge did not satisfy the protected-map
criterion, and the initial screen reversed on the independent rotation. The
temporary source and tests were removed; candidate source is recursively
byte-identical to immutable v0043 at
`reports/iter-v256-gunner-ray-shield/rollback-source.diff`. Rollback focused
coverage was **26/26**, compileall passed, and rollback smoke was **4/4**.
No 60-game release gate, package, remote test, upload, activation, promotion,
or live-state transition occurred.

## Remaining risk

The SmartFridge replay still demonstrates a route stopping behind a hostile
Gunner, but a generic Barrier shield is not robust across map geometry. Do not
reopen it or the broad infiltrator family without a map-local causal replay
that identifies a legal shield site and a conversion edge.
