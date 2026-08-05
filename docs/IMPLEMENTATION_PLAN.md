# Detailed bot implementation plan

## Product goal

Create a deterministic, CPU-safe bot that establishes reliable titanium delivery, adapts its opening to map geometry, defends its Core, and converts economic advantage into Core pressure.

The first objective is not “cleverness.” It is a bot that never crashes, never deadlocks its economy, and exposes measurable decisions.

## Architectural principles

- One `Player` class with entity-type dispatch.
- Thin action layer: every action is legality-gated.
- Per-unit persistent local state for FSM and caches.
- Team Store only for high-value shared state.
- Single writer per Store slot.
- Separate sensing, planning, and execution.
- Plans are invalidated by observations.
- Bounded pathfinding with cache and fallback.
- Strategy chooses budgets; tactical units consume them.
- Deterministic tie-breaking.
- All dynamic costs queried.
- Hot paths avoid global scans and allocations.

## Proposed modules

```text
bots/candidate/
  main.py                  # submission entry point
  bot/
    player.py              # dispatch and safety boundary
    constants.py           # stable policy constants, no mutable prices
    types.py               # local enums/dataclasses
    comms.py               # 16-slot schema and coordinate packing
    world.py               # per-unit observations/map memory
    navigation.py          # bounded BFS/A*, fallback movement
    actions.py             # legality-gated action helpers
    core.py                # spawning, global budget, ammo
    builder.py             # role FSM
    economy.py             # ore scoring, harvester and route plans
    logistics.py           # conveyor/splitter topology and verification
    defense.py             # threat assessment and defensive building
    offense.py             # rally, sabotage, Core assault
    turrets.py             # Gunner/Sentinel/Launcher behavior
    policy.py              # map/opening/phase selection
```

The starter repository begins smaller. Split modules only when behavior and tests justify it; avoid abstraction before the first working route.

---

## Milestone 0 — current-rule lock and harness

### Deliverables

- Current rules snapshot and source precedence.
- Static package test.
- Local matrix runner.
- Remote gate and live snapshot scripts.
- Immutable package/upload/activate workflow.
- Sol/Luna/Sol agent loop.

### Acceptance

- `make doctor`, `make static`, and `make smoke` run.
- No upload/activation occurs without `--confirm`.
- Candidate package contains valid `main.py`.

---

## Milestone 1 — safe deterministic baseline

### 1.1 Dispatch and safety

Implement handlers for:

- Core;
- Builder;
- Gunner;
- Sentinel;
- Launcher;
- inert infrastructure if engine invokes it.

Top-level `run()`:

1. identify entity type;
2. call one handler;
3. catch unexpected exceptions;
4. emit bounded diagnostics;
5. return without killing the unit.

Do not swallow `BaseException`. Count repeated failures in local state and switch to a safe no-op/fallback mode.

### 1.2 Core opening

- Cache legal spawn positions.
- Spawn a small configurable Builder quota.
- Avoid filling every spawn exit.
- Reserve a minimum bank.
- Convert ammo only when combat infrastructure exists or an immediate plan requests it.
- Use actual `get_*_cost()`.

### 1.3 Builder fallback

- deterministic exploration order keyed by unit ID;
- cardinal moves only;
- no action after move;
- no move after action;
- bounded blocked-move recovery;
- no repeated illegal target.

### Acceptance

- no exceptions over all maps/seeds;
- Builders leave Core;
- p99 CPU under 2 ms;
- mirror matches deterministic for fixed seed.

---

## Milestone 2 — sensing, memory, and navigation

### 2.1 World model

Per Builder, record:

- map dimensions;
- known static terrain;
- ore positions;
- last-seen occupancy with round stamp;
- own Core anchor;
- observed enemy Core/threats;
- current goal and age.

Static terrain can be cached permanently. Dynamic occupancy must expire.

### 2.2 Shared discoveries

Define Store schema:

- schema version;
- strategy/phase;
- primary ore;
- enemy Core;
- threat;
- logistics status;
- desired unit/ammo budgets;
- rally/defense alerts.

Pack coordinates with `+1`; include epochs. Assign one writer per slot.

### 2.3 Navigation

Start with bounded BFS on known/assumed passable cells.

Requirements:

- cardinal neighbors;
- do not path through known impassable entities;
- configurable penalty for unknown tiles;
- cache by `(start, goal, obstacle_epoch)`;
- invalidate on blocked next step;
- deterministic neighbor order;
- maximum expansions bounded by map area;
- greedy/cardinal fallback if no path;
- oscillation detector.

Optimization:

- pathfinding only when goal changes or path invalidates;
- consume cached next steps;
- one BFS per active Builder at most per replan;
- optionally share static distance fields later.

### Acceptance

- coverage improves monotonically in empty-map tests;
- no diagonal action;
- blocked route recovers;
- p99 below 4 ms on 30×30;
- target on x=0/y=0 encodes correctly.

---

## Milestone 3 — minimum viable economy

### 3.1 Ore selection

Score candidate deposits by:

```text
value =
  expected_output_horizon
  - harvester_cost
  - route_cost
  - travel_time_cost
  - exposure_risk
  - congestion_penalty
```

First version can approximate with Manhattan distance and legal-route existence.

### 3.2 Harvester FSM

```text
DISCOVER → CLAIM → APPROACH_BUILD_TILE → BUILD → VERIFY → ROUTE → DELIVER → MAINTAIN
```

Rules:

- claim prevents duplicate builders;
- stand adjacent, not on target build tile;
- verify exact Harvester entity after building;
- immediately plan an accepting output;
- retry/replan on stale state;
- release claim on timeout.

### 3.3 Conveyor route

Build from a planned directed path.

Key constraints:

- each build is adjacent to Builder;
- Builder cannot move on build round;
- conveyor direction must point to next link;
- Harvester output must enter first accepting building;
- final link must be accepted by Core;
- do not infer route completion from movement failure;
- verify exact building type/direction when visible.

Build order options:

- Core outward: guarantees last mile early but delays Harvester output.
- Harvester inward: captures immediate first output only if a receiver exists.
- Hybrid: reserve full route, establish receiver/output, then connect shortest critical chain.

Test all three; choose by delivered-Ti curve, not intuition.

### Acceptance

- at least one Harvester delivers on every map where reachable ore exists;
- no duplicate first-Harvester claims;
- first-delivery and throughput metrics recorded;
- route repair after one destroyed link.

---

## Milestone 4 — economy scaling and logistics resilience

### 4.1 Expansion policy

Before second/subsequent Harvester:

- estimate marginal payback;
- include new scale on future purchases;
- preserve defense/ammo reserve;
- penalize route overlap and exposure;
- cap simultaneous construction projects.

### 4.2 Route health

- detect stored-stack backlog;
- detect non-delivery timeout;
- locate likely broken link from visible route state;
- send repair Builder;
- destroy obsolete/misdirected friendly links when beneficial;
- recover in-transit resources on deliberate teardown.

### 4.3 Redundancy

Use Splitter when:

```text
expected loss avoided > extra route cost + throughput/latency penalty
```

Prioritize redundancy on:

- long exposed routes;
- chokepoints;
- maps with easy sabotage access;
- mature high-output deposits.

### Acceptance

- second expansion only when projected payback fits horizon;
- single-link cut recovers;
- redundant route retains measurable throughput;
- scale does not explode from unused infrastructure.

---

## Milestone 5 — defense and global budgeting

### 5.1 Threat model

Classify:

- enemy Builder proximity to Core/logistics;
- observed Gunner/Sentinel firing lanes;
- route sabotage;
- Core HP trend;
- enemy economy/rush timing.

Write a compact alert with target, type, and expiry.

### 5.2 Budget allocator

Core maintains:

- construction reserve;
- emergency defense reserve;
- ammo target;
- expansion allowance;
- minimum liquidity.

Use current prices and forecast near-term shot demand.

Ammo policy example:

```text
desired_ammo =
  gunner_count * expected_gunner_shots_horizon * 4
  + sentinel_count * expected_sentinel_shots_horizon * 10
  + emergency_buffer
```

Do not convert all Ti early; ammo cannot buy economy.

### 5.3 Defensive placement

Gunner:

- short changing corridor;
- can rotate;
- cheap but fragile;
- protect from Sentinel lines.

Sentinel:

- long line;
- fixed facing;
- shoots through walls/units;
- durable anchor.

Barrier:

- block path/LOS;
- shape movement;
- avoid blocking own logistics/escape.

Launcher:

- reposition defenders;
- eject adjacent enemy Builder;
- bridge mobility gaps.

Use `get_attackable_tiles_from`/`can_fire_from` to score prospective placements.

### Acceptance

- defend scripted Builder rush without economy deadlock;
- no-ammo idle rate reduced;
- emergency response does not trap Core;
- defensive spending has explicit trigger and expiry.

---

## Milestone 6 — offense and sabotage

### 6.1 Enemy localization

- scout via frontiers and symmetry priors;
- verify enemy Core;
- store coordinate + epoch;
- avoid sending every Builder to one tile.

### 6.2 Attack modes

- **economic pressure:** cut exposed conveyors/splitters/harvesters;
- **Builder raid:** adjacent attacks on valuable buildings;
- **turret siege:** establish facing lines;
- **Launcher insertion:** throw friendly Builder past obstacle/defense;
- **direct Core push:** only when expected damage outruns defense/economy opportunity.

### 6.3 Force allocation

Assign:

- scout;
- economy builder;
- logistics repair;
- defender;
- raider;
- siege builder.

Prefer stable role identity from unit ID plus strategy phase. Avoid race-prone “everyone increments a counter” assignment.

### Acceptance

- attacks do not consume the economy reserve unintentionally;
- rally points prevent tile pileup;
- offense falls back when target is stale/blocked;
- sabotage has measurable enemy delivery impact.

---

## Milestone 7 — map-adaptive openings

Build descriptors from synced map:

- width/height/area;
- Core-to-nearest-ore estimate after sensing;
- number of nearby ore deposits;
- corridor/chokepoint score;
- expected enemy distance;
- route exposure;
- symmetry class.

Opening families:

1. **compact pressure:** small maps, short enemy distance, fast defense/offense.
2. **balanced economy:** medium maps, one reliable deposit then defense.
3. **wide expansion:** large maps, more scouts and staged logistics.
4. **chokepoint control:** early Sentinel/Barrier geometry.
5. **anti-rush:** reserve and Core-ring defense when enemy approach is short.

Do not hard-code map names until behavior-based descriptors are stable. Map-specific overrides are last resort and require dedicated tests.

### Acceptance

- opening selection logged in replay;
- no map class catastrophic;
- descriptors explain decisions;
- override removal does not reveal hidden dependence.

---

## Milestone 8 — tactical optimization

Candidates:

- threat-aware movement;
- reservation of next tiles to reduce friendly collision;
- attack/heal expected-value decisions;
- turret target prioritization;
- Gunner rotation lookahead;
- Sentinel line placement;
- Launcher destination scoring;
- route-repair prioritization;
- late-game tiebreak optimization.

Implement one at a time with paired evaluation.

---

## Milestone 9 — CPU and robustness hardening

Profile:

- sensing frequency;
- pathfinding expansions;
- object allocations;
- list sorting;
- repeated API calls;
- logging;
- map-size worst cases.

Techniques:

- local variables for hot API results;
- precomputed direction tuples;
- fixed-size arrays where useful;
- incremental map updates;
- bounded queues;
- no recursion;
- no all-pairs pathfinding in `run`;
- draw/log only under debug flag;
- early return after action.

Fault injection tests:

- target destroyed;
- route occupied;
- no affordable action;
- Store target stale;
- all adjacent spawn/build positions blocked;
- no ore in vision;
- unit thrown by Launcher;
- unit at map edge;
- no ammo;
- TLE budget nearly exhausted.

### Acceptance

- p99 < 8 ms, max investigated;
- no uncaught exceptions;
- deterministic fixed-seed replay hash where engine permits;
- full 21-map matrix passes.

---

## Experiment backlog

Rank by expected value / implementation risk:

1. cached BFS versus greedy movement;
2. route verification and last-mile fix;
3. ore claim protocol;
4. economy payback gating;
5. Core ammo reserve policy;
6. current Gunner/Sentinel mix;
7. route repair;
8. Splitter redundancy;
9. threat-aware defense placement;
10. enemy logistics sabotage;
11. Launcher ally insertion/enemy ejection;
12. map-descriptor opening selection;
13. tiebreak-aware late game.

Each experiment gets one plan, one version, one primary metric, and explicit rollback.
