# Florent Code League — Next Iterations Plan

**Planning basis:** the uploaded `v0003_entrypoint-class_20260805-1805_2de8371f` submission archive and the uploaded planning packet.  
**Important:** the planning packet's embedded candidate source is stale. The archive already contains 17 bot files and substantially more functionality than the starter shown in the packet. Luna must inspect the actual repository source before editing and must not reimplement the obsolete starter milestone.

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

# Iteration 4 — Correct Core economy, spawning, budget, and ammunition

## Objective

Turn the proven first route into a stable economy while preventing spawning, expansion, and ammo conversion from starving each other.

## Files allowed to change

- `bot/core.py`
- `bot/economy.py`
- budget/status portions of `bot/comms.py`
- limited `bot/builder.py` expansion gating
- Core/economy tests

## Required changes

### A. Cache opening analysis

`_observed_opening()` currently performs repeated sensing work every Core round.

- Compute the initial descriptor during a bounded early window.
- Recompute only on a fixed low frequency or when a meaningful new observation exists.
- Do not derive full-map conclusions from Core-local vision.
- Keep “enemy distance unknown” distinct from “enemy far away.”

### B. Spawn policy

- Count desired Builders as Builders, not Core plus Builders.
- Preserve at least one legal Core exit.
- Stop spawning when a candidate route cannot be funded.
- Replace dead assignment owners when unit count falls.
- Record spawn role/assignment deterministically.

### C. Budget policy

Budget should be based on the actual active project:

- remaining Conveyor count × current Conveyor cost;
- current Harvester cost;
- emergency defense reserve;
- liquidity reserve;
- planned ammo demand;
- no generic “four Conveyors” reserve for a 15-cell route.

Expansion is allowed only when:

```text
remaining expected delivered Ti
> exact marginal construction cost
+ added scale cost estimate
+ reserves
```

Start with a maximum of one active expansion beyond the proven route.

### D. Ammunition

- Ammo conversion may occur in the same Core turn as spawning because conversion does not consume the action cooldown.
- Do not condition conversion on `not turn.acted`.
- Do not count only turrets in Core vision.
- Publish turret/ammo demand through Store or maintain a conservative demand report from designated builders/turrets.
- Convert only the deficit up to a horizon target.
- Preserve route completion and emergency liquidity.
- Before round 850, avoid converting all free titanium.
- In endgame, respect the tiebreak policy and avoid useless conversion.

## Tests

1. Spawn and ammo conversion can both occur in one Core turn when legal.
2. No ammo conversion occurs with zero turret demand.
3. Remote turret demand is included.
4. Route completion reserve uses remaining exact links.
5. Builder spawning stops before starving the first route.
6. One expansion starts only after the first route is maintaining.
7. Dead assignment owner becomes replaceable.
8. Unknown enemy distance does not select anti-rush by accident.
9. Core hot path remains bounded.

## Evaluation

Compare against the Iteration 3 economy-only baseline:

- first-delivery rate must not regress;
- delivered Ti at rounds 100/250/500;
- route completion round;
- second Harvester payback;
- unspent bank;
- cost scale;
- no-ammo turret idle rate;
- p99 Core CPU.

---

# Iteration 5 — Re-enable defense and fix turret economics

## Objective

Add reliable threat-triggered defense without sacrificing the proven economy or wasting titanium/ammo.

## Files allowed to change

- `bot/defense.py`
- defensive portions of `bot/builder.py`
- `bot/turrets.py`
- ammo-demand reporting
- focused combat tests

Keep redundancy, raids, and Launcher construction disabled initially.

## Required changes

1. **Enemy Core must always have top fire priority** when it is legally attackable, unless an explicit one-shot survival rule is proven.
2. Remove double-counting that makes a Harvester exceed Core priority.
3. Gunner rotation:
   - compare current-facing score with alternative-facing score;
   - rotate only for a strictly positive expected improvement;
   - require a titanium reserve check;
   - never rotate merely because all directions tie at zero.
4. Early defense:
   - do not hard-code “no turret before round 240”;
   - trigger from verified close threat, Core damage, or firing line;
   - retain a cooldown/hysteresis so one sighting does not cause overspending.
5. Placement:
   - preserve Core exits;
   - preserve route cells;
   - preserve at least one Builder escape tile;
   - require the selected orientation to attack the actual threat or a valuable lane.
6. Gunner versus Sentinel:
   - Gunner for short/changing corridors when rotation cost is justified;
   - Sentinel for fixed long/wall-crossing lines;
   - current costs/ammo must be queried or read from current constants.
7. Demand reporting:
   - every live turret should contribute to global ammo target without depending on Core vision.

## Tests

- Core beats Harvester in target priority.
- No-target Gunner does not rotate.
- Rotation occurs only when expected target value improves enough to justify 10 Ti.
- Early close Builder rush can trigger defense before round 240.
- Defense never blocks all Core exits.
- Defense never builds on the route.
- No defensive purchase violates route/liquidity reserve.
- Sentinel/Gunner choice matches tested geometry.
- Turret demand reaches Core across Store delay.

## Evaluation

Run scripted rush/defense scenarios first, then:

```text
sprint, duel, bridge, crossfire, vault
seeds 1, 7, 19
both sides
```

Guardrails:

- first-delivery rate unchanged;
- no increase in route completion failures;
- defense spend tied to verified threats;
- damage per ammo and turret survival improve;
- no TLE.

---

# Iteration 6 — Only after the above: offense, Launcher, redundancy, and map adaptation

This is intentionally deferred. Implement these as separate experiments, not one patch.

Recommended order:

1. **Shared verified enemy-Core target**
   - scout writes coordinate + epoch;
   - raiders actually navigate to rally;
   - stale target expires.
2. **Infrastructure sabotage**
   - approach adjacent attack stance;
   - prioritize Harvester/Splitter/loaded Conveyor;
   - preserve economy reserve.
3. **Launcher**
   - enable only after deterministic destination tests;
   - allied insertion must produce positive progress;
   - enemy ejection must improve Core/logistics safety;
   - bound candidate destinations more tightly than a 32×8 brute-force scan if CPU requires.
4. **Route redundancy**
   - only on mature, exposed, high-output routes;
   - prove branch direction and Splitter input/output semantics;
   - compare expected avoided loss against scale and latency.
5. **Map-adaptive openings**
   - use measured descriptors from synced map files or accumulated sensing;
   - do not classify an entire map from one Core vision snapshot;
   - add map-name overrides only as a last resort.
6. **Late-game tiebreak policy**
   - stop non-payback builds;
   - preserve delivered/collected titanium;
   - avoid useless ammo conversion and paid attacks;
   - pursue a Core kill only when near-term kill probability is verified.

Each item should have its own candidate version and paired evaluation.

---

# Cross-iteration engineering rules

## Do not combine experiments

One version should answer one causal question. In particular, do not combine:

- navigation cache rewrite with Store schema rewrite;
- route FSM rewrite with turret tuning;
- ammo policy with Launcher behavior;
- map adaptation with broad role changes.

## Required evidence after every Luna session

Luna must return:

```text
Files changed
Behavior changed
Behavior deliberately unchanged
Focused tests run and result
Smoke/regression commands and result
Report/replay paths
CPU/reliability observations
Known remaining risks
Git diff summary
```

Full logs belong in `reports/`, not in chat.

## Promotion ladder

1. Focused unit tests.
2. `make static`.
3. Four-game smoke.
4. Selected regression maps, both sides.
5. Full 21-map local matrix only for a release candidate.
6. Remote server test only after local release gate.
7. Upload without activation.
8. Activate during an observation window with previous version recorded.
9. Promote or roll back based on defined metrics.

---

# Exact first Luna XHigh task

Copy the following into `docs/CURRENT_PLAN.md` for the first implementation session after Iteration 0 baseline capture:

## Objective

Fix Builder navigation so construction targets are approached from legal orthogonal adjacency, paths are reused across movement turns, and static route planning does not restart because of transient Builder occupancy.

## Allowed files

- `bots/candidate/bot/navigation.py`
- `bots/candidate/bot/world.py`
- navigation-related sections of `bots/candidate/bot/builder.py`
- `bots/candidate/bot/actions.py`
- focused tests only

## Required behavior

1. Add separate move-to-tile and move-to-adjacent navigation.
2. Make route/Harvester/repair construction use move-to-adjacent.
3. Replace `(start, goal, epoch)` cache semantics with one reusable active path per unit.
4. Split transient navigation blockage from permanent route-layout blockage.
5. Make route planning use permanent-layout changes only.
6. Correct `TurnActions.destroy()` so it does not consume the wrapper action.
7. Preserve cardinal movement, action gating, deterministic tie-breaking, and CPU cutoff.
8. Do not change Store layout, budgets, roles, defense, offense, or route economics.

## Required tests

- adjacency target is never entered;
- already-adjacent target needs no movement;
- path reused for at least two subsequent steps;
- blocked next step replans once;
- transient Builder movement does not reset static route search;
- permanent obstacle does reset it;
- 30×30 BFS bounded to 900 expansions;
- CPU cutoff returns safely;
- destroy does not set `acted`;
- static tests and smoke pass.

## Completion output

Return a concise implementation summary, exact commands/results, report paths, cache/replan observations, remaining risks, and diff summary. Do not spawn subagents and do not run the full map matrix.
