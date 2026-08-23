# v283 post-economy dynamic confirmed-Core consumption — rejected

Date: 2026-08-19

## Objective and scope

The fresh active-v107 match/loss audit (`reports/live-observe-20260819T143902Z`
and `reports/live-v107-match-6c041-loss-audit-20260819T1440Z`) showed four to
eight candidate Harvesters but zero or one Sentinel on several losses, while
the opponent had three to six.  A fixed attacker can publish confirmed enemy-
Core intel into `SLOT_ENEMY_CORE`, but a Dynamic Builder's final advance path
kept using its per-instance mirrored guess.  v283 therefore read a valid packed
Store Core position only when a Dynamic Builder was already executing its
existing final `TASK_ADVANCE`; all early Defender/Dynamic task selection and
intel publication stayed unchanged.

Allowed implementation files were `bots/candidate/bot/dynamic.py` and
`tests/test_candidate_nearest_defense.py`; bookkeeping was limited to this
record, the plan/update/state metadata, and reports.  No baseline/archive or
platform state changed.

## Validation

- Focused nearest-defense/economy-phase/seeded-route coverage: **36/36**;
  candidate compileall passed. `make smoke` was **4/4** command-clean at
  `reports/local-20260819T144305Z`.
- `make static` retained inherited exit **2** (15 obsolete deleted-module
  imports and two navigation fast-path assertions); no v283-specific failure.
  Output: `reports/iter-v283-confirmed-core-static.log`.
- Seed-172 screen: candidate-A **9-6**, collection **71,790/58,280 Ti**,
  Harvesters **109/106**, Sentinels **44/40**, delivery **15/15 vs 15/15**,
  and max p99/peak **1,381/2,718 us**.  Raw report
  `reports/local-20260819T144339Z`; parsed
  `reports/iter-v283-confirmed-core-screen172.json`.
- Seed-175 screen: candidate-A **5-10**, collection **66,040/79,550 Ti**,
  Harvesters **94/138**, Sentinels **37/46**, delivery **15/15 vs 15/15**,
  and max p99/peak **1,297/5,451 us**.  Raw report
  `reports/local-20260819T144526Z`; parsed
  `reports/iter-v283-confirmed-core-screen175.json`.

## Decision and rollback

Reject v283: the paired screens were **14-16**, aggregate collection tied at
**137,830/137,830 Ti**, but the candidate placed fewer Harvesters (**203/244**)
and Sentinels (**81/86**).  Runtime and delivery were clean, but the first
screen edge did not reproduce, so no repair or 60-game gate was justified.

The candidate dynamic source is recursively byte-identical to immutable v0044
(`iter-v283-rollback-dynamic.diff` is zero lines); rollback focused coverage
was **34/34**, compileall passed, and rollback smoke was **4/4** at
`reports/local-20260819T144736Z`.  No promotion, package, upload, activation,
or live transition occurred.

## Next direction

Do not broaden shared-Core reads or repeat the early-intel family without a
new causal signal.  Continue with a distinct direct route-conversion or
workforce/pressure hypothesis; v105 remains the requested operational rollback
target and v0044 the local comparator.
