# v411 Route-conversion priority — rejected

Date: 2026-08-21

## Objective and scope

Starting from immutable
`v0047_pressure-economy-steward_20260821-0200_eeafad8f`, v411 tested whether
dynamic Builders should choose a funded Harvester opportunity before a visible
non-Core-ring belt repair during OPENING/CONVERTING.  Core-ring repairs,
CRISIS repairs, PRESSURE behavior, fixed attackers, the route FSM, prices,
Store schema, spawning, and live state were non-goals.

The rule was deliberately narrow: it applied only after three completed
routes, only with a currently affordable Harvester and a visible/advertised
route opportunity, and never for Core-ring or crisis repairs.

## Validation

- Candidate focused coverage passed **34/34** before the repair; compileall
  passed and the 4-game smoke was command-clean at
  `reports/local-20260821T085426Z`.
- The first 15-map screen (`screen_seed=2411`) was **5-10** for the candidate,
  with a candidate no-delivery Royale row.  Raw games are in
  `reports/local-20260821T085543Z`; the partial interrupted run at
  `reports/local-20260821T085453Z` was discarded because its manifest was
  never written.
- A bounded repair kept all non-ring repairs ahead of route conversion until
  the three-route floor, then required an actual route opportunity.  Focused
  coverage passed **35/35**, compileall passed, and repair smoke was **4/4**
  at `reports/local-20260821T085842Z`.
- The independent repaired 15-map screen (`screen_seed=2412`) was **6-9**;
  it still contained a candidate no-delivery Icefloe row.  Raw games are in
  `reports/local-20260821T085912Z`.
- `make static` returned the inherited exit 2 (15 obsolete removed-module
  imports plus two navigation fast-path assertions) with no v411-specific
  error.  Rollback focused coverage passed **32/32**, compileall passed,
  and baseline-parity smoke was **4/4** at
  `reports/local-20260821T090213Z`.

## Decision and rollback

Reject v411 after one bounded repair.  The candidate's occasional extra
Harvesters did not compensate for fragile delivery and the screens missed the
9-6 promotion floor.  The temporary dynamic/test/config edits were removed;
recursive production parity with immutable v0047 is exact.  No release gate,
package, remote gate, upload, activation, or baseline transition occurred.

Keep v0047 as the moving baseline.  The next experiment should target a
verified route-conversion or defensive response without changing the strict
early belt-repair contract.

Reports: `reports/iter-v411-route-conversion/` and the two complete screen
reports listed above.
