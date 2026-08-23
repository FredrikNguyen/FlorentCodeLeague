# v410 large-board dynamic route floor — rejected

Date: 2026-08-21

## Objective and scope

Starting from immutable
`v0047_pressure-economy-steward_20260821-0200_eeafad8f`, v410 tested a
map-conditioned economy gate for the optional dynamic Builder pool.  On
boards with area at least 900, dynamic raid/advance work waited for five
completed Harvester routes unless a forward Sentinel had already published a
pressure witness; fixed attackers, opening/converting/crisis routing, and
ordinary short-board behavior were unchanged.  The hypothesis targeted the
Glacierkeep/Ragnarok conversion losses in the v0047 replay audit without
removing fixed pressure.

The bounded repair left the large-board raid/advance floor in place but allowed
the first pressure Sentinel at the ordinary three-route milestone, so it could
publish the witness and release the dynamic pool.  No Store schema, route FSM,
prices, spawning, baseline snapshot, package, upload, activation, or live
state was changed.

## Validation

- Initial focused coverage was **38/38**, compileall passed, and smoke was
  **4/4** (`reports/local-20260821T081446Z`).  The scoped static run retained
  the inherited exit-2 profile: 15 removed-module imports and two navigation
  fast-path assertions, with no v410-specific failure.
- The rotated 15-game all-map screen was **8-7** for the candidate, with zero
  command failures (`reports/local-20260821T081545Z`).
- A side-balanced 30-game confirmation was **17-13**, delivery- and
  reliability-clean (`reports/local-20260821T081855Z`).  The complete
  endpoint-seed/both-side 60-game gate then tied **30-30**, with collection
  **336,640 vs 332,380 Ti**, zero command/TLE/suspicious rows, and no delivery
  command failures (`reports/local-20260821T082232Z`).
- Replay review showed the principal regression: Midgard and Ragnarok
  received fewer dynamic Sentinels while the large-board gate also delayed
  pressure construction.  The repair focused coverage was **39/39**,
  compileall passed, and smoke was **4/4** (`reports/local-20260821T083102Z`).
  Its independent 30-game screen tied **15-15**
  (`reports/local-20260821T083128Z`).

## Decision and rollback

Reject v410 and its bounded Sentinel repair: neither established a reliable
win-rate edge over v0047, and the release gate tied.  Temporary source,
focused-test, and screen-config edits were removed.  Rollback focused
coverage was **36/36**, compileall passed, rollback smoke was **4/4**, and
recursive production parity with immutable v0047 is exact.  Rollback logs are
under `reports/iter-v410-large-board-pressure-rollback-*.log`; the initial
focused/static/compile/smoke logs are under
`reports/iter-v410-large-board-pressure-*.log`.

No release package, remote gate, upload, activation, or baseline transition
occurred.  Keep v0047 as the moving baseline.  The next hypothesis should
address route conversion or pressure allocation without applying a global
large-board delay to Sentinel production.
