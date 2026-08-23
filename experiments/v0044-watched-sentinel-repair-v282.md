# v282 watched forward-Sentinel repair lease — rejected

Date: 2026-08-19

## Objective and scope

Fresh v107 Drumlin evidence showed four placed forward Sentinels with none
alive at the end, while the opponent retained twelve.  v282 tested one
post-placement support change: the owning attacker could heal its most recent
visible, adjacent, damaged Sentinel during the existing 20-round
`SENTINEL_MIN_LIFETIME` watch, then return to the normal core lane.  Placement,
route conversion, economy, roles, and all non-watched units were unchanged.

Allowed implementation files were `bots/candidate/bot/attacker.py` and
`tests/test_candidate_nearest_defense.py`; bookkeeping was limited to this
record, the plan/update/state metadata, and reports.  No baseline/archive or
platform state changed.

## Validation

- Focused nearest-defense/economy-phase/seeded-route coverage: **36/36**;
  candidate compileall passed. `make smoke` was **4/4** command-clean at
  `reports/local-20260819T143202Z`.
- `make static` retained the inherited exit **2** (15 obsolete deleted-module
  imports and two navigation fast-path assertions); no v282-specific failure.
  Output: `reports/iter-v282-sentinel-support-static.log`.
- Seed-172 screen: candidate-A **7-8**, collection **61,940/54,540 Ti**,
  Harvesters **113/110**, Sentinels **48/46**, and delivery **15/15 vs
  15/15**. Runtime was clean; max p99/peak **1,336/2,113 us**. Raw report
  `reports/local-20260819T143238Z`, parsed
  `reports/iter-v282-sentinel-support-screen172.json`.
- Seed-175 screen: candidate-A **6-9**, collection **47,570/63,330 Ti**,
  Harvesters **106/125**, Sentinels **34/53**, and delivery **15/15 vs
  15/15**. Runtime was clean; max p99/peak **1,325/4,649 us**. Raw report
  `reports/local-20260819T143418Z`, parsed
  `reports/iter-v282-sentinel-support-screen175.json`.

## Decision and rollback

Reject v282: paired screens were **13-17**, collection
**109,510/117,870 Ti**, Harvesters **219/235**, Sentinels **82/99**, and
delivery **30/30 vs 30/30**. The support lease did not create a repeatable
win or survival edge and the independent Sentinel/collection footprint
regressed. No repair or 60-game gate was justified.

The candidate attacker source is recursively byte-identical to immutable v0044
(`iter-v282-rollback-attacker.diff` is zero lines); rollback focused coverage
was **34/34**, compileall passed, and rollback smoke was **4/4** at
`reports/local-20260819T143624Z`. No promotion, package, upload, activation,
or live transition occurred.

## Next direction

Do not re-add an attacker-held Sentinel repair lease without event-level proof
that it preserves attack tempo. Revisit the direct route-conversion/attrition
cause with a distinct map-context or economy-to-pressure hypothesis; v105
remains the requested operational rollback target and v0044 the local
comparator.
