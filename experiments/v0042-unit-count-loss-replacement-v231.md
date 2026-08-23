# v231 unit-count loss replacement

## Objective

Test one workforce-liveness hypothesis against the exact v0042 baseline: the
Core already replaces a Builder whose destruction it can query, but an
attacker can die outside Core vision and remain in `builder_ids` forever. The
authoritative `get_unit_count()` includes the Core and active non-Harvester
units, so a persistent drop with no corresponding confirmed Builder prune is
evidence that one tracked unit disappeared. After a short confirmation window,
allow one replacement Builder once the existing target roster, normal reserve,
and ramp-established gates are satisfied.

This is deliberately a recovery signal, not a larger opening: it does not
change initial/reinforcement targets, role assignment, attack priorities,
turret policy, Store schema, or any route behavior. A single pending loss is
consumed only by a successful spawn and has a cooldown before another unseen
loss can authorize a replacement.

## Allowed files

- `bots/candidate/main.py` (Core liveness state);
- `bots/candidate/bot/core_role.py` (unit-count observation and bounded spawn
  exception);
- `bots/candidate/bot/constants.py` (confirmation/cooldown constants);
- one focused unit-count/loss-replacement test module;
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable
  report/state metadata.

## Non-goals

No infiltration/anti-infiltration task, opening economy or route rewrite,
Harvester target increase, ammo/turret/Sentinel/Barrier/Launcher tuning,
navigation change, Store-slot change, map-name branch, baseline/archive,
package, upload, activation, or live-state operation.

## Done criteria

Focused tests must prove first-sample initialization, confirmed Builder-loss
separation, unseen-loss confirmation, cooldown, normal reserve and
unit-cap gates, and no change to the ordinary target spawn path. Candidate
compileall, `make static`, and `make smoke` must retain the inherited runtime
profile. A rotated 15-map screen against exact v0042 must be command- and
delivery-clean, show a material paired win-rate or repeatable workforce/
collection edge, and introduce no protected-map collapse. Allow at most one
bounded repair; otherwise remove the temporary code/test and restore exact
v0042 parity. Do not run the 60-game gate without a clear screen edge.

## Repair 1

The initial screen was command-clean at 8-7 but collected 83,820 versus
94,770 Ti and placed 114 versus 129 Harvesters. The only allowed repair lowers
the aggregate-loss confirmation from three rounds to two so a real off-screen
Builder death can be replaced before the next economy phase, while preserving
the same target, reserve, cap, and cooldown gates.

## Result

The initial implementation passed focused coverage **27/27**, compileall, and
smoke **4/4**; static retained the inherited exit 2. The 15-map screen was
command/delivery-clean at **8-7**, but collected **83,820 vs 94,770 Ti** and
placed **114 vs 129 Harvesters** (`reports/local-20260818T222707Z`; replay
metrics in `reports/iter-v231-unit-count/replay-analysis.json`). The one
allowed two-round repair stayed command-clean but regressed to **6-9**, with
**41,870 vs 56,710 Ti** and **92 vs 127 Harvesters**
(`reports/local-20260818T223103Z`; replay metrics in
`reports/iter-v231-unit-count/repair-replay-analysis.json`). Both variants
had zero TLE/suspicious rows. The unit-count signal could not separate a dead
Builder from a dead turret, so the hypothesis was rejected. Temporary
source/test were removed; rollback focused coverage was **23/23**, compileall
passed, static retained the inherited result, smoke was **4/4**, and all
candidate Python files match immutable v0042 recursively
(`reports/iter-v231-unit-count/rollback/`). No promotion or platform operation
occurred.
