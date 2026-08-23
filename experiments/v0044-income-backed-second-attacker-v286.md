# v286 income-backed second-attacker release — rejected

Date: 2026-08-19

## Hypothesis and scope

The fresh v107 loss audit showed short Midgard/Yulerune/Frostgate games where
the candidate had a productive first route but too little forward pressure.
The stage-two workforce already unlocks after one route, but its first Builder
remains dynamic until the three-route offense gate.  v286 temporarily
designated that first stage-two Builder as the second fixed attacker after a
positive Core income heartbeat, only when the dynamic bank could still fund a
replacement Builder route, two Conveyors, and the existing fixed-offense
reserve.  Permanent attacker/defender roles, route FSM, Sentinel gates,
dynamic tasks, workforce target, and all platform state were unchanged.

Temporary files were `bots/candidate/bot/core_role.py` and
`tests/test_candidate_nearest_defense.py`.

## Validation

- Initial focused tests: **35/35**;
- candidate compileall: pass;
- `make static`: inherited **exit 2** (15 obsolete imports and two navigation
  assertions);
- initial `make smoke`: **4/4**, report `reports/local-20260819T151635Z`;
- seed-172 screen: **8-7** candidate-A, command/delivery-clean;
- screen collection: **94,930/92,240 Ti** candidate/comparator;
- screen first-delivery mean: **41.4/22.6** turns candidate/comparator;
- screen placed Sentinels: **46/64** candidate/comparator;
- screen reliability: zero command failures, TLEs, suspicious rows, and
  delivery failures;
- rollback focused tests: **34/34**;
- rollback compileall: pass;
- rollback `make static`: inherited **exit 2**;
- rollback `make smoke`: **4/4**, report `reports/local-20260819T152001Z`;
- rollback source parity: zero diff under recursive source comparison,
  excluding `__pycache__` and `*.pyc`, versus immutable v0044.

## Decision

Rejected at the first screen.  The 8-7 result and small collection edge were
not repeatable evidence, while first delivery was substantially slower and
Sentinel pressure was lower.  The first-screen criterion therefore failed;
no second screen, bounded repair, 60-game gate, promotion, package, upload,
activation, or live-state transition was justified.

## Evidence

- `reports/iter-v286-income-second-attacker/focused.log`
- `reports/iter-v286-income-second-attacker/compileall.log`
- `reports/iter-v286-income-second-attacker/static.log`
- `reports/iter-v286-income-second-attacker/smoke.log`
- `reports/iter-v286-income-second-attacker/screen172.log`
- `reports/iter-v286-income-second-attacker/screen172-analysis.json`
- `reports/iter-v286-income-second-attacker/rollback-focused.log`
- `reports/iter-v286-income-second-attacker/rollback-compileall.log`
- `reports/iter-v286-income-second-attacker/rollback-static.log`
- `reports/iter-v286-income-second-attacker/rollback-smoke.log`
- `reports/iter-v286-income-second-attacker/source-parity.diff`

The live rollback remains v105; v107 remains active-observing.
