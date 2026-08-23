# STRATEGY.md ↔ karrigan alignment

`STRATEGY.md` (repo root) is the aspirational design doc — what the bot is
*supposed* to do. `README.md` (this directory) is what karrigan *actually*
does right now. This doc is the bridge between them: a point-by-point
mapping of every claim in `STRATEGY.md` against karrigan's real code, so
whoever's iterating on either doc can see where they already agree, where
they're close but not identical, and where there's a real gap to close.

**Sections below the verdict table were written before the dynamic-builder
work landed and describe gaps that are now closed** — they're kept for the
reasoning, but the table is the current truth. `README.md` documents how the
implemented versions actually behave.

This is a snapshot, not a contract — re-check it whenever either document
changes. I haven't touched `STRATEGY.md` itself; if something here reads as
a correction to it rather than a gap in the code, that's a conversation to
have with whoever's maintaining it, not something to silently resolve here.

## Quick verdict

Updated after the dynamic-builder work — see `DESIGN_dynamic_builders.md`.
Most of what was previously a gap is now implemented.

| Strategy point | Status | Where in karrigan |
|---|---|---|
| Two dedicated attackers | ✅ Aligned | `SLOT_PERMA_ATTACKER_ID` + `SLOT_SECOND_ATTACKER_ID` |
| One dedicated defender, rest dynamic | ✅ Aligned | `SLOT_PERMA_DEFENDER_ID` + `dynamic.py` |
| Builders never idle | ✅ Aligned | `TASK_ADVANCE` is an always-valid fallback |
| Attackers path to enemy core | ✅ Aligned | `attacker.py::_run_attacker` |
| Attackers deny enemy ore with obstacles | ✅ Aligned | `TASK_ORE_DENIAL` (dynamic builders, not attackers — see below) |
| Repair/rebuild damaged belts | ✅ Mostly | `TASK_BELT_REPAIR`; orphaned-harvester case still open |
| Hunt turrets threatening our core | ✅ Aligned | `TASK_HOME_THREAT`, turret sub-priority first |
| 3-sentinel pool, maintained "at all times" | ✅ Aligned | `SENTINEL_POOL_TARGET = 3`, re-observed each round so losses are replaced |
| Home turret placement | ⚠️ Partial | dynamic cap exists; doesn't reason about enemy turret vision |
| "Harvester one tile from core" edge case | ❓ Untested | plausibly handled, not specifically verified |

One deliberate divergence worth noting: `STRATEGY.md` assigns ore denial to
*attackers*, but it's implemented as a dynamic-builder task instead. The two
floor attackers are kept tightly focused on the core-then-sentinel-then-belts
sequence; dynamic builders passing through enemy territory are better placed
to opportunistically barrier ore without derailing that sequence.

## Roles

> "At all times, there should be 1 defender builder and two attacker
> builders. The rest of the builders should be dynamic and therefore be
> able to take on any roles depending on the situation."

**The two-attacker floor is already real.** `core_role.py` designates the
first builder ever spawned (`SLOT_PERMA_ATTACKER_ID`) and the first builder
of the stage-2 reinforcement wave (`SLOT_SECOND_ATTACKER_ID`) as permanent
attackers — see `README.md`'s "Builder role assignment" section. That part
of the strategy is implemented as written.

**The "1 defender, rest dynamic" half is not.** Two real gaps, one small and
one structural:

- *Small*: there's no explicit floor guaranteeing at least one defender.
  In practice this is almost always true anyway — role assignment
  (`main.py::_assign_role`) defaults every non-designated builder to
  DEFENDER until `HARVESTER_MILESTONE` (2) chains are complete, so the
  early game is defender-heavy by construction — but it's incidental, not
  guaranteed the way the attacker floor is.
- *Structural, the bigger one*: karrigan has **no dynamic role pool at
  all**. `self.role` is decided once, on a builder's second round of life,
  and never changes again for that unit's entire lifetime (see
  `README.md`'s role-assignment section). "Take on any role depending on
  the situation" implies runtime reassignment — e.g. a defender near an
  active threat switching to respond, or an idle/blocked defender being
  redirected to reinforce an attack — and there's currently no mechanism
  for that at all. This is the single biggest architectural gap between
  the strategy doc and the code: it's not a missing behavior you can bolt
  on to one file, it touches the core role model in `main.py`,
  `defender.py`, and `attacker.py` together.

> "When a builder spawns... it will start going towards the general
> direction of the enemy core. On its way, it will repair any friendly
> buildings or destroy any nearby enemy turrets targeting our core."

This describes the *dynamic* builder's default behavior specifically (see
above — it doesn't apply to attacker.py's designated attackers, who already
do exactly this, or to defenders, who deliberately stay ore-focused). Since
the dynamic pool doesn't exist yet, this behavior doesn't either. Two
sub-pieces worth calling out separately once it's built:

- *Repair friendly buildings encountered en route*: defenders currently only
  heal via `_try_heal`, which checks its own adjacent tiles reactively —
  there's no "seek out damaged buildings" behavior for any role.
- *Destroy nearby enemy turrets targeting our core*: doesn't exist in any
  form. The closest thing karrigan has is `_danger_tiles`/`_navigate`'s
  `avoid` mechanism, which is purely defensive (route around a turret's fire
  line) — never offensive (go destroy the turret). A builder that notices an
  enemy turret threatening our core today just avoids it, permanently,
  rather than ever doing anything about it.

> "Builders should never idle... walking back and forth or just standing
> still."

Mostly aligned, and this was a direct focus of an earlier fix this session
(the 7-idle-builders-at-round-19 report that led to staged spawning — see
`README.md`'s "Staged spawning" section). The BFS navigation in
`navigation.py::_navigate` combined with the blacklist/no-progress escape in
`defender.py::_move_toward_target` is specifically designed to avoid
back-and-forth loops. Two soft edges remain, neither confirmed as an actual
problem in play, just worth knowing about:

- An attacker that's close to the enemy core but can't yet afford the
  sentinel (`attacker.py::_try_build_sentinel` fails) falls back to
  `_harass`, which only fires if `can_fire()` succeeds — if it's on
  cooldown and not adjacent to anything else, it does nothing that round.
  Not idle in the "wandering" sense, but not clearly *purposeful* either.
- Home-turret-designated builders (`SLOT_DEFENDER_ID`) that can't find a
  legal build tile just fall through to normal SCOUT movement, so this
  isn't actually a gap — flagging only because it's the kind of interaction
  worth re-checking if "idle builder" reports come up again.

## Defenders

> "A defender builder will lay down harvesters and belts, repair buildings
> etc."

Aligned — this is `defender.py`'s SCOUT/CHAIN loop plus `_try_heal`, exactly
as described.

> "It's important to realise that the enemy can remove our belts, fix any
> missing belts."

**Clear gap.** Once a chain finishes (`_end_chain(ct, success=True)`), that
harvester is never revisited by anyone. If the enemy destroys a conveyor
partway along an established chain, karrigan has no detection mechanism
(nothing checks whether a completed chain is still intact) and no repair
behavior (no builder is ever dispatched to rebuild a broken segment) — the
harvester just silently stops delivering for the rest of the game. This is
probably the highest-value gap to close from an economy-protection
standpoint, since it's exactly the kind of failure that's invisible in a
replay unless you're specifically looking for a harvester that stopped
contributing.

> "Defenders also need to be aware of any enemy turrets that have vision of
> our turrets... put down defensive turrets along with builders defending
> against attackers."

Partially aligned. `core_role.py::_update_defense` already reacts to
visible enemy presence near our core by maxing out the home-turret cap (see
`README.md`'s Core section) — that's the "put down defensive turrets in
response to threats" half. What's missing is the more specific framing here:
proactively tracking whether an *existing* enemy turret already has our
own turret in its sights (as opposed to just "is anything enemy visible
right now") and responding to that specifically — e.g. reinforcing or
relocating a turret that's about to trade unfavorably. Nothing in
`core_role.py` reasons about enemy turret facing/range relative to our own
turret placements today.

> "It is also important to make sure that the conveyor belts are correct.
> It's common to see mistakes when there are harvester one tile away from
> the core."

Not specifically verified. `_facing_to_core` (`defender.py`) checks all four
cardinal neighbors of a chain tile for core-adjacency, which *should*
generalize correctly to a harvester built one tile from the core — but this
exact geometry (does a legal conveyor-tile actually exist that's adjacent
to both a one-tile-from-core harvester and the core itself, given the
core's 2×2 footprint?) hasn't been specifically stress-tested. Worth a
targeted check — e.g. force an ore tile immediately next to the core on a
custom map and watch what the chain does — before assuming it's fine just
because it hasn't shown up as a crash.

## Attackers

> "Attackers should path towards the enemy core"

Aligned — `attacker.py::_run_attacker`, step 2 in the priority order (see
`README.md`'s Attacker section).

> "Attackers should put obstacles on ores that are close to enemy turf."

**Clear gap, not implemented at all.** The idea — building a barrier (or
similar) on an ore tile near the enemy so they can never build a harvester
there, since harvesters require an ore tile — is a real area-denial tactic
with no equivalent anywhere in `attacker.py` today. Attackers currently only
ever interact with enemy *harvester/conveyor/splitter* buildings
(`ECONOMY_TARGET_TYPES`), never with bare ore tiles.

> "Attackers will lay down a sentinel according to the global pool. This
> global pool consist of three sentinels, and we strive towards having
> three sentinels facing the enemy core at all times."

**Clear numeric gap, and worth flagging as a direct tension with recent
direction, not just an oversight.** Karrigan currently builds **exactly
one** sentinel, ever, team-wide (`SLOT_SENTINEL_ID`), with no replacement if
it's destroyed (`self.sentinel_built` is a one-way flag — see `README.md`'s
"Known limitations"). The strategy doc asks for a pool of three, actively
maintained ("at all times" implies replacing losses, not just building once).

The reason it's one and not three isn't an accident: it's a direct
consequence of explicit user feedback earlier this session — "far too many
turrets... keep them close to the core" — which is *why* the earlier
multi-gunner siege behavior was removed entirely and replaced with a single,
carefully-aimed sentinel (see `README.md`'s "Why a sentinel, not gunners").
Going to three sentinels maintained persistently is a meaningfully bigger
forward investment than what that feedback was pushing back on, even though
a sentinel's much higher survivability (long range, ignores obstacles) than
a gunner changes the cost/benefit calculation. This is worth resolving as a
conversation, not a unilateral code change — the two directions actively
disagree, and only one of them was written down as explicit prior feedback
on this exact area.

## What's left

Items 1, 2, 4 and 5 from the original ranking here are **done** — shipped
together as the dynamic-builder work (`dynamic.py`, plus the
`SLOT_PERMA_DEFENDER_ID` floor). Remaining, roughly by value:

1. ~~Sentinel count (1 → 3, with replacement)~~ — **done.** The earlier
   tension with "far too many turrets" resolved in favour of `STRATEGY.md`:
   that feedback was about *gunners* parked near the enemy core, and
   sentinels are a different proposition (r²=32 range, obstacle-ignoring
   line shot). Forward sentinels are now the primary win condition — see
   README.md's "Forward sentinels" section.
2. **Orphaned-harvester repair** — the belt-gap detector only catches breaks
   with a surviving upstream conveyor; a harvester whose whole chain died is
   never reconnected. Needs chain-restart logic, not just gap-filling.
3. **Enemy-turret-vision awareness for home turret placement** — currently
   we react to "anything enemy visible near core", not to "that turret has
   line of fire on our turret".
4. **Verify the harvester-adjacent-to-core geometry** — cheap to check with
   a custom map, never actually confirmed.
5. **Opportunity sharing for belt gaps / denial targets** — two dynamic
   builders can duplicate effort. Needs a store slot reclaimed first (the
   store is full); `SLOT_GUNNER_COUNT` is write-only and reclaimable.
