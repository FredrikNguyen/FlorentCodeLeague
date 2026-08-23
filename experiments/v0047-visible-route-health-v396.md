# v396 Visible route-health orphan repair (rejected)

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward_20260821-0200_eeafad8f`,
test one bounded route-conversion hypothesis from the Glacierkeep release
replay: an immediately accepting Conveyor is not sufficient when its fully
visible directed suffix is a dead end or cycle.  The candidate temporarily
classified visible suffixes during the published economy phases and allowed
the existing local orphan-seed repair to choose one alternate first hop.
Splitter and unseen suffixes remained conservative, and no Store schema,
spawning, combat, prices, map-name branch, baseline, package, or live state
was in scope.  Repair 1 extended the same check through `PRESSURE` after the
first screen showed the remaining Glacierkeep loss had already reached that
phase.

## Evidence

- Focused coverage was **39/39** for the initial candidate and Repair 1;
  rollback coverage was **36/36** at
  `reports/iter-v396-route-health/rollback-focused.log`.
- Compileall passed for both candidate attempts and rollback.  `make smoke`
  was **4/4** after rollback at raw report
  `reports/local-20260821T033007Z`.  `make static` retained the inherited
  exit-2 profile (obsolete imports and two navigation assertions), with no
  v396-specific failure.
- Initial rotated all-map 30-game screen (`screen_seed=1163`) was **15–15**;
  the one prevented no-delivery row did not produce a win-rate edge.  Raw
  report and replay evidence are under
  `reports/local-20260821T031836Z` and
  `reports/iter-v396-route-health/replay-analysis.json`.
- Repair 1 rotated all-map 30-game screen (`screen_seed=1171`) was **17–13**,
  with zero command failures, TLEs, or suspicious output.  Per-map losses
  remained concentrated on Drumlin and Drakkarfjord; candidate delivery and
  collection were not a reliable improvement.  Raw report and bounded replay
  analysis are `reports/local-20260821T032512Z` and
  `reports/iter-v396-route-health/repair1-replay-analysis.json`.

## Decision

Reject v396 after the initial screen and one bounded repair: neither result
met the **19–11** promotion floor, so no release/long gate, remote gate,
package, upload, activation, or baseline transition was justified.  Remove
the temporary source/test/config changes and retain exact recursive production
parity with immutable v0047.  The route-health diagnosis remains a follow-up
risk, but this local suffix classifier is not promoted unchanged.
