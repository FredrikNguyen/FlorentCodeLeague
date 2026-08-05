# Florent Code League: current rules and gameplay reference

**Verified:** 2026-08-05  
**Coverage:** public docs, all tutorial series, public changelog, current maps page, and relevant competition terms.

This is an engineering reference, not a replacement for official announcements. The game can change during the competition. When this file conflicts with the latest official changelog or observed engine behavior, update this file and follow the newer authority.

---

## 1. Objective and match format

Florent Code League is a two-team programming game on a rectangular 2D grid. Each team controls:

- one stationary **Core**;
- mobile **Builder Bots** spawned by the Core;
- stationary turrets and infrastructure built by Builders.

Your Python `Player` class is instantiated separately for every unit. The engine calls that unit instance's `run(ct)` once per round. The `Controller` is the only supported interface to game state and actions.

### Winning

A team wins immediately when it destroys the opposing Core.

A game lasts at most **1000 rounds**. If both Cores survive, current public docs use these tiebreakers, in order:

1. most titanium collected;
2. most Harvesters;
3. most titanium stored;
4. coin flip.

Treat the exact name of the first statistic as platform-defined: some official AI-context wording has used “delivered to Core,” while the main current rules say “collected.” The practical strategy is the same: build a functioning economy and deliver/collect output rather than merely placing structures.

### Series and ladder

- A ladder match is a **five-game series**; all five games are played.
- Five maps are selected from the current competition pool.
- Series outcome is the fraction of games won. For Elo, 3–2 is treated as `0.6`, 4–1 as `0.8`, and so on.
- New teams start at **1500 Elo**; the documented K-factor is **32**.
- Ladder matches are rated. Local matches, remote test matches, and unrated challenges are not.
- The scheduler runs regularly; current docs describe a roughly ten-minute scheduling cadence.
- Only the team's **active submission** plays ladder matches.
- Local and server performance can differ. The server runs on AWS Graviton3 and enforces the CPU limit.

---

## 2. Map and coordinate model

### Coordinates

- `(0, 0)` is the northwest corner.
- `x` grows east.
- `y` grows south.
- `NORTH` is `(0, -1)`.
- Maps are currently between **8×8 and 30×30**.

Terrain:

- `Environment.EMPTY`: traversable ground.
- `Environment.WALL`: impassable and blocks Gunner line of sight.
- `Environment.ORE_TITANIUM`: passable to a Builder until a Harvester occupies it.

### Current map pool

The public map page lists **21 maps**. Ladder and unrated series draw five at random. Always run `fcode maps sync` before an evaluation campaign.

| Map | Size | Area | Aspect | Symmetry |
|---|---:|---:|---|---|
| atoll | 18×18 | 324 | square | rotational |
| aurora | 26×26 | 676 | square, large | rotational |
| bridge | 21×8 | 168 | very wide | horizontal |
| crossfire | 16×16 | 256 | square | rotational |
| duel | 12×12 | 144 | small square | rotational |
| fjord | 20×20 | 400 | square | rotational |
| hive | 25×25 | 625 | square, large | rotational |
| jackpot | 16×16 | 256 | square | rotational |
| longship | 28×20 | 560 | wide, large | rotational |
| pinch | 14×18 | 252 | tall | rotational |
| quarry | 24×24 | 576 | square, large | rotational |
| runestone | 24×24 | 576 | square, large | rotational |
| showdown | 16×12 | 192 | wide | horizontal |
| skerry | 22×22 | 484 | square | rotational |
| sprint | 10×10 | 100 | very small | rotational |
| strait | 20×26 | 520 | tall, large | rotational |
| string | 12×8 | 96 | very small/wide | rotational |
| sweden | 25×15 | 375 | wide | vertical |
| twins | 21×21 | 441 | square | rotational |
| vase | 11×16 | 176 | tall | horizontal |
| vault | 24×24 | 576 | square, large | rotational |

Dimensions and symmetry are not enough to infer walls or ore placement. Sync and inspect the actual `.map26` files. Preserve retired maps locally because `maps sync` adds/updates but does not remove maps that leave the rotation.

### Map implications

At minimum, strategy must adapt to:

- **travel scale:** early rush distance and infrastructure payback differ sharply between 10×10 and 26×26;
- **aspect ratio:** long corridors alter Gunner/Sentinel value and congestion;
- **symmetry:** useful for priors about enemy Core/ore, but never substitute a prior for sensing;
- **chokepoints:** barriers, Gunners, and route redundancy become more valuable;
- **route length:** long conveyor chains cost more and create more cut points;
- **ore topology:** number, distance, and defensibility of deposits should drive expansion order.

---

## 3. Execution, turns, CPU, and failure behavior

### Unit instances and order

- The engine creates one `Player` object per unit.
- Per-unit instance fields persist across that unit's turns.
- Units run in spawn/creation order.
- Buildings with bot behavior, including turrets, also receive turns.
- Harvesters and conveyor mechanics operate automatically and do not consume your bot's CPU.

### CPU limit

- Ladder: **10 ms CPU per unit per round**.
- The engine maintains a small documented time bank of roughly **5%**.
- A timeout skips that unit's action for the turn; it may act again next round with a fresh allowance.
- Local `fcode run` has no limit unless `--tle 10` is supplied.
- Use `ct.get_cpu_time_elapsed()` for microsecond-level checks.

Design for p99 below 8 ms, not merely average below 10 ms. Repeated full-map scans, repeated BFS per unit, deep copies, large debug output, and unbounded retries are common failure modes.

### Exceptions

An uncaught exception escaping `run()` **permanently destroys that unit for the rest of the game**. This differs from a CPU timeout.

Production code should:

- check every action with its matching `can_*`;
- keep a narrow top-level safety boundary;
- avoid using exceptions as normal control flow;
- record or draw diagnostics without raising again;
- test malformed/stale state transitions.

---

## 4. Resources and cost scaling

### Titanium

Titanium is the only economic resource.

- Official AI context currently lists **500 starting titanium**.
- Passive income: **10 Ti every 4 rounds**.
- Harvesters add 10-Ti stacks every 4 rounds.
- Every unit/building purchase spends titanium.
- Builder attacks cost titanium.
- Healing costs titanium.
- Ammunition is created from titanium 1:1.

Opening balance is a rule most likely to be changed during balancing. Query current resources and affordability rather than designing around a hard-coded bank.

### Global ammunition

- Teams begin with **0 ammo**.
- There is no passive ammo.
- The Core calls `convert_ammo(amount)` to convert titanium to ammo 1:1.
- Conversion is allowed at most once per team per turn.
- Converted ammo is usable in the same turn.
- Conversion does not consume the Core's action cooldown.
- Gunners spend 4 ammo/shot.
- Sentinels spend 10 ammo/shot.
- Launchers use no ammo.

Ammunition is global. Turrets do not store ammo and conveyors do not feed turrets.

### Dynamic prices

Costs scale with currently live entities. Current documented base costs and each entity's contribution to cost scale are:

| Entity | Base cost | Scale contribution |
|---|---:|---:|
| Builder Bot | 30 | +20% |
| Gunner | 20 | +20% |
| Sentinel | 30 | +20% |
| Launcher | 20 | +10% |
| Harvester | 20 | +5% |
| Conveyor | 3 | +1% |
| Splitter | 6 | +1% |
| Barrier | 3 | +1% |

Destroying an entity removes its contribution. Do not reproduce the price formula or rounding yourself. Use:

- `get_builder_bot_cost()`
- `get_harvester_cost()`
- `get_gunner_cost()`
- `get_sentinel_cost()`
- `get_launcher_cost()`
- `get_conveyor_cost()`
- `get_splitter_cost()`
- `get_barrier_cost()`
- `get_scale_percent()`

---

## 5. Core

| Property | Current value |
|---|---:|
| HP | 500 |
| Footprint | 2×2 |
| Vision radius² | 36 |
| Spawn range² | 2 |
| Passive income | 10 Ti / 4 rounds |
| Initial ammo | 0 |

The Core:

- is stationary and impassable, including to friendly Builders;
- spawns Builders on legal positions around its 2×2 footprint;
- converts titanium to global ammunition;
- receives delivered titanium from logistics;
- should usually act as the single writer for global strategy, budget, and ammo-policy slots.

Core API:

- `can_spawn(pos)`
- `spawn_builder(pos) -> unit_id`
- `can_convert_ammo(amount)`
- `convert_ammo(amount)`

A Core spawning a Builder consumes its action cooldown; ammo conversion does not.

---

## 6. Builder Bot

| Property | Current value |
|---|---:|
| HP | 40 |
| Base cost | 30 Ti |
| Vision radius² | 20 |
| Move cooldown | 1 |
| Action cooldown | 1 |
| Action target | orthogonally adjacent tile |

Builders are the mobile workforce. They can move, build, attack buildings, heal allies, destroy friendly buildings, and self-destruct.

### Movement

Builder movement is **cardinal only**:

- NORTH, EAST, SOUTH, WEST are legal.
- Diagonal movement raises `GameError`.
- `can_move(diagonal)` returns false.
- Use `Position.cardinal_direction_to(target)`, not `direction_to(target)`.
- A successful move prevents an action in the same round.
- A successful action prevents movement in the same round.

Passable:

- empty terrain;
- uncovered ore;
- Conveyors of either team;
- Splitters of either team.

Impassable:

- walls;
- any Builder;
- Harvesters;
- Barriers;
- either Core;
- Gunners, Sentinels, and Launchers.

### Builder actions

All of these target an orthogonally adjacent tile, never a diagonal or the Builder's own tile:

- build;
- attack/fire;
- heal;
- destroy.

Attack:

- spends **2 Ti**;
- deals **2 damage**;
- targets a building in the adjacent tile.

Heal:

- spends **1 Ti**;
- restores **4 HP**;
- heals all friendly entities on the target tile, so a friendly Builder standing on a friendly passable building can be healed together with it.

Destroy:

- removes a friendly adjacent building;
- is free;
- does not use action cooldown;
- may be called multiple times if legal;
- returns a resource stack in transit on a destroyed Conveyor/Splitter to the team's balance.

Self-destruct destroys the Builder and deals **zero damage**.

---

## 7. Buildings and logistics

### Harvester

| Property | Current value |
|---|---:|
| HP | 30 |
| Base cost | 20 Ti |
| Scale | +5% |
| Output | 10 Ti every 4 rounds |
| First output | immediately when built |
| Blocks movement | yes |
| Blocks LOS | no |
| Counts toward unit cap | no |
| Bot CPU | none |

A Harvester can only be built on an ore tile. It emits a whole 10-Ti stack to a cardinally adjacent accepting building. It chooses the least-recently-used valid output direction.

A Harvester with no accepting neighbor idles. Therefore “Harvester built” is not the same as “economy works.” Measure first delivered stack and steady-state throughput.

### Conveyor

| Property | Current value |
|---|---:|
| Base cost | 3 Ti |
| Scale | +1% |
| Storage | one 10-Ti stack |
| Speed | one tile per round |
| Input | any of 3 non-output cardinal sides |
| Output | fixed facing direction |

Conveyors move resources automatically and consume no bot CPU.

### Splitter

| Property | Current value |
|---|---:|
| Base cost | 6 Ti |
| Scale | +1% |
| Storage | one 10-Ti stack |
| Input | back only |
| Outputs | facing + left + right |
| Selection | least-recently-used output |

A Splitter does not divide a stack. It routes the entire stack among outputs. Key uses:

- redundant paths to the Core;
- branching one source toward multiple destinations;
- reducing single-tile supply-line failure;
- controlled merge/flow layouts.

Every added path can also add cost, congestion, exposure, and delay. Test delivered throughput, not visual complexity.

### Barrier

| Property | Current value |
|---|---:|
| HP | 30 |
| Base cost | 3 Ti |
| Scale | +1% |
| Blocks movement | yes |
| Blocks Gunner LOS | yes |

Barriers are cheap topology-control tools. They can protect a Core/turret, force pathing, create a firing lane, or accidentally trap friendly Builders and logistics.

---

## 8. Turrets and combat

Turrets are stationary buildings whose `Player.run()` executes each round.

### Gunner

| Property | Current value |
|---|---:|
| HP | 25 |
| Base cost | 20 Ti |
| Scale | +20% |
| Damage | 7 |
| Ammo/shot | 4 |
| Reload | 1 round |
| Vision/attack radius² | 13 |
| Pattern | single-tile forward ray |
| Rotation | yes, 10 Ti and 1-round cooldown |

The Gunner ray:

- follows its facing direction;
- skips empty tiles;
- stops at the first targetable unit/building tile;
- is blocked by walls;
- can be rotated after construction.

Current role: cheap initial turret and flexible corridor control, but fragile, scale-expensive, and less ammo-efficient than Sentinel.

### Sentinel

| Property | Current value |
|---|---:|
| HP | 40 |
| Base cost | 30 Ti |
| Scale | +20% |
| Damage | 18 |
| Ammo/shot | 10 |
| Reload | 2 rounds |
| Vision/attack radius² | 32 |
| Pattern | single-tile straight facing line |
| Rotation | no |

Sentinel fire is not blocked by walls or intervening units. It is the durable, long-range anchor. Facing is fixed at build time, so placement/facing quality matters more than reactive control.

### Launcher

| Property | Current value |
|---|---:|
| HP | 30 |
| Base cost | 20 Ti |
| Scale | +10% |
| Ammo | none |
| Damage | none |
| Reload | 1 round |
| Throw radius² | 26 |
| Facing | none |

A Launcher:

- picks up an adjacent Builder, including diagonal adjacency;
- may pick up a Builder from **either team**;
- throws it to a bot-passable destination within range;
- can reposition allies, cross obstacles, rescue stuck Builders, deliver attackers, or exile an adjacent enemy Builder.

The “either team” behavior was clarified on 2026-08-03. Old “friendly only” text is obsolete.

### Targeting helpers

Prefer API helpers over reimplementing geometry:

- `can_fire(target)`
- `fire(target)`
- `can_fire_from(pos, direction, turret_type, target)`
- `get_attackable_tiles()`
- `get_attackable_tiles_from(pos, direction, turret_type)`
- `get_gunner_target()`
- `can_rotate(direction)` / `rotate(direction)`
- `can_launch(bot_pos, target)` / `launch(bot_pos, target)`

`get_attackable_tiles()` is a raw pattern and may ignore ammo, cooldown, and occupancy; legality still comes from `can_fire`.

---

## 9. Unit cap

The documented maximum is **50 team units**, including the Core and active units that count as units. Harvesters are explicitly buildings and do not count toward the cap. Use `ct.get_unit_count()` and avoid assumptions when planning mass production.

A larger army increases:

- cost scale;
- CPU calls;
- congestion;
- coordination load;
- exposure to role-assignment bugs.

---

## 10. Vision and partial information

Useful methods:

- `get_nearby_tiles(dist_sq=None)`
- `get_nearby_entities(dist_sq=None)`
- `get_nearby_buildings(dist_sq=None)`
- `get_nearby_units(dist_sq=None)`
- `is_in_vision(pos)`
- `get_tile_env(pos)`
- `get_tile_building_id(pos)`
- `get_tile_builder_bot_id(pos)`
- `is_tile_empty(pos)`
- `is_tile_passable(pos)`
- `get_stored_resource(id=None)`
- `get_stored_resource_id(id=None)`

Do not treat an unseen tile as empty. Maintain confidence/age for remembered observations. A stale route may now contain a wall-like building, enemy turret, friendly blocker, or destroyed link.

---

## 11. Global Communication Store

Each team has **16 private non-negative integer slots**, initialized to zero.

- Reads see the snapshot from the start of the round.
- Writes are buffered and become visible next round.
- Opponents cannot read your store.
- Use named slots and encode “unknown” distinctly from legitimate zero coordinates.
- Pack coordinates as `1 + y * width + x`; reserve `0` for unknown.
- Prefer a single designated writer per slot.
- Include an epoch/round stamp for stale observations.
- Never assume multiple `read + 1` writers produce an atomic aggregate. Buffered snapshots are consistent, but last/multiple-write semantics should not be used as a counter primitive without an engine test.

Recommended ownership:

| Slots | Suggested owner | Purpose |
|---|---|---|
| 0 | Core | protocol/schema version |
| 1 | Core | strategy mode + epoch |
| 2 | designated scout | primary ore coordinate |
| 3 | designated scout | enemy Core coordinate |
| 4 | designated scout | enemy threat coordinate/type |
| 5 | logistics leader | route status/phase |
| 6 | Core | desired Builder count |
| 7 | Core | ammo target/reserve |
| 8 | defense leader | defense alert |
| 9 | offense leader | attack rally |
| 10–15 | explicit owner | claims, backup targets, diagnostics |

The exact schema belongs in `bots/candidate/bot/comms.py` and must be versioned.

---

## 12. Controller API checklist

### Movement

- `move(direction)`
- `can_move(direction)`

### Construction

- `spawn_builder(pos)`
- `can_spawn(pos)`
- `build_harvester` / `can_build_harvester`
- `build_conveyor` / `can_build_conveyor`
- `build_splitter` / `can_build_splitter`
- `build_barrier` / `can_build_barrier`
- `build_gunner` / `can_build_gunner`
- `build_sentinel` / `can_build_sentinel`
- `build_launcher` / `can_build_launcher`
- generic `build(entity_type, pos, extra=None)` / `can_build(...)`
- `destroy(pos)` / `can_destroy(pos)`

### Combat/support

- `fire(target)` / `can_fire(target)`
- `can_fire_from(...)`
- `get_attackable_tiles()`
- `get_attackable_tiles_from(...)`
- `get_gunner_target()`
- `heal(pos)` / `can_heal(pos)`
- `self_destruct()`
- `rotate(direction)` / `can_rotate(direction)`
- `launch(bot_pos, target)` / `can_launch(bot_pos, target)`

### Entity/state

- `get_position(id=None)`
- `get_entity_type(id=None)`
- `get_hp(id=None)`
- `get_max_hp(id=None)`
- `get_direction(id=None)`
- `get_id()`
- `get_team(id=None)`
- `get_vision_radius_sq(id=None)`
- `get_action_cooldown()`
- `get_move_cooldown()`
- `can_act()`
- `get_unit_count()`

### Economy

- `get_global_resources()`
- `get_global_ammo()`
- `convert_ammo(amount)` / `can_convert_ammo(amount)`
- `get_scale_percent()`
- current-cost getters listed earlier

### Map/match/debug

- `get_map_width()`
- `get_map_height()`
- `get_current_round()` — first round is **0**
- `get_cpu_time_elapsed()`
- `draw_indicator_line(...)`
- `draw_indicator_dot(...)`
- `resign(message=None)`

### Core types

Importable from `fcode`:

- `Controller`
- `Team`
- `EntityType`
- `Environment`
- `Direction`
- `Position`
- `ResourceType`
- `GameConstants`
- `GameError`

`Position` provides `add`, `distance_squared`, `direction_to`, and `cardinal_direction_to`. `Direction` provides direction transforms and `is_cardinal`.

---

## 13. Submission rules and sandbox constraints

A submission may be:

- a directory containing `main.py`;
- a single `.py` file;
- a `.zip`.

Current documented limits:

- 5 MB uploaded archive;
- 50 MB unpacked;
- 500 files;
- pure Python;
- no native extensions;
- no path traversal;
- `main.py` must expose `Player`.

Statuses include processing, ready, flagged, rejected, and error. Only a ready active version plays.

Competition terms permit AI coding tools unless an official rule says otherwise. You remain responsible for the code. Do not:

- escape or interfere with the sandbox;
- access network, filesystem, or memory outside the API;
- access or reverse-engineer another team's private submission;
- exploit platform vulnerabilities.

---

## 14. Tutorial-derived engineering lessons

The tutorials teach a progression:

1. route `run()` by entity type;
2. spawn a Builder;
3. move with `can_move`;
4. sense environment and draw replay indicators;
5. locate ore;
6. build a Harvester;
7. understand scaling and expansion;
8. build conveyor chains;
9. solve the last mile into the Core;
10. use Splitters for branching/redundancy;
11. build and operate turrets;
12. convert global ammo;
13. heal and sabotage;
14. coordinate with the 16-slot Store;
15. assign roles;
16. combine economy, logistics, and combat.

Production lessons beyond tutorial examples:

- A state machine must validate the world before assuming the previous step succeeded.
- `can_move == false` does not identify the cause; inspect action state and occupancy.
- Building consumes the round's action and blocks movement.
- Query exact building/entity state when verifying a route.
- One conveyor chain is a single point of failure.
- Multiple Builders independently chasing one target cause pileups.
- Random wandering is only a bootstrap; use bounded pathfinding and frontier selection.
- Cache static facts per unit, but age dynamic facts.
- A visible economy is not necessarily a delivering economy.
- Turrets require a global ammo budget, not a physical ammo conveyor.

### Known stale or unsafe tutorial snippets

Do not copy tutorial code blindly:

- Some coordination samples use `Position.direction_to(target)` for Builder movement. That can return a diagonal and stall/raise. Use `cardinal_direction_to`.
- One combined sample contains duplicate `CARDINALS` assignments.
- Older tutorial narrative describes an “ammo pipeline” or implies local turret feeding. Current ammo is global and created at the Core through `convert_ammo`.
- Old combat examples may contain pre-2026-08-04 Gunner/Sentinel numbers.
- Old Launcher descriptions may say “friendly Builder” only; current Launchers can throw either team.
- A zero-valued coordinate protocol fails for targets on row/column zero; pack coordinates with a sentinel offset.
- “Every bot increments a Store counter” is not a safe atomic counter design without verifying same-slot multi-writer resolution.

---

## 15. Current changelog migrations that affect code

### 2026-08-04: Gunner/Sentinel rebalance

- Gunner damage 10 → 7.
- Gunner base cost 10 → 20.
- Gunner scale +10% → +20%.
- Gunner ammo 2 → 4.
- Gunner HP 40 → 25.
- Sentinel HP 30 → 40.
- Sentinel reload 3 → 2.

Implications:

- recompute ammo reserves and kill thresholds;
- do not hard-code first-turret savings;
- expect Gunner attrition;
- revisit Sentinel use;
- account for higher turret scale;
- test old openings for economic stalls.

### 2026-08-03

- Launcher documentation corrected: either-team pickup.
- Splitter tutorial expanded for route redundancy.

### 2026-07-29

- Current maps page and `fcode maps list/sync` introduced.
- Map pool became platform-managed and can change.

### 2026-07-24

- Current round confirmed 0-indexed.
- Uncaught exceptions documented as permanent unit death.
- Destroy restricted to orthogonal adjacency.
- `ACTION_RADIUS_SQ` removed.
- `ct.can_act()` added.
- missing API methods documented.
- `--json` added to scriptable CLI commands including run, status, ladder, submissions, teams, and matches.
- `FCODE_NO_UPDATE_CHECK=1` keeps update notices out of automation output.

### 2026-07-23

- Builder build/attack/heal changed to orthogonal adjacency.
- Builder move and action became mutually exclusive.
- Sentinel changed to a single-tile-wide line.

---

## 16. Strategic interpretation

A strong bot must solve five coupled problems.

### Information

- discover terrain, ore, enemy Core, and threats;
- retain useful map memory without trusting stale occupancy;
- share only high-value observations through 16 slots.

### Economy

- choose deposits by total payback, not nearest distance only;
- construct the minimum viable route quickly;
- verify delivery;
- avoid overbuilding entities that inflate every later price;
- reserve titanium for emergency defense and ammo.

### Logistics

- produce legal directed paths;
- solve Harvester output and Core last mile;
- detect broken links and blocked outputs;
- add redundancy only when its expected survival benefit exceeds cost/latency;
- avoid Builder congestion on route tiles.

### Combat

- build the correct turret for geometry and timing;
- choose facing from actual attackable tiles;
- maintain ammo without starving construction;
- protect fragile Gunners;
- exploit Sentinel wall penetration;
- use Launchers for mobility/control rather than damage;
- attack infrastructure when cutting income is cheaper than killing the Core directly.

### Reliability

- no illegal actions or escaping exceptions;
- bounded CPU;
- deterministic behavior;
- robust across all maps, both sides, and multiple seeds;
- preserve a fallback action when a plan becomes invalid.

The implementation and evaluation plans in `docs/` turn these into staged deliverables.
