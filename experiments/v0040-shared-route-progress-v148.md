# v0040 shared route progress — v148

Date: 2026-08-17

## Objective

Prevent the designated home defender from spending the opening economy on a
Gunner before any Harvester route has completed, while preserving normal home
defense after the first route milestone.

## Allowed scope

- `bots/candidate/bot/defender.py`
- `tests/test_candidate_nearest_defense.py`
- evaluation reports and durable experiment metadata

Non-goals were navigation, route construction, workforce spawning, Store
layout, attacker behavior, and platform operations.

## Implementation

`DefenderMixin._try_build_gunner` now returns before turret conversion when
`SLOT_HARVESTER_COUNT == 0`. The existing defender designation, distance,
resource, belt-sever, and legality gates remain unchanged. The focused suite
covers both sides of the gate: no opening Gunner and an allowed Gunner after
one completed route.

## Validation

- Focused tests: 20/20 pass (`reports/iter-v148-shared-route-progress/focused.log`).
- Compileall: pass (`reports/iter-v148-shared-route-progress/compileall.log`).
- Static: inherited repository failure, 15 obsolete-module import errors and
  2 navigation fast-path assertions (`reports/iter-v148-shared-route-progress/static.log`).
- Smoke: 4/4, zero command failures (`reports/local-20260817T182520Z`).
- 54-game checkpoint: candidate 36–18 versus v0039 (control was 30–24), zero
  command failures (`reports/local-20260817T182542Z`).
- 210-game gate: candidate 120–90 versus v0039, zero command failures,
  candidate replay audit has zero TLEs/suspicious output and max p99 1.615 ms
  (`reports/local-20260817T183119Z`,
  `reports/iter-v148-shared-route-progress/long-replay-analysis.json`).

## Review and decision

The candidate differs from v0039 only at the documented Gunner gate. No
legality or exception path was introduced. One long-gate candidate loss had no
delivery on Glacierkeep seed 149 despite four Harvesters and 125 conveyors;
that remains the next route-continuity risk. The aggregate paired win-rate
gain is substantial, so v148 is promoted as the moving local baseline.

## Platform submission

The immutable package was uploaded as platform version 104 under
`v0040-shared-route-progress-eeafad8f` (submission id
`8ebb41eb-fe2f-4402-af1a-ea4051b53b6c`). The platform reports the submission
`ready` and active; the guarded upload command itself did not request an
activation. Observation state is captured in
`reports/live-observe-20260817T185904Z`.

## Next risk

Audit the Glacierkeep no-delivery topology and test one bounded route-seal or
route-progress repair from the v148 baseline. Do not change the baseline while
that audit is pending.
