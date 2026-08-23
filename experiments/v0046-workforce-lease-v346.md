# v346 map-aware workforce lease — rejected, v0046 retained

Date: 2026-08-20

## Objective and scope

Build on immutable local baseline
`bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`
with a genuinely map-aware workforce contract.  The nearest one/two dynamic
Builders on extended boards would remain route owners until a map-scaled route
target was reached; surplus Builders could still hijack visible enemy
Harvesters, repair belts, raid logistics, or answer home threats.  The lease
was enforced both by dynamic task selection and by the Defender SCOUT FSM.

Allowed production files were `bots/candidate/bot/defender.py`,
`bots/candidate/bot/dynamic.py`, and the temporary focused
`tests/test_candidate_workforce_lease.py`.  Store schema, Core spawn policy,
fixed identities, route geometry, immutable snapshots, package, platform, and
live state were non-goals.

## Replay basis and implementation

The v345 seed-179 losses showed fewer early Harvesters/conveyors and lower
delivery despite command-clean execution.  Top-team samples kept a small
economy shell productive while using surplus control/pressure.  v346 therefore
ranked locally visible non-fixed Builders by distance to the verified Core,
kept one additional owner on 18–24-span boards until six completed routes and
two owners on larger boards until seven, and released the owner when the route
target was reached.  Home threats and belt gaps still preempted the lease.

Repair 1 made the lease authoritative inside the Defender FSM: lease owners
could not silently switch to enemy-harvester hijack or optional ore-turret
spend before own-route conversion.  Repair 2 changed the lease from a late
`PRESSURE` toggle to an all-phase route-owner lifecycle and gave an active
owner first attempt at a local Harvester before optional Core-ring upkeep.
The stale-Core case was explicitly released and covered.

## Validation

- Initial focused coverage was **36/36**; repair 1 **37/37**; repair 2
  **39/39**.  Rollback focused coverage was **31/31**.
- Compileall passed for the initial candidate, both repairs, and rollback.
  `make static` retained the inherited repository profile (obsolete candidate
  module imports plus two navigation fast-path assertions); no new production
  budget failure appeared.  Smoke was **4/4 command-clean** for each repair
  (`reports/local-20260820T100449Z` and `reports/local-20260820T101317Z`) and
  rollback (`reports/local-20260820T101819Z`).
- Initial seed-173 screen was **6-9 candidate-A**, **55,110 vs 70,090 Ti**,
  delivery-clean.  Repair 1 remained **6-9**, **69,910 vs 72,320 Ti** on
  seed-173 and reached **7-8**, **91,640 vs 102,710 Ti** on seed-179; combined
  repair-1 result was **13-17**, **161,550 vs 175,030 Ti**.  Reports:
  `reports/iter-workforce-lease-v346-screen-seed173-analysis.json`,
  `reports/iter-workforce-lease-v346-repair1-screen-seed173-analysis.json`,
  and `reports/iter-workforce-lease-v346-repair1-screen-seed179-analysis.json`.
- Repair 2 was **6-9**, **74,990 vs 90,940 Ti** on seed-173 and **6-9**,
  **79,620 vs 70,550 Ti** on seed-179.  Both rotations were delivery-clean
  with zero candidate TLE/suspicious rows, but the combined result was
  **12-18**, **154,610 vs 161,490 Ti**.  Reports:
  `reports/iter-workforce-lease-v346-repair2-screen-seed173-analysis.json`
  and `reports/iter-workforce-lease-v346-repair2-screen-seed179-analysis.json`.

## Decision and rollback

Reject v346 after the two permitted repairs.  The lease improved some
resource-conversion rows but did not improve paired win rate and produced a
large seed-173 conversion regression after the all-phase rewrite.  Restore
`bots/candidate/bot/dynamic.py` and `bots/candidate/bot/defender.py`
byte-for-byte to immutable v0046 and delete the temporary focused test;
`reports/iter-workforce-lease-v346-rollback-source-parity.diff` is empty when
generated caches are excluded.  No release gate, promotion, package, upload,
activation, or live transition occurred.  Live v108 remains
`active_observing`; immutable v0046 remains the local baseline.

## Remaining risk and next direction

The failure is architectural: a global map-sized route lease, even when made
local and FSM-authoritative, still confuses route ownership with useful
resource conversion and does not explain the Royale/Auroraveil/Fjordgate
opening deficits.  The next experiment should be a different mechanism: a
verified route-commit state machine that assigns a concrete visible ore/path
mission, abandons it on stale sighting or no progress, and lets the same unit
alternate between route construction and a reachable sabotage/defense target.
Do not retry this lease or another phase-only threshold unchanged.
