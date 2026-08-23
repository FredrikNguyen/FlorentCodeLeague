# v259 event-gated chain detour — rejected after one repair

## Objective and evidence

Fresh v106 losses showed route conversion as the dominant failure: one loss
built no Harvester, another built only two, and an enemy Builder placed
Barriers over an opening route. The direct home-infiltrator response in v258
had no local edge. v259 therefore tested route preservation instead of
chasing the Builder: if an active chain's normal navigation could not improve
because a visible enemy building or wall sealed the inward frontier, the chain
owner could take one legal cardinal detour and resume the existing Conveyor
FSM.

## Scope and non-goals

The temporary production change was limited to `bots/candidate/bot/defender.py`
and the focused additions in `tests/test_candidate_nearest_defense.py`.
There was no Store, role, workforce, hijack, sabotage, turret, Sentinel,
Launcher, map, packaging, upload, activation, or live-state change.

## Validation

- Initial focused coverage: **29/29**; compileall passed; `make smoke` **4/4**.
- `make static` retained the inherited failures only (15 obsolete deleted-
  module imports and two navigation fast-path assertions).
- Initial rotated 15-map screen against exact v0043:
  **7-8**, all 15 deliveries, zero TLE/suspicious rows, **64,130 vs 63,950
  Ti**, max p99/peak **1,292/4,974 us**. Raw report:
  `reports/local-20260819T072434Z`.
- Replay inspection found actual enemy-Barrier/conveyor frontier interactions
  on the screen, so the one permitted repair narrowed the trigger from any
  enemy building to only an enemy Barrier or wall. Repair focused coverage was
  **30/30**, compileall passed, and smoke was **4/4**.
- Repair screen: **4-11**, candidate delivery **14/15 vs 15/15**, collection
  **65,480 vs 93,640 Ti**, zero TLE/suspicious rows, max p99/peak
  **1,438/2,636 us**. Raw report: `reports/local-20260819T072856Z`.

## Decision and rollback

Reject v259. The initial candidate was effectively tied and the repair caused
a large win-rate/collection regression plus one no-delivery row. The detour
helper and its tests were removed; candidate Python is recursively byte-
identical to immutable v0043 (`reports/iter-v259-chain-detour/rollback-source.diff`).
Rollback focused coverage was **26/26**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260819T073136Z`. No release gate, promotion,
package, upload, activation, or live transition occurred.

## Follow-up

The live infiltrator signal remains useful for diagnosis, but generic
interception and route detours are not local win-rate levers. The next
hypothesis should address the opening resource-conversion gap directly, with
an event or delivery guard that does not add another route-repair loop.
