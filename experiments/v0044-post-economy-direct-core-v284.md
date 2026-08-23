# v284 post-economy direct-Core sighting — rejected

Date: 2026-08-19

## Hypothesis

The v107 loss audit showed funded Dynamic Builders reaching the final advance
phase with too few forward Sentinels.  A Dynamic Builder could see the enemy
Core but never invoke the existing direct/store intel updater, leaving its
final Sentinel attempt on a stale mirrored task target.  The bounded change
called that helper only inside `_execute_advance` when no confirmed position
was already known, then preferred the confirmed position over the task target.

## Scope

Only `bots/candidate/bot/dynamic.py` and focused coverage in
`tests/test_candidate_nearest_defense.py` were temporary production/test
changes.  No startup, Defender, task-selection, Store schema, Sentinel rule,
route, fixed-attacker, baseline, package, upload, activation, or live-state
change was allowed.

## Validation

- Initial focused tests: **36/36**;
- candidate compileall: pass;
- `make static`: inherited **exit 2** (15 obsolete imports and two navigation
  assertions);
- initial `make smoke`: **4/4**, report `reports/local-20260819T145327Z`;
- seed 172 screen: **7-8**, **57,280/54,970 Ti**, **97/119 Harvesters**,
  **47/48 Sentinels**, first delivery means **29.80/22.87**;
- seed 175 screen: **8-7**, **73,770/61,250 Ti**, **113/126 Harvesters**,
  **38/54 Sentinels**, first delivery means **28.00/24.47**;
- paired screens: **15-15**, **131,050/116,220 Ti**, **210/245 Harvesters**,
  **85/102 Sentinels**, first delivery means **28.90/23.67**;
- both screens: zero command failures, TLEs, suspicious rows, and delivery
  failures; max p99 **1,363 us**, max peak **4,650 us**;
- rollback focused tests: **34/34**;
- rollback compileall: pass;
- rollback `make smoke`: **4/4**, report `reports/local-20260819T145825Z`;
- rollback source parity: zero diff under `diff -ru --exclude='__pycache__'
  --exclude='*.pyc'` against immutable v0044.

## Decision

Rejected.  The collection advantage appeared on both screens, but the pair
was only a tie and the candidate consistently trailed in Harvesters,
Sentinels, and delivery speed.  This did not meet the repeatable strategic
edge criterion, so no repair, 60-game gate, promotion, package, upload,
activation, or live-state transition was justified.

## Evidence

- `reports/iter-v284-direct-core/focused.log`
- `reports/iter-v284-direct-core/compileall.log`
- `reports/iter-v284-direct-core/static.log`
- `reports/iter-v284-direct-core/smoke.log`
- `reports/iter-v284-direct-core/screen172.log`
- `reports/iter-v284-direct-core/screen172-analysis.json`
- `reports/iter-v284-direct-core/screen175.log`
- `reports/iter-v284-direct-core/screen175-analysis.json`
- `reports/iter-v284-direct-core/rollback-focused.log`
- `reports/iter-v284-direct-core/rollback-compileall.log`
- `reports/iter-v284-direct-core/rollback-static.log`
- `reports/iter-v284-direct-core/rollback-smoke.log`
- `reports/iter-v284-direct-core/rollback-source.diff`

The live rollback remains v105; v107 remains active-observing.
