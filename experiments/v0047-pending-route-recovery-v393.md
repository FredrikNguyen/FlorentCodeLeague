# v393 Pending-route recovery (rejected)

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward_20260821-0200_eeafad8f`,
test one bounded fix for the Glacierkeep seed-1 no-delivery replay.  The
diagnosis was that survival fleeing between a chain move and its build turn
caused `_run_chain` to discard `chain_pending`, leaving a permanent conveyor
gap.  The candidate retained the pending obligation and walked back to it,
with a bounded fallback through a stale danger set.  Repair 1 limited that
recovery to a four-tile local displacement so long detours did not consume the
workforce.  No other strategy, map policy, baseline, package, or live state
was in scope.

## Evidence

- Focused candidate coverage passed **27/27** after the initial change and
  **27/27** after the bounded-radius repair.  Rollback focused coverage was
  **32/32** (`reports/iter-v393-pending-route-recovery/rollback-focused.log`).
- Candidate compileall passed for both attempts and rollback.  `make smoke`
  was **4/4** for rollback at `reports/local-20260821T022431Z`.
- `make static` retained the repository's inherited exit-2 profile (obsolete
  module imports and two navigation fast-path assertions); no v393-specific
  static error appeared.  Logs are under
  `reports/iter-v393-pending-route-recovery/`.
- Initial rotated all-map screen (`screen_seed=887`) scored **17–13** against
  v0047, with **30/30** candidate deliveries, zero command/TLE/suspicious
  rows, and raw games at `reports/local-20260821T021600Z`.
- Repair 1 rotated all-map screen (`screen_seed=941`) also scored **17–13**,
  with **29/30** candidate deliveries (the remaining no-delivery row was
  Glacierkeep), zero command/TLE/suspicious rows, and raw games at
  `reports/local-20260821T022012Z`.

## Decision

Reject v393 after the two allowed unsuccessful repairs: neither screen met
the **19–11** promotion floor.  Restore exact recursive production parity with
v0047, preserve both screen reports and the Glacierkeep diagnosis, and do not
run a release gate, remote gate, package, upload, activation, or baseline
transition.  The next iteration should use v0047 and pursue a distinct
map-context conversion hypothesis rather than reviving this pending-return
logic unchanged.
