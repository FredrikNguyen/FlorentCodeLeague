# karrigan — how it works

This is the v0047 Florent Code League bot (`bots/baseline/`). It's a Battlecode-style
game: `Player.run(ct)` gets called once per round for *every living unit* on
our team (core, builder bots, gunners), and each unit type needs different
logic. This doc explains the current design so you can jump in and iterate
without re-deriving it from the code.

If you haven't read it yet, read `AGENTS.md` at the repo root first — it's the
full game/API reference (entities, costs, the `Controller` methods, compass
convention, etc.). This doc assumes you already know that and just explains
*our* bot's decisions on top of it.

## File layout

```
main.py         Entry point: Player class, per-unit state, run() dispatch
bot/constants.py    Every tuning knob + communication-store slot map
bot/util.py         Stateless store-position and adjacency helpers
bot/navigation.py   Shared BFS pathing + enemy-fire-line detection
bot/core_role.py    CORE spawning, ammo, and home-turret sizing
bot/defender.py     DEFENDER economy and home-turret building
bot/attacker.py     ATTACKER enemy-core/economy pressure
bot/dynamic.py      DYNAMIC per-round task selection
```

Two companion docs live here too: `DESIGN_dynamic_builders.md` (why the
dynamic pool is built the way it is) and `STRATEGY_ALIGNMENT.md` (how the
repo-root `STRATEGY.md` spec maps onto this code, including open gaps).

`Player` (in `main.py`) is composed from mixins in `bot/`:
`Player(CoreMixin, DefenderMixin, AttackerMixin, DynamicMixin, NavigationMixin)`. All of
them share one `self` — there's no per-role object, just methods grouped into
files by concern. Every unit gets its **own** `Player` instance that persists
for that unit's whole lifetime (so `self.foo` set in round 5 is still there in
round 50), but two different units (e.g. two builders) never share state
directly — the *only* way units coordinate is the 16-slot communication store
(see below) or by looking at what's physically on the map.

## The big picture

- **Core**: spawns builder bots in two stages (see below), keeps a small
  ammo buffer topped up, and decides how many home-defense turrets we want
  (2–5, dynamic).
- **Builder bots** take one of three roles, chosen once for life. Only
  three builders hold *fixed* roles — the floors — and everyone else is
  dynamic:
  - **Defender** (exactly 1, the 2nd builder ever spawned): find ore, build
    a harvester, lay a conveyor chain back to the core, repeat. Also builds
    home turrets when the core asks. This is the economy floor.
  - **Attacker** (exactly 2): find the enemy core, ring it with forward
    sentinels, then destroy any enemy harvester/conveyor/splitter spotted
    along the way. Never builds gunners away from home — see "Why sentinels,
    not gunners" below.
  - **Dynamic** (everyone else): no fixed job. Greedily re-picks a *task*
    from a strict priority list whenever it's between tasks — see
    "Dynamic builders" below.
- **Gunners**: auto-fire at anything in their facing line; rotate toward a
  new target when there's nothing to shoot at right now.
- **Sentinels** (a maintained pool of 3, forward-deployed at the enemy
  core): longer range than a gunner and their line-shot ignores obstacles,
  but they can never rotate — see "Gunners vs. sentinels" below. **This is
  the primary win condition** — see "Forward sentinels" below.

## Core (`core_role.py`)

Every round the core:

1. Publishes its own position to the store (`SLOT_CORE_X/Y`) so builders can
   find their way home.
2. Prunes its list of tracked builder ids down to ones still confirmed
   alive (`_prune_dead_builders` — see the vision gotcha below, this was
   trickier than it looks).
3. Computes whether it's under threat right now (any enemy unit/building
   visible) and sizes the home-turret cap accordingly (`_update_defense`):
   base 2, +1 if we're economically comfortable, +1 on a "cramped" map
   (small map, enemy core nearby — see `_is_cramped`), or straight to 5 if
   there's a visible threat. It designates exactly one nearby builder per
   round to actually build the next turret (`SLOT_DEFENDER_ID`), so the cap
   can't be raced past by multiple builders reacting to the same round.
4. Tops up the global ammo pool (shared by every gunner, home or away) once
   it's actually needed.
5. Spawns another builder bot if we're under our current stage's
   living-builder target and can afford it (see "Staged spawning" below).

### Staged spawning, not one flat cap

We used to spawn straight up to a single flat living-builder cap (8), gated
only by a fixed Ti reserve. In practice this produced **7 living builders by
round 19 with only 2 harvesters and zero completed belts** (real replay
feedback) — every spawn permanently raises the *shared* cost-scale
multiplier (`get_scale_percent()`, shared across every entity type, not
siloed per category), so spawning fast early inflates harvester/conveyor
costs before any economy exists to pay for them, and most of the fleet just
sits idle next to ore it can't afford to harvest.

Now spawning happens in two explicit stages (`INITIAL_BUILDER_TARGET` /
`REINFORCEMENT_BUILDER_TARGET` in `constants.py`):

1. **Stage 1** (`living < 3`): the starting roster — 1 permanent attacker
   (`SLOT_PERMA_ATTACKER_ID`, the very first builder ever spawned) + 2
   defenders. Normal Ti reserve applies throughout — no rushing this.
2. **Stage 2** (unlocks once `SLOT_HARVESTER_COUNT >= HARVESTER_MILESTONE`,
   currently 2 completed chains): up to 5 living builders. The *first*
   builder spawned in this wave is also always an attacker
   (`SLOT_SECOND_ATTACKER_ID`), reinforcing the first one.

### Builder replacement, not a lifetime cap

Separately from staging: the core keeps a list of builder ids it believes
are alive (`self.builder_ids`) and prunes it every round (see the vision
gotcha below), so both stage targets above are checked against *current*
living count, not a running "spawned so far" total — a team that lost
builders to combat can always trigger a replacement. There's also a hard
floor (`MIN_BUILDERS_ALIVE = 3`) that skips the normal economy safety margin
(not the raw cost) to replace losses immediately — but only after
`self.ramp_established` flips True (we've *once* reached the stage-1
roster). That gate matters: without it, the same bypass would also fire
during the very first ramp-up to 3 builders and reproduce the exact
overspend problem staging above was built to fix.

## Builder role assignment (`main.py::_assign_role`)

Decided once, on a builder's **second** round of life (not its first — see
"Store-write timing" below for why), and never changes after that:

1. If this builder's id matches `SLOT_PERMA_ATTACKER_ID` (the 1st builder
   ever spawned) or `SLOT_SECOND_ATTACKER_ID` (the 1st builder of the
   stage-2 wave) → **Attacker**.
2. Else if it matches `SLOT_PERMA_DEFENDER_ID` (the 2nd builder ever
   spawned) → **Defender**.
3. Else → **Dynamic**.

So the spawn order is: #1 attacker, #2 defender, #3+ dynamic, with the first
stage-2 spawn becoming the 2nd attacker.

The floors are deliberately **fixed designations, not emergent** from the
dynamic pool. A greedy rule only holds a floor probabilistically — nothing
stops every dynamic builder independently deciding the same urgent thing is
worth chasing, leaving zero defenders that round — and verifying a floor
centrally would need vision-limited counting, the same trap already hit with
home-turret counting. Reusing the designation pattern that already worked
for the attackers costs one store slot and removes the failure mode.

## Defender (`defender.py`)

Two-mode state machine per builder:

- **SCOUT**: walk toward the nearest known ore (visible, or advertised by a
  teammate via the ore ring-buffer — `SLOT_ORE_QUEUE_BASE`), and build a
  harvester the moment we're adjacent to an uncovered tile. Falls back to
  picking a random distant exploration target if there's no known ore.
  Also opportunistically builds a home turret if the core designated us this
  round (`SLOT_DEFENDER_ID`), and heals an adjacent damaged friendly.
- **CHAIN**: after building a harvester, walk straight toward the core one
  step at a time, dropping a conveyor on each tile we vacate, facing the way
  we walked. The chain is done the moment a placed conveyor faces directly
  into a core tile — **only the literal core counts as a verified sink**;
  we deliberately never chain into another still-in-progress conveyor, since
  it might never actually reach home (a real, hard-to-spot bug we hit
  early: it builds fine, looks connected, and silently delivers nothing).
  On success, increments `SLOT_HARVESTER_COUNT` (the attacker-trigger
  milestone). Checks adjacency to the pending tile *before* querying
  anything about it (see the vision gotcha below) — the danger-flee check
  earlier in `_run_builder` can pull a chaining builder away from its
  pending tile for one or more rounds, and by the time `_run_chain` resumes
  that tile may no longer be in vision.

  **The final belt is a special case.** Normally the builder walks one step
  closer to the core and builds on the tile it just left. That rhythm
  cannot finish the last link: from a core-adjacent tile the only step that
  gets closer is *onto the core*, and builders cannot stand on their own
  core (see the engine-behavior section — `AGENT.md` is wrong about this).
  So on reaching a core-adjacent tile the builder steps **aside** — any
  legal neighbour — and lays the connecting conveyor on the tile it vacated
  next round. Without this, chains reliably died one belt short of
  delivering anything.

Builders never build on a tile orthogonally adjacent to the core — those 8
tiles are reserved for the core ring.

### The core ring

Every tile orthogonally adjacent to the core carries a permanent conveyor
facing **into** the core, rebuilt whenever one is missing. Eight tiles, 3 Ti
each — probably the best value-per-titanium rule in the bot.

Why it matters: without it, a chain has to land its *final* tile exactly
right, and that endgame is genuinely awkward (see the "final belt" note
above — builders can't stand on their own core, so the last step needs a
sidestep). With the ring up, **any chain that merely reaches the core's
neighbourhood delivers.** It also makes the network self-healing exactly
where a single lost belt would otherwise cost a whole chain's output —
observed in testing: a base beaten down to 1/8 ring tiles rebuilt itself
back to 8/8.

Maintained two ways, deliberately:
- **Opportunistically, with zero travel** (`_try_build_core_ring`) — any
  builder already standing next to a gap fills it. Builders pass the core
  constantly since every chain ends there, so the ring largely maintains
  itself for free. Ranked above starting a harvester: 3 Ti that unlocks
  every future delivery beats 20 Ti that needs one.
- **As a repair task worth walking to** — `_find_belt_gap` reports ring gaps
  before conveyor dead-ends, so `TASK_BELT_REPAIR` dispatches a dynamic
  builder to one.

Measured ring occupancy holds at 8/8 on open maps; lower counts are tiles
genuinely blocked by walls or ore.

### Never plug a live belt (`_would_sever_belt`)

Before committing **any** non-conveyor build — harvester, home gunner,
counter-gunner, denial barrier — the builder checks whether a friendly
conveyor already outputs into that tile, and skips it if so.

This fixes what *looks* like misdirected conveyors but isn't. A conveyor's
facing is always valid the moment it's laid: the builder just walked that
way, so the target tile was passable. The break is a **build-ordering**
problem — something solid gets built on that tile afterwards, and
harvesters, turrets and barriers never accept resources, so the stack stops
dead and everything upstream stops delivering. Audited in real matches:
belts feeding into our own harvester and into our own home gunners. After
the guard, both went to zero and belts terminating correctly at the core
went up.

## Attacker (`attacker.py`)

Each round, in **strict** priority order — later steps don't happen until
earlier ones are satisfied:

1. Update/share enemy-core intel: if the enemy core is in vision, remember
   its position and broadcast it (`SLOT_ENEMY_CORE`) so teammates don't have
   to rediscover it themselves.
2. **Plant a forward sentinel** aimed at the core, if the pool isn't full
   and we're anywhere within sentinel range. Deliberately attempted *before*
   closing distance — see below.
3. Travel toward the best known enemy-core position: a confirmed sighting if
   we have one, else the 180°-rotation mirror of our own core (maps are
   symmetric, so this is a strong first guess before we've scouted
   anything). **No economy detours while still travelling** — finding the
   core comes first, full stop.
4. Once on top of it: detour to destroy any enemy harvester/conveyor/
   splitter currently visible (walk adjacent, then repeatedly `fire()` —
   builder attacks cost 2 Ti per hit, separate from the turret ammo pool),
   falling back to punching the core directly.

## Forward sentinels — the win condition

Gold League games are observably decided around round 100 by whoever gets
turrets onto the opponent's core first. Karrigan aims for a **maintained
pool of 3** sentinels covering the enemy core (`SENTINEL_POOL_TARGET`,
matching `STRATEGY.md`), and this is now the primary path to victory rather
than a side activity — local testing flipped most matches from "runs to
round 1000, decided on titanium tiebreak" to `core_destroyed` around rounds
200–350.

**Range is the whole point, and an earlier version threw it away.** A
sentinel's attack radius is r²=32; placement used to be gated on
`HARASS_RANGE_SQ` (5) — the builder-fire adjacency threshold — which is
**six times smaller**, forcing attackers to walk to point-blank range and
survive there before building anything. Placement is now gated on
`SENTINEL_RANGE_SQ` (32), so sentinels go up from real standoff, outside the
core's defended ring.

That works because **`can_fire_from()` is purely geometric, not
vision-gated** — verified empirically (see the engine-behavior section
below): it returns `True` for an aligned target at dist_sq 25, past a
builder's own r²=20 vision, and `False` only past 32. So a builder can plant
a sentinel correctly aimed at a core it *knows about but cannot currently
see*.

Other properties of the implementation:

- **Confirmed sightings only.** Placement requires `self.enemy_core_known`
  (someone actually saw the core), never the symmetry guess. A sentinel's
  facing is permanent, so aiming at a guessed position risks paying 30 Ti
  for a turret pointed at empty ground for the rest of the game.
- **Pool is re-observed, not latched.** `_count_forward_sentinels` counts
  live sentinels near the core every round, so a destroyed one is naturally
  replaced. (The previous one-way `sentinel_built` flag meant the team's
  single sentinel was never rebuilt once killed.)
- **Dynamic builders help fill it**, not just the two floor attackers — two
  attackers arriving one at a time is too slow to have three up by round
  ~100. The pool cap lives inside `_try_build_sentinel`, so extra
  participants can't overbuild.
- **A hard ammo floor sits under everything.** `AMMO_FLOOR` (10 — one
  sentinel shot, or five gunner shots) is topped up *every* round,
  ungated by round number, threat, or the economy reserve; the only limit
  is what we can afford. Every other ammo rule is conditional, and those
  conditions can all be false at the exact moment a turret first needs to
  fire. Measured in-match: the floor holds in ~95% of rounds, the misses
  being rounds where titanium was genuinely 0. Note `convert_ammo()` may
  only be called **once per team per turn**, so the floor and the buffers
  resolve into a single target/budget pair before converting.
- **Ammo is scaled to match, but never at the economy's expense.** A
  sentinel shot costs 10 ammo (vs a gunner's 2), and killing a 500 HP core
  at 18 dmg/shot takes ~28 shots ≈ 280 ammo. Once any forward sentinel
  exists (`SLOT_SENTINEL_COUNT`) *and* the economy gate is met, the core
  switches from `AMMO_BUFFER` (30) to `AMMO_BUFFER_SIEGE` (150), banking
  from `AMMO_PRESTOCK_ROUND` (40). Conversion is 1:1 titanium, so
  `AMMO_ECONOMY_RESERVE` (100) is held back from conversion entirely —
  otherwise the siege chest is bought straight out of the harvester budget,
  which is exactly how an over-aggressive build loses on resources.

### Why sentinels, not gunners

An earlier version had attackers build *gunners* next to the enemy core. We
removed that: a gunner alone in enemy territory gets picked off cheaply, and
it inflated our total turret count for little value (feedback after a replay
— "far too many turrets, keep them close to the core"). Gunner construction
remains exclusively at home under the core's dynamic cap.

Sentinels are a genuinely different proposition, not a reversal of that
call: r²=32 range vs a gunner's 13, and a line-shot that ignores obstacles,
so they threaten the core from outside its defended ring instead of having
to sit adjacent to it.

## Dynamic builders (`dynamic.py`)

Every builder beyond the three floor roles. Instead of a fixed job, it
greedily re-picks a **task** whenever it's between tasks. Full rationale in
`DESIGN_dynamic_builders.md`; the operational summary:

Priority list, strict order — first one with a valid, *visible* target wins:

1. **`TASK_HOME_THREAT`** — enemy near our own core (within
   `HOME_THREAT_RADIUS_SQ`, 7 tiles). Sub-ranked: **turret** (ongoing ranged
   damage) → **harvester** (economic denial) → **enemy builder**. Against a
   *turret* the answer is to **build a counter-gunner and walk away**, not to
   trade punches — see below. Softer targets get ordinary builder-fire.

   Enemy **conveyors/splitters/barriers are deliberately NOT home threats**.
   They can't hurt the core, and counting them was measured to break the
   whole pool — see "What dynamic builders actually do" below.
2. **`TASK_BELT_REPAIR`** — a gap in our conveyor network. Outranks denial:
   protecting income we already built beats denying income they haven't.
3. **`TASK_HARVEST`** — delegates wholesale to `_run_defender`. Taken
   whenever ore is visible/advertised, **and unconditionally while the team
   is below `OFFENSE_MIN_HARVESTERS` completed chains** — see the economy
   gate below.
4. **`TASK_BASE_REPAIR`** — heal a damaged friendly building at home (1 Ti
   → +4 HP), so chip damage doesn't accumulate until a harvester or belt
   run dies and has to be rebuilt outright. Deliberately *below* harvest:
   healing preserves income, harvesting *adds* it, so expansion wins
   whenever ore is actually available. (Tried above harvest; measured
   worse — see `constants.py`.)
5. **`TASK_ORE_DENIAL`** — barrier an ore tile on the enemy's half so they
   can never harvest it (harvesters need a bare ore tile).
6. **`TASK_ADVANCE`** — fallback so nobody idles: march on the enemy core,
   planting a forward sentinel if the pool has room (see "Forward
   sentinels"), else harassing on arrival.

### Answering enemy turrets: build, don't brawl

A builder deals **2 damage per hit**. An enemy sentinel has 30 HP, so
grinding one down with builder-fire means **15 consecutive rounds parked
inside its firing line** — and a gunner shooting back kills the 40 HP
builder in 4. That trade is hopeless, and it was visibly too slow in
replays.

So `_execute_strike` now answers an enemy *turret* by building a
**counter-gunner** aimed at it (`_try_build_counter_turret`), then clearing
its task and going back to useful work. A gunner does 10 dmg on reload 1 —
it kills that sentinel in 3 shots — and keeps fighting after the builder has
left. Build tiles inside the enemy's own fire line are skipped, and the
facing is verified with `can_fire_from()` so it bears on the target
immediately rather than wasting a turn (and 10 Ti) rotating.

Softer threats (harvesters, enemy builders) still get plain builder-fire —
they don't shoot back hard, so a turret would be over-investment.

**Anti-thrash, three layers** (a plain round-timer is deliberately *not* the
main mechanism):

- Tasks end on their **termination condition** — achieved, or confirmed gone
  — not a clock. `TASK_MAX_ROUNDS` (40) is only a runaway backstop.
- A task is preempted only by a **strictly** higher priority, never an equal
  one. Priorities being a discrete list means this gives tie-hysteresis for
  free: two near-tied options can't trade places round after round.
- **Commitment scales with sunk investment.** A chain in progress is
  effectively non-preemptible — abandoning it strands conveyors that deliver
  *nothing*, i.e. spent titanium turned to zero, strictly worse than wasted
  walking. Merely walking somewhere is cheap to drop. `COMMIT_FLOOR` (3–5
  rounds, **varied by id**) is just the residual anti-flicker damper, and the
  id-variation keeps the pool from re-evaluating in lockstep and herding onto
  the same target.

### What dynamic builders actually do (measure it, don't assume)

The priority list above describes what *can* happen. What actually happens
is an empirical question, and twice now it has been badly different from the
design intent. **Instrument `_run_dynamic` and count tasks** before believing
the pool is behaving — it's a handful of lines and it has caught two
pool-wrecking bugs that no amount of reading the code revealed:

| task | originally | after threat-scope fix | after de-thrash |
|---|---|---|---|
| HOME_THREAT | **48%** | 8% | 37% |
| BELT_REPAIR | 22% | **50%** | 8% |
| HARVEST | 23% | 27% | 34% |
| CHAIN_LOCKED | 7% | 15% | 20% |
| ORE_DENIAL / ADVANCE | **0% / 0%** | 0% / 0% | 0% / 0% |

Two real bugs found this way:

1. **Every enemy belt counted as a "home threat"** with a 10-tile radius that
   reached past the midline on most maps. There is always some enemy conveyor
   in range and each takes ~10 rounds of builder-fire to chew through, so the
   pool sat at 48% HOME_THREAT and *never once* advanced or denied ore. Fixed
   by scoping threats to turrets/harvesters/enemy-builders within 7 tiles.
2. **A chain still being laid looks exactly like a broken belt** — its
   leading conveyor points at an empty tile. Every idle builder piled onto
   the chain-layer's own frontier, pushing belt repair to 50% of all rounds.
   Fixed by `_someone_working_at()`: if a friendly builder is already
   adjacent to a gap, leave it to them.

Note ORE_DENIAL and ADVANCE remain at 0% — the dynamic pool is in practice
"economy + repair + local defence", with offence left to the two fixed
attackers. That's defensible under the current base-first direction, but it
means the dynamic pool is narrower than the task list implies. The
HOME_THREAT swing between the last two columns is across different matches
with unseeded RNG, so treat single-run percentages as indicative only.

### The economy-before-offense gate (`OFFENSE_MIN_HARVESTERS`)

Below `OFFENSE_MIN_HARVESTERS` completed harvester chains team-wide, dynamic
builders don't advance, deny ore, or plant sentinels at all — they behave
exactly like defenders. The *second* fixed attacker is gated on this too;
the first is not, since one builder of early scouting/pressure is deliberate.

This exists because of a real, losing failure mode. `TASK_HARVEST` was
originally only picked when ore was **already visible or advertised** —
but a DEFENDER with no ore in sight goes and *explores* for some
(`_explore_target`), and dynamic builders skipped that. So the moment ore
wasn't inside a builder's r²=20 vision, it fell through to `TASK_ADVANCE`
and left for the enemy core — permanently, since it was then far from home
and never saw ore again. The whole dynamic pool self-converted into
attackers. The bot besieged well and never built an economy, then lost on
resources.

The fix is the second clause in `_should_harvest`: below the threshold, take
the harvest task **even with no ore in sight**, because `_run_defender` will
go find some. Above it, normal priority applies — and harvesting still
outranks denial/advance whenever ore is actually available.

The two fixed attackers are deliberately *not* gated: 2 builders is the
entire early-aggression budget, and that's intentional.

**Proximity gating is free**: every detector reads this builder's own vision,
so a builder that can't see a threat never bids on it. `TASK_HOME_THREAT`
therefore recruits builders already near home rather than acting as a global
interrupt that yanks the whole pool back across the map.

### Belt-gap detection

The detector is **local and memoryless** on purpose — the builder that laid a
chain may be long dead, and per-unit state isn't shared:

> A friendly conveyor whose **output tile is empty** is a broken link.

Read its facing, look at the tile it points into; if that's empty, the chain
is severed exactly there. A conveyor pointing into the core or a wall is not
a false positive (neither reads as empty). Repairs **self-propagate**: the
rebuilt conveyor faces onward toward the core, so if *its* output is also
empty, that's found next round — a multi-tile break heals segment by segment
with nobody tracking the original route. Bounded by `harvest_range`.

Known limit: this only catches breaks with a surviving *upstream* conveyor.
A harvester whose entire outbound chain is gone is not detected — restarting
a chain from scratch is a bigger job, still open.

## Gunners vs. sentinels (`main.py::_run_gunner` / `_run_sentinel`)

Getting turret targeting right took two rounds of bugfixing, both worth
understanding before touching this again:

1. **A gunner is a facing weapon, not a radius weapon.**
   `get_gunner_target()` only ever reports something along the *single*
   direction the turret is currently pointed. Without ever rotating, a
   turret is blind to anything approaching from any other angle, including a
   builder attacking it point-blank from the "wrong" side. So: if there's
   nothing to shoot in our current facing, we look for the nearest enemy we
   could hit by rotating, and rotate toward it (`_best_rotate_facing`).
   Rotating costs an action (10 Ti, 1-round cooldown, same as reload), so
   against a stationary target this alternates rotate → fire.
2. **Don't guess the rotation direction from `Position.direction_to()`.**
   That just rounds to the nearest 45°, which is only ever *exactly* right
   when the target is orthogonally adjacent (adjacency forces exact
   alignment by construction). Anything farther away is almost never sitting
   exactly on one of the turret's 8 firing lines, so a "roughly right"
   rotation still never connects — this was a second, subtler bug on top of
   the first (turrets that would only ever engage point-blank despite having
   real range). Fix: search actual candidate directions against
   `can_fire_from()`, the engine's own geometry check (ignores ammo/cooldown,
   just tells you if a hypothetical turret at this facing would hit).
3. **`get_gunner_target()` does not filter by team.** It returns the nearest
   *occupied* tile in the line, friend or foe — confirmed directly against
   the engine, not just inferred from docs. Left unchecked, a turret will
   happily gun down a friendly harvester or conveyor that ends up in its
   fire line later (e.g. built after the turret, along the same cardinal).
   We check `_is_friendly_tile()` before ever firing.
4. **A sentinel has no rotate() at all** — `can_rotate()`/`rotate()` are
   documented "Gunner-only" in the engine's own `Controller` stub, and this
   was confirmed, not assumed. Its facing is **permanent** from the moment
   it's built. `_run_sentinel` therefore never tries to reorient — it just
   fires at the nearest enemy in its fixed line, found via
   `get_attackable_tiles()` (`get_gunner_target()` is gunner-only, so this
   is the equivalent built by hand: sort the turret's attack-pattern tiles
   by distance, return the first enemy-occupied one). All the actual
   decision-making for a sentinel happens once, at build time, in
   `attacker.py::_try_build_sentinel` — get that placement wrong and there's
   no fixing it later, which is exactly why it verifies alignment with
   `can_fire_from()` against the enemy core's footprint before ever
   committing, rather than guessing a facing the way an early gunner
   implementation once did.

## Communication store (16 slots, team-shared, one round of write lag)

See the docstring at the top of `constants.py` for the authoritative,
up-to-date table — don't let this doc drift out of sync with it. Summary:

| Slot | Name | Writer | Purpose |
|---|---|---|---|
| 0–1 | `SLOT_CORE_X/Y` | core | our core's position |
| 2 | `SLOT_DEFENDER_ID` | core | which builder may build a home turret this round |
| 3 | `SLOT_GUNNER_COUNT` | core | live home gunners (informational) |
| 4 | `SLOT_ORE_CURSOR` | any | ring-buffer write cursor |
| 5–8 | ore ring-buffer | any | up to 4 advertised uncovered-ore tiles |
| 9 | `SLOT_ENEMY_CORE` | attackers | enemy core position once spotted |
| 10 | `SLOT_GUNNER_CAP` | core | current home-turret target (2–5) |
| 11 | `SLOT_HARVESTER_COUNT` | defenders | completed chains (attacker/stage-2 milestone) |
| 12 | `SLOT_PERMA_ATTACKER_ID` | core | id of the first (always-on) attacker |
| 13 | `SLOT_SECOND_ATTACKER_ID` | core | id of the stage-2 reinforcement attacker |
| 14 | `SLOT_SENTINEL_ID` | attackers | id of the team's one forward sentinel, once placed |
| 15 | `SLOT_PERMA_DEFENDER_ID` | core | id of the one always-on defender (the floor) |

**The store is now full (0–15).** Any new shared signal needs a slot
reclaimed first; `SLOT_GUNNER_COUNT` (3) is the best candidate, being
written every round but read by nothing. Notably *not* given slots:
belt-gap and ore-denial opportunity sharing, so two dynamic builders can
duplicate effort on the same gap — accepted, since the waste is one
conveyor and there was no slot left to spend.

**The single most important gotcha**: a `write_store()` this round is not
visible to *anyone* — including the unit that wrote it — until **next**
round. This breaks the naive "core designates something for the builder it
just spawned" pattern, since that builder's very first `run()` call happens
the *same* round it spawns, before its own designation is visible. Our fix:
builders defer their one-time role decision to their second round of life
(`main.py::_run_builder`) rather than deciding immediately. If you add a new
core → freshly-spawned-unit handoff via the store, you'll hit this same
issue — either delay the reader by a round, or don't rely on same-round
visibility.

Also: **never** do a read-modify-write "counter" that multiple units might
increment in the same round — every writer sees the same stale pre-round
value, so simultaneous writes silently clobber each other instead of
accumulating. Slots 2, 3, 10, 12 and 13 are single-writer (core only)
specifically to avoid this, as is `SLOT_PERMA_DEFENDER_ID` (15).
`SLOT_HARVESTER_COUNT` (11) and `SLOT_SENTINEL_ID` (14) are the deliberate
exceptions — multiple units can
write them, and a same-round race just costs a round of latency (an
under-count, or briefly two attackers both trying to build the sentinel),
which is harmless since both are coarse "has this happened yet" signals, not
hard caps.

## Non-obvious engine behavior we learned the hard way

These aren't documented in `AGENT.md` — we found them by writing small
throwaway diagnostic bots and querying the engine directly. Worth knowing
before you assume an API behaves the way its docstring alone suggests:

- **Id-based queries are not vision-free**, despite the `Controller` stub's
  docstrings not mentioning any restriction. Querying `get_hp(id)`,
  `get_position(id)`, `get_entity_type(id)`, etc. for a unit currently
  outside your vision raises `GameError("Position out of vision range")`
  — same as querying an out-of-vision `Position` directly. This applies to
  your *own* units too, not just the enemy's.
- **A destroyed entity's id raises a different error**: `GameError("Unknown
  id")`. This is how `core_role._prune_dead_builders` distinguishes "alive
  but I can't currently see it" (don't prune) from "confirmed gone" (prune)
  — treating both as "dead" would make the core think every attacker who
  wandered out of vision was dead and endlessly try to replace them.
- **Any `Position`-based query needs an explicit `is_in_vision()` guard, OR
  a cheap pure-math check that implies it (e.g. `adjacent()`), performed
  *before* the query — never after.** A remembered/stale position (e.g.
  "where I last saw that harvester," or "the tile I owe a conveyor on") is
  not safe to query directly once time has passed. We hit this twice, in
  the same shape both times: the vision-unsafe call came *before* the code
  that would have caught the stale state and bailed out cleanly, instead of
  after. `attacker.py`'s `_handle_attack_target` (chasing a
  harvester/conveyor it can lose sight of while closing in) and
  `defender.py`'s `_run_chain` (a chain segment interrupted by the
  danger-flee check elsewhere in `_run_builder`, which can pull a builder
  away from its pending tile for a round or more) both needed their
  adjacency/vision check reordered to run *first*. A third instance showed
  up immediately when `dynamic.py::_find_belt_gap` was written: it derives
  a tile from a *visible* conveyor's facing (`pos + direction`), and a
  conveyor sitting on the rim of vision has its output tile one step
  *beyond* that rim — in bounds, fully legitimate, and not queryable.
  **Deriving a position from a visible thing does not make the derived
  position visible.** A fourth instance appeared when the core-ring scan
  was added: it correctly vision-checked each candidate tile, then called
  `_facing_to_core()`, which looks at that tile's *neighbours* — one step
  further out again. That one produced 16,000+ errors in a single sweep.
  The guard now lives **inside `_facing_to_core` itself** rather than at
  its call sites, which is the right altitude for it: a helper that walks
  to neighbouring tiles must vision-guard its own walk, because callers
  cannot know how far it reaches. **This class of bug did
  not show up in self-play** (bot vs. itself) — only against a genuinely
  different opponent (`bots/friend`) — because self-play's identical,
  symmetric behavior rarely creates the divergence that makes a remembered
  position go stale. See "Running it locally" below.
- **`get_gunner_target()` is a facing-line query, not a radius query, and
  doesn't filter by team.** See the Gunners section above.
- **A builder CANNOT stand on its own team's core — `AGENT.md` says it can,
  and `AGENT.md` is wrong.** The repo-root reference explicitly lists "your
  own team's core tiles" as passable; the engine reports
  `is_tile_passable() == False` and `can_move() == False` for them
  (verified directly with a diagnostic bot). This one silently broke
  conveyor chains for a long time: the chain lays a belt on the tile it
  *vacates*, so the last core-adjacent tile can only be built by stepping
  off it — and the only step that gets closer to the core is onto the core.
  Builders parked one tile out, made no progress, and abandoned the chain a
  single belt short of delivering. Measured 14 of 19 chain failures.
  `_run_chain` now special-cases the final belt by stepping *aside* instead
  of forward (chain completion 69% → 98%). **Treat `AGENT.md`'s passability
  rules as unverified** — the rest of that list has not been re-tested.
- **`can_fire_from()` is vision/bounds-safe AND purely geometric** — unlike
  the position queries above, it returns `False` for an out-of-bounds target
  rather than raising, and it evaluates *range and alignment only*, with no
  vision requirement at all: verified `True` for an aligned target at
  dist_sq 25 (past a builder's own r²=20 vision) and `False` only past the
  sentinel's r²=32 range. Both confirmed with diagnostic bots, not inferred
  from docs. This is what makes standoff sentinel placement possible — you
  can correctly aim a turret at something you cannot currently see, provided
  you know where it is.

If you find another one of these, add it here — they're the kind of thing
that's easy to silently reintroduce in a rewrite.

## Running it locally

```
uv run fcode run bots/baseline bots/baseline maps/<name>.map26 --json
uv run fcode run bots/baseline bots/friend  maps/<name>.map26 --json
```

`--json` gives a machine-readable summary (winner, titanium collected, unit/
building counts) instead of the formatted table — useful for quick sanity
checks across many maps. Add `--watch` to open the replay visualizer, or
`fcode watch replay.replay26` afterward. `--tle 10` matches the real
competition's 10ms/turn CPU limit (omitted/0 disables it).

**Test against `bots/friend`, not just self-play.** Self-play (karrigan vs.
karrigan) is cheap and fine for a first pass, but it's not sufficient on its
own: a real bug (see the `_run_chain` entry above) produced zero errors
across ~35 maps of self-play and then failed almost immediately against
`bots/friend`, because self-play's two sides behave identically and rarely
create the kind of divergence (one side chasing something the other
destroyed, one side fleeing somewhere the other wouldn't) that surfaces
these bugs. Treat a clean self-play run as necessary, not sufficient.

We generally don't judge *strategy* quality by running matches ourselves —
that's a call for whoever's watching the replay. Local runs are mainly for
catching crashes/exceptions: grep the run's stderr for `[bot]` — that prefix
means a unit hit an uncaught exception this round (caught by the top-level
`run()` guard in `main.py`, so the unit survives, but something's wrong).
Zero `[bot]` lines across a handful of maps *against both opponents* is the
bar before calling a change done.

If you need to find exactly which line raised an error (the `[bot]` line
only gives you the exception type/message, not a traceback), temporarily
add `import traceback; traceback.print_exc(file=sys.stderr)` right after the
`print(f"[bot] ...")` in `main.py::run()`'s except block, reproduce, then
revert it — don't leave it in.

## Known limitations / ideas for next iteration

- Attacker targeting (of harvesters/belts) is purely opportunistic (whatever
  is in vision right now) — there's no shared memory of *previously* seen
  enemy economy targets the way there is for the enemy core, so a
  spotted-then-lost harvester is forgotten.
- Only one sentinel, ever, team-wide, and it's never replaced if destroyed
  (`sentinel_built` is a one-way flag). `STRATEGY.md` asks for a maintained
  pool of three — see `STRATEGY_ALIGNMENT.md`, this is an open disagreement
  rather than a simple gap. No launchers anywhere yet either.
- Belt repair only catches breaks with a surviving upstream conveyor; an
  orphaned harvester (whole chain destroyed) is never re-connected.
- Dynamic builders switch *tasks* freely, but a builder's *role* is still
  fixed for life — a floor attacker never becomes a defender, or vice versa.
- Home turret placement is a simple ring around the core
  (`GUNNER_MIN_CORE_DIST_SQ`..`GUNNER_NEAR_CORE_DIST_SQ`); it doesn't
  reason about which approach directions are actually most exposed.
- No coordination between multiple simultaneous attackers — each acts
  independently off the same shared intel, which works fine at low attacker
  counts but doesn't do anything smarter (e.g. converging together) as more
  come online.
- All tuning constants in `constants.py` are hand-picked/empirical, not
  tuned via any systematic search — there's a lot of room to actually
  benchmark alternatives with `fcode run --json` across many maps.
