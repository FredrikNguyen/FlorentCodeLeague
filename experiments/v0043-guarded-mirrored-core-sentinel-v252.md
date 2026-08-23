# v252 — guarded mirrored-Core first Sentinel — rejected after one repair

## Objective and scope

The first attributable v106 series showed long-map attackers reaching the
opposing half with Harvesters but no Sentinels, while the cramped win used an
early shell. v252 tested one new transition: before direct enemy-Core intel, a
fixed attacker could plant one first Sentinel at the rotationally mirrored
Core estimate only when it was in Sentinel range, could see a friendly
Harvester, and dynamic prices left a Harvester plus two Conveyors after the
Sentinel. The Store-based later pool, direct-intel path, routes, raids,
hijacks, and defense were unchanged.

Allowed production/test files were `bots/candidate/bot/attacker.py` and
`tests/test_candidate_nearest_defense.py`; no baseline/archive or platform
operation was permitted.

## Validation

- Initial focused coverage: **30/30**; compileall passed; static retained the
  inherited 15 obsolete deleted-module imports and two navigation fast-path
  assertions; smoke was **4/4** at `reports/local-20260819T045933Z`.
- Seed-172 screen: **10-5** candidate-A, no delivery failures, zero
  TLE/suspicious rows, **65,380 vs 56,410 Ti**, and 54 vs 34 Sentinels. Raw
  `reports/local-20260819T045955Z`; parsed
  `reports/iter-v252-mirrored-sentinel-screen-replay-analysis.json`.
- Independent seed-173 screen: **4-11** candidate-A, no delivery failures,
  zero TLE/suspicious rows, **53,900 vs 66,980 Ti**, and 43 vs 53 Sentinels.
  Raw `reports/local-20260819T050143Z`; parsed
  `reports/iter-v252-mirrored-sentinel-screen173-replay-analysis.json`.
- One bounded repair required **two** visible Harvesters instead of one. It
  passed focused **30/30**, compileall, static with the same inherited
  failures, and smoke **4/4** at `reports/local-20260819T050412Z`, but the
  seed-172 screen fell to **6-9**, **62,300 vs 72,990 Ti**, with one
  no-delivery row. Raw `reports/local-20260819T050439Z`; parsed
  `reports/iter-v252-mirrored-sentinel-repair-screen-replay-analysis.json`.

## Decision and rollback

Reject v252 after the independent screen and one permitted repair. The
mirrored guess added early turret spend without a repeatable pressure edge;
the repair also delayed delivery on Drakkarfjord. Temporary source/tests and
the screen config were removed. Candidate parity with immutable v0043 is zero;
rollback focused coverage was **26/26**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260819T050708Z`. No release gate, package,
upload, activation, promotion, or live transition occurred.

## Follow-up

Do not widen guessed-Core Sentinel or the closed infiltrator/hijack family
again without new causal live evidence. The baseline remains v0043 and active
platform v106 with v101 rollback preserved.
