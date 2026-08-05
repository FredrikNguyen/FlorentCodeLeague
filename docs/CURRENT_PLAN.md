# Objective

Fix Builder navigation so construction targets are approached from legal orthogonal adjacency, paths are reused across movement turns, and static route planning does not restart because of transient Builder occupancy.

## Allowed files

* `bots/candidate/bot/navigation.py`
* `bots/candidate/bot/world.py`
* Navigation-related sections of `bots/candidate/bot/builder.py`
* `bots/candidate/bot/actions.py`
* Focused tests only

## Required behavior

1. Add separate move-to-tile and move-to-adjacent navigation.
2. Make route, Harvester, and repair construction use move-to-adjacent.
3. Replace `(start, goal, epoch)` cache semantics with one reusable active path per unit.
4. Split transient navigation blockage from permanent route-layout blockage.
5. Make route planning respond only to permanent layout changes.
6. Correct `TurnActions.destroy()` so it does not consume the wrapper action.
7. Preserve cardinal movement, `can_*` action gating, deterministic tie-breaking, and the CPU cutoff.
8. Do not change Store layout, budgets, roles, defense, offense, route economics, or opening policy.

## Implementation requirements

### Navigation modes

Provide two explicit operations:

* Move toward and potentially stand on a target tile.
* Move to any legal orthogonally adjacent stance around a target.

When moving to an action stance:

* Generate the target’s four cardinal neighbors.
* Remove out-of-bounds and blocked candidates.
* If already on a legal stance, return `Direction.CENTRE`.
* Select the shortest deterministically reachable stance.
* Never deliberately enter the action target tile.

### Active path reuse

Store per-Navigator:

* current goal and mode;
* relevant obstacle epoch;
* active path;
* current path index;
* replan count;
* cache-hit count.

Reuse the path while:

* goal and mode are unchanged;
* the relevant obstacle epoch is unchanged;
* current position remains on the path;
* the next step remains legal.

Replan only when one of those conditions fails.

### Obstacle separation

`WorldMemory` must distinguish:

* navigation blockers: walls, Core footprint, impassable buildings, recently observed Builders;
* route-layout blockers: walls, Core footprint, and known permanent impassable buildings.

Temporary Builder occupancy must not restart incremental route planning.

### Destroy semantics

`TurnActions.destroy()` must:

* call `can_destroy()` before `destroy()`;
* not require `_ready_action()`;
* not set `acted`;
* permit multiple legal destroy attempts in one wrapper instance;
* rely on the engine’s legality checks for any interaction with movement or later actions.

## Required tests

1. A Builder two cells away stops adjacent to a build target and never enters it.
2. An already-adjacent Builder does not move or increment blocked-step state.
3. A path is reused over at least two subsequent movement turns.
4. Changing the goal invalidates the active path.
5. A permanent obstacle invalidates the active path.
6. Transient movement by another Builder does not restart static route search.
7. An illegal next step triggers one deterministic replan.
8. BFS on a 30×30 map performs no more than 900 expansions.
9. CPU cutoff returns safely without an unbounded search.
10. `destroy()` does not set `acted`.
11. Two legal destroys may be attempted in one wrapper turn.
12. Build and movement mutual exclusion remains intact.

## Commands

```bash
make static
make smoke

python scripts/run_local_matrix.py \
  --config configs/eval_regression.toml \
  --maps sprint bridge crossfire vault \
  --seeds 1 7 19
```

## Success criteria

* All focused tests pass.
* No Builder stalls by standing on its intended construction tile.
* Path replans decrease relative to v0003.
* Conveyor construction progresses monotonically.
* No new exception, TLE, or deterministic-behavior regression.
* Store, economy, defense, offense, and budget behavior remain unchanged.

## Completion report

Return:

* files changed;
* behavior changed;
* behavior deliberately unchanged;
* exact tests and results;
* report and replay paths;
* cache-hit and replan observations;
* remaining risks;
* concise Git diff summary.

Do not spawn subagents and do not run the complete 21-map release matrix.
