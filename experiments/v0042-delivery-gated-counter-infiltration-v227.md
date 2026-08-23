# v227 delivery-gated counter-infiltration — rejected after one repair

## Replay basis

The v224/v226 infiltration audit found that route-radius enemy Builder entries
before first delivery were uncommon, while top-team winners converted the
opening into early Harvesters and connected paths. The current v0042 dynamic
selector can claim a visible enemy Harvester before any own route is recorded;
that is a workforce detour during the same phase in which the replay sample
shows the largest first-delivery gap. v195/v196 tested late sabotage/takeover
primitives, not this opening phase firewall, and both were rejected without
changing the existing route priority.

## Objective

Keep the existing counter-infiltration/hijack behavior, but open it only after
one own completed route and a live replacement reserve of one Harvester plus
two Conveyors. Before that point a dynamic Builder must stay on the existing
home-threat, belt-repair, and economy policy. Once open, one deterministic
nearest dynamic Builder owns a visible enemy Harvester, preventing duplicate
route-seed detours. The existing legal Conveyor build and seeded-route FSM are
unchanged.

## Allowed files

- `bots/candidate/bot/dynamic.py`;
- one focused v227 counter-infiltration test module;
- `docs/CURRENT_PLAN.md`, this record, `UPDATES.md`, and durable report/state
  metadata.

## Non-goals

No Store change, new sabotage primitive, route geometry, Launcher/Barrier/
Sentinel/Gunner/ammo policy, fixed-role change, map branch, baseline/archive,
package, upload, activation, or live-state change.

## Done criteria

Focused phase/ownership/reserve/legality tests, compileall, static, and smoke
must retain the inherited profile. The rotated 15-map screen must be
command-clean, introduce no new no-delivery/TLE/suspicious row, and show a
paired win-rate or early delivery/collection edge without a protected-map
collapse. Run the 60-game gate only after that edge; otherwise permit one
bounded repair and then restore exact v0042 parity.

## Validation and decision

The initial candidate passed focused coverage **31/31**, compileall, and smoke
**4/4**; `make static` retained the inherited exit 2. Its seed-172 15-map
screen was command-clean and delivery-clean at **8-7**, with collection
**48,980 vs 56,390 Ti**, first-delivery mean **27.27 vs 85.20** (one baseline
no-delivery row), and zero candidate no-delivery/TLE/suspicious rows. Because
the edge was only one game and collection was lower, an independent rotated
screen was required rather than a release gate.

The seed-173 rotated screen reversed to **7-8**, with collection
**74,190 vs 91,380 Ti**, first-delivery mean **89.60 vs 23.80**, and one
candidate no-delivery row. The one allowed repair added an existing round-20
fallback: when no own ore is visible/advised, a funded steal may open even
before the first route. Repair focused coverage remained **31/31**, compileall
and smoke **4/4** stayed clean, and static retained the inherited exit 2; the
rotated screen remained **7-8** but improved collection to **64,250 vs 63,620
Ti**, first delivery to **23.13 vs 27.20**, and removed all no-delivery rows.
The repair still supplied no win-rate edge, so no 60-game gate was justified.

The temporary phase gate, nearest-owner logic, fallback, and test were removed.
Final rollback focused coverage was **27/27**, compileall passed, static kept
the inherited failures, and smoke was **4/4** at
`reports/local-20260818T210643Z`. Every candidate Python file is byte-
identical to immutable v0042; no promotion, package, upload, activation, or
live-state transition occurred. Full evidence is in this folder and the two
screen reports `reports/local-20260818T205827Z`,
`reports/local-20260818T210032Z`, and `reports/local-20260818T210403Z`.
