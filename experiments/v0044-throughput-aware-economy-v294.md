# v294 throughput-aware economy handoff — rejected

Date: 2026-08-19

## Hypothesis and scope

The v107 Auroraveil loss had positive lifetime income but ended with one own
Harvester and 5,120 Ti versus nine Harvesters and 14,430 Ti for the opponent.
The existing v271 phase signal reset on any positive net-resource delta, so
passive income or one surviving route could keep the dynamic workforce in
PRESSURE after the historical route milestone.  v294 added an eight-round
rolling sum of positive net income and published CONVERTING when that full
window was below 50 Ti (passive income plus roughly three effective
Harvesters).  It changed only `main.py`, `constants.py`, `core_role.py`, and
the economy-phase tests; route, workforce, task, combat, Store, baseline, and
platform policy were unchanged.

## Validation

- Initial focused economy/nearest-defense tests: **32/32**;
  `reports/iter-v294-throughput-handoff/focused.log`.
- Initial candidate compileall: pass;
  `reports/iter-v294-throughput-handoff/compileall.log`.
- Initial `make static`: inherited exit **2** (15 obsolete deleted-module
  imports and two navigation fast-path assertions);
  `reports/iter-v294-throughput-handoff/static.log`.
- Initial `make smoke`: **4/4 command-clean**, report
  `reports/local-20260819T175026Z`.
- First 15-map screen: **9–6**, collection **60,380/57,560 Ti**, first
  delivery **14/15 vs 15/15**, zero command failures/TLEs/suspicious rows;
  report `reports/local-20260819T175100Z`, analysis
  `reports/iter-v294-throughput-handoff/replay-analysis.json`.
- Independent all-map screen: **6–9**, collection **56,060/82,440 Ti**, first
  delivery **15/15 vs 15/15**, zero command failures;
  report `reports/local-20260819T175256Z`, analysis
  `reports/iter-v294-throughput-handoff/independent-analysis.json`.
- Rollback focused coverage: **30/30**;
  `reports/iter-v294-throughput-handoff/rollback-focused.log`.
- Rollback compileall: pass; `rollback-compileall.log`.
- Rollback `make static`: inherited exit **2**; `rollback-static.log`.
- Rollback `make smoke`: **4/4 command-clean**, report
  `reports/local-20260819T175524Z` and `rollback-smoke.log`.
- Recursive candidate/source parity with immutable v0044 is zero diff;
  `reports/iter-v294-throughput-handoff/parity-after-revert.diff`.

## Decision

Reject v294.  The first screen's one-sided 9–6 edge was not repeatable; the
independent screen regressed to 6–9 and lost 26,380 Ti of aggregate collection
against v0044.  Both screens were command-clean and the second restored
delivery parity, but the throughput gate did not improve the economy.  All
temporary production and test edits were removed and exact v0044 was restored.
No repair, promotion, package, upload, activation, or live-state transition
was performed.  v105 remains the operational rollback target and v107 remains
active-observing.

## Remaining risks

- The live workforce/Harvester attrition gap remains unresolved; do not retry
  this rolling-rate threshold unchanged.
- `make static` retains the inherited obsolete imports and navigation failures.
- v105 remains the guarded rollback even though local v0044 is the comparator.
