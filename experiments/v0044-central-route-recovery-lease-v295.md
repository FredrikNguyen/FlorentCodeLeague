# v295 central route-recovery lease — rejected

Date: 2026-08-19

## Hypothesis and scope

Fresh v107 losses still ended with one-to-four surviving Harvesters while the
opponent retained seven-to-twelve.  v295 reused the existing delayed
`SLOT_DEFENDER_ID` as a centrally selected route lease after five historical
routes when no home Gunner purchase was pending.  The nearest visible
non-fixed Builder was selected deterministically; a high-bit marker alongside
the unchanged low-bit Gunner cap distinguished the lease from turret
designation.  Only `constants.py`, `core_role.py`, `dynamic.py`, and economy
phase tests were changed temporarily.

## Validation

- Focused economy/nearest-defense coverage: **32/32**;
  `reports/iter-v295-route-lease-focused.log`.
- Candidate compileall: pass;
  `reports/iter-v295-route-lease-compileall.log`.
- `make static`: inherited exit **2** (15 obsolete deleted-module imports and
  two navigation fast-path assertions);
  `reports/iter-v295-route-lease-static.log`.
- `make smoke`: **4/4 command-clean**, report
  `reports/local-20260819T180329Z`.
- First 15-map screen: **1–14**, collection **49,010/86,520 Ti**, candidate
  delivery **14/15 vs 15/15**, with zero command failures, TLEs, or suspicious
  rows; report `reports/local-20260819T180358Z`, analysis
  `reports/iter-v295-route-lease-screen-analysis.json`.
- The candidate's Harvester counts collapsed on most maps (Auroraveil **3/7**,
  Royale **0/9**, Ragnarok **1/11**) so no independent screen or repair was
  warranted.
- Rollback focused coverage: **30/30**;
  `reports/iter-v295-route-lease-rollback-focused.log`.
- Rollback compileall: pass; `reports/iter-v295-route-lease-rollback-compileall.log`.
- Rollback `make static`: inherited exit **2**;
  `reports/iter-v295-route-lease-rollback-static.log`.
- Rollback `make smoke`: **4/4 command-clean**, report
  `reports/local-20260819T180637Z` and
  `reports/iter-v295-route-lease-rollback-smoke.log`.
- Recursive candidate/source parity with immutable v0044 is zero diff;
  `reports/iter-v295-route-lease-parity-after-revert.diff`.

## Decision

Reject v295 at the first screen.  The central lease starved the economy rather
than recovering it, likely because the delayed defender channel was not a
reliable visible workforce owner under pressure.  All temporary production and
test edits were removed and exact v0044 was restored.  No repair, promotion,
package, upload, activation, or live-state transition was performed.  v105
remains the operational rollback target and v107 remains active-observing.

## Remaining risks

- Do not retry the defender-slot lease or its high-bit marker unchanged.
- The live workforce/Harvester attrition gap remains unresolved; inspect route
  death and replacement causality before another workforce experiment.
- `make static` retains the inherited obsolete imports and navigation failures.
