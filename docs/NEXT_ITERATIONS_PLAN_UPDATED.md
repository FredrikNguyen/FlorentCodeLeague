# Florent Code League — Next Iterations Plan

**Planning basis:** the v0003 archive, the current rules reference, and the latest `UPDATES.md` through the blocked Iteration 3 repair audit.
**Current truth:** Iterations 0–2 passed; Iteration 3 remains behaviorally blocked despite clean tests and two bounded repairs. Luna must inspect the actual repository and latest reports before editing. Later iterations are detailed here but remain gated on restoring reliable first-route delivery.

---

## Executive diagnosis

The current bot is not a simple Milestone 1–2 candidate. It already contains:

- safe entity dispatch and a platform-visible `Player` subclass;
- action wrappers;
- a versioned 16-slot Store codec;
- per-unit world memory;
- bounded BFS and a `Navigator`;
- Core spawning, opening selection, budget, and ammo logic;
- ore claims, route planning, conveyor construction, Harvester construction, route repair, and redundancy;
- threat scoring and defensive construction;
- raids, rallies, turret targeting, Gunner rotation, and Launcher decisions.

The problem is that this breadth has arrived before the packet records any trustworthy local report, CPU report, first-delivery metric, or live baseline. Several fundamental mechanics also contain likely correctness or efficiency defects. The next work should therefore **stabilize and measure the economy/navigation foundation before adding more strategy**.

### Highest-priority defects found in the archive

1. **The path cache is effectively not reused.** `Navigator.next_direction()` keys cached paths by `(start, goal, obstacle_epoch)`. Since `start` changes after every move, a Builder normally misses the cache and runs another BFS every step.
2. **Builders navigate to build tiles instead of legal build stances.** `_build_route()` and `_harvester()` call `_move(..., target)` even though construction requires an orthogonally adjacent position. A Builder can step onto the intended build tile, then require several fallback turns to leave it.
3. **Route planning depends on transient unit occupancy.** `WorldMemory.obstacle_epoch` changes when visible Builders move, and route planning uses `world.is_blocked`. Incremental route searches can restart because of temporary friendly traffic.
4. **`TurnActions.destroy()` incorrectly consumes the local action.** Official rules say friendly destruction does not use action cooldown and may be repeated in one round. The wrapper sets `acted = True`.
5. **The Store schema names do not match their actual use.** `PRIMARY_ORE`, `LOGISTICS`, and `THREAT` are currently used as project counters/heartbeats. Claim slots are written by both the Core and Builders. This makes ownership and one-round-lag behavior difficult to reason about.
6. **Initial route construction cannot resolve an occupied wrong-direction cell.** A mismatched Conveyor or other building can make `_build_route()` repeatedly fail without a clean destroy/replan transition.
7. **Delivery detection is ambiguous.** Global titanium increases may come from another Harvester or passive income, while spending can hide a real delivery. A route can be marked healthy or broken for the wrong reason.
8. **Core ammunition demand only counts nearby visible turrets.** Turrets outside Core vision may never be included in `desired_ammo()`.
9. **Ammo conversion is unnecessarily blocked after spawning.** Conversion does not consume the Core action cooldown, but `run_core()` requires `not turn.acted`.
10. **Gunner rotation can spend 10 Ti without a positive target improvement.** When all directions score zero, the current tie-break selects a direction anyway.
11. **Combat target scoring can prefer a Harvester over the enemy Core.** The Harvester receives both a base priority and a sabotage bonus.
12. **The advanced systems are insufficiently isolated.** Defense, redundancy, raids, Launcher behavior, map-opening policy, and late-game policy can all affect results before basic delivery has been proven.

---

# Iteration 0 — Reconcile the real source and establish a measured baseline

## Objective

Make the repository, planning state, tests, and baseline refer to the actual v0003 source, then record deterministic evidence without changing bot behavior.

## Scope

- Repository state files and planning bundle generation.
- Existing test fixtures/harness.
- `bots/candidate/` only if it does not already match the uploaded v0003 archive.
- `bots/baseline/` only through an explicit immutable snapshot of v0003.
- No strategy changes.

## Required implementation steps

1. Compare every file in the uploaded archive with `bots/candidate/`.
2. If they differ, preserve the current repository candidate as an immutable version, then replace `bots/candidate/` with the intended v0003 source.
3. Update:
   - `state/project_state.json`;
   - `docs/START_HERE.md`;
   - `UPDATES.md`;
   - the generated ChatGPT planning packet.
4. Record the archive hash, source version name, Git SHA, and candidate file hashes.
5. Add or confirm tests for:
   - importing `main.py`;
   - `main.py` containing a class declaration named `Player`;
   - all bot files compiling;
   - package size/file-count limits;
   - no forbidden native extensions.
6. Add a reusable fake `fcode` module/Controller fixture for pure unit tests. Do not duplicate one if the repository already has it.
7. Run the current candidate unchanged:
   - static tests;
   - four-game smoke;
   - one small regression subset.
8. Save full logs/replays under one report directory and write only the summary into `UPDATES.md`.

## Commands

```bash
git status --short
make static
make smoke
python scripts/run_local_matrix.py \
  --config configs/eval_regression.toml \
  --maps sprint string duel bridge crossfire \
  --seeds 1 7
make handoff
```

## Baseline metrics to record

- command failures;
- exceptions/safe-mode indicators;
- game score by map and side;
- whether any Builder spawns;
- whether any Harvester is built;
- whether any route reaches the Core;
- first Harvester round;
- first confirmed delivery round;
- maximum observed CPU time if available;
- obvious oscillation or permanent stall.

## Done criteria

- The planning packet embeds the same source that is actually being tested.
- v0003 is recoverable as an immutable baseline.
- At least one reproducible report exists.
- No behavior changes were mixed into the baseline capture.

---

# Iteration 1 — Fix navigation, build-range movement, and route-search stability

## Objective

Ensure Builders move to a legal orthogonal action stance, reuse paths across steps, and do not restart long-term route searches because another Builder temporarily moved.

## Files allowed to change

- `bot/navigation.py`
- `bot/world.py`
- `bot/builder.py`
- `bot/actions.py`
- focused navigation/action tests

Do not modify economy thresholds, Store layout, combat priorities, role assignment, or Core budget policy in this iteration.

## Exact design

### A. Add explicit movement goal modes

Do not use one generic “move onto target” helper for every task.

Implement two clear operations:

1. `next_direction_to_tile(start, target, ...)`
   - used when standing on the target is valid, such as scouting.
2. `next_direction_to_adjacent(start, target, ...)`
   - goal set is the legal in-bounds cardinal neighbors of `target`;
   - exclude blocked or currently illegal stance cells;
   - if already adjacent, return `CENTRE`;
   - never deliberately step onto `target`.

Builder construction, repair, destruction, and Harvester placement must use the adjacent form.

### B. Replace the ineffective cache key

The active path should persist across movement.

Recommended per-unit `Navigator` state:

```text
active_goal_key
active_obstacle_epoch
active_path: tuple[Position, ...]
active_index
replans
cache_hits
```

Behavior:

- Reuse the active path when the goal and relevant obstacle epoch are unchanged.
- If the current position equals `active_path[active_index]`, advance to the next path cell.
- If the current position appears later in the path, jump the index forward.
- Replan only when:
  - goal/mode changes;
  - obstacle epoch changes materially;
  - current position is no longer on the path;
  - next step is blocked/illegal;
  - oscillation is detected.
- Keep BFS expansion bounded by map area and stop before 7 ms.
- Do not maintain a dictionary keyed by every changing start position.

### C. Separate navigation obstacles from route-planning obstacles

In `WorldMemory`, provide distinct methods:

- `is_navigation_blocked(pos)`:
  - walls;
  - Core footprint;
  - current known impassable buildings;
  - recently seen Builder occupancy.
- `is_route_planning_blocked(pos)`:
  - walls;
  - Core footprint;
  - known permanent impassable buildings;
  - **not transient Builder occupancy**;
  - passable Conveyors/Splitters are handled during route construction rather than forcing search churn.

Maintain separate epochs if necessary:

- `navigation_epoch` for dynamic movement changes;
- `layout_epoch` for static/permanent layout changes.

`plan_core_outward_route()` should use `layout_epoch`, not the transient navigation epoch.

### D. Correct destroy semantics

`TurnActions.destroy()` must:

- call only `can_destroy()` and `destroy()`;
- not require `_ready_action()`;
- not set `acted = True`;
- allow another legal destroy in the same round;
- let the engine's own `can_*` checks decide whether movement or another action remains legal.

Do not assume destroy plus build is legal; test the engine/fake contract separately.

### E. Update Builder call sites

Use action-adjacent movement in:

- `_build_route()`
- `_harvester()`
- `_repair()` when the next operation is build/destroy
- `_defend()` or `_support_build()` when approaching a known build target
- `_raid()` only when movement toward an adjacent attack target is later implemented

Scouting/rally travel can still use move-to-tile.

## Focused unit tests

Create or extend:

```text
tests/test_navigation.py
tests/test_actions.py
tests/test_builder_navigation.py
```

Required cases:

1. A Builder two cells from a build target stops on a cardinal neighbor and never enters the target tile.
2. Already-adjacent Builder returns `CENTRE` without increasing blocked-step count.
3. Path reuse produces at least one cache hit across a three-step route.
4. Goal change invalidates the active path.
5. Permanent obstacle/layout change invalidates the route.
6. A transient Builder appearing elsewhere does not restart the static route search.
7. A blocked next step triggers one replan and deterministic fallback.
8. BFS on 30×30 never exceeds 900 expansions.
9. CPU guard aborts safely and returns a bounded fallback.
10. `destroy()` does not set `acted`; two legal destroys can be attempted in one wrapper instance.
11. Build/move mutual exclusion remains enforced.

## Behavioral evaluation

```bash
make static
make smoke
python scripts/run_local_matrix.py \
  --config configs/eval_regression.toml \
  --maps sprint bridge crossfire vault \
  --seeds 1 7 19
```

Primary metrics:

- fewer BFS replans per Builder;
- no “stand on intended build tile” stalls;
- route cells built in monotonic order;
- no new exceptions/TLEs.

## Rollback

Revert only the Iteration 1 commit. No serialized Store/state format changes occur.

## Done criteria

- All construction targets are approached from legal adjacency.
- A moving Builder can reuse a path across multiple turns.
- Route search is unaffected by unrelated transient Builder motion.
- Static/smoke pass with no reliability regression.

---

# Iteration 2 — Replace the ambiguous Store/project protocol

## Objective

Create a single-writer, versioned Store protocol whose slot names match their actual data and whose behavior is explicit under one-round-delayed writes.

## Files allowed to change

- `bot/comms.py`
- `bot/core.py`
- claim/project portions of `bot/builder.py`
- `bot/types.py`
- Store protocol tests

Do not change navigation, route geometry, combat, or economic thresholds.

## Proposed slot ownership

Keep 16 slots but make ownership explicit:

| Slot | Meaning | Writer |
|---:|---|---|
| 0 | schema version | Core |
| 1 | strategy phase/opening | Core |
| 2 | project 0 status | assigned Builder 0 |
| 3 | verified enemy Core + epoch | designated scout |
| 4 | project 2 status | assigned Builder 2 |
| 5 | project 1 status | assigned Builder 1 |
| 6 | desired Builder count | Core |
| 7 | ammo target | Core |
| 8 | defense alert + expiry | designated defender |
| 9 | rally + expiry | designated scout |
| 10–12 | claim owner assignments | Core only |
| 13 | budget | Core |
| 14 | protocol diagnostics/feature flags | Core |
| 15 | global epoch | Core |

Rename `PRIMARY_ORE`, `LOGISTICS`, and `THREAT` to `PROJECT_0`, `PROJECT_1`, and `PROJECT_2` if those slots continue to hold project status.

## Protocol rules

1. Core is the only writer of claim-assignment slots.
2. A Builder writes only the project slot associated with its current assignment.
3. Project status must encode:
   - target coordinate or unknown;
   - 6-bit epoch;
   - small state enum such as `IDLE`, `CLAIMED`, `PLANNING`, `BUILDING`, `VERIFYING`, `DELIVERING`, `MAINTAIN`, `FAILED`.
4. Owner ID does not need to be repeated in the project slot because the corresponding claim slot identifies the assigned owner.
5. Core reassigns a claim only when:
   - project heartbeat is stale;
   - assigned unit is no longer counted/observed according to the chosen reliable mechanism;
   - project reports `FAILED`;
   - target becomes invalid.
6. Builders must tolerate the one-round delay:
   - after Core assignment, wait until the assignment is readable;
   - after Builder heartbeat/status write, do not expect Core to see it until next round.
7. Remove raw bit manipulation from `builder.py`; expose tested codec helpers.

## Required helpers

Suggested API:

```python
encode_assignment(owner_id, generation)
decode_assignment(value)

encode_project(position, epoch, project_state)
decode_project(value, width, height)

read_assignment(ct, index)
write_assignment(ct, index, ...)
read_project(ct, index)
write_project(ct, index, ...)
```

Reject invalid coordinates, boolean-as-integer inputs, negative values, and out-of-range states.

## Focused tests

1. Every map coordinate up to 30×30 round-trips.
2. `(0, 0)` is distinct from unknown.
3. Epoch wrap 63→0 is handled.
4. Stale heartbeat is rejected.
5. Invalid/out-of-map coordinate decodes to `None`.
6. Core and Builder ownership checks reject the wrong writer.
7. Simulated round N write is not visible until N+1.
8. Assignment handoff does not cause two Builders to own the same project.
9. A failed/stale project becomes reassignable.
10. Schema mismatch causes safe no-op/reinitialization rather than exception.

## Evaluation checkpoint

No game-strength improvement is required. Require:

- identical or better smoke reliability;
- no duplicate ore target ownership;
- no project count above three;
- no project that remains “pending” forever due solely to one-round lag.

## Rollback

This is a schema change. Bump `SCHEMA_VERSION` and keep the entire change in one commit. Roll back code and schema together; never mix old and new codecs.

---

# Iteration 3 — Make one Harvester-to-Core route provably complete

## Objective

Deliver the first Harvester stack reliably on every reachable smoke/regression map before enabling expansion, redundancy, defense construction, or raids.

## Files allowed to change

- route/economy sections of `bot/builder.py`
- `bot/logistics.py`
- `bot/economy.py`
- limited Core-side delivery acknowledgement if needed
- focused route/FSM tests
- one small feature-flag module if none exists

Do not change combat targeting or add a second Harvester in this iteration.

## Isolation requirement

Introduce explicit feature gates if the repository does not already have them:

```text
ENABLE_SECONDARY_EXPANSION = False
ENABLE_REDUNDANCY = False
ENABLE_DEFENSIVE_BUILDING = False
ENABLE_RAIDS = False
ENABLE_LAUNCHERS = False
```

Turrets that already exist may still execute safely. The purpose is to measure the economy foundation without unrelated spending or behavior.

## Route FSM

Use explicit transitions driven by verified facts:

```text
UNASSIGNED
→ CLAIMED
→ ROUTE_PLANNING
→ ROUTE_BUILDING
→ ROUTE_VERIFYING
→ HARVESTER_APPROACH
→ HARVESTER_BUILD
→ WAIT_FIRST_DELIVERY
→ MAINTAIN
→ REPAIRING
→ WAIT_FIRST_DELIVERY
```

Do not advance state merely because a helper was called.

### Route construction rules

1. Build Core-outward so the last mile exists before the Harvester's immediate first output.
2. For each route cell:
   - approach an orthogonal build stance;
   - inspect exact building type, team, and direction;
   - reuse a matching friendly Conveyor;
   - destroy a mismatched friendly Conveyor only after verification;
   - mark an enemy/other occupied cell as a replan obstacle;
   - never loop forever on `can_build == False`.
3. Limit route replans and record failure reason.
4. After all links are built, verify every visible link and the final direction into the Core.
5. Build the Harvester only after route verification.

### Delivery acknowledgement

Prefer a route-local signal over raw global-resource growth.

Recommended implementation order:

1. If the Core can see the final Conveyor, let Core-side logic track its `get_stored_resource_id()` transition and publish a one-round-delayed delivery acknowledgement in the corresponding project status.
2. If Core-side acknowledgement is impractical within the slot budget, use a conservative combination:
   - final Conveyor observed non-empty then empty;
   - expected passive-income subtraction;
   - no route-local backlog;
   - timeout long enough to cover route length.
3. Never treat an arbitrary global titanium increase alone as proof that this route delivered.

### Repair behavior

- Missing/misdirected visible link → approach, destroy if friendly and verified wrong, rebuild.
- Permanent occupied cell → invalidate route and replan.
- Backlog at final link → inspect last mile before destroying a correct Conveyor.
- Do not destroy a correct link solely because no global increase was observed while other units may be spending.
- Bound repair attempts and fall back to `FAILED` so Core can reassign.

## Focused tests

1. Straight route into each side of a 2×2 Core.
2. Route around a wall.
3. Harvester is not built before receiver chain verification.
4. First output is not lost because no adjacent receiver exists.
5. Matching existing Conveyor is reused.
6. Friendly wrong-direction Conveyor triggers destroy/rebuild.
7. Enemy occupied route cell triggers replan, not infinite retries.
8. Broken middle link is identified and repaired.
9. Correct final Conveyor is not destroyed because unrelated spending hid resource growth.
10. First confirmed delivery moves project to `MAINTAIN`.
11. Timeout moves project to `FAILED` after bounded attempts.
12. No Builder stands on its intended build tile.

## Behavioral maps

- `sprint`: very short route and congestion.
- `string`: narrow geometry.
- `bridge`: long horizontal path/chokepoint.
- `crossfire`: obstacles.
- `vault`: large route/CPU.
- `aurora`: large-map worst case.

Run both sides with seeds `1, 7, 19`.

## Primary metric

**First confirmed delivery rate** across map/seed/side cases.

Promotion threshold for this iteration:

- 100% on smoke maps where reachable ore exists;
- at least 95% on the selected regression set;
- zero exceptions/TLEs;
- no advanced-feature spending.

---


## Current Iteration 3 status and mandatory recovery gate

**Do not begin Iteration 4 yet.** The latest repository evidence shows:

- Iterations 0, 1, and 2 passed their focused/static/smoke/regression gates.
- Iteration 3 and two bounded repairs are command-clean but behaviorally blocked.
- First-delivery/collection proxy remains `12/36` (`33.3%`).
- Candidate wins remain `0/36`.
- Mean collected titanium is about `824`, versus about `4,778` for the passed Iteration 2 comparator.
- All advanced feature flags are still disabled, so this regression is inside the first-route/economy path rather than combat or expansion.
- The first identified claim-generation expiry defect was repaired, but the promotion metric did not improve.
- Live v0003 evidence also shows the larger strategic problem: the bot sometimes survives to the 1000-round collection tiebreak, but it scales too slowly on some maps and can be destroyed by aggressive opponents around rounds 266–317.

### Iteration 3R — Diagnose the earliest route failure before further feature work

This is a diagnosis-and-repair gate, not a broad redesign.

#### Objective

Identify the earliest causal divergence between the passed Iteration 2 comparator and blocked Iteration 3 candidate, then fix only that divergence and restore first-route performance.

#### Required evidence instrumentation

For each active project, emit an offline/report trace with one row per meaningful transition:

```text
round
builder_id
assignment_owner
assignment_generation
project_index
project_state
project_epoch
ore_target
route_length
route_cursor
route_plan_status
current_position
next_build_cell
next_build_direction
global_titanium
current_harvester_cost
current_conveyor_cost
last_delivery_evidence_round
repair_attempts
failure_reason
```

Do not print all of this every turn in the submitted bot. Capture it through:

- replay-derived analysis where possible;
- test-only/fake-controller hooks;
- bounded debug output enabled only for selected local diagnostic games.

#### Required differential workflow

1. Select the 12 successful and 24 unsuccessful rows from the current 36-game regression.
2. For at least:
   - one successful small map;
   - one failed small/narrow map;
   - one failed medium map;
   - one failed large map;
   compare the candidate against the Iteration 2 comparator.
3. Find the **first round** at which any of these differs:
   - assignment ownership;
   - ore target;
   - route plan availability;
   - route cursor progress;
   - first Conveyor build;
   - route verification;
   - Harvester build;
   - first resource-stack movement;
   - delivery acknowledgement.
4. Classify each failure into exactly one primary reason:
   - no reachable ore selected;
   - assignment lost/stale;
   - route planner failed or restarted;
   - Builder could not reach stance;
   - insufficient titanium/reserve gate;
   - route-cell occupancy/conflict;
   - wrong Conveyor direction/last mile;
   - Harvester never built;
   - Harvester output blocked;
   - delivery happened but proxy missed it;
   - repair loop/churn;
   - unknown.
5. Do not patch a later symptom until the earliest divergence is identified.
6. Add one deterministic focused test reproducing the selected root cause.
7. Apply one bounded repair.
8. Rerun the exact 36-game matrix.
9. Stop after two repairs if no row-level improvement occurs; write a new diagnosis plan instead of continuing blind patches.

#### Iteration 3R promotion gate

Proceed to Iteration 4 only when all are true:

- first-delivery/collection proxy is at least `34/36`;
- candidate titanium collection is no worse than 90% of the Iteration 2 comparator aggregate;
- no map/side category has a systematic first-route failure;
- zero command failures, exceptions, and TLE indicators;
- route churn is bounded and materially below the observed `runestone`-style build/remove churn;
- the successful behavior is explained by deterministic tests, not only aggregate score.

---

# Iteration 4 — Stable economy scaling, spawning, project budgeting, and route maintenance

## Objective

Once Iteration 3R proves one reliable Harvester-to-Core route, scale from one working route to a durable multi-route economy without starving construction, overproducing Builders, inflating cost scale unnecessarily, or converting titanium into unused ammunition.

## Strategic outcome

At the end of Iteration 4, the bot should:

1. complete and maintain its first route;
2. add the nearest next profitable ore project one at a time;
3. keep enough liquidity to repair active infrastructure;
4. spawn enough Builders to build and maintain the economy, but not so many that +20% Builder scaling destroys payback;
5. keep idle Builders productive by assigning them to the next valid harvesting/logistics task;
6. report exact economic state to later defense and offense phases;
7. avoid combat spending except for a tightly bounded emergency reserve.

## Files allowed to change

Expected surface:

- `bots/candidate/bot/core.py`
- `bots/candidate/bot/economy.py`
- economy/project portions of `bots/candidate/bot/builder.py`
- `bots/candidate/bot/logistics.py`
- budget/status codecs in `bots/candidate/bot/comms.py`
- local enums/data structures in `bots/candidate/bot/types.py`
- `bots/candidate/bot/feature_flags.py`
- focused Core/economy/logistics tests
- evaluation/report scripts only when needed to expose the required metrics

Do not change:

- turret target selection;
- offensive target priority;
- Launcher behavior;
- map-name-specific openings;
- live deployment thresholds;
- the Iteration 3 route FSM except for an independently reproduced maintenance defect.

## Feature gates

For this iteration:

```python
ENABLE_SECONDARY_EXPANSION = True
ENABLE_REDUNDANCY = False
ENABLE_DEFENSIVE_BUILDING = False
ENABLE_RAIDS = False
ENABLE_FORWARD_GUNNERS = False
ENABLE_LAUNCHERS = False
ENABLE_PHASE_STRATEGY = False
```

Existing turrets, if present in a test fixture or old replay, may act safely. The economy code must not intentionally build combat infrastructure in this iteration.

## 4.1 Introduce an explicit economy phase model

Add a compact economy phase enum:

```text
BOOTSTRAP
FIRST_ROUTE_BUILDING
FIRST_ROUTE_MAINTAINING
EXPANSION_EVALUATION
SECONDARY_ROUTE_BUILDING
MULTI_ROUTE_MAINTAINING
REPAIR_PRIORITY
ECONOMY_SATURATED
ENDGAME_HOLD
```

Core is the authoritative phase writer. Builders consume the phase after the Store's one-round delay.

### Transition rules

```text
BOOTSTRAP
  -> FIRST_ROUTE_BUILDING
     when a valid first assignment is issued

FIRST_ROUTE_BUILDING
  -> FIRST_ROUTE_MAINTAINING
     only after route-local delivery acknowledgement is fresh

FIRST_ROUTE_MAINTAINING
  -> REPAIR_PRIORITY
     when a maintained route reports a verified break/backlog
  -> EXPANSION_EVALUATION
     when liquidity and payback gates pass
  -> ENDGAME_HOLD
     when too little horizon remains for another route

EXPANSION_EVALUATION
  -> SECONDARY_ROUTE_BUILDING
     when exactly one unclaimed ore project is approved
  -> FIRST_ROUTE_MAINTAINING
     when no project is profitable or affordable

SECONDARY_ROUTE_BUILDING
  -> REPAIR_PRIORITY
     when any existing route is broken
  -> MULTI_ROUTE_MAINTAINING
     when the new route delivers

MULTI_ROUTE_MAINTAINING
  -> REPAIR_PRIORITY
     on active-route damage
  -> EXPANSION_EVALUATION
     when another project remains profitable
  -> ECONOMY_SATURATED
     when no eligible project remains

REPAIR_PRIORITY
  -> previous maintaining phase
     after all critical routes become healthy
  -> project FAILED/reassignment
     after bounded repair attempts
```

The phase must be derived from project state, not a round-number-only script.

## 4.2 Build an exact economic snapshot

Create an immutable per-Core-turn snapshot, for example:

```python
@dataclass(frozen=True, slots=True)
class EconomySnapshot:
    round: int
    titanium: int
    ammo: int
    scale_percent: int
    live_units: int
    desired_builders: int
    active_projects: int
    maintaining_routes: int
    building_routes: int
    failed_projects: int
    broken_routes: int
    remaining_route_cost: int
    emergency_repair_reserve: int
    defense_reserve: int
    ammo_reserve: int
    free_titanium: int
```

Compute each value once per Core turn. Do not repeatedly call expensive sensing helpers or dynamic-cost getters in multiple policy functions.

### Required cost calculation

For every proposed route project:

```text
remaining_conveyor_cost =
    sum(current conveyor cost for each missing link,
        updating conservatively for expected +1% scale per new Conveyor)

harvester_cost =
    current get_harvester_cost()

optional_splitter_cost =
    0 in Iteration 4

repair_contingency =
    max(2 * current_conveyor_cost,
        ceil(0.10 * planned_infrastructure_cost))

project_total_cost =
    remaining_conveyor_cost
    + harvester_cost
    + repair_contingency
```

Do not duplicate the platform's price formula. Query current getters and use a conservative local projection only for future planned purchases.

### Reserve order

Titanium is allocated in this strict order:

1. cost to complete any already-started critical first route;
2. cost to repair a broken delivering route;
3. minimum emergency liquidity;
4. approved Builder spawn, if its marginal value exceeds cost/scale;
5. approved next Harvester route;
6. later defense/ammo reserves, which remain disabled in this iteration;
7. discretionary spending.

A later category may not consume an earlier reserve.

## 4.3 Profitability and payback gate

A Harvester produces 10 Ti every 4 rounds, or 2.5 Ti/round before disruption and route latency. Use a conservative effective rate rather than assuming perfect operation.

Suggested first model:

```text
gross_rate = 2.5 Ti/round
uptime_factor = 0.75 for unknown/new route
              = measured recent uptime for maintained route
effective_rate = gross_rate * uptime_factor

delivery_latency =
    route_length
    + construction_travel_estimate
    + build_turns_remaining

remaining_productive_rounds =
    1000 - current_round - delivery_latency

expected_gross_return =
    max(0, remaining_productive_rounds) * effective_rate

risk_penalty =
    exposure_weight * exposed_route_cells
    + congestion_weight * shared_route_cells
    + failure_weight * recent_project_failures

expected_net_value =
    expected_gross_return
    - project_total_cost
    - risk_penalty
```

Approve the project only when:

```text
expected_net_value >= MIN_EXPANSION_MARGIN
and free_titanium >= project_total_cost
and active_building_projects < MAX_SIMULTANEOUS_BUILD_PROJECTS
and no critical route is broken
and current_round <= LAST_EXPANSION_START_ROUND
```

Start with:

```text
MAX_SIMULTANEOUS_BUILD_PROJECTS = 1
```

Do not start multiple speculative routes.

## 4.4 Ore ranking

Rank known unclaimed ore by total project value, not Euclidean proximity alone.

```text
ore_score =
    - route_length_weight * planned_route_length
    - builder_travel_weight * builder_distance_to_stance
    - exposure_weight * enemy_threat_exposure
    - overlap_weight * route_overlap
    - congestion_weight * narrow_shared_cells
    + defensibility_bonus
    + existing_network_reuse_bonus
    + map_horizon_bonus
```

Tie-break deterministically by:

1. higher score;
2. shorter planned route;
3. lower `y`;
4. lower `x`;
5. lower assigned Builder ID.

“Closest ore” in the integrated strategy means the **closest reachable economically valid ore**, not simply the smallest squared distance.

## 4.5 Builder spawning policy

Builders have 30 Ti base cost and add +20% scale, so uncontrolled mass spawning is expensive.

Use a demand-based target:

```text
base_builders = 3

construction_demand =
    1 per actively building route

maintenance_demand =
    1 if any route is delivering
    + 1 additional if there are at least 3 long/exposed routes

scout_demand =
    1 until enough ore/enemy information is known

reserve_defenders =
    0 in Iteration 4 feature behavior
    but leave the policy field available for Iteration 5/7

desired_builders =
    clamp(base_builders
          + construction_demand
          + maintenance_demand
          + scout_demand,
          min=3,
          max=ECONOMY_BUILDER_CAP)
```

Use an initial safe cap such as 7–9, then tune from evidence. Do not copy the 27–28 Builder opponent counts without proving their value under the scaling rules.

Spawn only when:

```text
current_builder_count < desired_builders
and free_titanium_after_critical_reserves >= current_builder_cost
and at least one useful unfilled role exists
and a spawn tile preserves at least one Core exit
```

The Core should assign a role/project immediately and deterministically after spawn ID is known.

## 4.6 Productive idle-Builder policy

A Builder is idle only when it has no valid active assignment and no emergency task.

Priority:

```text
1. repair a broken owned route
2. take an approved unowned route project
3. maintain/inspect an existing route with stale health
4. scout the nearest useful frontier for ore and enemy information
5. move toward a staging tile that does not block Core/logistics
6. no-op safely
```

In Iteration 4, “idle Builders harvest” means they seek and construct the next approved Harvester route. Builders do not directly mine titanium.

Never let every idle Builder independently select the same ore. Assignment remains Core-authoritative and single-writer.

## 4.7 Route maintenance and churn prevention

For each maintained route track:

```text
route_id
ore_position
ordered_cells
expected_directions
last_verified_round
last_delivery_ack_round
last_stack_seen_round
break_index
repair_owner
repair_attempts
replan_count
churn_count
```

A route becomes suspect only when evidence exceeds a threshold:

- missing/misdirected visible link;
- final-link backlog beyond expected transit time;
- Harvester output blocked for multiple cycles;
- stale delivery acknowledgement beyond route length plus a bounded grace period;
- explicit enemy destruction event inferred from visible state.

Do not tear down correct links merely because global titanium did not increase during spending.

### Repair priority

```text
criticality =
    delivered_rate_before_break
    * remaining_horizon
    - estimated_repair_cost
```

Repair the highest-criticality route first. Pause new expansion while a high-value route is broken.

### Churn limits

Per route:

```text
MAX_REPLANS_PER_50_ROUNDS
MAX_DESTROYS_PER_CELL
MAX_REPAIR_ATTEMPTS
```

If exceeded, mark the project `FAILED`, preserve the still-correct infrastructure, and request a fresh bounded plan. Do not repeatedly remove and rebuild the same chain as observed in the live `runestone` match.

## 4.8 Ammo behavior in Iteration 4

Do not proactively convert ammunition when no combat demand exists.

Implement only the correct primitive:

```python
def maybe_convert_ammo(ct, snapshot, requested_ammo):
    deficit = max(0, requested_ammo - snapshot.ammo)
    affordable = max(0, snapshot.free_titanium)
    amount = min(deficit, affordable, MAX_AMMO_CONVERSION_PER_TURN)
    if amount > 0 and ct.can_convert_ammo(amount):
        ct.convert_ammo(amount)
```

Important:

- ammo conversion may occur in the same Core turn as spawning because it does not consume the Core action cooldown;
- `requested_ammo` remains zero while combat feature gates are off;
- do not convert titanium “just in case.”

## 4.9 Endgame economy policy

At a configurable cutoff, stop projects that cannot repay before round 1000.

```text
if current_round >= LAST_EXPANSION_START_ROUND:
    do not start new routes
    complete near-finished profitable route only
    prioritize repair of delivering routes
    preserve stored titanium
    avoid unnecessary Builder attacks, healing, ammo, and construction
```

This matters because unresolved games use titanium/Harvester/storage tiebreakers.

## Iteration 4 pseudocode

```python
def run_core_economy(ct, state):
    snapshot = collect_economy_snapshot(ct, state)
    reconcile_project_health(snapshot, state)

    if snapshot.broken_routes:
        set_phase(REPAIR_PRIORITY)
        assign_best_repair(snapshot, state)
    elif not first_route_is_maintaining(state):
        set_phase(FIRST_ROUTE_BUILDING)
        preserve_first_route_budget(snapshot, state)
    elif should_stop_expanding(snapshot):
        set_phase(ENDGAME_HOLD)
    elif has_profitable_unclaimed_ore(snapshot, state):
        set_phase(EXPANSION_EVALUATION)
        project = choose_best_ore_project(snapshot, state)
        if project and can_fund_project(snapshot, project):
            assign_exactly_one_project(project, state)
            set_phase(SECONDARY_ROUTE_BUILDING)
    else:
        set_phase(MULTI_ROUTE_MAINTAINING)

    desired = compute_desired_builder_count(snapshot, state)
    if should_spawn_builder(snapshot, desired, state):
        spawn_and_assign_builder(ct, snapshot, state)

    # This remains zero until later iterations enable demand.
    maybe_convert_ammo(ct, snapshot, requested_ammo=0)
```

## Focused tests

At minimum:

1. first-route reserve cannot be consumed by a Builder spawn;
2. broken-route repair preempts expansion;
3. only one new route project is active at a time;
4. closest unreachable ore loses to a reachable ore;
5. high-risk short route can lose to a safer slightly longer route;
6. no expansion begins after the payback cutoff;
7. Builder target rises when a construction role exists and falls when it does not;
8. spawn is denied when it would consume route completion reserve;
9. spawn selection preserves a Core exit;
10. idle Builder receives an approved unowned harvest project;
11. two idle Builders cannot claim the same project;
12. maintained route is not destroyed due solely to global spending;
13. repair attempts/churn are bounded;
14. ammo remains zero when requested demand is zero;
15. spawn and ammo conversion can legally happen in the same Core turn;
16. deterministic tie-breaking produces the same project and owner;
17. every dynamic price is obtained through the Controller getter;
18. 30×30/worst-case Core policy stays under the CPU guard.

## Evaluation checkpoint

Run:

```bash
make static
make smoke

python scripts/run_local_matrix.py \
  --config configs/eval_regression.toml \
  --maps sprint string bridge crossfire twins runestone vault aurora \
  --seeds 1 7 19
```

Primary metrics:

- first-route delivery rate;
- delivered/collected titanium at rounds 100, 250, 500, and 1000;
- number of maintaining Harvesters;
- first and second route completion rounds;
- route payback round;
- Builder count and scale percent;
- route build/remove churn;
- broken-route downtime;
- p95/p99 Core and Builder CPU;
- paired score against the passed Iteration 3 comparator.

## Iteration 4 promotion gate

- Iteration 3 first-route metric does not regress.
- Aggregate collected titanium improves over the passed Iteration 3 comparator.
- `twins` and `runestone` no longer show one-Harvester stagnation or uncontrolled route churn.
- No systematic map/side failure.
- Zero exception/TLE indicators.
- Builder count remains explainable by active demand.
- At least one second route reaches `MAINTAIN` on maps where it is profitable.
- No broad combat behavior has been introduced.

## Rollback

Keep economy scaling behind `ENABLE_SECONDARY_EXPANSION`. Reverting the Iteration 4 commit or setting the flag false must restore the passed single-route behavior without changing the Store schema.

---

# Iteration 5 — Reactive defense of the Core, Harvesters, and logistics network

## Objective

Protect the Core and economically valuable buildings from active enemy pressure while preserving the working economy. Defense must be event-driven, targeted, and reversible—not a permanent state in which every Builder waits at home.

## Strategic outcome

The bot should:

- detect attackers before they reach critical assets where vision permits;
- keep two or three defenders available later in the integrated strategy;
- temporarily recall nearby Builders when an attack is real;
- use movement blocking, healing, Barriers, Gunners, and Sentinels appropriately;
- repair damaged logistics after the threat;
- stand down when the threat expires;
- avoid spending the route-completion reserve on unnecessary turrets.

## Files allowed to change

- `bots/candidate/bot/defense.py`
- defensive role/interrupt portions of `bots/candidate/bot/builder.py`
- `bots/candidate/bot/turrets.py`
- threat and defense Store codecs in `bots/candidate/bot/comms.py`
- role/phase enums in `bots/candidate/bot/types.py`
- demand/reserve integration in `bots/candidate/bot/core.py`
- focused defense/turret tests
- feature flags

Do not yet implement:

- broad offensive raids;
- forward siege construction;
- full integrated phase strategy;
- Launcher tactics unless required by an isolated defensive test;
- map-name hard-coding.

## Feature gates

```python
ENABLE_DEFENSIVE_BUILDING = True
ENABLE_RAIDS = False
ENABLE_FORWARD_GUNNERS = False
ENABLE_LAUNCHERS = False
ENABLE_PHASE_STRATEGY = False
```

## 5.1 Threat data model

Represent one authoritative current threat, plus local per-unit observations.

```python
class ThreatKind(IntEnum):
    NONE = 0
    ENEMY_BUILDER = 1
    ENEMY_GUNNER = 2
    ENEMY_SENTINEL = 3
    ENEMY_LAUNCHER = 4
    CORE_UNDER_FIRE = 5
    ROUTE_UNDER_ATTACK = 6
    HARVESTER_UNDER_ATTACK = 7

@dataclass(frozen=True, slots=True)
class ThreatReport:
    kind: ThreatKind
    position: Position
    target_asset: Position | None
    severity: int
    first_seen_round: int
    last_seen_round: int
    expiry_round: int
    reporter_id: int
```

The Store cannot hold this whole object directly. Encode only the minimum shared payload:

```text
threat kind
packed position
severity
epoch/expiry
```

A designated defense leader is the only writer of the shared threat slot. Other units keep local observations and may become the leader through deterministic assignment.

## 5.2 Threat severity

Suggested score:

```text
severity =
    type_weight
    + core_proximity_weight
    + critical_asset_proximity_weight
    + observed_damage_weight
    + enemy_support_weight
    - distance_to_nearest_defender_weight
```

Initial type weights:

```text
enemy Builder near route          medium
enemy Builder adjacent to asset   high
enemy Gunner/Sentinel line        high
Core HP decreased                 critical
Harvester/route HP decreased      high
Launcher adjacent to defender     medium/high
```

Escalate immediately when:

- Core HP drops;
- a visible enemy can legally attack the Core or a critical route cell;
- a route/Harvester is currently taking damage;
- multiple enemies are approaching the same asset.

Do not escalate from a single stale enemy coordinate after expiry.

## 5.3 Defense mode and hysteresis

Defense is an interrupt overlay, not necessarily the global economy phase.

```text
DEFENSE_CLEAR
DEFENSE_WATCH
DEFENSE_ACTIVE
DEFENSE_CRITICAL
DEFENSE_RECOVERY
```

Transitions:

```text
CLEAR -> WATCH
    on fresh low/medium threat

WATCH -> ACTIVE
    when threat persists or enters protected radius

ACTIVE -> CRITICAL
    on Core damage, adjacent attacker, or overwhelming line

ACTIVE/CRITICAL -> RECOVERY
    when no fresh threat for DEFENSE_STANDDOWN_DELAY

RECOVERY -> CLEAR
    after damaged assets are repaired and routes are healthy

RECOVERY -> ACTIVE
    if threat reappears
```

Use hysteresis so Builders do not switch attack/defense roles every round.

## 5.4 Protected assets and zones

Maintain priorities:

```text
1. own Core
2. first/primary delivering route's last mile
3. delivering Harvesters
4. other delivering route junctions/splitters
5. turrets
6. unfinished speculative infrastructure
```

Define:

- Core defense radius;
- route critical-cell set;
- Harvester defense radius;
- staging tiles that do not block the Core or Conveyor flow.

Do not occupy all Core exits. Do not place impassable buildings on:

- legal spawn exits;
- route cells;
- Builder escape lanes;
- the only path to a Harvester repair stance.

## 5.5 Defender assignment

The integrated strategy will normally reserve 2 defenders on small/medium maps and 3 on large or threatened maps. Iteration 5 implements the mechanism, not the final phase switch.

Choose defenders deterministically:

```text
defender_score =
    distance_to_threat
    + penalty_if_critical_route_owner
    + penalty_if_carrying_near-complete_project
    + penalty_if_low_hp
    - bonus_if_already_near_core
    - bonus_if_designated_defender
```

Select the lowest scores.

Rules:

- never recall the only Builder completing the first route unless Core danger is critical;
- do not assign more defenders than needed for current severity;
- maintain stable defender identity until stand-down;
- if a defender dies or becomes unreachable, replace it after Store delay;
- non-defenders continue economy work unless their local asset is under immediate attack.

## 5.6 Defender action priority

A Builder cannot directly attack enemy Builders; its paid attack targets adjacent buildings. Therefore defense against enemy Builders uses blocking, turrets, Launchers later, and protection/repair—not illegal Builder-vs-Builder attacks.

Per defender:

```python
def run_defender(ct, state, threat):
    if immediate_legal_heal_of_core_or_critical_asset(ct):
        heal_highest_value_asset(ct)
        return

    if adjacent_enemy_building_threat(ct):
        attack_if_budgeted(ct)
        return

    if can_build_high_value_defense(ct, threat):
        build_selected_turret_or_barrier(ct, threat)
        return

    if can_take_safe_intercept_or_block_tile(ct, threat):
        move_to_intercept(ct, threat)
        return

    if threat_is_stale(threat):
        enter_recovery_or_resume_previous_role(state)
        return

    move_to_defense_staging(ct, threat)
```

Every paid Builder attack/heal must respect the emergency budget and use `can_*`.

## 5.7 Defensive building selection

### Barrier

Use when:

- it blocks a direct Builder path;
- it protects a route junction;
- it creates a Gunner lane;
- it does not trap friendly Builders or block logistics.

Barrier score:

```text
path_delay_created
+ protected_asset_value
+ friendly_turret_synergy
- friendly_path_block_penalty
- route_block_penalty
- escape_block_penalty
```

### Gunner

Use when:

- enemy Builders repeatedly approach through a short corridor;
- the Gunner has an immediate or likely firing ray;
- the position can be protected;
- ammunition demand is affordable.

Current characteristics from the supplied rules:

- 25 HP;
- 20 Ti base cost;
- +20% scale;
- 7 damage;
- 4 ammo/shot;
- reload 1;
- rotation costs 10 Ti.

A Gunner is not “cheap disposable defense” after scaling. Build only with positive expected value.

### Sentinel

Use when:

- a fixed long line protects Core/logistics;
- wall penetration matters;
- the facing can be chosen confidently at build time;
- 10 ammo/shot can be funded.

Current characteristics:

- 40 HP;
- 30 Ti base cost;
- +20% scale;
- 18 damage;
- 10 ammo/shot;
- reload 2;
- no rotation.

### Placement score

```text
placement_score =
    attackable_threat_tiles
    + protected_asset_coverage
    + expected_shots_before_destroyed
    + wall_line_bonus_for_sentinel
    - route_obstruction
    - core_exit_obstruction
    - blind_facing_penalty
    - exposure_to_enemy_turret
    - construction_travel_cost
```

Use `get_attackable_tiles_from()` and `can_fire_from()` rather than reimplementing attack geometry.

## 5.8 Turret behavior and ammo demand

### Target priority

For defensive turrets:

```text
1. enemy unit/building currently able to damage own Core
2. enemy Builder adjacent to own Core/Harvester/critical route
3. enemy turret threatening own asset
4. enemy Launcher able to displace defenders
5. enemy economic building in legal range
6. other legal target
```

### Gunner rotation

Rotate only when:

```text
best_alternative_score
> current_direction_score
+ ROTATION_MINIMUM_GAIN
```

Also require:

- enough free titanium after reserves;
- a fresh target/lane;
- no equivalent zero-score tie.

Never spend 10 Ti to rotate when every direction scores zero.

### Ammo request

Each turret contributes a bounded demand report:

```text
gunner demand =
    min(expected_legal_shots_in_horizon, GUNNER_SHOT_HORIZON) * 4

sentinel demand =
    min(expected_legal_shots_in_horizon, SENTINEL_SHOT_HORIZON) * 10
```

Aggregate at the Core through a single-writer or deterministic slot protocol. Do not depend on Core vision.

Core converts only the deficit while preserving:

1. route completion/repair reserve;
2. critical defense construction reserve;
3. minimum liquidity.

## 5.9 Defense recovery

After threat expiry:

1. inspect Core, Harvesters, last-mile Conveyors, junctions, and turrets;
2. heal only when the expected preserved value exceeds 1 Ti per 4 HP;
3. repair broken route cells;
4. remove only clearly harmful temporary friendly Barriers;
5. return excess defenders to previous economy roles;
6. retain the configured 2–3 standing defenders only when Iteration 7 enables phase strategy.

## Iteration 5 pseudocode

```python
def update_defense_overlay(ct, team_state):
    local = observe_local_threats(ct)
    shared = read_fresh_shared_threat(ct)

    authoritative = merge_and_score_threat(local, shared)

    if core_or_asset_is_taking_damage(ct, authoritative):
        mode = DEFENSE_CRITICAL
    elif authoritative.is_fresh and authoritative.severity >= ACTIVE_THRESHOLD:
        mode = DEFENSE_ACTIVE
    elif authoritative.is_fresh:
        mode = DEFENSE_WATCH
    elif recently_had_threat(team_state):
        mode = DEFENSE_RECOVERY
    else:
        mode = DEFENSE_CLEAR

    required = required_defender_count(mode, authoritative)
    assign_stable_defenders(required, authoritative, team_state)

    return mode, authoritative
```

## Focused tests

1. fresh Core damage creates a critical threat;
2. stale threat expires and defenders stand down;
3. one-round delayed threat write does not cause duplicate leaders;
4. only the required number of Builders switch to defense;
5. first-route owner is not recalled for a low threat;
6. critical Core threat may recall the nearest eligible worker;
7. enemy Builder is never targeted by an illegal Builder attack;
8. defender can block or stage without blocking all Core exits;
9. Barrier placement rejects route/core-exit cells;
10. Gunner placement has a positive firing-lane score;
11. Sentinel is chosen for a long wall-crossing line;
12. no-target Gunner does not rotate;
13. Gunner rotates only after a positive score improvement and reserve check;
14. enemy Core/critical attacker target priority is correct;
15. remote turret demand reaches Core after Store delay;
16. ammo conversion preserves economy/repair reserves;
17. recovery repairs critical route before returning workers;
18. deterministic defender selection remains stable;
19. CPU remains bounded with maximum visible entities.

## Evaluation checkpoint

Scenario tests first:

- Builder rush at Core;
- Builder attacking Harvester;
- enemy Gunner line on last-mile route;
- two simultaneous route threats;
- false/stale threat;
- defense recovery.

Then local maps:

```text
sprint, duel, string, bridge, crossfire, sweden, vault
seeds 1, 7, 19
both sides
```

Primary metrics:

- own Core HP and survival round;
- time from threat observation to defender response;
- critical-asset damage avoided;
- defense titanium spend;
- ammo spent and damage per ammo;
- route downtime under attack;
- first-delivery/economy regression;
- defender over-allocation time;
- p95/p99 CPU.

## Iteration 5 promotion gate

- first-route and economy metrics remain within agreed guardrail of Iteration 4;
- scripted rushes no longer destroy the Core without a response;
- defense begins before fixed old thresholds when a fresh threat exists;
- no permanent “everyone defends” state;
- at least one route continues producing during non-critical defense;
- no illegal Builder-vs-Builder attack;
- no zero-value Gunner rotation;
- zero exception/TLE indicators.

## Rollback

Set `ENABLE_DEFENSIVE_BUILDING = False` and disable the defense overlay while retaining safe turret execution for already-existing buildings. The Iteration 4 economy must remain operational.

---

# Iteration 6 — Real offensive capability: scouting, sabotage, forward pressure, and Core siege

## Objective

Prove that the bot can deliberately find and damage the opponent rather than merely survive or wait for the 1000-round tiebreak. Implement reusable attack primitives before combining them with the full economy-to-offense strategy in Iteration 7.

## Strategic outcome

By the end of Iteration 6:

- at least one designated scout can locate and publish a verified enemy Core or enemy economy;
- attacker Builders can navigate to legal adjacent attack stances;
- they can destroy enemy Conveyors, Splitters, Harvesters, turrets, and eventually the Core;
- enemy Builders are handled by friendly turrets, blocking, or later Launcher tactics—not illegal Builder attacks;
- forward Gunners/Sentinels may support an assault when their expected value is positive;
- attacks stop or retreat when they would bankrupt the economy or feed units into a defended lane;
- the bot records actual damage, destroyed infrastructure, and Core-pressure metrics.

## Files allowed to change

- `bots/candidate/bot/offense.py`
- offensive role/state portions of `bots/candidate/bot/builder.py`
- `bots/candidate/bot/turrets.py`
- enemy target memory in `bots/candidate/bot/world.py`
- rally/target Store codecs in `bots/candidate/bot/comms.py`
- phase/role/target enums in `bots/candidate/bot/types.py`
- offensive budget integration in `bots/candidate/bot/core.py`
- feature flags
- focused offense/combat tests

Do not yet implement the complete automatic economy-to-attack phase transition. Iteration 6 exposes and validates the primitives under explicit feature/test control.

## Feature gates

```python
ENABLE_RAIDS = True
ENABLE_FORWARD_GUNNERS = True
ENABLE_LAUNCHERS = False
ENABLE_PHASE_STRATEGY = False
```

Keep route redundancy separately disabled unless already passed as an isolated economy feature.

## 6.1 Enemy information protocol

Track:

```python
@dataclass(frozen=True, slots=True)
class EnemyTarget:
    position: Position
    entity_type: EntityType
    last_seen_round: int
    hp: int | None
    confidence: int
    source_id: int
```

Store only the highest-value verified shared target plus epoch. Local units may remember additional targets.

Required shared slots/concepts:

```text
verified enemy Core coordinate + epoch
current offensive rally coordinate + epoch
current attack objective type + epoch
```

Single writer:

- designated scout/offense leader publishes enemy Core and rally;
- Core publishes global offensive permission/phase;
- attackers do not all overwrite the same slots.

Target expires if unseen beyond a type-specific TTL unless it is the fixed enemy Core coordinate on a known map and has not been disproven.

## 6.2 Scouting behavior

Scout objective order:

```text
1. verify likely enemy Core region
2. identify enemy Conveyor/Harvester network
3. identify turret lanes and safe approach cells
4. refresh stale high-value target
5. expand frontier coverage
```

Use symmetry only as a prior. The scout must sense/verify before publishing high confidence.

Avoid suicide scouting through known turret lanes unless the expected information value justifies losing the Builder and no safer scout exists.

## 6.3 Offensive role states

```text
OFFENSE_IDLE
SCOUTING
RALLYING
APPROACHING_OBJECTIVE
SABOTAGING_LOGISTICS
DESTROYING_HARVESTER
CLEARING_DEFENSE
BUILDING_FORWARD_TURRET
PRESSURING_CORE
RETREATING
REGROUPING
```

Each attacker keeps:

```text
current objective
objective epoch
assigned rally
approach path
last progress round
paid attacks this objective
damage observed
retreat reason
```

Progress means one of:

- distance to valid stance decreases;
- target HP decreases;
- target is destroyed;
- a blocking defense is removed;
- forward turret is completed;
- enemy Core HP decreases.

If no progress occurs for a bounded window, replan, select a new target, or retreat.

## 6.4 Legal attack capability

### Builder limitations

From the supplied rules:

- Builder attack costs 2 Ti;
- deals 2 damage;
- targets an orthogonally adjacent **building**;
- Builders cannot attack enemy Builders directly.

Implementation:

```python
def try_builder_attack(ct, target, budget):
    if not target_is_building(target):
        return False

    if ct.get_position().distance_squared(target.position) != 1:
        return False

    if budget.free_attack_titanium < 2:
        return False

    if ct.can_fire(target.position):
        ct.fire(target.position)
        budget.record_attack_spend(2)
        return True

    return False
```

Use the actual API wrapper naming already present in the repository; do not invent a second action abstraction.

### Approach

Attackers must use move-to-adjacent stance logic. The target tile itself may be impassable.

Choose a stance by:

```text
path length
+ enemy turret exposure
+ friendly congestion
+ escape-route penalty
+ line-of-support bonus
```

## 6.5 Attack target hierarchy

The user's desired step-by-step attack is implemented with mechanics-aware separation.

### Builder attacker target order

Default:

```text
1. exposed Conveyor carrying/feeding an active enemy route
2. Splitter/junction whose destruction cuts multiple paths
3. Harvester connected to enemy economy
4. enemy turret or Barrier that blocks the assault
5. Launcher supporting enemy defense
6. enemy Core
```

A Builder does **not** target enemy Builders.

### Friendly turret target order during offense

```text
1. enemy Builder threatening attackers/forward turret
2. enemy turret able to fire on the assault
3. enemy Launcher able to displace attackers
4. enemy Core if legally attackable
5. Harvester/junction/high-value infrastructure
6. other legal target
```

### Direct-Core override

Attack the Core earlier when all are true:

```text
verified Core coordinate
and legal attack/firing opportunity exists
and estimated turns-to-kill < enemy repair/response window
and own economy/defense reserve remains intact
```

Do not walk past a free Core-kill window merely to obey the infrastructure ordering.

## 6.6 Infrastructure-cut scoring

Score a visible building:

```text
target_score =
    base_type_value
    + connectivity_cut_value
    + observed_resource_value
    + distance_to_enemy_core_bonus
    + current_damage_bonus
    - approach_cost
    - turret_exposure
    - paid_attack_cost_to_kill
    - stale_information_penalty
```

Approximate `connectivity_cut_value` from observed local network:

- Splitter feeding multiple outputs: high;
- Conveyor adjacent to Harvester and on only visible path: high;
- isolated Conveyor with no stack/network evidence: low;
- Harvester: high recurring value;
- Core: ultimate objective.

Use deterministic tie-breaking.

## 6.7 Paid attack budget

Builder attacks can drain titanium rapidly.

Core publishes:

```text
offense_spend_limit
minimum_economy_reserve
minimum_defense_reserve
ammo_target
```

An attacker may spend 2 Ti only when:

```text
global free titanium above all reserves
and target expected value exceeds attack cost
and paid attack count for objective is below bound
```

Estimate attacks to kill from observed HP when available:

```text
builder_attack_cost_to_kill =
    ceil(target_hp / 2) * 2 Ti
```

A 500-HP Core would require enormous paid Builder attacks if unsupported. This is why forward turrets and multiple attackers may be needed.

## 6.8 Forward Gunner/Sentinel support

Build a forward turret only when:

- enemy Builder/defense pressure blocks progress;
- a legal useful firing lane exists;
- construction position is reachable and protectable;
- route/economy and home defense reserves remain funded;
- ammo horizon can be funded;
- the turret is expected to fire enough times to justify cost and +20% scale.

### Gunner

Use for:

- short dynamic lane;
- enemy Builders near attackers;
- position that may need one carefully justified rotation.

### Sentinel

Use for:

- long fixed line toward Core/defense;
- shooting through walls/intervening units;
- durable siege anchor.

### Forward turret state

```text
SELECT_SITE
APPROACH_SITE
BUILD
VERIFY
SUPPLY_AMMO
FIRE_SUPPORT
ABANDON_OR_HOLD
```

The turret itself executes target logic after construction. A Builder should not remain stuck “supporting” it if no maintenance is needed.

## 6.9 Retreat and regroup

Retreat trigger:

- attacker HP below threshold;
- no progress for bounded rounds;
- target stale/destroyed;
- route/home threat escalates;
- offensive budget exhausted;
- known turret exposure exceeds support;
- fewer than minimum attackers remain.

Retreat objective:

1. safe tile outside known firing lane;
2. nearest friendly defensive line;
3. home rally;
4. resume economy/defense role after cooldown.

Do not oscillate attack/retreat every round; use commitment and cooldown windows.

## 6.10 Offensive pseudocode

```python
def run_attacker(ct, state, team):
    if team.defense_mode >= DEFENSE_CRITICAL and state.is_recallable:
        state.role = DEFENDER
        state.offense_state = RETREATING
        return run_defender(ct, state, team.threat)

    objective = refresh_or_choose_objective(ct, state, team)

    if objective is None:
        state.offense_state = SCOUTING
        return run_offensive_scout(ct, state, team)

    if objective.is_building and is_adjacent(ct, objective.position):
        if can_afford_paid_attack(team.budget, objective):
            if try_builder_attack(ct, objective, team.budget):
                state.last_progress_round = team.round
                return

    if objective.requires_forward_fire_support:
        site = choose_forward_turret_site(ct, objective, team)
        if site is not None:
            return approach_or_build_forward_turret(ct, state, site, team)

    stance = choose_safe_attack_stance(ct, objective, team)
    if stance is not None:
        if move_toward_stance(ct, state, stance):
            return

    if should_replan_or_retreat(state, team):
        state.offense_state = RETREATING
        return retreat_to_rally(ct, state, team)
```

## Focused tests

1. scout publishes a verified enemy Core with epoch;
2. stale unverified target expires;
3. attackers do not overwrite the offense leader's shared target;
4. Builder approaches adjacent stance, not target tile;
5. Builder never attacks an enemy Builder;
6. Builder attacks a legal adjacent Conveyor when budget permits;
7. attack is denied when it violates economy/defense reserve;
8. Splitter cut target outranks isolated Conveyor;
9. active Conveyor outranks irrelevant empty infrastructure;
10. Harvester outranks non-critical Barrier;
11. blocking turret can outrank Harvester;
12. Core becomes target after infrastructure is crippled;
13. direct Core-kill override works;
14. no-progress timer causes replan/retreat;
15. critical home threat recalls eligible attackers;
16. forward Gunner site has positive firing support;
17. forward turret is denied without ammo/economic budget;
18. Gunner/Sentinel choice matches geometry;
19. turret targets enemy Builder that Builder attackers cannot hit;
20. target destruction advances to next objective;
21. CPU remains bounded with many visible targets.

## Evaluation checkpoint

Purpose-built scenarios:

- one enemy Conveyor chain and Harvester;
- guarded Harvester;
- enemy Builder defending infrastructure;
- enemy turret lane;
- exposed enemy Core;
- attack interrupted by home threat;
- failed assault requiring retreat.

Then maps:

```text
duel, sprint, bridge, crossfire, sweden, twins, runestone
seeds 1, 7, 19
both sides
```

Primary metrics:

- first enemy building damage round;
- first enemy infrastructure destroyed;
- enemy Harvester/Conveyor count reduction;
- first enemy Core damage round;
- Core kill rate and kill round;
- attacker losses;
- paid Builder attack titanium;
- damage per titanium/ammo;
- home economy regression;
- home Core survival;
- no-progress/retreat frequency;
- p95/p99 CPU.

## Iteration 6 promotion gate

- at least one deterministic scenario destroys enemy logistics;
- at least one scenario damages or destroys the enemy Core;
- attackers never use illegal Builder-vs-Builder attacks;
- enemy Builders are handled through turrets/blocking/other legal means;
- offense can abort and return when home defense becomes critical;
- economy and route delivery remain within guardrails;
- no runaway paid attack spend;
- zero exception/TLE indicators.

## Rollback

Disable `ENABLE_RAIDS` and `ENABLE_FORWARD_GUNNERS`. The Iteration 5 economy/defense bot must remain fully operational.

---

# Iteration 7 — Integrated economy-first, defend-on-contact, then coordinated all-out attack strategy

## Objective

Implement the complete strategic loop requested by the user:

1. rush the closest profitable ore deposits;
2. construct working Conveyor routes back to the Core;
3. defend the Core, Harvesters, and logistics when they are actively attacked;
4. once the economy network is established, retain only two or three home defenders and transition the remaining force to offense;
5. assign otherwise idle Builders to additional profitable harvesting/logistics work;
6. dismantle the enemy economy step by step—Conveyors/Splitters, Harvesters, defending units through turrets, blocking defenses, then the Core;
7. use forward Gunners or Sentinels when direct Builder pressure is insufficient.

This iteration integrates only mechanisms that have individually passed Iterations 4–6.

## Critical mechanics correction

The requested ordering includes “attack the enemy Builder.” Builder Bots cannot directly attack enemy Builders under the supplied rules; Builder paid attacks target adjacent buildings. Therefore:

- Builder raiders attack enemy Conveyors, Splitters, Harvesters, Barriers, turrets, Launchers, and Core.
- Friendly Gunners/Sentinels target enemy Builders and other units.
- Builders may body-block or route around enemy Builders.
- Launcher ejection can be added later as a separate passed feature.

## Files allowed to change

Integration surface:

- `bots/candidate/bot/policy.py`
- `bots/candidate/bot/core.py`
- phase/role orchestration in `bots/candidate/bot/builder.py`
- `bots/candidate/bot/economy.py`
- `bots/candidate/bot/defense.py`
- `bots/candidate/bot/offense.py`
- `bots/candidate/bot/turrets.py`
- phase/role Store codec in `bots/candidate/bot/comms.py`
- enums/state in `bots/candidate/bot/types.py`
- `bots/candidate/bot/feature_flags.py`
- integration tests and phase-level evaluation tooling

Do not rewrite passed low-level navigation, action legality, route FSM, or Store codec unless an integration test proves a defect.

## Feature gate

```python
ENABLE_PHASE_STRATEGY = True
```

One flag must restore the Iteration 6 primitives without automatic phase orchestration.

## 7.1 Global strategic phases

```python
class StrategyPhase(IntEnum):
    BOOTSTRAP_ECON = 0
    FIRST_ROUTE_RUSH = 1
    ECONOMY_EXPANSION = 2
    DEFENSE_ALERT = 3
    ATTACK_PREPARATION = 4
    OFFENSIVE_PRESSURE = 5
    CORE_SIEGE = 6
    RECOVERY = 7
    ENDGAME = 8
```

Core is the only writer of global phase and phase epoch.

### Phase meaning

#### BOOTSTRAP_ECON

- spawn the minimum useful Builder team;
- discover reachable nearby ore;
- choose the closest profitable ore project;
- no discretionary combat spending;
- one scout may search while others construct.

#### FIRST_ROUTE_RUSH

- all necessary construction effort goes to the first route;
- build Core-outward so the Harvester's immediate first output has a receiver;
- keep one Builder free enough to avoid total deadlock;
- defense interrupts only on a real active threat.

#### ECONOMY_EXPANSION

- first route is delivering;
- build the next closest profitable routes sequentially;
- maintain/repair existing network;
- prepare defender reserve and offense rally;
- do not attack yet unless responding locally to an enemy building threat.

#### DEFENSE_ALERT

- temporary interrupt when Core or infrastructure is under active attack;
- retain economy-critical workers where safe;
- assign enough defenders for severity;
- build targeted defense only when valuable;
- return to prior phase after stand-down/recovery.

#### ATTACK_PREPARATION

- economy-complete gate has passed;
- freeze speculative low-payback expansion;
- select 2–3 persistent defenders;
- retain required maintenance/repair workers;
- assign all remaining eligible Builders as scouts/attackers;
- publish verified enemy Core and initial logistics target;
- fund bounded forward-turret/ammo budget.

#### OFFENSIVE_PRESSURE

- attackers move to rally and cut enemy logistics;
- economy continues in background;
- home defense remains staffed;
- idle noncombat Builders take profitable unclaimed ore projects or maintenance;
- recall only the minimum required attackers on home threat.

#### CORE_SIEGE

- enemy economy is materially weakened, or a direct Core-kill window is open;
- attackers converge on legal Core-adjacent stances;
- forward Gunner/Sentinel support suppresses enemy Builders/defense;
- preserve enough home defense to avoid counter-kill.

#### RECOVERY

- broken home route, failed assault, high attacker loss, or expired target;
- repair economy;
- heal valuable units/buildings;
- regroup attackers;
- choose whether to resume pressure or rebuild.

#### ENDGAME

- stop low-payback expansion;
- choose between:
  - immediate Core kill;
  - preserve tiebreak economy;
  - emergency defense.
- avoid wasteful attacks/ammo if no kill is plausible.

## 7.2 Economy-complete gate

“Set up all the Conveyor” must be measurable.

Define economy readiness:

```text
primary route state == MAINTAIN
and primary delivery acknowledgement is fresh
and broken critical routes == 0
and maintaining_route_count >= required_route_count(map/economy)
and total recent delivered rate >= MIN_ATTACK_ECONOMY_RATE
and free titanium >= attack_preparation_reserve
```

Initial `required_route_count`:

```text
very small maps: 1–2
medium maps: 2
large maps: 2–3
```

Use actual payback and known ore availability. Do not force three routes on a map where only one is profitable or reachable.

Add readiness hysteresis:

```text
economy_ready must remain true for ECONOMY_READY_STABLE_ROUNDS
```

This prevents switching to attack during a one-round transient status.

## 7.3 Persistent role allocation

Roles:

```text
CORE_CONTROLLER
ECONOMY_BUILDER
ROUTE_MAINTAINER
SCOUT
DEFENDER
ATTACKER
SIEGE_BUILDER
RECOVERY_WORKER
```

### Role budget after economy readiness

```text
persistent_defenders =
    2 on very small/medium map with no recent threat
    3 on large map or recent/high threat
    up to more temporarily during DEFENSE_ALERT

maintenance_workers =
    max(1, ceil(maintaining_routes / 2))
    + 1 if route exposure/churn is high

scouts =
    1 until enemy Core and economy are fresh
    0–1 after verification

attackers =
    total_builders
    - persistent_defenders
    - maintenance_workers
    - scouts
    - active critical construction workers
```

Never reduce attackers below zero. If the team is too small, spawn only when the marginal Builder is affordable and useful.

### Stable assignment

Core assigns roles by deterministic score:

```text
defenders:
    nearest to Core/critical assets
    not sole owner of active route
    healthy and reachable

maintenance:
    existing route owners
    nearest to broken/critical network

scout:
    highest unexplored-frontier value
    not critical worker

attackers:
    remaining healthy Builders
    closest to rally
```

Use role generation/epoch so a Builder can detect a real reassignment after one-round Store delay.

## 7.4 Continuous defense interrupt

Defense runs above the strategy phase:

```python
def choose_effective_phase(global_phase, defense_overlay):
    if defense_overlay == DEFENSE_CRITICAL:
        return DEFENSE_ALERT
    if defense_overlay == DEFENSE_ACTIVE:
        return DEFENSE_ALERT
    return global_phase
```

Rules:

- Do not recall all attackers for one distant scout.
- Recall nearest attackers only until required defender count is met.
- Persistent 2–3 defenders never abandon home during offensive phases unless a higher-value deterministic reassignment is made.
- Economy owner of the only delivering route remains on maintenance unless Core destruction is imminent.
- After stand-down, temporary defenders return to previous roles.

## 7.5 Idle Builder means new harvesting or maintenance

An idle Builder cannot harvest directly. It should:

```text
1. take an approved repair
2. take an approved profitable unclaimed ore project
3. inspect/maintain a stale route
4. scout useful frontier
5. reinforce offense if economy-ready and attack force below target
6. stage safely
```

This satisfies the intent that Builders not engaged in attack or defense should grow the economy.

## 7.6 Enemy dismantling sequence

### Stage A — cut logistics

Priority:

```text
1. loaded or Harvester-adjacent Conveyor
2. high-connectivity Splitter/junction
3. last-mile Conveyor into enemy Core
4. long exposed Conveyor segment whose loss isolates a route
```

Goal:

- stop titanium delivery;
- force enemy repair Builders away from combat;
- reduce future turret/ammo/building capacity.

### Stage B — destroy Harvesters

After a route is cut or a Harvester is exposed:

- approach an adjacent stance;
- budget paid Builder attacks;
- destroy the Harvester;
- avoid spending more titanium than the prevented expected output unless it enables a Core kill.

### Stage C — neutralize enemy Builders and defenses

Mechanics-aware:

- forward Gunners/Sentinels fire on enemy Builders;
- attackers destroy enemy turrets/Barriers/Launchers when they block progress;
- use body-blocking only when safe and deterministic;
- do not attempt illegal Builder-vs-Builder attacks.

### Stage D — Core siege

Enter when:

```text
enemy Core verified
and either:
    enemy economy sufficiently disrupted
    or direct kill window exists
and minimum home defense maintained
and offensive budget available
```

Use:

- multiple Builder attack stances;
- forward turret lines;
- target focus to avoid spreading 2-damage Builder attacks across many buildings;
- retreat/recovery if no progress.

## 7.7 Attack objective state machine

```text
SELECT_NETWORK_TARGET
RALLY
APPROACH_TARGET
ATTACK_TARGET
VERIFY_DESTRUCTION
SELECT_NEXT_TARGET
CLEAR_DEFENSE
APPROACH_CORE
SIEGE_CORE
RETREAT
REGROUP
```

Transition pseudocode:

```python
def update_attack_objective(team, observations):
    objective = team.current_objective

    if objective is None or objective.is_stale:
        objective = choose_best_network_target(observations)

    if objective and objective.destroyed:
        objective = choose_next_target(observations)

    if no_high_value_network_target(observations):
        blocker = choose_blocking_defense(observations)
        if blocker:
            objective = blocker
        elif core_is_verified(observations):
            objective = enemy_core_target(observations)

    publish_objective_single_writer(objective)
```

## 7.8 Core strategic controller pseudocode

```python
def choose_strategy_phase(ct, team):
    snapshot = collect_team_snapshot(ct, team)
    defense = update_defense_overlay(ct, team)

    if defense.mode >= DEFENSE_ACTIVE:
        return StrategyPhase.DEFENSE_ALERT

    if snapshot.round >= ENDGAME_START:
        return StrategyPhase.ENDGAME

    if not snapshot.first_route_delivering:
        if snapshot.first_project_assigned:
            return StrategyPhase.FIRST_ROUTE_RUSH
        return StrategyPhase.BOOTSTRAP_ECON

    if snapshot.broken_critical_routes:
        return StrategyPhase.RECOVERY

    if not economy_ready_for_attack(snapshot):
        return StrategyPhase.ECONOMY_EXPANSION

    if not snapshot.enemy_core_fresh or not snapshot.attack_roles_assigned:
        return StrategyPhase.ATTACK_PREPARATION

    if direct_core_kill_window(snapshot):
        return StrategyPhase.CORE_SIEGE

    if snapshot.attack_force_healthy:
        return StrategyPhase.OFFENSIVE_PRESSURE

    return StrategyPhase.RECOVERY
```

## 7.9 Builder controller pseudocode

```python
def run_builder_by_phase(ct, state, team):
    # Immediate legal local survival/support action.
    if try_critical_heal_or_local_asset_protection(ct, state, team):
        return

    effective_phase = choose_effective_phase(
        team.strategy_phase,
        team.defense_mode,
    )

    role = read_fresh_role_assignment(ct, state)

    if effective_phase == DEFENSE_ALERT:
        if role == DEFENDER or state.is_temporarily_recalled:
            return run_defender(ct, state, team)
        return continue_critical_economy_task(ct, state, team)

    if role in (ECONOMY_BUILDER, ROUTE_MAINTAINER, RECOVERY_WORKER):
        if run_assigned_economy_or_repair(ct, state, team):
            return

    if role == SCOUT:
        return run_strategic_scout(ct, state, team)

    if role in (ATTACKER, SIEGE_BUILDER):
        return run_attacker(ct, state, team)

    # Productive idle fallback.
    project = request_or_read_profitable_project(ct, state, team)
    if project:
        return run_project(ct, state, project)

    if team.strategy_phase in (OFFENSIVE_PRESSURE, CORE_SIEGE):
        return move_to_offensive_rally(ct, state, team)

    return safe_frontier_or_staging_move(ct, state, team)
```

## 7.10 Forward Gunner/Sentinel use

“Can use Gunners if needed” becomes a scored support decision.

Build forward fire support when:

```text
enemy Builders repeatedly block assault
or enemy defensive turret prevents adjacent Builder attacks
or a fixed line to Core has high expected shots
```

Require:

```text
economy routes healthy
home defenders staffed
forward turret construction cost funded
ammo horizon funded
positive placement score
Builder available without abandoning critical maintenance
```

Prefer:

- Gunner for short lanes and enemy Builder control;
- Sentinel for long fixed siege line or wall penetration.

Do not build a chain of turrets merely because the phase is offensive.

## 7.11 Strategy parameters to start with

These are initial test values, not immutable rules:

```text
PERSISTENT_DEFENDERS_SMALL = 2
PERSISTENT_DEFENDERS_LARGE = 3
MIN_MAINTENANCE_WORKERS = 1
MAX_SIMULTANEOUS_ECON_PROJECTS = 1
ECONOMY_READY_STABLE_ROUNDS = 8
ATTACK_NO_PROGRESS_ROUNDS = 20
OFFENSE_REGROUP_ROUNDS = 12
THREAT_STANDDOWN_ROUNDS = 8
MIN_ATTACKERS_TO_PRESS = 2
ENDGAME_START = 850
```

Luna must expose them in one constants/policy location and evaluate, not scatter magic numbers.

## 7.12 Integration tests

### Phase transitions

1. no route → `BOOTSTRAP_ECON`/`FIRST_ROUTE_RUSH`;
2. first route delivers but expansion remains profitable → `ECONOMY_EXPANSION`;
3. economy-ready remains true for stable window → `ATTACK_PREPARATION`;
4. verified enemy target and roles ready → `OFFENSIVE_PRESSURE`;
5. direct Core-kill window → `CORE_SIEGE`;
6. broken home route → `RECOVERY`;
7. active threat overrides attack with `DEFENSE_ALERT`;
8. stale threat returns to prior phase;
9. round cutoff selects `ENDGAME`.

### Role allocation

10. exactly 2 persistent defenders on small safe map;
11. exactly 3 on large/recently threatened map;
12. critical threat can temporarily allocate more;
13. at least one maintenance worker remains;
14. remaining eligible Builders become attackers;
15. idle Builder receives profitable harvesting project;
16. no duplicate project assignment;
17. role generation survives one-round Store delay;
18. dead/stale owner is replaced.

### Combat sequence

19. attackers cut active Conveyor before distant Core;
20. Splitter/junction outranks irrelevant Conveyor;
21. Harvester follows route cut;
22. enemy Builder is targeted by turret, not Builder attack;
23. blocking turret is removed before unsafe Core approach;
24. Core becomes final objective;
25. direct Core-kill override bypasses unnecessary sabotage;
26. paid attacks stop at budget limit;
27. forward Gunner builds only with positive support value;
28. home critical threat recalls the nearest needed attackers;
29. two or three persistent defenders remain home during attack;
30. recovery repairs route and can later resume offense.

### Reliability

31. no phase oscillation within hysteresis window;
32. no Builder remains permanently roleless;
33. no full-map scan per unit every turn;
34. p99 remains below 8 ms on worst-case fixture;
35. fixed seed yields deterministic phase/role/objective sequence;
36. feature flag off restores Iteration 6 behavior.

## 7.13 Evaluation program

### Stage 1 — deterministic scenario tests

Create or reuse maps/fixtures for:

- closest ore with short route;
- two ore choices, one closer but blocked/unprofitable;
- enemy Builder rush during first-route construction;
- attack on Harvester/Conveyor;
- economy completes then phase switches;
- enemy Conveyor→Harvester chain;
- enemy Builder defending network;
- blocking Gunner/Sentinel;
- exposed Core;
- home counterattack during siege;
- failed assault and recovery.

### Stage 2 — local paired matrix

Maps:

```text
sprint, string, duel,
bridge, showdown,
crossfire, atoll,
sweden, twins, runestone,
vault, aurora, longship
```

Seeds:

```text
1, 7, 19, 43, 101
```

Both sides. Compare against the latest passed Iteration 6 snapshot.

### Stage 3 — full release matrix

Only after Stage 2 passes:

```text
21 maps × 5 seeds × 2 sides = 210 games
```

Then remote server gate.

## 7.14 Metrics

### Economy

- first route delivery rate;
- first/second/third route completion;
- titanium collected at 100/250/500/1000;
- route uptime;
- churn;
- Builder count/scale;
- idle-Builder productive assignment rate.

### Defense

- own Core survival;
- first response latency;
- critical asset damage;
- persistent versus temporary defender count;
- route production during attack;
- defense spend.

### Offense

- phase-switch round;
- attackers deployed;
- first enemy Conveyor damage/destruction;
- first Harvester destruction;
- enemy Builder kills by turret;
- first enemy Core damage;
- Core kill rate/round;
- paid attack spend;
- forward turret value;
- retreat/recovery rate.

### Overall

- game and series score;
- win by Core kill versus collection tiebreak;
- map/side stratification;
- exception/TLE count;
- p95/p99/max CPU.

## 7.15 Promotion gates

Do not activate live unless:

1. Iterations 3R–6 remain passed.
2. First-route delivery does not regress.
3. Economy-ready phase transition occurs on appropriate maps.
4. The bot creates actual enemy damage in deterministic scenarios.
5. It can destroy logistics and damage the Core.
6. It preserves 2–3 home defenders as configured.
7. Idle Builders take economy/maintenance work rather than wandering.
8. Critical defense interrupts offense correctly.
9. Full local matrix has no catastrophic map class.
10. Zero systematic exception/TLE.
11. Remote gate passes.
12. Previous live version and rollback command are recorded.

## 7.16 Rollback

- Disable `ENABLE_PHASE_STRATEGY`.
- Reactivate the last passed Iteration 6 behavior locally.
- For live deployment, reactivate the previous known-good platform version.
- Preserve the failed replays and classify whether the regression was:
  - phase timing;
  - role allocation;
  - economy starvation;
  - defense under-allocation;
  - offense overspending;
  - target selection;
  - CPU;
  - map-specific.

---

# Cross-iteration engineering rules

## Current implementation order

```text
Iteration 3R: unblock and prove the first route
Iteration 4: stable multi-route economy
Iteration 5: reactive defense
Iteration 6: offensive primitives
Iteration 7: integrated economy → defense interrupt → attack phase strategy
```

Never skip the Iteration 3R gate merely because later strategic work is more interesting.

## One Luna session can execute multiple iterations, but checkpoints remain mandatory

A single Luna XHigh session may continue through multiple iterations only when:

1. the current iteration's focused/static/behavior gates pass;
2. `UPDATES.md` and project state are updated;
3. a clean Git checkpoint or immutable snapshot is created;
4. the next iteration is restated before editing;
5. no failed iteration is carried forward.

Recommended grouping:

```text
Session A: Iteration 3R only
Session B: Iteration 4
Session C: Iteration 5–6 if context remains clean and each checkpoint passes
Session D: Iteration 7 integration
```

Iteration 7 should not share an un-compacted context with a long failed Iteration 3 diagnosis.

## Required evidence after every Luna checkpoint

Luna returns:

```text
objective
files changed
behavior changed
behavior deliberately unchanged
tests and exact return codes
report/replay paths
primary metric versus comparator
CPU/reliability findings
remaining risks
checkpoint/hash
whether next iteration is authorized
```

Full logs stay under `reports/`.

## No silent mechanics violations

- Builders move cardinally.
- Build/attack/heal/destroy targets are orthogonally adjacent.
- Builder attack targets buildings, not enemy Builders.
- Paid Builder attack costs 2 Ti and deals 2 damage.
- Spawn and normal action cooldown interact normally; ammo conversion is separate.
- Dynamic costs come from API getters.
- Store writes are one-round delayed.
- Uncaught exceptions permanently destroy the unit.
- p99 target remains below 8 ms.

## Experiment isolation

Do not combine:

- route unblocking with expansion policy;
- economy scaling with defense;
- defense with offense;
- offensive primitives with global phase integration.

Iteration 7 is the intentional integration experiment only after those components pass independently.

## Release discipline

1. focused tests;
2. `make static`;
3. smoke;
4. selected regression;
5. immutable snapshot;
6. full 21-map matrix for release candidate;
7. remote server test;
8. upload without activation;
9. activate during observation window;
10. promote or roll back using recorded live state.
