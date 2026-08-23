# v229 home-interceptor Launcher — rejected after one repair

## Replay-backed hypothesis

The v228 release recheck tied **30-30** despite collecting more titanium,
while the loss rows had materially fewer surviving Builders, Harvesters,
Barriers, and Sentinels. The current dynamic policy also treats a visible
enemy Builder near home as a normal strike target even though Builder-versus-
Builder fire is illegal; that can consume turns without removing the
infiltrator. The infiltration audit shows this is an occasional event, so the
response must be reactive and bounded rather than an opening detour.

Test one structural defense: after the economy has completed three routes and
the Core has a reserve for a Harvester and replacement conveyors, the Core's
designated Defender may build at most one home Launcher when an enemy Builder
is actually inside the home-threat radius. The Launcher only exiles an
adjacent enemy Builder to a visible, empty, API-legal tile farther from our
Core. It never launches friendly units, never builds during the opening, and
does not alter the offensive Launcher/attacker policy.

## Allowed files

- `bots/candidate/main.py` (Launcher dispatch and per-unit state);
- `bots/candidate/bot/defender.py` (one reserve-gated home build hook);
- one focused v229 Launcher legality test module;
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable state/report
  metadata.

## Non-goals

No opening route/ore policy, chain geometry, dynamic task ordering, enemy-route
hijack, sabotage, Sentinel/Barrier/Gunner/ammo tuning, offensive Launcher
relay, Store schema/slot change, map branch, baseline/archive, package,
upload, activation, or live-state transition.

## Done criteria

Focused tests must cover the three-route/reserve/threat gate, single-build
ownership, safe placement, enemy-only pickup, far-from-Core destination
selection, `can_launch` gating, and no-op behavior without an adjacent enemy
Builder. Candidate compileall, `make static`, and `make smoke` retain the
inherited profile. The rotated 15-map screen must be command-clean, have no
new candidate no-delivery/TLE/suspicious rows, and show a clear paired win or
survival/pressure edge over exact v0042. Run the 60-game gate only if that
edge is repeatable; otherwise allow one bounded repair and restore exact v0042
parity.

## Status

The implementation passed the new focused legality/ownership suite **27/27**,
compileall, and smoke **4/4**; `make static` retained the inherited exit 2
(15 obsolete-module import errors plus two navigation fast-path assertions).
The initial rotated 15-map screen was command-clean but lost **6-9**, with
candidate collection **50,040 vs 60,620 Ti**, first-delivery mean
**26.07 vs 28.07**, and no candidate no-delivery/TLE/suspicious rows
(`reports/local-20260818T214418Z`). Four candidate Launcher placements were
observed in that screen, but there was no paired edge.

The one allowed repair required the intruder to be within the tighter Core
radius and adjacent to the prospective Launcher site so the purchase could
immediately change the threat geometry. Focused coverage remained **27/27**,
compileall passed, repair static retained the inherited exit 2, and repair
smoke was **4/4** (`reports/iter-v229-home-interceptor/repair-static.log`,
`reports/iter-v229-home-interceptor/repair-smoke.log`, report
`reports/local-20260818T215650Z`). The repaired 15-map screen was again
command-clean but again **6-9**, with collection **50,040 vs 60,620 Ti**,
first-delivery mean **26.07 vs 28.07**, no-delivery **0/0**, zero
TLE/suspicious rows, and no Launcher placements
(`reports/local-20260818T214923Z`). No 60-game gate was justified.

The temporary Launcher dispatch, build hook, state, and test were removed.
Rollback focused coverage was **27/27**, compileall passed, static retained
the inherited exit 2, and rollback smoke was **4/4** at
`reports/local-20260818T215408Z`. Every candidate Python file is recursively
byte-identical to immutable v0042. No promotion, package, upload, activation,
or live-state transition occurred; v0042 remains the baseline. Full logs and
analyses are in `reports/iter-v229-home-interceptor/`.
