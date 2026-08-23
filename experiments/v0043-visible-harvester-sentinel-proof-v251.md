# v251 — visible-Harvester proof for first Sentinel — rejected

## Objective and scope

Direct v106 losses reached the opposing half with two-to-four friendly
Harvesters but no forward Sentinels on four long maps, while the cramped win
placed three early. The candidate therefore tested a narrow first-Sentinel
transition: when `SLOT_HARVESTER_COUNT` was still zero, a fixed attacker could
use a visible friendly Harvester as proof only with directly confirmed enemy
Core intel and enough dynamic-price reserve for one Harvester plus two
Conveyors after the Sentinel. Later Sentinel pools, routes, raids, hijacks,
and all defense remained unchanged.

Allowed production/test files were `bots/candidate/bot/attacker.py` and
`tests/test_candidate_nearest_defense.py`; bookkeeping was limited to this
record, plan/update/state metadata, and reports. No baseline/archive or live
operation changed.

## Validation

- Focused tests: **29/29**; candidate/baseline compileall passed.
- `make static`: inherited exit 2 only (15 obsolete deleted-module imports and
  two navigation fast-path assertions); no v251-specific static failure.
- `make smoke`: **4/4** command-clean at
  `reports/local-20260819T044906Z`.
- Seed-172 all-map screen: **8-7** candidate-A, all 15 deliveries, zero
  TLE/suspicious rows, **58,520 vs 55,330 Ti**; raw
  `reports/local-20260819T044934Z`, parsed
  `reports/iter-v251-visible-harvester-sentinel/screen-replay-analysis.json`.
- Independent seed-173 screen: **7-8** candidate-A, one comparator
  no-delivery row, zero TLE/suspicious rows, **66,630 vs 81,120 Ti**; raw
  `reports/local-20260819T045143Z`, parsed
  `reports/iter-v251-visible-harvester-sentinel/screen173-replay-analysis.json`.

## Decision and rollback

Reject v251: the first screen's small win edge reversed on the independent
screen and collection regressed materially. No bounded repair had a fresh
causal signal distinct from the tested gate, so no release/60-game gate was
justified. Temporary source/test edits were removed; recursive candidate
parity with immutable v0043 is zero. Rollback focused coverage was **26/26**,
compileall passed, and rollback smoke was **4/4** at
`reports/local-20260819T045508Z`. No package, upload, activation, promotion,
or live transition occurred.

## Next direction

The live failure is still an offense-timing problem rather than evidence for
the closed infiltrator family. A subsequent hypothesis may test a guarded
mirrored-Core first-Sentinel fallback with the same visible-economy and
liquidity proof, but it must be a new iteration and must not reopen broad
hijack, body-block, or route-detour behavior.
