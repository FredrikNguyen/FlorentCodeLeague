# v281 compact-map visible-income first Sentinel — rejected

Date: 2026-08-19

## Objective and scope

Fresh v107 live losses included compact Antler with no forward Sentinel even
though the first Harvester was placed on turn 8, and Drumlin with four placed
Sentinels that all died.  v281 tested one narrow timing handoff: on a cramped,
rotationally symmetric board only, a fixed attacker could use a directly
visible friendly Harvester as proof for exactly one early Sentinel while the
Core's historical route counter was still zero.  The bank also had to cover a
Sentinel, one replacement Harvester, two short Conveyor links, and the fixed
offense reserve.  Later Sentinel gates, route policy, roles, and all non-cramped
maps were unchanged.

Allowed implementation files were `bots/candidate/bot/attacker.py` and
`tests/test_candidate_nearest_defense.py`; bookkeeping was limited to this
record, the current plan, `UPDATES.md`, durable state, and reports.  No
baseline/archive or platform state was changed.

## Validation

- Focused nearest-defense/economy-phase/seeded-route coverage: **37/37**;
  candidate compileall passed.  `make smoke` was **4/4** command-clean at
  `reports/local-20260819T142205Z`.
- `make static` retained the inherited exit **2**: 15 obsolete deleted-module
  imports and two navigation fast-path assertions; no v281-specific failure.
  Full output is `reports/iter-v281-compact-sentinel/static.log`.
- Seed-172 15-map screen: candidate-A **8-7**, collection
  **77,280/66,570 Ti**, Harvesters **103/141**, Sentinels **38/52**, and first
  delivery **15/15 vs 15/15**.  Reliability was clean; max p99/peak was
  **1,470/5,937 us**.  Raw report `reports/local-20260819T142320Z` and parsed
  diagnostics `reports/iter-v281-compact-sentinel/screen-172-analysis.json`.
- Independent seed-175 screen: candidate-A **5-10**, collection
  **39,090/55,300 Ti**, Harvesters **95/129**, Sentinels **37/46**, and first
  delivery **14/15 vs 15/15**.  Reliability was clean; max p99/peak was
  **1,422/3,374 us**.  Raw report `reports/local-20260819T142536Z` and parsed
  diagnostics `reports/iter-v281-compact-sentinel/screen-175-analysis.json`.

## Decision and rollback

Reject v281: the paired screens were **13-17**, collection
**116,370/121,870 Ti**, Harvesters **198/270**, Sentinels **75/98**, and
delivery **29/30 vs 30/30**.  The first-screen edge reversed and the local
economy/pressure footprint regressed, so no repair or 60-game gate was
justified.  The candidate attacker source now compares byte-for-byte with
immutable v0044 (`rollback-source.diff` is zero lines); rollback focused
coverage was **34/34**, compileall passed, and rollback smoke was **4/4** at
`reports/local-20260819T142805Z`.  No promotion, package, upload, activation,
or live transition occurred.

## Next direction

Do not re-add an early visible-Harvester Sentinel proof without new event-level
evidence.  Revisit the Antler/Drumlin route-conversion and Sentinel-survival
causes with a structurally different hypothesis; v105 remains the requested
operational rollback target and v0044 remains the immutable local comparator.
