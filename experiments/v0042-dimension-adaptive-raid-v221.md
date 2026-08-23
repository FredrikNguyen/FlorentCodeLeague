# v221 dimension-adaptive raid lease — rejected

## Objective and scope

Keep the existing loaded-logistics raid on compact boards, where a lateral
target can be converted into pressure quickly, but preserve the economy and
advance path on boards whose geometry makes the same detour expensive. The
temporary source scope was `bots/candidate/bot/dynamic.py` plus one focused
test module and checkpoint metadata. No fixed-attacker, Store, cost, unit-cap,
map-name, package, upload, or live-state change was allowed.

## Validation

The seven new dimension/priority/legality tests passed, the root focused
subset passed **44/44**, candidate compileall passed, and smoke was **4/4**
command-clean. `make static` retained the inherited exit-2 profile (15
obsolete deleted-module imports and two navigation fast-path assertions), with
no v221-specific failure.

The rotated 15-map screen (seed 187) was command- and delivery-clean at
**8-7**, with zero TLE/suspicious/no-delivery rows, collection **77,110 vs
77,400 Ti**, mean first delivery **27.33 vs 21.67**, and max p99/peak
**1,436/2,729 us**. The release gate therefore ran.

The 60-game endpoint-seed/both-side gate was command-clean with zero TLE or
suspicious output but scored only **27-33 (45.0%)** candidate-side. Collection
was **283,140 vs 290,860 Ti** (the candidate averaged **4,719 vs 4,848 Ti per
replay**), had
**3 vs 1** no-delivery rows, and max p99/peak **1,503/5,395 us**. Nordkap
collapsed to **0-4**; Drumlin and Frostgate were **1-3**. The complete replay
analysis is in `reports/iter-v221-dimension-adaptive-raid/release-replay-analysis.json`.

## Decision and rollback

Reject v221. The compact-board exception did not recover the long-board
weakness or improve the aggregate against immutable v0042. The exact pre-v221
`dynamic.py` SHA-256 was restored to
`bcaa62c16403024e37a2149659160d04c01ec287d80679394d7bc8d7980651fd`; the
temporary test and screen config were removed. Rollback focused coverage was
**37/37**, compileall passed, and rollback smoke was **4/4** at
`reports/local-20260818T190732Z`. v0042 remains the immutable baseline; no
promotion, package, upload, activation, or live transition occurred.

Evidence: `reports/local-20260818T185509Z`,
`reports/local-20260818T185744Z`, and
`reports/iter-v221-dimension-adaptive-raid/`.
