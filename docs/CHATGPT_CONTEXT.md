

# Start here

> Generated cross-session handoff. Do not hand-edit dynamic fields. Update
> `state/project_state.json` with `scripts/set_project_state.py` and deployment state
> through the live operator, then run `make refresh-start`.

## Current development focus

| Field | Value |
|---|---|
| Milestone | Current plan navigation checkpoint: behavior gates pass; static harness blocker |
| Current hypothesis | Active per-unit paths and legal adjacent stances reduce Builder replans without changing strategy policy. |
| Current experiment | reports/navigation-20260805T2110 |
| Next recommended task | Repair the pre-existing harness/startup static failures before starting NEXT_ITERATIONS_PLAN Iteration 0; do not alter navigation behavior meanwhile. |
| Candidate | `bots/candidate` |
| Frozen baseline | `bots/baseline` |
| Last Codex task | Implement docs/CURRENT_PLAN.md navigation, adjacency, epoch separation, and destroy semantics. |
| Last Codex outcome | BLOCKED: focused/smoke/regression gates pass, but make static exits 2 on 4 harness failures and 3 missing-agent errors outside current-plan scope. |
| Last Codex report | reports/navigation-20260805T2110 |
| Last local report | reports/navigation-20260805T2110 |

## Live deployment snapshot

| Field | Value |
|---|---|
| Phase | `idle` |
| Active platform version | unknown |
| Pending version | unknown |
| Previous active version | unknown |
| Last known-good version | unknown |
| Last known-good live score | unknown |
| Current candidate live score | unknown |
| Last observation | unknown |
| Last decision | unknown |

## Working tree snapshot

| Field | Value |
|---|---|
| Branch | `main` |
| Commit | `2de8371f` |
| Status | working tree has changes |

Always run `git status --short` yourself; this generated snapshot may be older than the working tree.

## Startup checklist

Before doing any work:

1. Read this file.
2. Read the current-state table and newest relevant entries in `UPDATES.md`.
3. Read `state/project_state.json` and `state/live_state.json`.
4. Run `git status --short` and inspect relevant diffs.
5. Read the nearest applicable `AGENTS.md` for files you will touch.
6. Load only the task-specific detailed documents below.

## Task-specific document routing

| Task | Required detailed reading |
|---|---|
| Bot mechanics or strategy | `bots/candidate/AGENTS.md`, `GAME_RULES.md`, relevant `docs/IMPLEMENTATION_PLAN.md` milestone |
| Non-trivial implementation | `docs/CODEX_HARNESS.md`, experiment record, relevant nested `AGENTS.md` |
| Evaluation or promotion | `docs/EVALUATION_PLAN.md`, experiment record, baseline/live comparison |
| Packaging or live operations | `scripts/AGENTS.md`, `docs/SUBMISSION_AND_VERSIONING.md`, `docs/LIVE_AUTOPILOT.md`, fresh `state/live_state.json` |
| Repository/tooling architecture | `docs/REPOSITORY_STRUCTURE.md`, `docs/PROJECT_CONSIDERATIONS.md` |

## Durable handoff rules

- `state/project_state.json`: authoritative current development focus.
- `state/live_state.json`: authoritative deployment and rollback state.
- `UPDATES.md`: human-readable append-only history.
- `docs/START_HERE.md`: generated concise view of those sources.
- Approved implementation tasks must record their report/outcome and regenerate this file.
- Platform actions may continue across sessions; never infer their state from chat history.

## Useful commands

```bash
make refresh-start
make codex TASK="<bounded task>"
make static
make smoke
make live-status
make live-autopilot
```

Generated at `2026-08-05T21:05:55Z` from project state updated `2026-08-05T21:00:21Z` and live state updated `2026-08-05T00:00:00Z`.


## Stable project brief

# Florent Code League project brief

## Objective

Build a reliable Python bot that establishes titanium delivery, adapts to map geometry, protects its Core, and converts economic advantage into enemy-Core pressure.

## Match constraints

- Two teams on an 8×8 to 30×30 grid.
- Destroy the enemy Core to win; maximum 1000 rounds.
- Ladder series contain five games.
- Approximately 10 ms CPU per unit per round on the ladder.
- An uncaught exception permanently destroys the affected unit.
- Builders move cardinally and cannot move and act in the same round.
- Build, attack, heal, and destroy target orthogonally adjacent tiles.
- Prices scale with currently live entities; query costs through the API.
- Team communication is 16 delayed integer Store slots.

## Main systems

- **Core:** Builder spawning, global budget, ammunition conversion.
- **Builders:** sensing, movement, construction, healing, sabotage.
- **Economy:** ore discovery, Harvester placement, payback-aware expansion.
- **Logistics:** directed Conveyors, Splitters, Core last mile, route repair.
- **Combat:** Gunner, Sentinel, Launcher, barriers, ammunition budgeting.
- **Coordination:** per-unit state plus a small versioned Store protocol.

## Current implementation direction

1. Safe deterministic dispatch and fallback behavior.
2. Versioned shared coordinate protocol.
3. Bounded cached cardinal BFS and stale-path recovery.
4. Verified Harvester-to-Core delivery route.
5. Payback-aware expansion and route repair.
6. Defense/ammo policy, then offense and map-adaptive openings.

## Engineering priorities

1. No illegal actions or escaping exceptions.
2. Bounded tail CPU.
3. End-to-end delivered titanium, not merely placed structures.
4. Deterministic paired evaluation across maps, seeds, and sides.
5. One isolated hypothesis per candidate and instant rollback to known-good live version.

## Workflow

- Sol High in ordinary ChatGPT creates an occasional bounded plan from the generated planning packet.
- Luna XHigh in Codex implements, tests, and self-reviews in one session.
- Deterministic Python scripts run broad evaluation, package, submit, monitor, score, promote, and roll back.
- External Sol review is optional and used primarily for release candidates or difficult regressions.


## Current external plan

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


## Current machine state

### `state/project_state.json`

```json
{
  "baseline_path": "bots/baseline",
  "candidate_path": "bots/candidate",
  "current_experiment": "reports/navigation-20260805T2110",
  "current_hypothesis": "Active per-unit paths and legal adjacent stances reduce Builder replans without changing strategy policy.",
  "current_milestone": "Current plan navigation checkpoint: behavior gates pass; static harness blocker",
  "last_codex_outcome": "BLOCKED: focused/smoke/regression gates pass, but make static exits 2 on 4 harness failures and 3 missing-agent errors outside current-plan scope.",
  "last_codex_report": "reports/navigation-20260805T2110",
  "last_codex_task": "Implement docs/CURRENT_PLAN.md navigation, adjacency, epoch separation, and destroy semantics.",
  "last_local_report": "reports/navigation-20260805T2110",
  "next_recommended_task": "Repair the pre-existing harness/startup static failures before starting NEXT_ITERATIONS_PLAN Iteration 0; do not alter navigation behavior meanwhile.",
  "schema_version": 1,
  "updated_at": "2026-08-05T21:00:21Z"
}
```

### `state/live_state.json`

```json
{
  "activated_at": null,
  "active_version": null,
  "baseline_match_ids": [],
  "candidate": null,
  "current_adjusted_score": null,
  "current_live_score": null,
  "last_decision": null,
  "last_known_good_adjusted_score": null,
  "last_known_good_live_score": null,
  "last_known_good_version": null,
  "last_observation_at": null,
  "last_report_dir": null,
  "observed_match_ids": [],
  "pending_version": null,
  "phase": "idle",
  "previous_active_version": null,
  "rank_after": null,
  "rank_before": null,
  "rating_after": null,
  "rating_before": null,
  "schema_version": 1,
  "updated_at": "2026-08-05T00:00:00Z"
}

```

## Git snapshot

- Branch: `main`
- Commit: `2de8371f`

```diff
No uncommitted relevant diff.
```

## Recent updates

### Current-plan navigation checkpoint — 2026-08-05T21:00:41Z

- Status: behavior checkpoint passed; next-plan iterations are paused because make static exits 2 on pre-existing harness/startup failures outside the approved scope.
- Files changed: bots/candidate/bot/navigation.py, world.py, builder.py, actions.py, tests/test_candidate_navigation.py, tests/test_candidate_actions.py, tests/test_candidate_builder_navigation.py.
- Focused tests: 34/34 passed; compileall passed. Full logs: reports/navigation-20260805T2110/focused.log and compileall.log.
- make static: exit 2; candidate/static-contract checks passed, with 4 harness failures and 3 missing-agent errors. Full log: reports/navigation-20260805T2110/make-static.log.
- make smoke: 4/4 games, zero command failures; report: reports/local-20260805T205901Z.
- Regression subset: 24/24 games, zero command failures/stderr; report: reports/local-20260805T205908Z.
- Metrics: active path one BFS and two cache hits over a three-step route; goal/epoch/blocked-step invalidations replan once; candidate production count is 1,800 lines.
- Behavior unchanged deliberately: Store/economy/budget/roles/defense/offense/opening policy. Remaining risk: static harness state must be repaired before NEXT_ITERATIONS_PLAN Iteration 0 can start.
- Report: reports/navigation-20260805T2110/summary.md


### Live battle observation — 2026-08-05T19:31:39Z

- Platform reports submission `v0003-entrypoint-class-2de8371f` as numeric version `1`, `ready`, and active for Kleos.
- Eight rated ladder series are complete: one win and seven losses. The newest series beat Git Glam 3–2 (+4.041 Elo), raising the rating to `1402.3331784619274` and placing Kleos at rank `39/102`.
- The newest series reached the 1000-turn titanium-collection limit on all five maps: wins on `crossfire`, `sweden`, and `skerry`; losses on `twins` and `runestone`. No match error or resignation was reported.
- Previous Powerpuff Girls 0–5 ended by `core_destroyed` on all five maps after 266–317 turns; no platform/runtime error was reported.
- Replay-level comparison: the Git Glam series first produced HP events at turns 325–766 and no core destruction; the Powerpuff series first produced HP events at turns 12–87 and destroyed the Kleos core in every game. The current weakness is collection/economy on `twins` and `runestone`, not a submission/runtime failure.
- Battle descriptions from the decoded replay streams:
  - Git Glam `crossfire`: Kleos stayed at 4 builders, 2 harvesters, and 4 conveyors while Git Glam expanded to 13 builders, 4 harvesters, 13 conveyors, and a full turret mix; no core damage, Kleos won the 1000-turn collection finish.
  - Git Glam `sweden`: first HP event at turn 458; Kleos reached 5 builders, 2 harvesters, and 13 conveyors, with sustained turret/resource activity and no core damage; Kleos won by collection.
  - Git Glam `twins`: first HP event at turn 454; Kleos stayed at 4 builders, 1 harvester, and 4 conveyors while Git Glam grew to 27 builders, 5 harvesters, 20 conveyors, and heavy defense; Git Glam won collection without destroying the core.
  - Git Glam `runestone`: first HP event at turn 622; Kleos recorded 85 conveyor placements and 70 later removals, indicating route churn or repair activity; Git Glam’s larger 28-builder/42-conveyor footprint won collection.
  - Git Glam `skerry`: first HP event at turn 766; Kleos finished with 4 builders, 3 harvesters, and 6 conveyors, survived without core damage, and won collection.
  - Powerpuff `duel`, `sweden`, `longship`, `hive`, and `quarry`: first HP events came at turns 12, 87, 29, 37, and 48 respectively; Powerpuff scaled substantial gunner/harvester/conveyor forces and destroyed the Kleos core at turns 273, 285, 271, 266, and 317.
- Full notes and per-map descriptions: `reports/live-battles-20260805T193139Z.md`; raw capture: `reports/live-latest-battles-20260805T193139Z/`; newest replays: `replays/live-c17b2501-20260805/`.

### Codex cap-replan fix — 2026-08-05T17:37:04Z

- Fixed blocked-route replanning for a Builder that already owns one of the three shared project reservations: admission now counts only other projects while preserving the owner's reservation, so it cannot deadlock at the cap or create a fourth project.
- Added Player.run coverage for reserved replanning at the shared cap and strengthened the unreserved fourth-project rejection test.
- Validation: independent Sol review `APPROVED`; focused unit suite 33/33; smoke 4/4; regression 54/54; full matrix 210/210 command-clean, 205/210 wins versus 165/210 prior, with bridge and string 10/10 and no non-target map regression; benchmark p99 6.246564 ms, max 6.830654 ms.
- Remote gate was attempted but DNS was unavailable; no platform upload or activation was performed. Luna harness compatibility remains unavailable (`native_luna_compatible: False`).
- Submission archive: `artifacts/submissions/v0002_cap-replan_20260805-1736_2de8371f.zip` (SHA-256 `5f3118ba1d25c98fc890f76b895ab6c68adc5a51

## Latest report summary

### `reports/navigation-20260805T2110/summary.md`

# Current-plan navigation checkpoint

Status: behavior checkpoint passed; repository `make static` remains blocked by pre-existing harness/startup failures outside the approved files.

## Files changed

- `bots/candidate/bot/navigation.py`: explicit tile/adjacent operations, bounded multi-goal BFS, active per-unit path/index, deterministic fallback, cache-hit/replan counters.
- `bots/candidate/bot/world.py`: separate navigation/layout epochs and blocker predicates; compatibility aliases retained.
- `bots/candidate/bot/builder.py`: construction/repair/Harvester/redundancy approaches use adjacent navigation; route search uses layout epoch/predicate; adjacent emergency fallback cannot enter the target.
- `bots/candidate/bot/actions.py`: `destroy()` uses only engine legality and does not set `acted`.
- Focused navigation/action/world/Builder tests.

## Validation

- Focused: 34/34 passed (`focused.log`).
- `make static`: exit 2; all candidate/static-contract tests passed, but 4 harness failures and 3 startup/harness errors remain (`make-static.log`). The failures are missing `.codex/agents/{luna-implementer,sol-planner}.toml` plus stale harness assertions in `configs/codex_harness.toml`, `scripts/codex_task.py`, and `AGENTS.md`; none are in the current-plan scope.
- `make smoke`: 4/4 games, zero command failures; report `reports/local-20260805T205901Z`.
- Required regression subset: 24/24 games, zero command failures/stderr; report `reports/local-20260805T205908Z`.
- Compileall: passed (`compileall.log`).

## Observations and risks

- A three-step empty-grid route used one BFS/replan and two active-path cache hits; goal/epoch changes and a blocked next step each caused a single deterministic replan.
- Smoke/regression replays are under the linked local report directories; no exceptions or TLEs were reported.
- No Store, economy, budget, role, defense, offense, or opening-policy code changed.
- The static gate cannot be declared fully green until the unrelated harness/startup state is repaired; per the iteration rules, do not start the next plan iteration while that gate is unresolved.

## Diff review

Candidate source was compared with the immutable v0003 archive before and after the change. Production candidate code remains at the 1,800-line static limit; compileall and all focused behavior checks pass.


## Current candidate source

### `bots/candidate/bot/__init__.py`

```python

```

### `bots/candidate/bot/actions.py`

```python
from __future__ import annotations

from fcode import Direction, EntityType, Position

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


def cpu_is_safe(ct: object, limit_us: int = 7000) -> bool:
    try: return int(ct.get_cpu_time_elapsed()) < limit_us
    except (AttributeError, TypeError, ValueError): return True


class TurnActions:
    __slots__ = ("ct", "moved", "acted", "ammo_converted")

    def __init__(self, ct: object) -> None:
        self.ct, self.moved, self.acted, self.ammo_converted = ct, False, False, False

    def _ready_action(self) -> bool:
        if self.moved or self.acted: return False
        try: return bool(self.ct.can_act())
        except AttributeError: return True
        except Exception: return False

    def move(self, direction: Direction) -> bool:
        if self.moved or self.acted or direction not in CARDINALS: return False
        try:
            if not self.ct.can_move(direction): return False
            self.ct.move(direction)
        except Exception: return False
        self.moved = True; return True

    def _build(self, method: str, can_method: str, *args: object) -> int | None:
        if not self._ready_action(): return None
        try:
            if not getattr(self.ct, can_method)(*args): return None
            result = getattr(self.ct, method)(*args)
        except Exception: return None
        self.acted = True; return result if isinstance(result, int) else 1

    def build_conveyor(self, position: Position, direction: Direction) -> int | None: return self._build("build_conveyor", "can_build_conveyor", position, direction)
    def build_splitter(self, position: Position, direction: Direction) -> int | None: return self._build("build_splitter", "can_build_splitter", position, direction)
    def build_harvester(self, position: Position) -> int | None: return self._build("build_harvester", "can_build_harvester", position)
    def build_barrier(self, position: Position) -> int | None: return self._build("build_barrier", "can_build_barrier", position)
    def build_gunner(self, position: Position, direction: Direction) -> int | None: return self._build("build_gunner", "can_build_gunner", position, direction)
    def build_sentinel(self, position: Position, direction: Direction) -> int | None: return self._build("build_sentinel", "can_build_sentinel", position, direction)
    def build_launcher(self, position: Position) -> int | None: return self._build("build_launcher", "can_build_launcher", position)

    def build(self, entity_type: EntityType, position: Position, extra: Direction | Position | None = None) -> int | None:
        return self._build("build", "can_build", entity_type, position, extra)

    def fire(self, target: Position) -> bool:
        if not self._ready_action(): return False
        try:
            if not self.ct.can_fire(target): return False
            self.ct.fire(target)
        except Exception: return False
        self.acted = True; return True

    def heal(self, target: Position) -> bool:
        if not self._ready_action(): return False
        try:
            if not self.ct.can_heal(target): return False
            self.ct.heal(target)
        except Exception: return False
        self.acted = True; return True

    def destroy(self, target: Position) -> bool:
        # Friendly destruction is a separate engine operation: it is gated by
        # the controller's own can_destroy() contract, but it does not consume
        # this wrapper's ordinary action slot.  The engine therefore remains
        # the authority on whether a later build, move, or destroy is legal.
        try:
            if not self.ct.can_destroy(target): return False
            self.ct.destroy(target)
        except Exception: return False
        return True

    def rotate(self, direction: Direction) -> bool:
        if not self._ready_action(): return False
        try:
            if not self.ct.can_rotate(direction): return False
            self.ct.rotate(direction)
        except Exception: return False
        self.acted = True; return True

    def launch(self, bot_position: Position, target: Position) -> bool:
        if not self._ready_action(): return False
        try:
            if not self.ct.can_launch(bot_position, target): return False
            self.ct.launch(bot_position, target)
        except Exception: return False
        self.acted = True; return True

    def spawn(self, position: Position) -> int | None: return self._build("spawn_builder", "can_spawn", position)

    def convert_ammo(self, amount: int) -> bool:
        if self.ammo_converted or isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0: return False
        try:
            if not self.ct.can_convert_ammo(amount): return False
            self.ct.convert_ammo(amount)
        except Exception: return False
        self.ammo_converted = True; return True

```

### `bots/candidate/bot/builder.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field

from fcode import Direction, EntityType, Environment, GameConstants, Position

from .actions import CARDINALS, TurnActions, cpu_is_safe
from .comms import Slot, claim_is_fresh, decode_alert, encode_alert, encode_budget, epoch_distance, pack_claim, unpack_claim
from .core import compute_budget
from .defense import assess_threat, choose_defensive_build, choose_turret_type
from .economy import claim_should_release, estimate_payback_round, estimate_route_cost, expansion_allowed, next_harvester_state, score_ore
from .logistics import find_broken_link, plan_core_outward_route, splitter_redundancy_justified, teardown_allowed, verify_route
from .navigation import Navigator, bounded_bfs
from .offense import choose_raid_action, choose_rally
from .policy import assign_role, late_game_policy, nearest_position
from .types import BuilderState, Role, RoutePlan, ThreatKind
from .world import WorldMemory


@dataclass(slots=True)
class BuilderStateData:
    role: Role = Role.SCOUT; state: BuilderState = BuilderState.DISCOVER; world: WorldMemory | None = None; navigator: Navigator | None = None
    ore_target: Position | None = None; route: RoutePlan | None = None; route_index: int = -1; repair_index: int | None = None
    claim_slot: int | None = None; claim_epoch: int = 0; claim_started_round: int = 0; last_delivery_round: int | None = None
    last_position: Position | None = None; blocked_steps: int = 0; cursor: int = 0
    built_links: dict[Position, tuple[EntityType, Direction]] = field(default_factory=dict)
    route_search: dict[str, object] | None = None; last_resource_total: int | None = None; last_resource_round: int | None = None; delivery_started_round: int | None = None
    backlog_rounds: int = 0; rally_target: Position | None = None; rally_expires_epoch: int = 0; last_final_storage: bool | None = None
    redundancy_branch: tuple[Position, ...] = (); redundancy_index: int = -1; redundancy_join: Position | None = None; project_count: int = 0; project_pending: bool = False


def _id(ct: object) -> int:
    try: return int(ct.get_id())
    except Exception: return 0


def _round(ct: object) -> int:
    try: return int(ct.get_current_round())
    except Exception: return 0


def _pos(ct: object) -> Position:
    try: return ct.get_position()
    except Exception: return Position(0, 0)


def _read_claims(ct: object, width: int, height: int):
    result = []
    for index, slot in enumerate((Slot.CLAIM_0, Slot.CLAIM_1, Slot.CLAIM_2)):
        try: claim = unpack_claim(ct.read_store(int(slot)), width, height)
        except Exception: claim = None
        if claim is not None: result.append((index, claim))
    return result


def _active_project_count(ct: object, state: BuilderStateData | None = None) -> int:
    width, height, round_no, owner_id = int(ct.get_map_width()), int(ct.get_map_height()), _round(ct), _id(ct); claims = dict(_read_claims(ct, width, height)); markers = tuple(int(ct.read_store(int(slot))) for slot in (Slot.PRIMARY_ORE, Slot.LOGISTICS, Slot.THREAT)); active = sum(min(3, value & 3) for index, value in enumerate(markers) if value & 3 and (claim := claims.get(index)) is not None and claim_is_fresh(claim, round_no & 63) and value >> 8 == claim.owner_id and epoch_distance(round_no & 63, (value >> 2) & 63) <= 31); local = max(int(getattr(state, "project_count", 0)), int(state is not None and bool(state.route_search is not None or state.route_index >= 0 or state.redundancy_branch))); own = markers[state.claim_slot] & 3 if state is not None and state.claim_slot is not None else 0; return min(3, active + max(0, local - own))


def _reserve_project(ct: object, state: BuilderStateData, *, wait_visible: bool = False) -> bool:
    if state.claim_slot is None: return False
    try: slot, owner, round_no = (Slot.PRIMARY_ORE, Slot.LOGISTICS, Slot.THREAT)[state.claim_slot], _id(ct), _round(ct); current = int(ct.read_store(int(slot))); current = current & 3 if current >> 8 == owner and epoch_distance(round_no & 63, (current >> 2) & 63) <= 31 else 0
    except Exception: return False
    if state.project_pending: state.project_pending = current < state.project_count; return not state.project_pending
    if state.project_count > 0 and not wait_visible: return True
    count = max(current, int(state.project_count)) + 1; allowed = count <= 3; count = min(3, count)
    if not allowed: return False
    try: ct.write_store(int(slot), (owner << 8) | ((round_no & 63) << 2) | count); state.project_count = count; state.project_pending = wait_visible; return not wait_visible
    except Exception: return False


def _ore_is_valid(ct: object, world: WorldMemory, position: Position | None) -> bool: return position is not None and 0 <= position.x < world.width and 0 <= position.y < world.height and (position in world.ore_positions or ct.get_tile_env(position) == Environment.ORE_TITANIUM)


def _reset_route_search(state: BuilderStateData) -> None:
    state.route_search = None; state.route = None; state.route_index = -1; state.repair_index = None; state.last_final_storage = None; state.redundancy_branch = (); state.redundancy_index = -1; state.redundancy_join = None


def _publish_owner_state(ct: object, state: BuilderStateData, world: WorldMemory, round_no: int) -> None:
    if state.claim_slot is None or round_no % 8 != 0: return
    try:
        count = max(int(state.project_count), int(bool(state.route_search is not None or state.route_index >= 0 or state.redundancy_branch))); project_value = (_id(ct) << 8) | ((round_no & 63) << 2) | min(3, count); ct.write_store(int((Slot.PRIMARY_ORE, Slot.LOGISTICS, Slot.THREAT)[state.claim_slot]), project_value)
        claim = next(claim for index, claim in _read_claims(ct, world.width, world.height) if index == state.claim_slot and claim.owner_id == _id(ct))
        if claim.position is None: return
        ct.write_store(int(Slot.CLAIM_0 + state.claim_slot), pack_claim(claim.position, world.width, round_no, _id(ct), world.height))
        if state.claim_slot == 2: ct.write_store(int(Slot.BUDGET), encode_budget(compute_budget(ct, route_projects=int(state.route is not None))))
    except Exception: pass


def _read_rally(ct: object, state: BuilderStateData) -> None:
    try:
        decoded = decode_alert(ct.read_store(int(Slot.RALLY)), int(ct.get_map_width()), int(ct.get_map_height()))
        round_no = int(ct.get_current_round()) & 63
    except Exception: state.rally_target, state.rally_expires_epoch = None, 0; return
    if decoded is None: state.rally_target, state.rally_expires_epoch = None, 0; return
    position, expires_epoch = decoded
    state.rally_target = position if position is not None and epoch_distance(expires_epoch, round_no) <= 8 else None; state.rally_expires_epoch = expires_epoch if state.rally_target is not None else 0


def _fresh_verified_rally(ct: object, state: BuilderStateData, world: WorldMemory, round_no: int) -> bool:
    target, observation = state.rally_target, world.dynamic.get(state.rally_target) if state.rally_target is not None else None
    if target is None or epoch_distance(state.rally_expires_epoch, round_no & 63) > 8 or observation is None or round_no - observation.seen_round >= 3: return False
    try: return observation.team is None or observation.team != ct.get_team()
    except Exception: return False


def _publish_rally(ct: object, state: BuilderStateData, world: WorldMemory, round_no: int) -> None:
    if state.claim_slot != 0 or world.enemy_core is None or round_no % 4 != 0: return
    observation = world.dynamic.get(world.enemy_core)
    if observation is None or round_no - observation.seen_round >= 3: return
    try:
        rally = choose_rally(_pos(ct), verified_target=world.enemy_core, target_age=0); expires = (round_no + 8) & 63; ct.write_store(int(Slot.RALLY), encode_alert(rally, world.width, expires)); state.rally_target, state.rally_expires_epoch = rally, expires
    except Exception: pass


def _can_spend(ct: object, cost: int, *, preserve_defense: bool = False, projected_output: float | None = None, allow_late_completion: bool = False, emergency: bool = False, near_term_core_kill: bool = False, state: BuilderStateData | None = None, new_project: bool = False) -> bool: return _can_spend_with_policy(ct, cost, preserve_defense=preserve_defense, projected_output=projected_output, allow_late_completion=allow_late_completion, emergency=emergency, near_term_core_kill=near_term_core_kill, state=state, new_project=new_project)


def _can_spend_with_policy(ct: object, cost: int, *, preserve_defense: bool = False, projected_output: float | None = None, allow_late_completion: bool = False, emergency: bool = False, near_term_core_kill: bool = False, state: BuilderStateData | None = None, new_project: bool = False) -> bool:
    try:
        round_no, resources = _round(ct), int(ct.get_global_resources()); active_projects = _active_project_count(ct, state); own_project = int(state is not None and bool(state.project_count or state.route_search is not None or state.route_index >= 0 or state.redundancy_branch)); budget = compute_budget(ct, route_projects=max(0, active_projects - own_project) + int(new_project))
    except Exception:
        return False
    cost = max(0, int(cost))
    if cost <= 0 or new_project and active_projects >= 3 or round_no >= 850 and not (allow_late_completion or emergency or near_term_core_kill) or projected_output is not None and float(projected_output) <= 0: return False
    protected = budget.construction + budget.ammo + budget.liquidity + (0 if emergency else budget.defense)
    if resources < cost + protected: return False
    if emergency or near_term_core_kill: return not new_project or (state is not None and _reserve_project(ct, state, wait_visible=True))
    if estimate_payback_round(cost, output_per_round=2.5, start_round=round_no, horizon=1000) is None: return False
    return not new_project or (state is not None and _reserve_project(ct, state, wait_visible=True))


def _claim(ct: object, state: BuilderStateData, world: WorldMemory, round_no: int):
    claims = _read_claims(ct, world.width, world.height)
    own = next(((index, claim) for index, claim in claims if claim.owner_id == _id(ct)), None)
    if own is None:
        if state.claim_slot is not None: claim_should_release(False, 0, 31, True); state.claim_slot, state.ore_target = None, None; _reset_route_search(state)
        return None
    state.claim_slot, claim = own; age = epoch_distance(round_no & 63, claim.epoch); valid_ore = claim.position is None or _ore_is_valid(ct, world, claim.position)
    if not claim_is_fresh(claim, round_no & 63): claim_should_release(valid_ore, age, 31, False); state.claim_slot, state.ore_target = None, None; _reset_route_search(state); return None
    if claim_should_release(valid_ore, age, 31, False): state.claim_slot, state.ore_target = None, None; _reset_route_search(state); return None
    if claim.position is not None: state.ore_target = claim.position; _publish_owner_state(ct, state, world, round_no); return claim.position
    claimed = {other.position for _, other in claims if other.position is not None and claim_is_fresh(other, round_no & 63)}
    candidates = [position for position in world.known_ore() if position not in claimed]
    if not candidates:
        try:
            candidates = [tile for tile in ct.get_nearby_tiles() if tile not in claimed and ct.get_tile_env(tile) == Environment.ORE_TITANIUM]
        except Exception: candidates = []
    if not candidates:
        if round_no % 8 == 0:
            try: ct.write_store(int(Slot.CLAIM_0 + state.claim_slot), pack_claim(None, world.width, round_no, _id(ct), world.height))
            except Exception: pass
        return None
    origin = _pos(ct)
    candidates.sort(key=lambda position: (-score_ore(position, origin=origin, expected_output_horizon=max(0, 1000 - round_no) * 2), position.y, position.x))
    target = candidates[min(state.claim_slot, len(candidates) - 1)]
    state.ore_target = target; state.claim_epoch, state.claim_started_round = round_no & 63, round_no
    try: ct.write_store(int(Slot.CLAIM_0 + state.claim_slot), pack_claim(target, world.width, round_no, _id(ct), world.height))
    except Exception: pass
    return target


def _visible(ct: object, position: Position):
    try:
        entity_id = ct.get_tile_building_id(position)
    except Exception: return None, None, None
    if entity_id is None: return None, None, None
    try: entity_type = ct.get_entity_type(entity_id)
    except Exception: entity_type = None
    try: direction = ct.get_direction(entity_id)
    except Exception: direction = None
    return entity_id, entity_type, direction


def _visible_route(state: BuilderStateData, ct: object, route: RoutePlan):
    def get(position: Position):
        _, entity_type, direction = _visible(ct, position)
        if entity_type is None:
            try: return state.built_links.get(position) if not ct.is_in_vision(position) else (entity_type, direction)
            except Exception: return state.built_links.get(position)
        return entity_type, direction

    return get


def _route_health(ct: object, state: BuilderStateData, route: RoutePlan, round_no: int) -> tuple[bool, bool]:
    try:
        resources = int(ct.get_global_resources())
    except Exception: resources = state.last_resource_total if state.last_resource_total is not None else 0
    previous_resources, previous_round = state.last_resource_total, state.last_resource_round; state.last_resource_total, state.last_resource_round = resources, round_no
    elapsed_rounds = 0 if previous_round is None else max(0, round_no - previous_round)
    passive_output = (0 if previous_round is None else max(0, round_no // GameConstants.PASSIVE_TITANIUM_INTERVAL - previous_round // GameConstants.PASSIVE_TITANIUM_INTERVAL)) * GameConstants.PASSIVE_TITANIUM_AMOUNT
    resource_gain = previous_resources is not None and resources > previous_resources and resources - previous_resources > passive_output
    final_storage: bool | None = None; positions = tuple(dict.fromkeys(route.cells[:2] + route.cells[-2:]))
    for position in positions:
        _, entity_type, _ = _visible(ct, position)
        if entity_type not in (EntityType.CONVEYOR, EntityType.SPLITTER): continue
        try: stored = ct.get_stored_resource(_visible(ct, position)[0]) is not None
        except Exception: continue
        if position == route.cells[-1]: final_storage = stored
    final_stored = bool(final_storage); storage_delivery = state.last_final_storage is True and final_storage is False; state.last_final_storage = final_storage
    output_blocked = final_storage is not None and final_stored and not resource_gain and not storage_delivery and elapsed_rounds > 0
    return storage_delivery, output_blocked


def _observe_route(ct: object, state: BuilderStateData, round_no: int) -> bool:
    if state.route is None: return False
    delivered, blocked_output = _route_health(ct, state, state.route, round_no)
    if delivered: state.last_delivery_round = round_no; state.backlog_rounds = 0; state.state = BuilderState.MAINTAIN; return True
    state.backlog_rounds = state.backlog_rounds + 1 if blocked_output else 0
    return False


def _world(ct: object, state: BuilderStateData) -> WorldMemory:
    width, height = int(ct.get_map_width()), int(ct.get_map_height()); fresh = state.world is None or (state.world.width, state.world.height) != (width, height); state.world = WorldMemory(width, height) if fresh else state.world; state.navigator = Navigator(width, height, state.world.is_navigation_blocked, cpu=ct.get_cpu_time_elapsed) if fresh else state.navigator; state.world.observe(ct); state.world.expire_dynamic(_round(ct)); return state.world


def _move(ct: object, state: BuilderStateData, goal: Position, actions: TurnActions, *, adjacent: bool = False) -> bool:
    world = state.world
    if world is None: return False
    if state.navigator is None: state.navigator = Navigator(world.width, world.height, world.is_navigation_blocked, cpu=ct.get_cpu_time_elapsed)
    current = _pos(ct)
    direction = (
        state.navigator.next_direction_to_adjacent(current, goal, world.navigation_epoch, can_step=ct.can_move)
        if adjacent
        else state.navigator.next_direction_to_tile(current, goal, world.navigation_epoch, can_step=ct.can_move)
    )
    if direction != Direction.CENTRE and actions.move(direction): state.blocked_steps = 0; return True
    state.blocked_steps += 1
    if state.blocked_steps >= 3:
        state.navigator.invalidate()
        for offset in range(4):
            direction = CARDINALS[(state.cursor + offset) % 4]
            if adjacent and current.add(direction) == goal:
                continue
            if actions.move(direction): state.cursor = (state.cursor + offset + 1) % 4; state.blocked_steps = 3; return True
    state.cursor = (state.cursor + 1) % 4; return False


def _expansion_ok(projected: int, harvester: int, route: int, budget: object, resources: int, *, concurrent_projects: int = 0) -> bool: return expansion_allowed(projected_output=projected, harvester_cost=harvester, route_cost=route, current_harvester_cost=harvester, construction_reserve=budget.construction, defense_reserve=budget.defense, ammo_reserve=budget.ammo, liquidity_reserve=budget.liquidity, available_resources=resources, concurrent_projects=concurrent_projects, max_projects=3)


def _route(ct: object, state: BuilderStateData, ore: Position, round_no: int) -> RoutePlan | None:
    world = state.world
    if world is None or world.own_core is None or not cpu_is_safe(ct): return state.route
    if state.route is not None and state.route.ore == ore and state.blocked_steps < 3: return state.route
    if round_no >= 850 and state.route is None and state.route_search is None: return state.route
    if state.navigator is not None: state.navigator.invalidate()
    try:
        conveyor_cost, harvester_cost, available_resources = max(0, int(ct.get_conveyor_cost())), max(0, int(ct.get_harvester_cost())), max(0, int(ct.get_global_resources()))
    except Exception: return state.route
    distance = abs(ore.x - world.own_core.x) + abs(ore.y - world.own_core.y); route_cost = estimate_route_cost(max(1, distance), conveyor_cost); active_projects = _active_project_count(ct, state); owns_route_reservation = state.project_count > 0; other_projects = max(0, active_projects - int(owns_route_reservation)); budget = compute_budget(ct, route_projects=active_projects if owns_route_reservation else active_projects + 1); projected_output = max(0, int((1000 - round_no) * 2.5))
    if estimate_payback_round(harvester_cost + route_cost, output_per_round=2.5, start_round=round_no, horizon=1000) is None: state.route_search = None; return state.route
    if not _expansion_ok(projected_output, harvester_cost, route_cost, budget, available_resources, concurrent_projects=other_projects) or (not owns_route_reservation and not _reserve_project(ct, state)): state.route_search = None; return state.route
    search = state.route_search if state.route_search is not None else {}
    planned = plan_core_outward_route(ore, world.core_footprint or {world.own_core}, world.width, world.height, world.is_route_planning_blocked, created_round=round_no, cpu_check=ct.get_cpu_time_elapsed, obstacle_epoch=world.layout_epoch, search_state=search)
    if planned is not None:
        exact_route_cost = estimate_route_cost(len(planned.cells), conveyor_cost)
        if estimate_payback_round(harvester_cost + exact_route_cost, output_per_round=2.5, start_round=round_no, horizon=1000) is None or not _expansion_ok(projected_output, harvester_cost, exact_route_cost, budget, available_resources, concurrent_projects=other_projects): ct.write_store(int((Slot.PRIMARY_ORE, Slot.LOGISTICS, Slot.THREAT)[state.claim_slot]), (_id(ct) << 8) | ((_round(ct) & 63) << 2)) if state.claim_slot is not None else None; state.project_count, state.project_pending = 0, False; state.route_search = None; return state.route
        state.route, state.route_index, state.repair_index, state.blocked_steps, state.route_search = planned, len(planned.cells) - 1, None, 0, None; state.built_links.clear()
    elif not search.get("complete"): state.route_search = search
    else: ct.write_store(int((Slot.PRIMARY_ORE, Slot.LOGISTICS, Slot.THREAT)[state.claim_slot]), (_id(ct) << 8) | ((_round(ct) & 63) << 2)) if state.claim_slot is not None else None; state.project_count, state.project_pending = 0, False; state.route_search = None
    return planned


def _build_route(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    route = state.route
    if route is None or state.route_index < 0: return False
    index, target, expected = state.route_index, route.cells[state.route_index], route.directions[state.route_index]
    if state.world is not None and state.world.is_route_planning_blocked(target): state.blocked_steps = 3; return False
    _, entity_type, direction = _visible(ct, target)
    if entity_type == EntityType.CONVEYOR and direction == expected: state.built_links[target], state.route_index = (entity_type, direction), index - 1; return True
    if _pos(ct).distance_squared(target) == 1:
        try:
            if not _can_spend(ct, int(ct.get_conveyor_cost()), projected_output=2.5, allow_late_completion=route.created_round < 850, state=state): return False
        except Exception: return False
        building_id = actions.build_conveyor(target, expected)
        if building_id is not None: state.built_links[target], state.route_index, state.state = (EntityType.CONVEYOR, expected), index - 1, BuilderState.VERIFY; return True
        return False
    return _move(ct, state, target, actions, adjacent=True)


def _verified(state: BuilderStateData, ct: object) -> bool: return state.route is not None and verify_route(state.route, _visible_route(state, ct, state.route))


def _harvester(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    if state.route is None or state.ore_target is None or not _verified(state, ct): return False
    round_no = _round(ct)
    _, entity_type, _ = _visible(ct, state.ore_target)
    if entity_type == EntityType.HARVESTER:
        state.delivery_started_round = state.delivery_started_round if state.delivery_started_round is not None else round_no
        if not _observe_route(ct, state, round_no) and state.last_delivery_round is None: state.state = BuilderState.DELIVER
        return True
    if _pos(ct).distance_squared(state.ore_target) != 1: return _move(ct, state, state.ore_target, actions, adjacent=True)
    try: harvester_cost = int(ct.get_harvester_cost())
    except Exception: return False
    if not _can_spend(ct, harvester_cost, projected_output=2.5, allow_late_completion=round_no >= 850, state=state): return False
    if actions.build_harvester(state.ore_target) is not None: (ct.write_store(int((Slot.PRIMARY_ORE, Slot.LOGISTICS, Slot.THREAT)[state.claim_slot]), (_id(ct) << 8) | ((round_no & 63) << 2)) if state.claim_slot is not None else None); state.project_count, state.project_pending, state.delivery_started_round, state.last_resource_total, state.last_resource_round, state.state = 0, False, round_no, None, None, BuilderState.DELIVER; return True
    return False


def _repair(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    route = state.route
    if route is None: return False
    round_no = _round(ct)
    backlog_due = state.backlog_rounds >= 3; delivered = _observe_route(ct, state, round_no); backlog_due = backlog_due and not delivered
    reference_round = state.last_delivery_round if state.last_delivery_round is not None else state.delivery_started_round; timeout_due = reference_round is not None and round_no - reference_round >= 12
    broken = find_broken_link(route, _visible_route(state, ct, route), current_round=round_no, last_delivery_round=state.last_delivery_round, route_start_round=state.delivery_started_round, blocked_output=backlog_due or state.backlog_rounds >= 3)
    if broken is None:
        if state.last_delivery_round is not None or state.state == BuilderState.MAINTAIN: state.state = BuilderState.MAINTAIN
        return False
    state.repair_index, target, expected = broken, route.cells[broken], route.directions[broken]
    entity_id, entity_type, direction = _visible(ct, target)
    try: friendly = entity_id is not None and ct.get_team(entity_id) == ct.get_team()
    except Exception: friendly = False
    if entity_type is not None and (entity_type != EntityType.CONVEYOR or direction != expected):
        if _pos(ct).distance_squared(target) == 1: return actions.destroy(target) if friendly and teardown_allowed(verified_misdirected=True) else False
        return _move(ct, state, target, actions, adjacent=True)
    if (backlog_due or timeout_due) and entity_type == EntityType.CONVEYOR and direction == expected:
        if _pos(ct).distance_squared(target) == 1: return actions.destroy(target) if friendly and teardown_allowed(verified_obsolete=True) else False
        return _move(ct, state, target, actions, adjacent=True)
    if _pos(ct).distance_squared(target) == 1:
        try:
            if not _can_spend(ct, int(ct.get_conveyor_cost()), projected_output=2.5, allow_late_completion=True, state=state): return False
        except Exception: return False
        if actions.build_conveyor(target, expected) is not None: state.built_links[target], state.repair_index, state.state = (EntityType.CONVEYOR, expected), None, BuilderState.DELIVER; state.delivery_started_round, state.backlog_rounds = round_no, 0; return True
        return False
    return _move(ct, state, target, actions, adjacent=True)


def _core_exit_tiles(world: WorldMemory) -> frozenset[Position]:
    footprint = set(world.core_footprint); exits: set[Position] = set()
    for cell in sorted(footprint, key=lambda pos: (pos.y, pos.x)):
        for direction in CARDINALS:
            position = cell.add(direction)
            if 0 <= position.x < world.width and 0 <= position.y < world.height and position not in footprint: exits.add(position)
    return frozenset(exits)


def _legal_escape_tiles(ct: object, current: Position) -> frozenset[Position]:
    escapes: set[Position] = set()
    for direction in CARDINALS:
        try:
            if ct.can_move(direction): escapes.add(current.add(direction))
        except Exception: continue
    return frozenset(escapes)


def _exposed_route_join(world: WorldMemory, route: RoutePlan, threat: object | None) -> Position | None:
    route_cells = set(route.cells)
    for cell in route.cells:
        if threat is not None:
            try:
                if cell.distance_squared(threat.position) <= 4: return cell
            except Exception: pass
        for direction in CARDINALS:
            neighbour = cell.add(direction)
            if neighbour in world.static_walls or ((neighbour.x == 0 or neighbour.y == 0 or neighbour.x == world.width - 1 or neighbour.y == world.height - 1) and neighbour not in route_cells):
                return cell
    return None


def _bounded_disjoint_branch(ct: object, world: WorldMemory, route: RoutePlan, start: Position, join: Position) -> tuple[Position, ...]:
    route_cells = set(route.cells); blocked = set(world.core_footprint) | set(world.static_walls) | (route_cells - {join}); blocked.update(position for position in world.dynamic if world.is_blocked(position) and position != join)
    try:
        branch = bounded_bfs(start, join, world.width, world.height, blocked, max_expansions=world.width * world.height, cpu_check=ct.get_cpu_time_elapsed)
    except Exception: return ()
    if len(branch) < 2 or len(branch) - 1 > 12 or branch[-1] != join: return ()
    return tuple(branch) if set(branch[:-1]).isdisjoint(route_cells) else ()


def _build_redundancy_branch(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    branch = state.redundancy_branch
    if not branch or state.redundancy_index < 0: return False
    join_index = len(branch) - 1
    if state.redundancy_index + 1 >= join_index: state.redundancy_branch = (); state.redundancy_index = -1; state.redundancy_join = None; return False
    index = state.redundancy_index
    current_target = branch[index + 1]
    expected = branch[index].cardinal_direction_to(current_target)
    if expected == Direction.CENTRE: state.redundancy_branch = (); state.redundancy_index = -1; state.redundancy_join = None; return False
    _, entity_type, direction = _visible(ct, current_target)
    if entity_type == EntityType.CONVEYOR and direction == expected: state.redundancy_index += 1; return True
    if _pos(ct).distance_squared(current_target) != 1: return _move(ct, state, current_target, actions, adjacent=True)
    try: conveyor_cost = int(ct.get_conveyor_cost())
    except Exception: return False
    if not _can_spend(ct, conveyor_cost, projected_output=2.5, allow_late_completion=True, state=state): return False
    if actions.build_conveyor(current_target, expected) is None: return False
    state.built_links[current_target] = (EntityType.CONVEYOR, expected); state.redundancy_index += 1
    if state.redundancy_index + 1 >= join_index: state.redundancy_branch = (); state.redundancy_index = -1; state.redundancy_join = None
    return True


def _defend(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    if not cpu_is_safe(ct): return False
    try:
        current = _pos(ct); positions = tuple(position for position in (current.add(direction) for direction in CARDINALS) if ct.is_tile_empty(position)); threat = next(iter(state.world.threat_list(_round(ct))), None) if state.world else None
        if threat is None: return False
        assessed = assess_threat(position=threat.position, enemy_builder_distance=max(0, int(current.distance_squared(threat.position) ** 0.5)), firing_line=threat.kind == ThreatKind.FIRING_LINE, sabotage=threat.kind == ThreatKind.SABOTAGE, current_round=_round(ct), entity_type=threat.entity_type)
        if assessed is not None: threat = assessed
        attackable_by_type: dict[EntityType, dict[tuple[Position, Direction], int]] = {EntityType.GUNNER: {}, EntityType.SENTINEL: {}}; wall_crossing = False
        for turret_type in (EntityType.GUNNER, EntityType.SENTINEL):
            for position in positions:
                for direction in CARDINALS:
                    if not cpu_is_safe(ct): return False
                    try: tiles = tuple(ct.get_attackable_tiles_from(position, direction, turret_type))[:32]
                    except Exception: tiles = ()
                    legal = 0
                    for target in tiles:
                        try:
                            legal += bool(ct.can_fire_from(position, direction, turret_type, target)); wall_crossing = wall_crossing or ct.get_tile_env(target) == Environment.WALL
                        except Exception: pass
                    attackable_by_type[turret_type][position, direction] = legal
    except Exception: return False
    lane_length = max((max(values.values(), default=0) for values in attackable_by_type.values()), default=0)
    if lane_length <= 0: return False
    turret_type = choose_turret_type(lane_length=lane_length, wall_crossing=wall_crossing, durable_anchor=bool(state.route and len(state.route.cells) >= 8), changing_corridor=not wall_crossing, threat_score=threat.score)
    if max(attackable_by_type[turret_type].values(), default=0) <= 0:
        available = tuple(candidate for candidate in (EntityType.SENTINEL, EntityType.GUNNER) if max(attackable_by_type[candidate].values(), default=0) > 0)
        if not available: return False
        turret_type = max(available, key=lambda candidate: (max(attackable_by_type[candidate].values(), default=0), int(candidate == EntityType.SENTINEL)))
    world = state.world
    escape_tiles = _legal_escape_tiles(ct, current)
    if len(escape_tiles) > 1: escape_tiles = frozenset()
    choice = choose_defensive_build(positions, threat=threat, lane_length=lane_length, wall_crossing=wall_crossing if turret_type == EntityType.SENTINEL else False, changing_corridor=turret_type == EntityType.GUNNER, durable_anchor=(bool(state.route and len(state.route.cells) >= 8) if turret_type == EntityType.SENTINEL else False), reserved_core_exits=_core_exit_tiles(world) if world else frozenset(), route_cells=set(state.route.cells) if state.route else frozenset(), escape_tiles=escape_tiles, attackable=attackable_by_type[turret_type])
    if choice is None: return False
    position, entity_type, direction, _ = choice
    if entity_type != turret_type or attackable_by_type[entity_type].get((position, direction), 0) <= 0: return False
    try:
        cost = ct.get_sentinel_cost() if entity_type == EntityType.SENTINEL else ct.get_gunner_cost()
    except Exception: return False
    immediate_loss = threat.position.distance_squared(current) <= 4 and _round(ct) >= 850
    if not _can_spend(ct, cost, preserve_defense=True, emergency=immediate_loss, projected_output=threat.score, state=state, new_project=True): return False
    return (actions.build_sentinel(position, direction) if entity_type == EntityType.SENTINEL else actions.build_gunner(position, direction)) is not None


def _support_build(ct: object, state: BuilderStateData, actions: TurnActions, round_no: int) -> bool:
    world, route = state.world, state.route
    if world is None or not cpu_is_safe(ct): return False
    try:
        current = _pos(ct); positions = tuple(position for position in (current.add(direction) for direction in CARDINALS) if ct.is_tile_empty(position))
    except Exception: return False
    if _build_redundancy_branch(ct, state, actions): return True
    reserved = set(world.core_footprint) | _core_exit_tiles(world) | (set(route.cells) if route else set()); choices = tuple(position for position in positions if position not in reserved)
    if not choices: return False
    threat = next(iter(world.threat_list(round_no)), None)
    if state.role == Role.REPAIR and route is not None and state.route_index < 0 and _verified(state, ct):
        try:
            splitter_cost, conveyor_cost = int(ct.get_splitter_cost()), int(ct.get_conveyor_cost())
        except Exception: return False
        mature, join = state.last_delivery_round is not None or state.state == BuilderState.MAINTAIN, _exposed_route_join(world, route, threat)
        if mature and join is not None:
            for target in sorted(choices, key=lambda position: (position.y, position.x)):
                if not cpu_is_safe(ct): break
                branch = _bounded_disjoint_branch(ct, world, route, target, join)
                if not branch: continue
                branch_length = len(branch) - 1; branch_cost = branch_length * max(0, conveyor_cost); avoided_output = max(0.0, (1000 - round_no) * max(1, route.expected_output) * 0.25)
                justified = splitter_redundancy_justified(0.75 if threat is not None else 0.5, avoided_output, splitter_cost, branch_cost, float(branch_length), mature_route=True, exposed_segment=True, disjoint_branch=set(branch[:-1]).isdisjoint(set(route.cells)) and branch[-1] == join, branch_length=branch_length)
                if not justified or not _can_spend(ct, splitter_cost, projected_output=avoided_output, state=state, new_project=True): continue
                direction = branch[0].cardinal_direction_to(branch[1])
                if direction == Direction.CENTRE: continue
                if actions.build_splitter(target, direction) is not None: state.redundancy_branch, state.redundancy_index, state.redundancy_join = branch, 0, join; return True
    if state.role == Role.DEFENDER and threat is not None and threat.position.distance_squared(current) <= 4:
        try:
            barrier_cost = int(ct.get_barrier_cost())
        except Exception: return False
        escape_tiles = _legal_escape_tiles(ct, current)
        if len(escape_tiles) <= 1: return False
        barrier_target = min(choices, key=lambda position: (position.y, position.x))
        if _can_spend(ct, barrier_cost, preserve_defense=True, emergency=round_no >= 850, projected_output=threat.score, state=state, new_project=True): return actions.build_barrier(barrier_target) is not None
    if state.role == Role.SIEGE and round_no < 850 and _fresh_verified_rally(ct, state, world, round_no):
        try:
            launcher_cost = int(ct.get_launcher_cost())
        except Exception: return False
        if _can_spend(ct, launcher_cost, projected_output=2.5, state=state, new_project=True): return actions.build_launcher(min(choices, key=lambda position: (position.y, position.x))) is not None
    return False


def _raid(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    if _round(ct) >= 850: return False
    try:
        own_team, current, targets = ct.get_team(), _pos(ct), []
        for entity_id in tuple(ct.get_nearby_buildings())[:32]:
            if ct.get_team(entity_id) == own_team: continue
            position, entity_type = ct.get_position(entity_id), ct.get_entity_type(entity_id)
            if current.distance_squared(position) == 1: targets.append((position, entity_type, bool(ct.get_stored_resource(entity_id)), 0))
    except Exception: return False
    if not targets: return False
    try:
        budget, resources = compute_budget(ct, route_projects=1), int(ct.get_global_resources())
    except Exception: return False
    economy_reserve = budget.construction + budget.defense + budget.ammo + budget.liquidity
    choice = choose_raid_action(tuple(targets), resources=resources, economy_reserve=economy_reserve, attack_cost=GameConstants.BUILDER_BOT_ATTACK_COST)
    if choice is None: return False
    position, score = choice
    if not _can_spend(ct, GameConstants.BUILDER_BOT_ATTACK_COST, projected_output=score, state=state): return False
    return actions.fire(position)


def _scout(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    if (world := state.world) is None: return False
    target = world.enemy_core or nearest_position(_pos(ct), world.known_ore())
    if target is None: target = (Position(0, 0), Position(max(0, world.width - 1), 0), Position(0, max(0, world.height - 1)))[state.cursor % 3]
    return _move(ct, state, target, actions)


def run_builder(ct: object, state: BuilderStateData | None = None) -> BuilderStateData:
    state = state or BuilderStateData()
    world, round_no = _world(ct, state), _round(ct)
    if state.role == Role.SCOUT and state.last_position is None: state.role = assign_role(_id(ct))
    _read_rally(ct, state)
    if state.rally_target is not None and not _fresh_verified_rally(ct, state, world, round_no): state.rally_target, state.rally_expires_epoch = None, 0
    target = _claim(ct, state, world, round_no)
    _publish_rally(ct, state, world, round_no)
    try:
        resources = int(ct.get_global_resources()); harvester_count = sum(1 for entity_id in tuple(ct.get_nearby_buildings())[:64] if ct.get_entity_type(entity_id) == EntityType.HARVESTER)
    except Exception: resources, harvester_count = 0, 0
    priorities = late_game_policy(round_no, delivery_due=state.state in (BuilderState.DELIVER, BuilderState.VERIFY), route_repair_due=state.repair_index is not None or state.backlog_rounds >= 3, harvester_payback_positive=target is not None, stored_titanium=resources, collected_titanium=state.last_delivery_round or 0, harvester_count=harvester_count)
    actions = TurnActions(ct)
    if target is not None:
        if state.route is not None and state.blocked_steps >= 3: _reset_route_search(state)
        if state.route is None:
            if round_no < 850 or state.route_search is not None: state.state = next_harvester_state(state.state); _route(ct, state, target, round_no)
        if state.route is not None and state.route_index >= 0:
            state.state = BuilderState.ROUTE; _build_route(ct, state, actions)
        elif state.route is not None:
            if _repair(ct, state, actions): state.last_position = _pos(ct); return state
            _harvester(ct, state, actions)
        state.last_position = _pos(ct); return state
    if state.route is not None and state.route_index < 0:
        if _repair(ct, state, actions): state.last_position = _pos(ct); return state
        if state.state in (BuilderState.DELIVER, BuilderState.VERIFY) and _harvester(ct, state, actions): state.last_position = _pos(ct); return state
    if state.role == Role.DEFENDER and round_no >= 240 and (round_no < 850 or "defense" in priorities):
        threats = world.threat_list(round_no); close_threat = bool(threats and threats[0].position.distance_squared(_pos(ct)) <= 4)
        if close_threat and _support_build(ct, state, actions, round_no): state.last_position = _pos(ct); return state
        if _defend(ct, state, actions): state.last_position = _pos(ct); return state
    if _support_build(ct, state, actions, round_no): state.last_position = _pos(ct); return state
    if state.role in (Role.RAIDER, Role.SIEGE) and "no_paid_attack" not in priorities and _raid(ct, state, actions): state.last_position = _pos(ct); return state
    _scout(ct, state, actions); state.last_position = _pos(ct); return state

```

### `bots/candidate/bot/comms.py`

```python
from __future__ import annotations

from enum import IntEnum
from fcode import Position
from .types import Budget, Claim, Opening, Phase, Threat, ThreatKind


class Slot(IntEnum):
    SCHEMA_VERSION = 0; STRATEGY = 1; PRIMARY_ORE = 2; ENEMY_CORE = 3; THREAT = 4; LOGISTICS = 5; DESIRED_BUILDERS = 6; AMMO_TARGET = 7; DEFENSE_ALERT = 8; RALLY = 9; CLAIM_0 = 10; CLAIM_1 = 11; CLAIM_2 = 12; BUDGET = 13; RESERVED = 14; EPOCH = 15


SCHEMA_VERSION = 2; UNKNOWN = 0; COORD_BITS = 10; EPOCH_BITS = 6; OWNER_BITS = 16; COORD_MASK = 1023; EPOCH_MASK = 63; OWNER_MASK = 65535; MAX_U32 = 0xFFFFFFFF
CORE_SLOTS = frozenset({Slot.SCHEMA_VERSION, Slot.STRATEGY, Slot.DESIRED_BUILDERS, Slot.AMMO_TARGET, Slot.EPOCH})
CLAIM_OWNER_SLOTS = {0: frozenset({Slot.PRIMARY_ORE, Slot.ENEMY_CORE, Slot.RALLY, Slot.CLAIM_0}), 1: frozenset({Slot.LOGISTICS, Slot.CLAIM_1, Slot.DEFENSE_ALERT}), 2: frozenset({Slot.THREAT, Slot.BUDGET, Slot.CLAIM_2})}
SLOT_OWNER = {slot: "core" for slot in CORE_SLOTS}
for _owner, _slots in CLAIM_OWNER_SLOTS.items():
    for _slot in _slots: SLOT_OWNER[_slot] = _owner
SLOT_OWNER[Slot.RESERVED] = None


def _valid(pos: Position, width: int, height: int | None = None) -> bool:
    return width > 0 and pos.x >= 0 and pos.y >= 0 and pos.x < width and (height is None or pos.y < height)


def pack_position(pos: Position, width: int, height: int | None = None) -> int:
    if not _valid(pos, width, height): raise ValueError("position outside map")
    value = 1 + pos.y * width + pos.x
    if value > COORD_MASK: raise ValueError("position does not fit ten-bit coordinate")
    return value


def unpack_position(value: int, width: int, height: int | None = None) -> Position | None:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= COORD_MASK or width <= 0: return None
    position = Position((value - 1) % width, (value - 1) // width)
    return position if _valid(position, width, height) else None


def pack_epoch(epoch: int) -> int:
    if isinstance(epoch, bool) or not isinstance(epoch, int): raise ValueError("epoch must be an integer")
    return epoch & EPOCH_MASK


def epoch_distance(now: int, then: int) -> int: return (int(now) - int(then)) & EPOCH_MASK
def claim_is_fresh(claim: Claim | None, now_epoch: int) -> bool: return claim is not None and claim.owner_id > 0 and epoch_distance(now_epoch, claim.epoch) <= 31


def pack_claim(position: Position | None, width: int, epoch: int, owner_id: int, height: int | None = None) -> int:
    if isinstance(owner_id, bool) or not isinstance(owner_id, int) or not 0 <= owner_id <= OWNER_MASK: raise ValueError("owner id does not fit codec")
    coordinate = 0 if position is None else pack_position(position, width, height)
    return (coordinate << 22) | (pack_epoch(epoch) << 16) | owner_id


def unpack_claim(value: int, width: int, height: int | None = None) -> Claim | None:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 < value <= MAX_U32: return None
    coordinate, epoch, owner = (value >> 22) & COORD_MASK, (value >> 16) & EPOCH_MASK, value & OWNER_MASK
    if owner == 0: return None
    position = None if coordinate == 0 else unpack_position(coordinate, width, height)
    return None if coordinate and position is None else Claim(position, epoch, owner)


def claim_slot(owner_index: int) -> Slot:
    if owner_index not in (0, 1, 2): raise ValueError("claim owner must be 0, 1, or 2")
    return Slot.CLAIM_0 + owner_index


def slot_owner(slot: int | Slot) -> str | int | None:
    try: return SLOT_OWNER.get(Slot(slot))
    except (TypeError, ValueError): return None


def can_write(slot: int | Slot, writer: str | int) -> bool: return (owner := slot_owner(slot)) is not None and owner == writer


def encode_strategy(phase: Phase, opening: Opening) -> int: return tuple(Phase).index(phase) | (tuple(Opening).index(opening) << 4)


def decode_strategy(value: int) -> tuple[Phase, Opening] | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0: return None
    try: return tuple(Phase)[value & 15], tuple(Opening)[(value >> 4) & 15]
    except IndexError: return None


def encode_threat(threat: Threat, width: int, height: int | None = None) -> int: return pack_position(threat.position, width, height) | (tuple(ThreatKind).index(threat.kind) << 10)


def decode_threat(value: int, width: int, height: int | None = None) -> Threat | None:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 < value <= MAX_U32: return None
    position, kind = unpack_position(value & COORD_MASK, width, height), (value >> 10) & 15
    return None if position is None or kind >= len(tuple(ThreatKind)) else Threat(position, tuple(ThreatKind)[kind])


def encode_budget(budget: Budget) -> int:
    encoded = 0
    for index, value in enumerate((budget.construction, budget.defense, budget.ammo, budget.expansion, budget.liquidity)): encoded |= max(0, min(63, int(value // 10))) << index * 6
    return encoded


def decode_budget(value: int) -> Budget | None:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= MAX_U32: return None
    return Budget(*(((value >> index * 6) & 63) * 10 for index in range(5)))


def encode_alert(position: Position | None, width: int, expires_epoch: int = 0) -> int: return (0 if position is None else pack_position(position, width)) | ((expires_epoch & EPOCH_MASK) << 10)


def decode_alert(value: int, width: int, height: int | None = None) -> tuple[Position | None, int] | None:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= MAX_U32: return None
    coordinate, position = value & COORD_MASK, None
    if coordinate: position = unpack_position(coordinate, width, height)
    return None if coordinate and position is None else (position, (value >> 10) & EPOCH_MASK)


```

### `bots/candidate/bot/core.py`

```python

from __future__ import annotations

from dataclasses import dataclass, field

from fcode import Direction, EntityType, Environment, GameConstants, Position

from .actions import TurnActions
from .comms import Slot, claim_is_fresh, encode_strategy, pack_claim, unpack_claim
from .policy import choose_opening, describe_opening, choose_phase
from .types import Budget, Opening, Phase


@dataclass(slots=True)
class CoreState:
    opening: Opening = Opening.BALANCED_ECONOMY; phase: Phase = Phase.OPENING
    spawned_ids: list[int] = field(default_factory=list); claim_owners: dict[int, int] = field(default_factory=dict)
    claim_initialized: bool = False; schema_written: bool = False; last_budget: Budget = field(default_factory=Budget)
    spawn_cursor: int = 0; near_term_core_kill: bool = False; opening_observed_round: int | None = None


def _get(ct: object, name: str, default: int = 0) -> int:
    try:
        return int(getattr(ct, name)())
    except (AttributeError, TypeError, ValueError): return default


def _cost(ct: object, name: str, default: int) -> int:
    return max(0, _get(ct, name, default))


def _cpu_safe(ct: object) -> bool:
    try:
        return int(ct.get_cpu_time_elapsed()) < 7000
    except Exception: return False


def compute_budget(ct: object, *, route_projects: int = 0) -> Budget:
    resources = _get(ct, "get_global_resources", 0); builder = _cost(ct, "get_builder_bot_cost", GameConstants.BUILDER_BOT_BASE_COST); harvester = _cost(ct, "get_harvester_cost", GameConstants.HARVESTER_BASE_COST); conveyor = _cost(ct, "get_conveyor_cost", GameConstants.CONVEYOR_BASE_COST); gunner = _cost(ct, "get_gunner_cost", GameConstants.GUNNER_BASE_COST); sentinel = _cost(ct, "get_sentinel_cost", GameConstants.SENTINEL_BASE_COST)
    construction = harvester + 4 * conveyor + max(0, int(route_projects)) * conveyor; defense = min(max(0, resources // 5), max(gunner, sentinel)); liquidity = max(builder, harvester, 20); ammo = max(0, min(resources // 8, 2 * GameConstants.GUNNER_AMMO_COST + GameConstants.SENTINEL_AMMO_COST)); expansion = max(0, resources - construction - defense - liquidity - ammo)
    return Budget(construction, defense, ammo, expansion, liquidity)


def _visible_counts(ct: object) -> tuple[int, int]:
    gunner = sentinel = 0
    try:
        ids = tuple(ct.get_nearby_buildings())
    except Exception: ids = ()
    for entity_id in ids:
        try: entity_type = ct.get_entity_type(entity_id)
        except Exception: continue
        gunner += entity_type == EntityType.GUNNER; sentinel += entity_type == EntityType.SENTINEL
    return gunner, sentinel


def desired_ammo(ct: object, *, horizon_rounds: int = 6, emergency_buffer: int = 0) -> int:
    gunner_count, sentinel_count = _visible_counts(ct)
    gunner_shots = max(0, int(horizon_rounds) // max(1, GameConstants.GUNNER_FIRE_COOLDOWN)); sentinel_shots = max(0, int(horizon_rounds) // max(1, GameConstants.SENTINEL_FIRE_COOLDOWN))
    return gunner_count * gunner_shots * GameConstants.GUNNER_AMMO_COST + sentinel_count * sentinel_shots * GameConstants.SENTINEL_AMMO_COST + max(0, int(emergency_buffer))


def _write_store(ct: object, slot: Slot, value: int) -> None:
    try:
        ct.write_store(int(slot), max(0, min(0xFFFFFFFF, int(value))))
    except Exception: pass


def _spawn_positions(ct: object) -> tuple[Position, ...]:
    try:
        positions = tuple(ct.get_nearby_tiles(dist_sq=GameConstants.CORE_SPAWNING_RADIUS_SQ))
    except Exception: return ()
    return tuple(sorted(positions, key=lambda pos: (pos.y, pos.x)))


def _observed_opening(ct: object):
    width = _get(ct, "get_map_width", 1)
    height = _get(ct, "get_map_height", 1)
    try:
        origin = ct.get_position()
        tiles = tuple(ct.get_nearby_tiles())[: max(1, width * height)]
    except Exception: origin, tiles = Position(0, 0), ()
    walls: set[Position] = set(); ore: list[Position] = []; passable: set[Position] = set()
    for tile in tiles:
        if not _cpu_safe(ct): break
        try:
            environment = ct.get_tile_env(tile); walls.update((tile,) if environment == Environment.WALL else ()); ore.extend((tile,) if environment == Environment.ORE_TITANIUM else ()); passable.update((tile,) if ct.is_tile_passable(tile) else ())
        except Exception: continue
    low_degree = exposed = 0
    for tile in tuple(sorted(passable, key=lambda pos: (pos.y, pos.x))):
        if not _cpu_safe(ct): break
        neighbours = tuple(tile.add(direction) for direction in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST))
        degree = sum(neighbour in passable for neighbour in neighbours); low_degree += degree <= 1; exposed += any(neighbour in walls for neighbour in neighbours)
    enemy_distance = 999
    try:
        own_team = ct.get_team()
        for entity_id in tuple(ct.get_nearby_buildings())[: max(64, width * height)]:
            if not _cpu_safe(ct): break
            if ct.get_entity_type(entity_id) == EntityType.CORE and ct.get_team(entity_id) != own_team:
                position = ct.get_position(entity_id); enemy_distance = min(enemy_distance, abs(position.x - origin.x) + abs(position.y - origin.y))
    except Exception: pass
    return describe_opening(width, height, nearby_ore_count=len(ore), nearest_ore_distance=min((abs(position.x - origin.x) + abs(position.y - origin.y) for position in ore), default=999), wall_density=len(walls) / max(1, len(tiles)), low_degree_passable_tiles=low_degree, route_exposure=exposed / max(1, len(passable)), estimated_enemy_distance=enemy_distance)


def _synchronize_claim_owners(ct: object, state: CoreState, width: int, height: int, round_no: int) -> None:
    for index in range(3):
        try:
            claim = unpack_claim(ct.read_store(int(Slot.CLAIM_0 + index)), width, height)
        except Exception: claim = None
        owner = state.claim_owners.get(index)
        if claim is not None and claim_is_fresh(claim, round_no & 63):
            if owner != claim.owner_id: state.claim_owners[index] = claim.owner_id
            continue
        if owner is not None: state.claim_owners.pop(index, None)


def run_core(ct: object, state: CoreState | None = None, actions: TurnActions | None = None) -> CoreState:
    state = state or CoreState(); turn = actions or TurnActions(ct); round_no = _get(ct, "get_current_round", 0)
    width = _get(ct, "get_map_width", 1); height = _get(ct, "get_map_height", 1); resources = _get(ct, "get_global_resources", 0)
    budget = compute_budget(ct, route_projects=0)
    state.last_budget = budget; _synchronize_claim_owners(ct, state, width, height, round_no)
    if not state.schema_written:
        _write_store(ct, Slot.SCHEMA_VERSION, 2); state.schema_written = True
    descriptor = _observed_opening(ct)
    state.opening = choose_opening(descriptor); state.phase = choose_phase(round_no, opening=state.opening, verified_enemy_core=descriptor.estimated_enemy_distance < 999, economy_ready=resources >= budget.construction + budget.liquidity)
    _write_store(ct, Slot.STRATEGY, encode_strategy(state.phase, state.opening)); _write_store(ct, Slot.AMMO_TARGET, desired_ammo(ct, emergency_buffer=0)); _write_store(ct, Slot.EPOCH, round_no & 63)
    state.opening_observed_round = round_no

    desired_builders = {Opening.COMPACT_PRESSURE: 3, Opening.ANTI_RUSH: 4, Opening.CHOKEPOINT_CONTROL: 4, Opening.WIDE_EXPANSION: 5, Opening.BALANCED_ECONOMY: 4}.get(state.opening, 4)
    _write_store(ct, Slot.DESIRED_BUILDERS, desired_builders)
    unit_count = _get(ct, "get_unit_count", desired_builders + 1)
    builder_cost = _cost(ct, "get_builder_bot_cost", GameConstants.BUILDER_BOT_BASE_COST)
    if unit_count < desired_builders + 1 and resources >= builder_cost + budget.liquidity and not turn.acted:
        positions = _spawn_positions(ct)
        if positions:
            start = state.spawn_cursor % len(positions); ordered = positions[start:] + positions[:start]
            for position in ordered:
                builder_id = turn.spawn(position)
                if builder_id is not None:
                    state.spawn_cursor = (start + 1) % len(positions); state.spawned_ids.append(int(builder_id))
                    owner_index = next((candidate for candidate in range(3) if candidate not in state.claim_owners), None)
                    if owner_index is not None:
                        state.claim_owners[owner_index] = int(builder_id)
                        try:
                            _write_store(ct, Slot.CLAIM_0 + owner_index, pack_claim(None, width, round_no, int(builder_id), height))
                        except ValueError: pass
                    break

    if not state.claim_initialized and len(state.claim_owners) >= 3: state.claim_initialized = True

    current_ammo = _get(ct, "get_global_ammo", 0); target_ammo = desired_ammo(ct, emergency_buffer=0); deficit = max(0, target_ammo - current_ammo); current_resources = _get(ct, "get_global_resources", 0); current_budget = compute_budget(ct, route_projects=0)
    if round_no < 850 and deficit and state.phase != Phase.OPENING:
        amount = min(deficit, max(0, current_resources - current_budget.construction - current_budget.defense - current_budget.liquidity))
        if amount and not turn.acted:
            turn.convert_ammo(amount)
    return state

```

### `bots/candidate/bot/defense.py`

```python

from __future__ import annotations

from fcode import Direction, EntityType, Position

from .types import Threat, ThreatKind


def assess_threat(
    *,
    position: Position = Position(0, 0),
    enemy_builder_distance: int = 999,
    firing_line: bool = False,
    sabotage: bool = False,
    core_hp_delta: int = 0,
    alert_age: int = 0,
    current_round: int = 0,
    entity_type: EntityType | None = None,
) -> Threat | None:
    scores = [
        max(0, 12 - max(0, int(enemy_builder_distance))),
        5 if firing_line else 0,
        4 if sabotage else 0,
        max(0, -int(core_hp_delta) // 2),
        max(0, 3 - int(alert_age) // 4),
    ]
    score = sum(scores)
    if score <= 0:
        return None
    kind = (
        ThreatKind.BUILDER_RUSH
        if enemy_builder_distance < 8
        else ThreatKind.FIRING_LINE
        if firing_line
        else ThreatKind.SABOTAGE
        if sabotage
        else ThreatKind.CORE_DAMAGE
    )
    return Threat(position, kind, score, int(current_round), int(current_round) + 3, entity_type)


def score_defense_placement(
    position: Position,
    turret_type: EntityType,
    *,
    threat: Threat | None = None,
    attackable_count: int = 0,
    reserved_core_exits: set[Position] | frozenset[Position] = frozenset(),
    route_cells: set[Position] | frozenset[Position] = frozenset(),
    escape_tiles: set[Position] | frozenset[Position] = frozenset(),
) -> int:
    if position in reserved_core_exits or position in route_cells or position in escape_tiles:
        return -10_000
    score = max(0, int(attackable_count)) * 3
    if turret_type == EntityType.SENTINEL:
        score += 4
    elif turret_type == EntityType.GUNNER:
        score += 2
    if threat is not None:
        score += threat.score
        score -= position.distance_squared(threat.position)
    return score


def choose_turret_type(
    *,
    lane_length: int = 0,
    wall_crossing: bool = False,
    durable_anchor: bool = False,
    changing_corridor: bool = False,
    threat_score: int = 0,
) -> EntityType:
    if wall_crossing or durable_anchor or int(lane_length) >= 6:
        return EntityType.SENTINEL
    if changing_corridor or threat_score > 0:
        return EntityType.GUNNER
    return EntityType.GUNNER if int(lane_length) < 6 else EntityType.SENTINEL


def choose_defensive_build(
    positions: list[Position] | tuple[Position, ...],
    *,
    threat: Threat | None = None,
    lane_length: int = 0,
    wall_crossing: bool = False,
    durable_anchor: bool = False,
    changing_corridor: bool = True,
    reserved_core_exits: set[Position] | frozenset[Position] = frozenset(),
    route_cells: set[Position] | frozenset[Position] = frozenset(),
    escape_tiles: set[Position] | frozenset[Position] = frozenset(),
    attackable: dict[tuple[Position, Direction], int] | None = None,
) -> tuple[Position, EntityType, Direction, int] | None:
    turret_type = choose_turret_type(
        lane_length=lane_length,
        wall_crossing=wall_crossing,
        durable_anchor=durable_anchor,
        changing_corridor=changing_corridor,
        threat_score=threat.score if threat else 0,
    )
    candidates: list[tuple[int, Position, Direction]] = []
    for position in sorted(positions, key=lambda pos: (pos.y, pos.x)):
        for direction in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            count = 0 if attackable is None else int(attackable.get((position, direction), 0))
            score = score_defense_placement(
                position,
                turret_type,
                threat=threat,
                attackable_count=count,
                reserved_core_exits=reserved_core_exits,
                route_cells=route_cells,
                escape_tiles=escape_tiles,
            )
            if score > -10_000:
                candidates.append((score, position, direction))
    if not candidates:
        return None
    score, position, direction = max(candidates, key=lambda item: (item[0], -item[1].y, -item[1].x, item[2].value))
    return position, turret_type, direction, score


```

### `bots/candidate/bot/economy.py`

```python

from __future__ import annotations

import math

from fcode import Position

from .types import BuilderState


def score_ore(
    ore: Position,
    *,
    origin: Position | None = None,
    route_cost: int = 0,
    harvester_cost: int = 0,
    expected_output_horizon: int = 0,
    exposure_risk: int = 0,
    congestion_penalty: int = 0,
) -> int:
    distance = 0 if origin is None else abs(ore.x - origin.x) + abs(ore.y - origin.y)
    return (
        int(expected_output_horizon)
        - max(0, int(harvester_cost))
        - max(0, int(route_cost))
        - distance * 2
        - max(0, int(exposure_risk))
        - max(0, int(congestion_penalty))
    )


def estimate_route_cost(
    route_length: int,
    conveyor_cost: int,
    *,
    splitter_count: int = 0,
    splitter_cost: int = 0,
    barrier_count: int = 0,
    barrier_cost: int = 0,
) -> int:
    return (
        max(0, int(route_length)) * max(0, int(conveyor_cost))
        + max(0, int(splitter_count)) * max(0, int(splitter_cost))
        + max(0, int(barrier_count)) * max(0, int(barrier_cost))
    )


def estimate_payback_round(
    total_cost: int,
    *,
    output_per_round: float = 2.5,
    start_round: int = 0,
    horizon: int = 1000,
) -> int | None:
    cost = max(0, int(total_cost))
    if cost == 0:
        return int(start_round)
    if output_per_round <= 0:
        return None
    payback = int(start_round) + math.ceil(cost / float(output_per_round))
    return payback if payback < int(horizon) else None


def expansion_allowed(
    *,
    projected_output: int,
    harvester_cost: int,
    route_cost: int,
    current_harvester_cost: int = 0,
    construction_reserve: int = 0,
    defense_reserve: int = 0,
    ammo_reserve: int = 0,
    liquidity_reserve: int = 0,
    available_resources: int | None = None,
    concurrent_projects: int = 0,
    max_projects: int = 3,
) -> bool:
    if int(concurrent_projects) >= min(3, max(1, int(max_projects))):
        return False
    total_cost = max(0, int(harvester_cost)) + max(0, int(route_cost))
    if int(projected_output) <= total_cost + max(0, int(current_harvester_cost)):
        return False
    reserves = sum(
        max(0, int(value))
        for value in (construction_reserve, defense_reserve, ammo_reserve, liquidity_reserve)
    )
    if available_resources is not None and int(available_resources) < total_cost + reserves:
        return False
    return True


def next_harvester_state(
    state: BuilderState,
    *,
    valid_ore: bool = True,
    claim_owned: bool = True,
    timed_out: bool = False,
    route_verified: bool = False,
    first_delivery_seen: bool = False,
) -> BuilderState:
    if not valid_ore or timed_out or not claim_owned:
        return BuilderState.DISCOVER
    transitions = {
        BuilderState.DISCOVER: BuilderState.CLAIM,
        BuilderState.CLAIM: BuilderState.APPROACH_BUILD_TILE,
        BuilderState.APPROACH_BUILD_TILE: BuilderState.ROUTE,
        BuilderState.ROUTE: BuilderState.BUILD,
        BuilderState.BUILD: BuilderState.VERIFY,
        BuilderState.VERIFY: BuilderState.DELIVER if route_verified else BuilderState.ROUTE,
        BuilderState.DELIVER: BuilderState.MAINTAIN if first_delivery_seen else BuilderState.DELIVER,
        BuilderState.MAINTAIN: BuilderState.MAINTAIN,
    }
    return transitions.get(state, BuilderState.DISCOVER)


def claim_should_release(valid_ore: bool, age: int, timeout: int, ownership_lost: bool) -> bool:
    return not valid_ore or ownership_lost or int(age) >= max(1, int(timeout))


```

### `bots/candidate/bot/logistics.py`

```python

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable, Mapping

from fcode import Direction, EntityType, Position

from .navigation import CARDINALS
from .types import RoutePlan, RouteStatus


def _footprint(core: Position | Iterable[Position]) -> tuple[Position, ...]:
    if isinstance(core, Position): return (core, Position(core.x + 1, core.y), Position(core.x, core.y + 1), Position(core.x + 1, core.y + 1))
    return tuple(core)


def _inside(pos: Position, width: int, height: int) -> bool:
    return 0 <= pos.x < width and 0 <= pos.y < height


def _direction_between(start: Position, end: Position) -> Direction:
    for direction in CARDINALS:
        if start.add(direction) == end: return direction
    return Direction.CENTRE


def directions_for_route(
    cells: Iterable[Position], core_footprint: Position | Iterable[Position]
) -> tuple[Direction, ...]:
    ordered = tuple(cells)
    footprint = set(_footprint(core_footprint))
    if not ordered: return ()
    directions: list[Direction] = []
    for index, cell in enumerate(ordered):
        if index + 1 < len(ordered): direction = _direction_between(cell, ordered[index + 1])
        else: direction = next((candidate for candidate in CARDINALS if cell.add(candidate) in footprint), Direction.CENTRE)
        if direction == Direction.CENTRE: return ()
        directions.append(direction)
    return tuple(directions)


def plan_core_outward_route(
    ore: Position,
    core_footprint: Position | Iterable[Position],
    width: int,
    height: int,
    blocked: Callable[[Position], bool] | set[Position] | frozenset[Position] | None = None,
    *,
    created_round: int = 0,
    cpu_check: Callable[[], int | bool] | None = None,
    obstacle_epoch: int = 0,
    search_state: dict[str, object] | None = None,
    stats: dict[str, int] | None = None,
) -> RoutePlan | None:
    footprint = tuple(sorted((cell for cell in _footprint(core_footprint) if _inside(cell, width, height)), key=lambda pos: (pos.y, pos.x)))
    if not footprint or not _inside(ore, width, height): return None
    blocked_set = set(footprint)

    def is_blocked(pos: Position) -> bool:
        if pos in blocked_set: return True
        if blocked is None: return False
        return pos in blocked if not callable(blocked) else bool(blocked(pos))

    def ordered_adjacent(seeds: Iterable[Position]) -> tuple[Position, ...]:
        seen: set[Position] = set()
        ordered: list[Position] = []
        for seed in seeds:
            for direction in CARDINALS:
                position = seed.add(direction)
                if position in seen or not _inside(position, width, height) or is_blocked(position): continue
                seen.add(position); ordered.append(position)
        return tuple(ordered)

    starts = ordered_adjacent((ore,))
    exits = ordered_adjacent(footprint)
    state = search_state if search_state is not None else {}
    signature = (ore, footprint, int(width), int(height), int(obstacle_epoch))
    if state.get("signature") != signature:
        state.clear(); state.update({"signature": signature, "queue": deque(exits), "parents": {position: None for position in exits}, "starts": frozenset(starts), "blocked": is_blocked, "complete": False, "created_round": int(created_round)})
    if stats is not None:
        stats["expansions"] = stats["stopped_cpu"] = stats["complete"] = 0
    if state.get("complete"):
        return None

    def planning_is_safe() -> bool:
        if cpu_check is None: return True
        try:
            value = cpu_check()
            return value if isinstance(value, bool) else int(value) < 7000
        except Exception: return True

    queue = state["queue"]
    parents = state["parents"]
    starts_set = state["starts"]
    blocked_fn = state["blocked"]
    expansions = int(state.get("expansions", 0))
    while queue and expansions < width * height:
        if cpu_check is not None and not planning_is_safe():
            state["expansions"] = expansions
            if stats is not None: stats["stopped_cpu"] = 1
            return None
        current = queue.popleft()
        expansions += 1
        if stats is not None: stats["expansions"] = int(stats.get("expansions", 0)) + 1
        if current in starts_set:
            cells_reversed = [current]
            while parents[cells_reversed[-1]] is not None: cells_reversed.append(parents[cells_reversed[-1]])
            cells = tuple(cells_reversed)
            directions = directions_for_route(cells, footprint)
            if directions:
                state["complete"] = True
                state["expansions"] = expansions
                if stats is not None:
                    stats["complete"] = 1
                return RoutePlan(
                    ore=ore,
                    cells=cells,
                    directions=directions,
                    core_footprint=footprint,
                    status=RouteStatus.PLANNED,
                    created_round=int(state.get("created_round", created_round)),
                    expected_output=10,
                )
        for direction in CARDINALS:
            neighbour = current.add(direction)
            if not _inside(neighbour, width, height) or neighbour in parents or blocked_fn(neighbour):
                continue
            parents[neighbour] = current
            queue.append(neighbour)
    state["complete"] = True
    state["expansions"] = expansions
    if stats is not None:
        stats["complete"] = 1
    return None


def _visible_at(
    visible: Mapping[Position, object] | Callable[[Position], object], pos: Position
) -> object | None:
    try:
        return visible(pos) if callable(visible) else visible.get(pos)
    except Exception:
        return None


def _entity_and_direction(value: object) -> tuple[EntityType | None, Direction | None]:
    if isinstance(value, tuple) and len(value) >= 2:
        entity, direction = value[0], value[1]
        return entity if isinstance(entity, EntityType) else None, direction if isinstance(direction, Direction) else None
    if isinstance(value, EntityType):
        return value, None
    return None, None


def verify_route(
    route: RoutePlan | Iterable[Position],
    visible: Mapping[Position, object] | Callable[[Position], object],
    core_footprint: Position | Iterable[Position] | None = None,
) -> bool:
    if isinstance(route, RoutePlan):
        cells = route.cells
        directions = route.directions
        footprint = set(route.core_footprint)
    else:
        cells = tuple(route)
        footprint = set(_footprint(core_footprint)) if core_footprint is not None else set()
        directions = directions_for_route(cells, footprint) if footprint else ()
    if not cells or len(cells) != len(directions):
        return False
    for cell, expected_direction, in zip(cells, directions):
        entity, direction = _entity_and_direction(_visible_at(visible, cell))
        if entity != EntityType.CONVEYOR or direction != expected_direction:
            return False
    if footprint and cells[-1].add(directions[-1]) not in footprint:
        return False
    return True


def find_broken_link(
    route: RoutePlan,
    visible: Mapping[Position, object] | Callable[[Position], object],
    *,
    current_round: int | None = None,
    last_delivery_round: int | None = None,
    route_start_round: int | None = None,
    delivery_timeout: int = 12,
    blocked_output: bool = False,
) -> int | None:
    for index, cell in enumerate(route.cells):
        value = _visible_at(visible, cell)
        entity, direction = _entity_and_direction(value)
        if entity != EntityType.CONVEYOR or direction != route.directions[index]:
            return index
    if blocked_output:
        return max(0, len(route.cells) - 1)
    reference_round = last_delivery_round if last_delivery_round is not None else route_start_round
    if current_round is not None and reference_round is not None and int(current_round) - int(reference_round) >= max(1, int(delivery_timeout)):
        return 0
    return None


def repair_priority(
    broken_index: int | None,
    route_length: int,
    *,
    backlog: int = 0,
    non_delivery_rounds: int = 0,
) -> int:
    if broken_index is None and backlog <= 0 and non_delivery_rounds <= 0:
        return 0
    proximity = max(0, int(route_length) - max(0, int(broken_index or 0)))
    return 10 + max(0, int(backlog)) + max(0, int(non_delivery_rounds)) + proximity


def splitter_redundancy_justified(
    probability_of_cut: float,
    remaining_expected_route_output: float,
    splitter_cost: int,
    branch_cost: int,
    estimated_latency_penalty: float,
    *,
    mature_route: bool,
    exposed_segment: bool,
    disjoint_branch: bool,
    branch_length: int,
    max_branch_length: int = 12,
) -> bool:
    if not (mature_route and exposed_segment and disjoint_branch):
        return False
    if int(branch_length) <= 0 or int(branch_length) > int(max_branch_length):
        return False
    avoided = max(0.0, float(probability_of_cut)) * max(0.0, float(remaining_expected_route_output))
    cost = max(0, int(splitter_cost)) + max(0, int(branch_cost)) + max(
        0.0, float(estimated_latency_penalty)
    )
    return avoided > cost


def teardown_allowed(
    *,
    verified_obsolete: bool = False,
    verified_misdirected: bool = False,
    friendly: bool = True,
) -> bool:
    return bool(friendly and (verified_obsolete or verified_misdirected))

```

### `bots/candidate/bot/navigation.py`

```python
from __future__ import annotations

from collections import deque
from typing import Callable, Iterable
from fcode import Direction, Position

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


def _inside(pos: Position, width: int, height: int) -> bool: return 0 <= pos.x < width and 0 <= pos.y < height


def _safe(check: Callable[[], bool] | None) -> bool:
    try: value = check() if check is not None else True; return value if isinstance(value, bool) else int(value) < 7000
    except Exception: return False


def bounded_bfs(start: Position, goal: Position | Iterable[Position], width: int, height: int, blocked: Callable[[Position], bool] | set[Position] | frozenset[Position] | None = None, *, max_expansions: int | None = None, cpu_check: Callable[[], bool] | None = None, stats: dict[str, int] | None = None) -> list[Position]:
    if stats is not None: stats["expansions"] = 0
    width, height = int(width), int(height)
    goals = (goal,) if isinstance(goal, Position) else tuple(goal)
    goals = tuple(sorted({pos for pos in goals if _inside(pos, width, height)}, key=lambda pos: (pos.y, pos.x)))
    if width <= 0 or height <= 0 or not _inside(start, width, height) or not goals: return []
    area = width * height; start_i = start.y * width + start.x; goal_i = {pos.y * width + pos.x for pos in goals}
    blocked_i: set[int] | None = None; blocked_fn: Callable[[Position], bool] | None = None
    if isinstance(blocked, (set, frozenset)): blocked_i = {pos.y * width + pos.x for pos in blocked if _inside(pos, width, height)}
    elif blocked is not None: blocked_fn = blocked
    def is_blocked(index: int, x: int, y: int) -> bool:
        if blocked_i is not None: return index in blocked_i
        if blocked_fn is None: return False
        try: return bool(blocked_fn(Position(x, y)))
        except Exception: return True
    if is_blocked(start_i, start.x, start.y): return []
    if start_i in goal_i: return [start]
    limit = min(area, max(1, area if max_expansions is None else int(max_expansions))); parents = [-2] * area; parents[start_i] = -1; queue = deque((start_i,)); found = -1; expansions = 0
    while queue and expansions < limit:
        if not _safe(cpu_check): break
        current = queue.popleft(); expansions += 1; x, y = current % width, current // width
        for dx, dy, delta in ((0, -1, -width), (1, 0, 1), (0, 1, width), (-1, 0, -1)):
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= width or ny < 0 or ny >= height: continue
            neighbour = current + delta
            if parents[neighbour] != -2 or is_blocked(neighbour, nx, ny): continue
            parents[neighbour] = current
            if neighbour in goal_i: found = neighbour; break
            queue.append(neighbour)
        if found >= 0: break
    if stats is not None: stats["expansions"] = expansions
    if found < 0: return []
    path: list[Position] = []; cursor = found
    while cursor >= 0: path.append(Position(cursor % width, cursor // width)); cursor = parents[cursor]
    path.reverse(); return path


class Navigator:
    __slots__ = ("width", "height", "blocked", "cpu", "history", "active_goal_key", "active_obstacle_epoch", "active_path", "active_index", "replans", "cache_hits")

    def __init__(self, width: int, height: int, blocked=None, *, cpu: Callable[[], int] | None = None, cache_limit: int = 12) -> None:
        self.width, self.height, self.blocked, self.cpu = max(0, int(width)), max(0, int(height)), blocked, cpu; self.history = deque(maxlen=4); self.active_goal_key = None; self.active_obstacle_epoch = None; self.active_path: tuple[Position, ...] = (); self.active_index = 0; self.replans = 0; self.cache_hits = 0

    def _blocked(self, pos: Position) -> bool:
        try: return (pos in self.blocked) if self.blocked is not None and not callable(self.blocked) else bool(self.blocked(pos)) if self.blocked is not None else False
        except Exception: return True

    def invalidate(self) -> None:
        self.active_goal_key = self.active_obstacle_epoch = None; self.active_path = (); self.active_index = 0

    def _locate(self, start: Position) -> int | None:
        if not self.active_path: return None
        if self.active_index < len(self.active_path) and self.active_path[self.active_index] == start: return self.active_index
        return next((index for index in range(self.active_index, len(self.active_path)) if self.active_path[index] == start), None)

    def _fallback(self, start: Position, goals: tuple[Position, ...], can_step: Callable[[Direction], bool] | None, forbidden: frozenset[Position]) -> Direction:
        choices: list[tuple[int, int, Direction]] = []
        for order, direction in enumerate(CARDINALS):
            candidate = start.add(direction)
            if candidate in forbidden or not _inside(candidate, self.width, self.height) or self._blocked(candidate): continue
            try: legal = can_step is None or bool(can_step(direction))
            except Exception: legal = False
            if legal: choices.append((min(abs(candidate.x - goal.x) + abs(candidate.y - goal.y) for goal in goals), order, direction))
        return min(choices, default=(0, 0, Direction.CENTRE))[2]

    def _search(self, start: Position, goals: tuple[Position, ...], key: tuple[object, ...], epoch: int, blocked=None) -> tuple[Position, ...]:
        self.active_goal_key, self.active_obstacle_epoch, self.active_index = key, epoch, 0; self.active_path = tuple(bounded_bfs(start, goals, self.width, self.height, self.blocked if blocked is None else blocked, max_expansions=self.width * self.height, cpu_check=self.cpu if self.cpu is not None else None)) if _safe(self.cpu) else ()
        self.replans += 1; return self.active_path

    def _next(self, start: Position, goals: tuple[Position, ...], key: tuple[object, ...], epoch: int, *, can_step: Callable[[Direction], bool] | None, forbidden: frozenset[Position] = frozenset()) -> Direction:
        if start in goals:
            self.history.clear(); self.history.append(start)
            if (self.active_goal_key, self.active_obstacle_epoch) != (key, int(epoch)): self.active_path, self.active_index = (start,), 0; self.active_goal_key, self.active_obstacle_epoch = key, int(epoch); self.replans += 1
            else: self.active_index = self._locate(start) or self.active_index
            return Direction.CENTRE
        oscillating = len(self.history) == 4 and start in self.history; self.history.append(start); same = (self.active_goal_key, self.active_obstacle_epoch) == (key, int(epoch)); index = self._locate(start) if same else None
        if same and index is not None and self.active_path: self.active_index = index; self.cache_hits += 1
        else: self._search(start, goals, key, int(epoch)) if _safe(self.cpu) and not oscillating else (self.invalidate(), setattr(self, "active_goal_key", key), setattr(self, "active_obstacle_epoch", int(epoch)), setattr(self, "replans", self.replans + 1))
        if self.active_path and self.active_index + 1 < len(self.active_path):
            step = self.active_path[self.active_index + 1]; direction = start.cardinal_direction_to(step)
            try: legal = can_step is None or bool(can_step(direction))
            except Exception: legal = False
            if step not in forbidden and not self._blocked(step) and legal: return direction
            blocked_step, base = step, self.blocked
            def retry(pos: Position) -> bool:
                if pos == blocked_step: return True
                try: return (pos in base) if base is not None and not callable(base) else bool(base(pos)) if base is not None else False
                except Exception: return True
            self._search(start, goals, key, int(epoch), retry) if _safe(self.cpu) else None
            if self.active_path and len(self.active_path) > 1:
                step, direction = self.active_path[1], start.cardinal_direction_to(self.active_path[1])
                try: legal = can_step is None or bool(can_step(direction))
                except Exception: legal = False
                if step not in forbidden and not self._blocked(step) and legal: return direction
        return self._fallback(start, goals, can_step, forbidden)

    def next_direction_to_tile(self, start: Position, target: Position, obstacle_epoch: int = 0, *, can_step: Callable[[Direction], bool] | None = None) -> Direction:
        return self._next(start, (target,), ("tile", target), int(obstacle_epoch), can_step=can_step)

    def next_direction_to_adjacent(self, start: Position, target: Position, obstacle_epoch: int = 0, *, can_step: Callable[[Direction], bool] | None = None) -> Direction:
        goals = tuple(target.add(direction) for direction in CARDINALS if _inside(target.add(direction), self.width, self.height) and not self._blocked(target.add(direction)))
        return self._next(start, goals, ("adjacent", target), int(obstacle_epoch), can_step=can_step, forbidden=frozenset({target}))

    def next_direction(self, start: Position, goal: Position, obstacle_epoch: int = 0, *, can_step: Callable[[Direction], bool] | None = None) -> Direction:
        return self.next_direction_to_tile(start, goal, obstacle_epoch, can_step=can_step)

```

### `bots/candidate/bot/offense.py`

```python

from __future__ import annotations

from fcode import EntityType, Position


def score_sabotage_target(
    entity_type: EntityType,
    *,
    loaded: bool = False,
    distance: int = 0,
    stale: bool = False,
) -> int:
    if stale:
        return -10_000
    priority = {
        EntityType.HARVESTER: 4,
        EntityType.SPLITTER: 3,
        EntityType.CONVEYOR: 2 if loaded else 1,
    }.get(entity_type, 0)
    return priority * 100 - max(0, int(distance))


def choose_rally(
    current: Position,
    *,
    verified_target: Position | None = None,
    enemy_core: Position | None = None,
    target_age: int = 0,
    max_age: int = 24,
) -> Position:
    if verified_target is not None and int(target_age) <= int(max_age):
        return verified_target
    if enemy_core is not None:
        return enemy_core
    return current


def choose_raid_action(
    targets: list[tuple[Position, EntityType, bool, int]] | tuple[tuple[Position, EntityType, bool, int], ...],
    *,
    resources: int,
    economy_reserve: int,
    attack_cost: int,
    stale_after: int = 24,
) -> tuple[Position, int] | None:
    if int(resources) - int(attack_cost) < int(economy_reserve):
        return None
    ranked = []
    for position, entity_type, loaded, age in targets:
        score = score_sabotage_target(entity_type, loaded=loaded, distance=0, stale=int(age) > stale_after)
        if score > 0:
            ranked.append((score, position))
    if not ranked:
        return None
    score, position = max(ranked, key=lambda item: (item[0], -item[1].y, -item[1].x))
    return position, score


def score_ally_insertion(
    before_distance: int,
    after_distance: int,
    *,
    threat_penalty: int = 0,
    route_penalty: int = 0,
) -> int:
    progress = int(before_distance) - int(after_distance)
    return progress - max(0, int(threat_penalty)) - max(0, int(route_penalty))


def score_enemy_ejection(
    destination: Position,
    *,
    own_core: Position,
    logistics: tuple[Position, ...] = (),
    enemy_target: Position | None = None,
) -> int:
    core_distance = destination.distance_squared(own_core)
    logistics_distance = min(
        (destination.distance_squared(position) for position in logistics),
        default=0,
    )
    target_utility = destination.distance_squared(enemy_target) if enemy_target is not None else 0
    return core_distance + logistics_distance + target_utility


def insertion_allowed(score: int) -> bool:
    return int(score) > 0


```

### `bots/candidate/bot/player.py`

```python

from __future__ import annotations

from fcode import Controller, EntityType

from .builder import BuilderStateData, run_builder
from .core import CoreState, run_core
from .turrets import run_gunner, run_launcher, run_sentinel


class Player:
    def __init__(self) -> None:
        self._error_count = 0
        self._safe_mode = False
        self._core_state = CoreState()
        self._builder_state = BuilderStateData()

    def run(self, ct: Controller) -> None:
        if self._safe_mode:
            return
        try:
            self._run(ct)
        except Exception:
            self._error_count += 1
            if self._error_count <= 3:
                try:
                    ct.draw_indicator_dot(ct.get_position(), 255, 0, 0)
                except Exception:
                    pass
            if self._error_count >= 3:
                self._safe_mode = True

    def _run(self, ct: Controller) -> None:
        entity_type = ct.get_entity_type()
        if entity_type == EntityType.CORE:
            self._core_state = run_core(ct, self._core_state)
        elif entity_type == EntityType.BUILDER_BOT:
            self._builder_state = run_builder(ct, self._builder_state)
        elif entity_type == EntityType.GUNNER:
            run_gunner(ct)
        elif entity_type == EntityType.SENTINEL:
            run_sentinel(ct)
        elif entity_type == EntityType.LAUNCHER:
            run_launcher(ct)
        elif entity_type in (
            EntityType.CONVEYOR,
            EntityType.SPLITTER,
            EntityType.HARVESTER,
            EntityType.BARRIER,
        ):
            return


```

### `bots/candidate/bot/policy.py`

```python

from __future__ import annotations

from fcode import Position

from .types import BuilderState, Opening, OpeningDescriptor, Phase, Role


def assign_role(entity_id: int, phase: Phase = Phase.OPENING, opening: Opening | None = None) -> Role:
    value = abs(int(entity_id)) % 8
    if phase == Phase.ENDGAME:
        return Role.RAIDER if value % 2 else Role.REPAIR
    if opening == Opening.ANTI_RUSH and value in (0, 1, 2):
        return Role.DEFENDER if value == 2 else Role.ECONOMY
    return {
        0: Role.ECONOMY,
        1: Role.ECONOMY,
        2: Role.REPAIR,
        3: Role.DEFENDER,
        4: Role.SCOUT,
        5: Role.RAIDER,
        6: Role.SIEGE,
        7: Role.REPAIR,
    }[value]


def describe_opening(
    width: int,
    height: int,
    nearby_ore_count: int = 0,
    nearest_ore_distance: int = 999,
    wall_density: float = 0.0,
    low_degree_passable_tiles: int = 0,
    route_exposure: float = 0.0,
    estimated_enemy_distance: int = 999,
) -> OpeningDescriptor:
    width = max(0, int(width))
    height = max(0, int(height))
    return OpeningDescriptor(
        width=width,
        height=height,
        area=width * height,
        nearby_ore_count=max(0, int(nearby_ore_count)),
        nearest_ore_distance=max(0, int(nearest_ore_distance)),
        wall_density=max(0.0, min(1.0, float(wall_density))),
        low_degree_passable_tiles=max(0, int(low_degree_passable_tiles)),
        route_exposure=max(0.0, min(1.0, float(route_exposure))),
        estimated_enemy_distance=max(0, int(estimated_enemy_distance)),
    )


def choose_opening(descriptor: OpeningDescriptor) -> Opening:
    compact = descriptor.area <= 196
    near_enemy = descriptor.estimated_enemy_distance <= max(5, min(descriptor.width, descriptor.height) // 2)
    chokepoint = descriptor.wall_density >= 0.28 or descriptor.low_degree_passable_tiles >= max(
        4, descriptor.area // 18
    )
    wide = descriptor.area >= 500 or descriptor.width >= 25 or descriptor.height >= 25
    if near_enemy:
        return Opening.ANTI_RUSH
    if chokepoint:
        return Opening.CHOKEPOINT_CONTROL
    if compact:
        return Opening.COMPACT_PRESSURE
    if wide:
        return Opening.WIDE_EXPANSION
    return Opening.BALANCED_ECONOMY


def choose_phase(
    round_no: int,
    *,
    opening: Opening = Opening.BALANCED_ECONOMY,
    threat_score: int = 0,
    verified_enemy_core: bool = False,
    economy_ready: bool = False,
) -> Phase:
    round_no = int(round_no)
    if round_no >= 850:
        return Phase.ENDGAME
    if threat_score >= 5:
        return Phase.DEFENSE
    if verified_enemy_core and economy_ready and round_no >= 250:
        return Phase.OFFENSE
    if round_no < 80 or opening == Opening.ANTI_RUSH and round_no < 120:
        return Phase.OPENING
    return Phase.ECONOMY


def late_game_policy(
    round_no: int,
    *,
    verified_near_term_core_kill: bool = False,
    delivery_due: bool = False,
    route_repair_due: bool = False,
    harvester_payback_positive: bool = False,
    stored_titanium: int = 0,
    collected_titanium: int = 0,
    harvester_count: int = 0,
) -> tuple[str, ...]:
    if int(round_no) < 850:
        return ("delivery", "repair", "harvester", "defense", "combat", "stored_titanium")
    if verified_near_term_core_kill:
        return ("core_kill", "defense", "delivery", "repair", "stored_titanium")
    priorities: list[str] = []
    if delivery_due:
        priorities.append("delivery")
    if route_repair_due:
        priorities.append("repair")
    if harvester_payback_positive:
        priorities.append("harvester")
    priorities.extend(("defense", "collected_titanium", "harvester_count", "stored_titanium"))
    priorities.extend(("no_ammo_conversion", "no_paid_attack"))
    return tuple(dict.fromkeys(priorities))


def state_for_role(role: Role, route_ready: bool = False) -> BuilderState:
    if role == Role.ECONOMY:
        return BuilderState.ROUTE if route_ready else BuilderState.DISCOVER
    if role == Role.REPAIR:
        return BuilderState.MAINTAIN
    return BuilderState.DISCOVER


def nearest_position(origin: Position, positions: tuple[Position, ...] | list[Position]) -> Position | None:
    if not positions:
        return None
    return min(positions, key=lambda pos: (origin.distance_squared(pos), pos.y, pos.x))

```

### `bots/candidate/bot/turrets.py`

```python

from __future__ import annotations

from fcode import Direction, EntityType, Position

from .actions import TurnActions, cpu_is_safe
from .comms import Slot, decode_alert, epoch_distance
from .offense import score_ally_insertion, score_enemy_ejection, score_sabotage_target


CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


def _entity_at(ct: object, target: Position) -> tuple[int | None, EntityType | None]:
    entity_id = None
    try:
        entity_id = ct.get_tile_building_id(target)
    except Exception: pass
    if entity_id is None:
        try:
            entity_id = ct.get_tile_builder_bot_id(target)
        except Exception: pass
    if entity_id is None:
        return None, None
    try: return entity_id, ct.get_entity_type(entity_id)
    except Exception: return entity_id, None


def choose_fire_target(ct: object, targets: list[Position] | tuple[Position, ...] | None = None) -> Position | None:
    if not cpu_is_safe(ct): return None
    if targets is None:
        try:
            targets = tuple(ct.get_attackable_tiles())
        except Exception: return None
    ranked: list[tuple[int, Position]] = []
    for target in tuple(targets)[:64]:
        try:
            legal = bool(ct.can_fire(target))
        except Exception: legal = False
        if not legal: continue
        _, entity_type = _entity_at(ct, target)
        if entity_type is None: continue
        priority = {
            EntityType.CORE: 500,
            EntityType.HARVESTER: 420,
            EntityType.SPLITTER: 320,
            EntityType.CONVEYOR: 220,
            EntityType.BUILDER_BOT: 180,
            EntityType.SENTINEL: 160,
            EntityType.GUNNER: 150,
            EntityType.LAUNCHER: 140,
            EntityType.BARRIER: 80,
        }.get(entity_type, 0)
        priority += score_sabotage_target(entity_type, distance=0) if entity_type in (
            EntityType.HARVESTER,
            EntityType.SPLITTER,
            EntityType.CONVEYOR,
        ) else 0
        if priority > 0: ranked.append((priority, target))
    if not ranked: return None
    return max(ranked, key=lambda item: (item[0], -item[1].y, -item[1].x))[1]


def choose_gunner_rotation(ct: object) -> Direction | None:
    if not cpu_is_safe(ct): return None
    try:
        position = ct.get_position()
    except Exception: return None
    choices: list[tuple[int, Direction]] = []
    for direction in CARDINALS:
        try:
            tiles = tuple(ct.get_attackable_tiles_from(position, direction, EntityType.GUNNER))[:32]
        except Exception: continue
        count = 0
        for target in tiles:
            try:
                if ct.can_fire_from(position, direction, EntityType.GUNNER, target):
                    count += 1
            except Exception: continue
        choices.append((count, direction))
    if not choices: return None
    return max(choices, key=lambda item: (item[0], -CARDINALS.index(item[1])))[1]


def _default_destinations(ct: object, origin: Position) -> tuple[Position, ...]:
    try:
        width = int(ct.get_map_width())
        height = int(ct.get_map_height())
    except Exception: return ()
    destinations: list[Position] = []
    seen: set[Position] = set()
    for radius in range(1, 6):
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy > 26 or (dx == 0 and dy == 0): continue
                position = Position(origin.x + dx, origin.y + dy)
                if position in seen or not (0 <= position.x < width and 0 <= position.y < height): continue
                seen.add(position)
                destinations.append(position)
                if len(destinations) >= 32:
                    return tuple(destinations)
    return tuple(destinations)


def choose_launch(
    ct: object,
    pickup_tiles: list[Position] | tuple[Position, ...] | None = None,
    destinations: list[Position] | tuple[Position, ...] | None = None,
    *,
    enemy_target: Position | None = None,
    own_core: Position | None = None,
    logistics: tuple[Position, ...] = (),
) -> tuple[Position, Position, int] | None:
    if not cpu_is_safe(ct): return None
    try:
        origin = ct.get_position()
    except Exception: return None
    if pickup_tiles is None:
        pickup_tiles = tuple(
            Position(origin.x + dx, origin.y + dy)
            for dy in (-1, 0, 1)
            for dx in (-1, 0, 1)
            if dx or dy
        )
    pickup_tiles = tuple(pickup_tiles)[:8]
    if destinations is None:
        destinations = _default_destinations(ct, origin)
    destinations = tuple(destinations)[:32]
    try:
        own_team = ct.get_team()
    except Exception: own_team = None
    best: tuple[int, Position, Position] | None = None
    for pickup in pickup_tiles:
        if not cpu_is_safe(ct):
            return (best[1], best[2], best[0]) if best and best[0] > 0 else None
        try:
            builder_id = ct.get_tile_builder_bot_id(pickup)
            builder_team = ct.get_team(builder_id) if builder_id is not None else None
        except Exception: builder_id, builder_team = None, None
        if builder_id is None: continue
        for destination in destinations:
            if not cpu_is_safe(ct):
                return (best[1], best[2], best[0]) if best and best[0] > 0 else None
            try:
                if not ct.can_launch(pickup, destination): continue
            except Exception: continue
            if own_team is not None and builder_team == own_team:
                if enemy_target is None: continue
                score = score_ally_insertion(pickup.distance_squared(enemy_target), destination.distance_squared(enemy_target))
            elif own_core is not None and (enemy_target is not None or logistics):
                score = score_enemy_ejection(destination, own_core=own_core, logistics=logistics, enemy_target=enemy_target)
            else:
                continue
            candidate_key = (score, -pickup.y, -pickup.x, -destination.y, -destination.x)
            best_key = None if best is None else (best[0], -best[1].y, -best[1].x, -best[2].y, -best[2].x)
            if best is None or candidate_key > best_key: best = (score, pickup, destination)
    if best is None or best[0] <= 0: return None
    return best[1], best[2], best[0]


def run_gunner(ct: object) -> None:
    actions = TurnActions(ct)
    target = choose_fire_target(ct)
    if target is not None and actions.fire(target): return
    direction = choose_gunner_rotation(ct)
    if direction is not None: actions.rotate(direction)


def run_sentinel(ct: object) -> None:
    actions = TurnActions(ct)
    target = choose_fire_target(ct)
    if target is not None: actions.fire(target)


def _observed_enemy_target(ct: object, target: Position) -> bool:
    try:
        own_team = ct.get_team()
        entity_ids = tuple(ct.get_nearby_entities())[:64]
    except Exception:
        try:
            own_team = ct.get_team()
            entity_ids = tuple(ct.get_nearby_buildings())[:64] + tuple(ct.get_nearby_units())[:64]
        except Exception: return False
    for entity_id in entity_ids:
        if not cpu_is_safe(ct): return False
        try:
            if ct.get_team(entity_id) != own_team and ct.get_position(entity_id) == target: return True
        except Exception: continue
    return False


def _fresh_rally(ct: object) -> Position | None:
    try:
        width, height = int(ct.get_map_width()), int(ct.get_map_height())
        decoded = decode_alert(ct.read_store(int(Slot.RALLY)), width, height)
        round_no = int(ct.get_current_round()) & 63
    except Exception: return None
    if decoded is None: return None
    position, expires_epoch = decoded
    if position is None or epoch_distance(expires_epoch, round_no) > 8: return None
    return position if _observed_enemy_target(ct, position) else None


def _own_core(ct: object) -> Position | None:
    try:
        own_team = ct.get_team()
        positions = []
        for entity_id in tuple(ct.get_nearby_buildings())[:64]:
            if not cpu_is_safe(ct): break
            if ct.get_entity_type(entity_id) == EntityType.CORE and ct.get_team(entity_id) == own_team: positions.append(ct.get_position(entity_id))
    except Exception: return None
    return min(positions, key=lambda position: (position.y, position.x)) if positions else None


def run_launcher(ct: object) -> None:
    rally = _fresh_rally(ct)
    own_core = _own_core(ct)
    logistics: list[Position] = []
    if own_core is not None:
        try:
            own_team = ct.get_team()
            for entity_id in tuple(ct.get_nearby_buildings())[:32]:
                if not cpu_is_safe(ct): break
                if ct.get_team(entity_id) != own_team: continue
                if ct.get_entity_type(entity_id) in (EntityType.CONVEYOR, EntityType.SPLITTER): logistics.append(ct.get_position(entity_id))
        except Exception: logistics = []
    choice = choose_launch(ct, enemy_target=rally, own_core=own_core, logistics=tuple(logistics))
    if choice is None: return
    pickup, destination, _ = choice
    TurnActions(ct).launch(pickup, destination)

```

### `bots/candidate/bot/types.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fcode import Direction, EntityType, Position


class Role(str, Enum):
    ECONOMY = "economy"; REPAIR = "repair"; DEFENDER = "defender"; SCOUT = "scout"; RAIDER = "raider"; SIEGE = "siege"; IDLE = "idle"


class Phase(str, Enum):
    OPENING = "opening"; ECONOMY = "economy"; DEFENSE = "defense"; OFFENSE = "offense"; ENDGAME = "endgame"


class Opening(str, Enum):
    COMPACT_PRESSURE = "compact_pressure"; BALANCED_ECONOMY = "balanced_economy"; WIDE_EXPANSION = "wide_expansion"; CHOKEPOINT_CONTROL = "chokepoint_control"; ANTI_RUSH = "anti_rush"


class BuilderState(str, Enum):
    DISCOVER = "discover"; CLAIM = "claim"; APPROACH_BUILD_TILE = "approach_build_tile"; ROUTE = "route"; BUILD = "build"; VERIFY = "verify"; DELIVER = "deliver"; MAINTAIN = "maintain"


class ThreatKind(str, Enum):
    BUILDER_RUSH = "builder_rush"; FIRING_LINE = "firing_line"; SABOTAGE = "sabotage"; CORE_DAMAGE = "core_damage"; ECONOMY_RUSH = "economy_rush"; UNKNOWN = "unknown"


class RouteStatus(str, Enum):
    PLANNED = "planned"; BUILDING = "building"; VERIFIED = "verified"; BROKEN = "broken"; DELIVERING = "delivering"; MAINTAIN = "maintain"; STALE = "stale"


@dataclass(frozen=True, slots=True)
class Claim:
    position: Position | None; epoch: int; owner_id: int


@dataclass(frozen=True, slots=True)
class Threat:
    position: Position; kind: ThreatKind = ThreatKind.UNKNOWN; score: int = 0; seen_round: int = 0; expires_round: int = 0; entity_type: EntityType | None = None


@dataclass(frozen=True, slots=True)
class Budget:
    construction: int = 0; defense: int = 0; ammo: int = 0; expansion: int = 0; liquidity: int = 0

    @property
    def reserved(self) -> int:
        return sum(max(0, value) for value in (self.construction, self.defense, self.ammo, self.liquidity))


@dataclass(frozen=True, slots=True)
class RoutePlan:
    ore: Position; cells: tuple[Position, ...] = (); directions: tuple[Direction, ...] = (); core_footprint: tuple[Position, ...] = (); status: RouteStatus = RouteStatus.PLANNED; created_round: int = 0; expected_output: int = 0

    @property
    def first_receiver(self) -> Position | None:
        return self.cells[0] if self.cells else None

    @property
    def final_conveyor(self) -> Position | None:
        return self.cells[-1] if self.cells else None


@dataclass(frozen=True, slots=True)
class OpeningDescriptor:
    width: int = 0; height: int = 0; area: int = 0; nearby_ore_count: int = 0; nearest_ore_distance: int = 999; wall_density: float = 0.0; low_degree_passable_tiles: int = 0; route_exposure: float = 0.0; estimated_enemy_distance: int = 999


```

### `bots/candidate/bot/world.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from fcode import EntityType, Environment, Position, Team
from .types import Threat, ThreatKind

PASSABLE_BUILDINGS = frozenset({EntityType.CONVEYOR, EntityType.SPLITTER})


@dataclass(frozen=True, slots=True)
class DynamicObservation:
    entity_type: EntityType; team: Team | None; seen_round: int; blocks: bool


class WorldMemory:
    __slots__ = ("width", "height", "static_walls", "ore_positions", "dynamic", "own_core", "enemy_core", "core_footprint", "threats", "navigation_epoch", "layout_epoch", "goal", "goal_invalidated", "last_round")

    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = max(0, int(width)), max(0, int(height)); self.static_walls=set(); self.ore_positions=set(); self.dynamic={}; self.own_core=None; self.enemy_core=None; self.core_footprint=set(); self.threats={}; self.navigation_epoch=0; self.layout_epoch=0; self.goal=None; self.goal_invalidated=False; self.last_round=0

    def _in_bounds(self, pos: Position) -> bool: return 0 <= pos.x < self.width and 0 <= pos.y < self.height
    def _core_cells(self, anchor: Position) -> set[Position]: return {cell for cell in (anchor, Position(anchor.x+1, anchor.y), Position(anchor.x, anchor.y+1), Position(anchor.x+1, anchor.y+1)) if self._in_bounds(cell)}
    @property
    def obstacle_epoch(self) -> int: return self.navigation_epoch

    def _set_dynamic(self, pos: Position, observation: DynamicObservation) -> None:
        old = self.dynamic.get(pos); self.dynamic[pos] = observation
        self.navigation_epoch += int((old is not None and old.blocks) != observation.blocks); self.layout_epoch += int((old is not None and old.entity_type != EntityType.BUILDER_BOT and old.entity_type not in PASSABLE_BUILDINGS) != (observation.entity_type != EntityType.BUILDER_BOT and observation.entity_type not in PASSABLE_BUILDINGS)); self.goal_invalidated = self.goal_invalidated or (self.goal == pos and observation.blocks)

    def _remove_dynamic(self, pos: Position) -> None:
        old = self.dynamic.pop(pos, None)
        self.navigation_epoch += int(old is not None and old.blocks); self.layout_epoch += int(old is not None and old.entity_type != EntityType.BUILDER_BOT and old.entity_type not in PASSABLE_BUILDINGS); self.goal_invalidated = self.goal_invalidated or (old is not None and self.goal == pos)

    def observe(self, ct: object, round_no: int | None = None) -> None:
        try: current = int(ct.get_current_round() if round_no is None else round_no)
        except Exception: current = self.last_round
        self.last_round = current
        try: tiles = tuple(ct.get_nearby_tiles())
        except Exception: tiles = ()
        try: own_team, own_id = ct.get_team(), int(ct.get_id())
        except Exception: own_team, own_id = None, None
        for pos in tiles:
            if not self._in_bounds(pos): continue
            try: environment = ct.get_tile_env(pos)
            except Exception: continue
            if environment == Environment.WALL:
                if pos not in self.static_walls: self.static_walls.add(pos); self.navigation_epoch += 1; self.layout_epoch += 1
                continue
            if environment == Environment.ORE_TITANIUM: self.ore_positions.add(pos)
            try: building_id, builder_id = ct.get_tile_building_id(pos), ct.get_tile_builder_bot_id(pos)
            except Exception: building_id, builder_id = None, None
            entity_id = building_id if building_id is not None else builder_id
            if entity_id is None or entity_id == own_id: self._remove_dynamic(pos); continue
            try: entity_type = ct.get_entity_type(entity_id); team = ct.get_team(entity_id)
            except Exception: continue
            self._set_dynamic(pos, DynamicObservation(entity_type, team, current, entity_type not in PASSABLE_BUILDINGS))
            if entity_type == EntityType.CORE:
                if team == own_team:
                    before = set(self.core_footprint); self.own_core = min((self.own_core, pos), key=lambda p: (p.y, p.x)) if self.own_core else pos; self.core_footprint.update(self._core_cells(self.own_core))
                    if before != self.core_footprint: self.navigation_epoch += 1; self.layout_epoch += 1
                elif team is not None: self.enemy_core = pos
            elif team is not None and own_team is not None and team != own_team:
                kind = ThreatKind.BUILDER_RUSH if entity_type == EntityType.BUILDER_BOT else ThreatKind.SABOTAGE; self.threats[pos] = Threat(pos, kind, 4 if entity_type == EntityType.BUILDER_BOT else 2, current, current + 3, entity_type)
        self.expire_dynamic(current)
        self.threats = {pos: threat for pos, threat in self.threats.items() if threat.expires_round > current}

    def expire_dynamic(self, current_round: int | None = None) -> None:
        current = self.last_round if current_round is None else int(current_round)
        for pos, observation in tuple(self.dynamic.items()):
            if current - observation.seen_round >= 3: self._remove_dynamic(pos)

    def is_navigation_blocked(self, pos: Position) -> bool:
        observation = self.dynamic.get(pos); return not self._in_bounds(pos) or pos in self.static_walls or pos in self.core_footprint or bool(observation and observation.blocks)

    def is_route_planning_blocked(self, pos: Position) -> bool:
        observation = self.dynamic.get(pos); return not self._in_bounds(pos) or pos in self.static_walls or pos in self.core_footprint or bool(observation and observation.entity_type != EntityType.BUILDER_BOT and observation.entity_type not in PASSABLE_BUILDINGS)

    def classify(self, pos: Position) -> EntityType | Environment | None:
        observation = self.dynamic.get(pos); return Environment.WALL if pos in self.static_walls else observation.entity_type if observation else None
    def is_blocked(self, pos: Position) -> bool: return self.is_navigation_blocked(pos)
    def is_passable(self, pos: Position) -> bool: return not self.is_navigation_blocked(pos)
    def set_goal(self, goal: Position | None) -> None: self.goal, self.goal_invalidated = goal, False
    def consume_goal_invalidation(self) -> bool: result = self.goal_invalidated; self.goal_invalidated = False; return result

    def invalidate_after_throw(self, position: Position | None = None) -> None:
        old = self.dynamic.pop(position, None) if position is not None else None; self.navigation_epoch += 1 + int(old is not None and old.blocks); self.layout_epoch += int(old is not None and old.entity_type != EntityType.BUILDER_BOT and old.entity_type not in PASSABLE_BUILDINGS); self.goal_invalidated = True

    def known_ore(self) -> tuple[Position, ...]: return tuple(sorted(self.ore_positions, key=lambda pos: (pos.y, pos.x)))
    def threat_list(self, current_round: int | None = None) -> tuple[Threat, ...]:
        current = self.last_round if current_round is None else current_round
        return tuple(sorted((threat for threat in self.threats.values() if threat.expires_round > current), key=lambda threat: (-threat.score, threat.position.y, threat.position.x)))

```

### `bots/candidate/main.py`

```python
"""Florent Code League submission entry point.

The platform checks the submission entry point for a class declaration named
``Player`` (rather than only accepting an imported alias), so keep this thin
wrapper here and the implementation in :mod:`bot.player`.
"""

from bot.player import Player as _Player


class Player(_Player):
    """Platform-visible entry point for the candidate bot."""

    pass

__all__ = ["Player"]

```

## Additional detailed sources available in the repository

- `GAME_RULES.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/EVALUATION_PLAN.md`
- `docs/SUBMISSION_AND_VERSIONING.md`
- `docs/LIVE_AUTOPILOT.md`

Generated at 2026-08-05T21:05:55Z.
