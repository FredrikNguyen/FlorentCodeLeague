# Design: dynamic builders (greedy task selection)

Design record for the dynamic-builder work. `STRATEGY.md` (repo root) is the
aspirational spec, `STRATEGY_ALIGNMENT.md` maps spec → code, and `README.md`
documents what the bot actually does. This file explains *why* the dynamic
pool is built the way it is — the reasoning that would otherwise be lost.

## The problem

Karrigan's roles were fixed for life: a builder decided DEFENDER or ATTACKER
on its second round and never changed. `STRATEGY.md` asks for a mostly
*dynamic* pool that takes on whatever role the situation needs, with a
defender floor. That's a change to the role model itself, not a behavior
you can bolt onto one file.

## Why greedy

The engine gives no cheap path to centralized optimal assignment: 16 store
slots, one-round write lag, no unit-to-unit messaging, vision-limited
queries. Anything auction-like or globally-optimal would spend most of its
budget coordinating. A decentralized greedy rule — each builder picks the
highest-priority thing it can personally see, recomputed as it goes — needs
zero coordination to function at all, which is exactly the constraint we're
under.

## Task priority (strict order)

Not roles — *tasks*. A dynamic builder walks this list top-down and takes
the first one with a valid target it can act on:

1. **`TASK_HOME_THREAT`** — something enemy near our own core. Sub-ordered,
   per explicit direction: **enemy turret** (ongoing ranged damage — worst)
   → **enemy harvester** (economic denial) → **anything else hostile**
   (fight directly, e.g. an enemy builder).
2. **`TASK_BELT_REPAIR`** — a gap in our conveyor network (see detection
   below). Outranks ore denial per explicit direction: protecting income we
   already built beats denying income the enemy hasn't built yet.
3. **`TASK_HARVEST`** — the existing SCOUT→harvester→CHAIN economy loop,
   reused wholesale from `defender.py`.
4. **`TASK_ORE_DENIAL`** — barrier an ore tile on the enemy's side of the
   map so they can never harvest it (harvesters require a bare ore tile).
5. **`TASK_ADVANCE`** — nothing local applies → march toward the enemy core,
   harassing it if we arrive. Never idle; this is the catch-all floor.

## Stickiness

A fixed round-count timer is the naive approach and the literature dominates
it. Three mechanisms instead, in order of how much work they do:

**Commitment until termination, not timeout.** Cohen & Levesque's
*Intention is Choice with Commitment* (1990): drop an intention when it's
achieved, believed unachievable, or its motivation is gone — not when a
clock expires. So every task self-terminates on target-invalid (verified
each round, vision-guarded), and `TASK_MAX_ROUNDS` exists only as a
backstop against chasing something forever.

**Strict-preemption hysteresis.** From preemption-threshold scheduling
(Wang & Saksena): a running task is preempted only by something *strictly*
higher priority, never merely equal. Because our priorities are a discrete
ordered list rather than continuous scores, this gives tie-hysteresis for
free — no epsilon tuning, and the classic dither case (two near-tied
options trading places round to round) simply cannot occur.

**Sunk-investment-proportional commitment.** Stickiness scales with what
abandoning would waste:

- **CHAIN in progress → effectively non-preemptible** (only the existing
  flee check overrides). Abandoning strands a partial conveyor chain that
  delivers *nothing* — spent titanium converted to zero, strictly worse
  than wasted walking. It's already bounded by `chain_limit` /
  `CHAIN_BLOCKED_LIMIT`, so it self-terminates.
- **Everything else** → cheap to abandon, preemptible by strictly-higher
  priority once past a short floor.
- **`COMMIT_FLOOR`** (3–5 rounds, id-varied) is the residual anti-flicker
  damper only — for a higher-priority target blinking in and out of vision,
  not the primary mechanism.

## Proximity gating comes free

Preemption should require "higher priority **and** close enough to matter" —
a builder 20 tiles from home that drops a chain to answer a home threat
arrives long after it's decided, paying the switching cost for nothing.

We get this without writing any distance rule: **all task detection is
vision-based**. A builder that can't see the threat doesn't bid on it. So
`TASK_HOME_THREAT` naturally recruits only builders already near home,
rather than acting as a global interrupt yanking the whole pool back. This
is deliberate — a core broadcast of "threat at home" would be strictly
worse here, and we have no spare store slot for one anyway.

## Herding: heterogeneous thresholds

Pure greedy with identical agents means everyone piles onto the same
stimulus. The swarm-robotics answer is response-threshold models from
social-insect division of labor (Bonabeau, Theraulaz, Deneubourg):
per-agent threshold variation produces division of labor with zero
communication. We already do `id % N` for role assignment; the same trick
varies each builder's `COMMIT_FLOOR` (3/4/5 by id), so builders re-evaluate
on different rounds and don't switch in lockstep. Cheap, and the piece most
easily forgotten.

## Role floors stay *fixed*, not emergent

The two attackers keep their existing fixed designations, and a **third
fixed designation is added for the defender floor**
(`SLOT_PERMA_DEFENDER_ID`, the 2nd builder ever spawned).

Deliberately *not* emergent from the greedy pool: a greedy rule only holds a
floor probabilistically — nothing stops every dynamic builder independently
deciding the same urgent thing is worth chasing, leaving zero defenders that
round — and verifying a floor centrally would need vision-limited counting,
the same trap already hit with home-turret counting. Reusing the
designation pattern that already works costs one store slot and removes the
failure mode entirely.

Spawn order: #1 → permanent attacker, #2 → permanent defender, #3+ →
dynamic, with the first stage-2 spawn → second permanent attacker.

## Belt-gap detection (new capability)

Needed a detector that's **local and memoryless** — the builder that laid a
chain may be dead, and per-unit state isn't shared. The rule:

> A friendly conveyor whose *output tile* is empty is a broken link.

Read the facing (`get_direction`), look at the tile it points into; if
that's empty, the chain is severed exactly there. No memory, works for
chains built by anyone, any age. A conveyor pointing into the core or a wall
is not a false positive (neither tile is "empty").

This **self-propagates**: the repaired conveyor faces onward toward the
core, so if *its* output is also empty, that's detected next round and
repaired too — a multi-tile break heals segment by segment without anyone
tracking the original route. Bounded by `harvest_range` so it can't wander.

Repair facing, in order: into the core if adjacent → into an adjacent
friendly conveyor closer to the core → cardinal step toward the core. Same
"only the literal core is a verified sink" caution as original chain-laying
(see `README.md`).

## Reuse, not reimplementation

- `TASK_HARVEST` delegates to `defender.py::_run_defender` unchanged.
- `TASK_ADVANCE` reuses `attacker.py`'s enemy-core targeting and `_harass`.
- All movement stays on `navigation.py::_navigate` with its danger-avoid.
- Sentinel building stays attacker-only (`STRATEGY.md` assigns it to
  attackers), so dynamic builders harass but don't place turrets forward.

## Store slots

`SLOT_PERMA_DEFENDER_ID = 15` takes the last free slot — **the store is now
full (0–15)**. Any future shared signal needs a slot reclaimed first;
`SLOT_GUNNER_COUNT` (3) is the best candidate, being write-only today.

Notably *not* given slots: belt-gap and ore-denial opportunity sharing. Two
builders can duplicate effort on the same gap. Accepted for now — the waste
is one conveyor, and there's no slot left to spend on it.

## Deliberately out of scope

- **Sentinel pool of 3** (`STRATEGY.md`) — still 1. Unresolved tension with
  earlier "far too many turrets" feedback; see `STRATEGY_ALIGNMENT.md`.
- **Orphaned-harvester repair** (harvester whose entire outbound conveyor is
  gone) — the gap detector only catches breaks with a surviving upstream
  conveyor. Restarting a chain from scratch is a bigger job.
- **Runtime role *reassignment*** — dynamic builders switch *tasks* freely,
  but a builder designated ATTACKER/DEFENDER stays that role for life. The
  floors are meant to be stable.
