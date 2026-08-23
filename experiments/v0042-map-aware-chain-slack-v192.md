# v192 map-aware chain slack — rejected

Date: 2026-08-18

## Objective

Prevent a legitimate first Harvester route from being abandoned solely because
a wall or chokepoint detour exceeded the fixed eight-tile chain slack on a
larger board. The temporary change added a bounded map-perimeter bonus only
when a new chain was seeded; navigation, route facing, and the blocked-round
escape remained unchanged.

## Allowed files and non-goals

Allowed source was `bots/candidate/bot/constants.py` and
`bots/candidate/bot/defender.py`, with a temporary focused test module, the
rotated 15-game screen configuration, this record, reports, `UPDATES.md`,
`docs/CURRENT_PLAN.md`, and durable state. The quick screen remained one game
per configured map (15 total); the release gate remained 60 games.

Non-goals were navigation, ore ranking, workforce/roles, combat, turrets,
Launchers, barriers, Store layout, baseline/archive, package, upload,
activation, and live-state changes.

## Validation and evidence

- Focused related suites passed **41/41** for the initial and repaired
  variants; rollback focused coverage passed **38/38**. Compileall passed for
  both variants and rollback. `make static` retained the inherited exit 2
  from missing legacy modules and two navigation fast-path assertions.
- Smoke was **4/4** command-clean for the initial, repaired, and rollback
  variants. Replay analysis found zero TLEs or suspicious-output rows; maximum
  p99/peak execution was **1391/2812 us** initially and **1301/2767 us** after
  repair. Reports are under `reports/iter-v192-chain-slack/`.
- Initial cap of eight extra tiles on large maps scored **5-10** on the
  seed-160 15-game screen, with candidate/comparator Ti **84,590/100,040**.
  All 15 commands were clean. Report: `reports/local-20260818T102648Z`.
- Repair 1 halved the map bonus cap while preserving compact-map behavior. It
  scored **6-9**, with Ti **80,480/89,600** and one comparator no-delivery
  row. All 15 commands were clean. Report:
  `reports/local-20260818T102941Z`.

## Decision and rollback

Neither screen beat the moving v0042 baseline, so v192 is rejected after its
single bounded repair without a 60-game gate. The temporary helper, constant,
and focused tests were removed. Candidate source is recursively identical to
immutable `bots/versions/v0042_low-liquidity-gunner_20260818-0737_eeafad8f`;
rollback focused, compileall, and smoke checks passed. No release, package,
remote gate, upload, activation, or baseline transition occurred.

## Remaining risk

The fixed chain slack may still abandon routes around unusually long
chokepoints, but increasing it globally worsened both tested screens. Future
route work needs replay evidence identifying a specific abandonment rather
than another map-size slack knob. The quick screen remains at its
map-complete minimum of 15 games; reducing it further would remove a map from
the checkpoint.
