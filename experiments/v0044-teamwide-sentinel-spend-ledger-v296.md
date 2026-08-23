# v296 teamwide Sentinel spend ledger

Date: 2026-08-19

## Hypothesis

The fresh v107 replay showed repeated forward-Sentinel replacement churn: on
Auroraveil the candidate placed 12 Sentinels, ended with one Harvester, and
collected 5,120 Ti while the opponent placed five Sentinels, kept nine
Harvesters, and collected 14,430 Ti.  A teamwide lifetime budget, carried in
unused high bits of the existing delayed `SLOT_SENTINEL_COUNT`, could stop
replacement churn without changing Sentinel geometry, route policy, or combat
priorities.

## Scope

Temporary production edits were limited to `bots/candidate/bot/constants.py`,
`bots/candidate/bot/core_role.py`, and `bots/candidate/bot/attacker.py`.
Focused coverage was limited to `tests/test_candidate_nearest_defense.py`.
The low nibble retained the legacy live Sentinel count; a high-nibble lifetime
counter imposed caps of three before five completed routes and eight after.
Core ammo gating read only the live count.

## Validation

- Focused tests: 33/33 pass; compileall passed; smoke 4/4 command-clean at
  `reports/local-20260819T181456Z`; `make static` retained inherited exit 2.
- First rotated 15-map screen: 8-7 candidate-A, 80,440/69,080 Ti, 15/15
  first deliveries for both sides, zero TLE/suspicious rows; analysis at
  `reports/iter-v296-sentinel-ledger/replay-analysis.json`.
- Independent 15-map screen: 10-5 candidate-A, 76,630/66,300 Ti, 15/15 vs
  14/15 first deliveries, zero TLE/suspicious rows; analysis at
  `reports/iter-v296-sentinel-ledger/independent-analysis.json`.
- Release gate: 60/60 command-clean at `reports/local-20260819T182124Z`;
  candidate-A won 31-29, collected 258,830/272,900 Ti, delivered first on
  60/60 vs 59/60, with zero TLE/suspicious rows and max p99 1,494 us.
  Nordkap was 0-4 and Icefloe/Drakkarfjord were each 1-3.

## Decision

Reject v296.  The quick screens were not repeatable at the release gate, the
candidate lost aggregate collection, and Nordkap had a protected-map collapse.
No repair, promotion, package, upload, activation, or live-state transition
was warranted.

All temporary production and test edits were removed.  Rollback focused tests
passed 26/26, compileall passed, rollback smoke was 4/4 command-clean at
`reports/local-20260819T182838Z`, static retained its inherited exit 2, and
recursive production-source parity with immutable v0044 is zero diff at
`reports/iter-v296-sentinel-ledger/parity-after-revert.diff`.  v105 remains
the operational rollback target; live v107 was untouched.

## Reports

- `reports/iter-v296-sentinel-ledger/focused.log`
- `reports/iter-v296-sentinel-ledger/compileall.log`
- `reports/iter-v296-sentinel-ledger/static.log`
- `reports/iter-v296-sentinel-ledger/smoke.log`
- `reports/iter-v296-sentinel-ledger/replay-analysis.json`
- `reports/iter-v296-sentinel-ledger/independent-analysis.json`
- `reports/iter-v296-sentinel-ledger/eval-local.log`
- `reports/iter-v296-sentinel-ledger/eval-local-analysis.json`
- `reports/iter-v296-sentinel-ledger/rollback-focused.log`
- `reports/iter-v296-sentinel-ledger/rollback-compileall.log`
- `reports/iter-v296-sentinel-ledger/rollback-static.log`
- `reports/iter-v296-sentinel-ledger/rollback-smoke.log`
- `reports/iter-v296-sentinel-ledger/parity-after-revert.diff`
