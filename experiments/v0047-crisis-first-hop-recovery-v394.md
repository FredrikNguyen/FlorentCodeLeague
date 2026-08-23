# v394 Crisis first-hop recovery (rejected)

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward_20260821-0200_eeafad8f`,
test a narrow map-context conversion fix for the Glacierkeep route failure.
During a late economy `CRISIS`, a visible own Harvester with an accepting
Conveyor whose first output was visibly a GAP/DEAD tile could seed one
alternate first-hop Conveyor.  Repair 1 required at least three historical
routes before spending the recovery Conveyor.  No topology walk, Store/schema,
chain FSM, spawning, combat, package, or live operation was in scope.

## Evidence

- Focused candidate coverage was **27/27** for the initial and repaired
  variants.  Rollback focused coverage was **32/32** at
  `reports/iter-v394-crisis-first-hop/rollback-focused.log`.
- Candidate and rollback compileall passed.  `make smoke` was **4/4** after
  rollback at `reports/local-20260821T024137Z`.  `make static` retained the
  inherited exit-2 profile (obsolete imports and two navigation assertions),
  with no v394-specific static error.
- Initial rotated all-map screen (`screen_seed=977`) was **14–16** against
  v0047, with **30/30** candidate deliveries, zero command/TLE/suspicious
  rows, and raw games at `reports/local-20260821T023355Z`.
- Repair 1 (`screen_seed=1031`) was **12–18**, also **30/30** delivery-clean
  and reliability-clean, with raw games at
  `reports/local-20260821T023748Z`.

## Decision

Reject v394 after the two allowed unsuccessful repairs: the crisis first-hop
spend reduced win rate and never cleared the **19–11** floor.  Remove the
temporary source/test/config changes, preserve both screens and replay
analyses, and keep exact recursive candidate parity with immutable v0047.  Do
not run a release gate, remote gate, package, upload, activation, or baseline
transition.  A future route fix needs a different causal signal; do not revive
this crisis alternate-seed rule unchanged.
