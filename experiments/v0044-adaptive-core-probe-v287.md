# v287 adaptive alternate-Core probe — rejected

Date: 2026-08-19

## Hypothesis and scope

Fresh v107 losses included four-to-eight Harvesters but zero or one forward
Sentinel.  The primary attacker used only the rotational 180-degree Core prior
until direct sighting, so a wrong or blocked prior could consume a short game
without confirmed intel.  v287 kept that prior first, then tested at most two
aspect-ordered horizontal/vertical counterparts after the attacker arrived at
the current probe and waited through a bounded 12-round sensing epoch.
Confirmed intel stopped the search immediately; Sentinel placement remained
confirmed-only except for the existing compact-map rule.  Economy, routes,
roles, reserves, tasks, barriers, sabotage, and platform state were unchanged.

Temporary files were `bots/candidate/bot/attacker.py`,
`bots/candidate/bot/constants.py`, and
`tests/test_candidate_nearest_defense.py`.

## Validation

- Initial focused tests: **36/36**;
- candidate compileall: pass;
- `make static`: inherited **exit 2** (15 obsolete imports and two navigation
  assertions);
- initial `make smoke`: **4/4**, report `reports/local-20260819T152954Z`;
- seed-172 screen: **5-10** candidate-A, command-clean;
- screen collection: **71,010/85,180 Ti** candidate/comparator;
- screen placed Sentinels: **70/76** candidate/comparator;
- screen first-delivery mean: **31.8/69.3** turns candidate/comparator, with a
  144-turn candidate delivery row;
- screen reliability: zero command failures, TLEs, suspicious rows, and
  delivery failures;
- rollback focused tests: **34/34**;
- rollback compileall: pass;
- rollback `make static`: inherited **exit 2**;
- rollback `make smoke`: **4/4**, report `reports/local-20260819T153352Z`;
- rollback source parity: zero diff under recursive source comparison,
  excluding `__pycache__` and `*.pyc`, versus immutable v0044.

## Decision

Rejected at the first screen.  The alternate search caused a clear 5-10
win-rate and collection regression without increasing Sentinel pressure.  Its
first-delivery mean and one extreme late-delivery row are not a useful trade
for the hypothesized Core-intel gain.  No repair, second screen, long gate,
promotion, package, upload, activation, or live-state transition was
justified.

## Evidence

- `reports/iter-v287-adaptive-core-probe/focused.log`
- `reports/iter-v287-adaptive-core-probe/compileall.log`
- `reports/iter-v287-adaptive-core-probe/static.log`
- `reports/iter-v287-adaptive-core-probe/smoke.log`
- `reports/iter-v287-adaptive-core-probe/screen172.log`
- `reports/iter-v287-adaptive-core-probe/screen172-analysis.json`
- `reports/iter-v287-adaptive-core-probe/rollback-focused.log`
- `reports/iter-v287-adaptive-core-probe/rollback-compileall.log`
- `reports/iter-v287-adaptive-core-probe/rollback-static.log`
- `reports/iter-v287-adaptive-core-probe/rollback-smoke.log`
- `reports/iter-v287-adaptive-core-probe/rollback-source-parity.diff`

The live rollback remains v105; v107 remains active-observing.
