# v285 positive-income first Sentinel transition — rejected

Date: 2026-08-19

## Hypothesis and scope

The fresh v107 loss audit showed short Midgard/Yulerune/Frostgate games where
the candidate had four-to-six Harvesters but zero or one Sentinel.  The
historical `SLOT_HARVESTER_COUNT` write can lag a real Core income observation,
so v285 changed the existing economy phase to publish `CONVERTING` after a
positive net-income heartbeat even when that counter was zero.  The existing
first-Sentinel path then accepted that phase only with dynamic reserve for one
Harvester and two Conveyors.  Confirmed-Core/cramped geometry, pool limits,
placement, later Sentinels, routes, and all other roles were unchanged.

Temporary production files were `bots/candidate/bot/core_role.py` and
`bots/candidate/bot/attacker.py`; focused coverage was updated in
`tests/test_candidate_economy_phase.py` and
`tests/test_candidate_nearest_defense.py`.

## Validation

- Initial focused tests: **35/35**;
- candidate compileall: pass;
- `make static`: inherited **exit 2** (15 obsolete imports and two navigation
  assertions);
- initial `make smoke`: **4/4**, report `reports/local-20260819T150700Z`;
- seed 172 screen: **8-7**, command/delivery-clean, collection
  **81,400/71,380 Ti**, Harvesters **117/120**, Sentinels **48/56**, and first
  delivery means **24.60/21.00** turns;
- seed 172 reliability: zero TLE/suspicious rows, max p99/peak
  **1,459/4,660 us**;
- first candidate Sentinel placements were late or absent on several losses
  (turns **84, 158, 242, 248, 319**, or no placement);
- rollback focused tests: **34/34**;
- rollback compileall: pass;
- rollback `make smoke`: **4/4**, report `reports/local-20260819T151006Z`;
- rollback source parity: zero diff under recursive source comparison
  excluding `__pycache__` and `*.pyc` versus immutable v0044.

## Decision

Rejected at the first screen.  The phase signal did not improve first
delivery or Sentinel placement and did not meet the required opening-shell
edge, so no second screen, repair, 60-game gate, promotion, package, upload,
activation, or live-state transition was justified.

## Evidence

- `reports/iter-v285-positive-income-sentinel-focused.log`
- `reports/iter-v285-positive-income-sentinel-compileall.log`
- `reports/iter-v285-positive-income-sentinel-static.log`
- `reports/iter-v285-positive-income-sentinel-smoke.log`
- `reports/iter-v285-positive-income-sentinel-screen172.log`
- `reports/iter-v285-positive-income-sentinel-screen172-analysis.json`
- `reports/iter-v285-positive-income-sentinel-rollback-focused.log`
- `reports/iter-v285-positive-income-sentinel-rollback-compileall.log`
- `reports/iter-v285-positive-income-sentinel-rollback-static.log`
- `reports/iter-v285-positive-income-sentinel-rollback-smoke.log`

The live rollback remains v105; v107 remains active-observing.
