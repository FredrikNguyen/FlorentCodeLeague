"""Everything the CORE unit does: publish its position, manage the ammo
buffer, and run home defense — detecting threats, sizing the dynamic
home-turret cap (2-5), and designating a builder to build the next one.
Builder bots never touch this module directly; they only read the slots it
writes (see constants.py).
"""

import random

from fcode import Controller, EntityType, GameError, Position

from .constants import (
    AMMO_BUFFER,
    AMMO_BUFFER_SIEGE,
    AMMO_ECONOMY_RESERVE,
    AMMO_FLOOR,
    AMMO_FLOOR_RESERVE,
    AMMO_LIFETIME_FRAC,
    AMMO_LIFETIME_MIN,
    AMMO_PRESTOCK_ROUND,
    CRAMPED_CORE_DIST,
    DEADLOCK_POOR_ROUNDS,
    ECONOMY_PHASE_CONVERTING,
    ECONOMY_PHASE_CRISIS,
    ECONOMY_PHASE_OPENING,
    ECONOMY_PHASE_PRESSURE,
    ECONOMY_PRIORITY_CHAINS,
    ECONOMY_RESERVE,
    ECONOMY_RESERVE_CRAMPED,
    ECONOMY_RICH_THRESHOLD,
    ECONOMY_STRONG_CHAINS,
    GUNNER_MIN_ROUND,
    GUNNER_MIN_ROUND_CRAMPED,
    HARVESTER_MILESTONE,
    INCOME_HEARTBEAT_ROUNDS,
    INITIAL_BUILDER_TARGET,
    LATE_BUILDER_TARGET,
    MAX_GUNNERS_CAP,
    MIN_BUILDERS_ALIVE,
    MIN_GUNNERS,
    OFFENSE_MIN_HARVESTERS,
    REINFORCEMENT_BUILDER_TARGET,
    SIEGE_HP_SHIFT,
    SLOT_CORE_SIEGE,
    SLOT_CORE_X,
    SLOT_CORE_Y,
    SLOT_DEFENDER_ID,
    SLOT_GUNNER_CAP,
    SLOT_HARVESTER_COUNT,
    SLOT_ORE_CURSOR,
    SLOT_PERMA_ATTACKER_ID,
    SLOT_PERMA_DEFENDER_ID,
    SLOT_SECOND_ATTACKER_ID,
    SLOT_SENTINEL_COUNT,
    SPAWN_RESERVE,
    STAGE2_FALLBACK_ROUND,
    ore_cursor_from_packed,
    pack_economy_cursor,
)
from .util import core_spawn_ring, manhattan, pack_pos

# Enemy buildings whose position is worth beaconing to the team when one
# turns up near our core. Launchers are included: they throw our builders
# off the core, which is a siege tool even though it deals no damage.
SIEGE_TURRETS = (EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER)


class CoreMixin:
    def _publish_economy_phase(
        self, ct: Controller, harvester_count: int, resources: int
    ) -> None:
        """Publish whether the dynamic workforce may leave route conversion.

        `SLOT_HARVESTER_COUNT` is intentionally historical: builders can only
        prove a chain's geometry locally, and it never falls when an
        infiltrator destroys that route. Pairing it with the Core's existing
        net-resource heartbeat gives the team one conservative, shared phase
        without claiming another Store slot. The low cursor bits are retained
        so an ore advertisement in the same round cannot be lost.
        """
        if (
            resources < ct.get_harvester_cost()
            or self.poor_streak >= DEADLOCK_POOR_ROUNDS
        ):
            phase = ECONOMY_PHASE_CRISIS
        elif harvester_count < ECONOMY_PRIORITY_CHAINS or self.income_seen <= 0:
            phase = ECONOMY_PHASE_OPENING
        elif (
            harvester_count < ECONOMY_STRONG_CHAINS
            or self.income_quiet_rounds > INCOME_HEARTBEAT_ROUNDS
        ):
            phase = ECONOMY_PHASE_CONVERTING
        else:
            phase = ECONOMY_PHASE_PRESSURE
        cursor = ore_cursor_from_packed(ct.read_store(SLOT_ORE_CURSOR))
        ct.write_store(SLOT_ORE_CURSOR, pack_economy_cursor(phase, cursor))

    def _run_core(self, ct: Controller) -> None:
        """Publish our position so builders can orient toward us, keep the ammo
        pool topped up (once it's actually needed), update home defense, and
        spawn builder bots in two stages — gated by a resource reserve so the
        shared cost-scale multiplier never outruns the economy's ability to
        fund a harvester (see INITIAL_BUILDER_TARGET / REINFORCEMENT_BUILDER_TARGET
        in constants.py).
        """
        if not hasattr(self, "income_quiet_rounds"):
            # Keep lightweight CoreMixin probes and archived harness fixtures
            # source-compatible; real Player instances initialise this field.
            self.income_quiet_rounds = 0
        pos = ct.get_position()
        # +1 offset so a core at x=0 or y=0 isn't indistinguishable from an
        # unwritten slot — see main._read_core_pos for the failure this caused.
        ct.write_store(SLOT_CORE_X, pos.x + 1)
        ct.write_store(SLOT_CORE_Y, pos.y + 1)

        self._prune_dead_builders(ct)
        cramped = self._is_cramped(ct)
        harvester_count = ct.read_store(SLOT_HARVESTER_COUNT)
        resources = ct.get_global_resources()
        living = len(self.builder_ids)
        # Workforce is a first-class phase of the strategy.  The opening
        # roster is deliberately small, but once one route is delivering (or
        # the bootstrap has reached a bounded round) we keep adding Builders
        # before discretionary ammo and combat can consume the bank.  This
        # breaks the old deadlock where the team remained at three workers
        # while the opponent reached 7--12.
        stage2 = (
            harvester_count >= HARVESTER_MILESTONE
            or ct.get_current_round() >= STAGE2_FALLBACK_ROUND
        )
        target_living = REINFORCEMENT_BUILDER_TARGET if stage2 else INITIAL_BUILDER_TARGET
        if harvester_count >= ECONOMY_STRONG_CHAINS and resources >= ECONOMY_RICH_THRESHOLD:
            target_living = LATE_BUILDER_TARGET

        # Defense bookkeeping — core is the sole writer of these slots, so there
        # is no read-modify-write race (see the store-slot note in constants.py
        # for why builders writing these directly was a real bug).
        threat = self._update_defense(ct, cramped)

        # --- Ammunition ---
        # convert_ammo() may only be called once per team per turn.
        ammo = ct.get_global_ammo()

        # Measure an intentionally conservative lower bound on income. Add
        # back our own prior conversion so spending does not hide delivery.
        if self.prev_resources is not None:
            delta = resources - self.prev_resources + self.last_conversion
            if delta > 0:
                self.income_seen += delta
                self.income_quiet_rounds = 0
            else:
                self.income_quiet_rounds += 1
        else:
            self.income_quiet_rounds = 0
        self.prev_resources = resources
        self.last_conversion = 0

        # Sustained-poverty counter, feeding _floor_reserve below. This exists
        # because SLOT_HARVESTER_COUNT only ever counts UP — it records chains
        # ever completed, not chains still alive — so "harvester_count == 0"
        # stops being true the moment our first harvester lands and never
        # becomes true again, including after every harvester we own has been
        # destroyed. That is precisely the ladder situation the reserve is for,
        # so the deadlock is detected from the balance directly instead.
        if resources >= ct.get_harvester_cost():
            self.poor_streak = 0
        else:
            self.poor_streak += 1

        self._publish_economy_phase(ct, harvester_count, resources)

        # Resolve the safety floor and optional buffer independently. Combining
        # their largest target with largest budget lets the floor's permissive
        # budget accidentally fund a full siege buffer.
        floor_amount = 0
        if ammo < AMMO_FLOOR:
            floor_amount = min(
                AMMO_FLOOR - ammo,
                max(0, resources - self._floor_reserve(ct, harvester_count, living, target_living)),
            )

        # Buffers on top are worth gating, since they
        # run to 150 Ti. Not before they're needed (that titanium funds the
        # early economy), but immediately if the core is under visible threat.
        buffer_amount = 0
        if threat or ct.get_current_round() >= AMMO_PRESTOCK_ROUND:
            # Once forward sentinels exist, they — not the home gunners —
            # become the dominant ammo consumer by an order of magnitude
            # (10/shot vs 2, and killing a core takes ~28 of those shots),
            # so switch to the much larger siege buffer. See AMMO_BUFFER_SIEGE.
            # Gated on the economy existing too: conversion is 1:1 titanium,
            # so banking a siege chest before we have harvesters just buys
            # ammunition for a war we then lose on resources.
            siege = ct.read_store(SLOT_SENTINEL_COUNT) > 0 and harvester_count >= OFFENSE_MIN_HARVESTERS
            buffer_target = AMMO_BUFFER_SIEGE if siege else AMMO_BUFFER
            if ammo < buffer_target:
                # Keep a hard economy reserve out of conversion — the buffers
                # must never eat the titanium that builds harvesters and belts.
                buffer_amount = min(
                    buffer_target - ammo,
                    max(0, resources - ct.get_builder_bot_cost() - AMMO_ECONOMY_RESERVE),
                )

        amount = min(max(floor_amount, buffer_amount), self._ammo_allowance())
        if amount > 0 and ct.can_convert_ammo(amount):
            ct.convert_ammo(amount)
            self.ammo_spent += amount
            self.last_conversion = amount

        if living >= target_living:
            return
        if living >= INITIAL_BUILDER_TARGET:
            self.ramp_established = True

        # Always keep enough Ti spare to fund a harvester after spawning — the
        # whole point is to never leave the economy unable to afford one. This
        # alone throttles spawning adaptively (each spawn raises the shared cost
        # scale, so the *next* spawn needs more banked first) without a fixed
        # round-delay that would cost tempo on small maps where speed matters
        # more than the marginal scale hit of one extra builder.
        #
        # Exception: if we'd already established our initial roster and
        # attrition has since dropped us below MIN_BUILDERS_ALIVE, replace
        # losses immediately — skip the reserve (we still need the raw cost,
        # just not the safety margin on top of it). Deliberately gated on
        # ramp_established so this bypass can't fire during the very first
        # ramp-up to INITIAL_BUILDER_TARGET — see the constants.py note on
        # why that used to blow through the early economy.
        cost = ct.get_builder_bot_cost()
        reserve = 0 if (self.ramp_established and living < MIN_BUILDERS_ALIVE) else SPAWN_RESERVE
        if ct.get_global_resources() < cost + reserve:
            return

        # Every tile adjacent to the core's 2x2 FOOTPRINT, not the 8 neighbours
        # of its anchor tile — see util.core_spawn_ring for why that distinction
        # was a guaranteed loss on three pool maps.
        candidates = core_spawn_ring(ct, pos)
        random.shuffle(candidates)
        for spawn_pos in candidates:
            if ct.can_spawn(spawn_pos):
                new_id = ct.spawn_builder(spawn_pos)
                self.builder_ids.append(new_id)
                # Hand out the three fixed floor roles, in spawn order: the
                # first builder is the permanent attacker, the second the
                # permanent defender, and the first stage-2 spawn the second
                # permanent attacker. Everyone else is dynamic (see main.py's
                # _assign_role). Each is written once — id 0 is never a real
                # entity id (see the pack_pos +1 offset convention in
                # util.py), so each check only fires before its designation.
                if ct.read_store(SLOT_PERMA_ATTACKER_ID) == 0:
                    ct.write_store(SLOT_PERMA_ATTACKER_ID, new_id)
                elif ct.read_store(SLOT_PERMA_DEFENDER_ID) == 0:
                    ct.write_store(SLOT_PERMA_DEFENDER_ID, new_id)
                elif harvester_count >= OFFENSE_MIN_HARVESTERS and ct.read_store(SLOT_SECOND_ATTACKER_ID) == 0:
                    # Second permanent attacker, gated on a real economy
                    # (OFFENSE_MIN_HARVESTERS, not the earlier stage-2 spawn
                    # milestone): one attacker is the early-pressure budget,
                    # and the offensive budget only grows once there's a base
                    # worth defending.
                    ct.write_store(SLOT_SECOND_ATTACKER_ID, new_id)
                return

    def _ammo_allowance(self) -> int:
        """Return unspent lifetime ammo budget, scaled by observed income."""
        budget = max(AMMO_LIFETIME_MIN, int(AMMO_LIFETIME_FRAC * self.income_seen))
        return max(0, budget - self.ammo_spent)

    def _floor_reserve(
        self,
        ct: Controller,
        harvester_count: int,
        living: int = 0,
        target_living: int = INITIAL_BUILDER_TARGET,
    ) -> int:
        """Titanium the ammo FLOOR may not touch this round.

        Need-based rather than flat. A flat reserve does fix the ratchet, but
        it also withholds titanium in the common case where we are neither
        broke nor under fire, and measurement showed that costs real offence:
        a flat 25 cut core damage dealt per 1000 turns from 2063 to 1136 in
        mirror matches. The two situations where a zero balance is actually
        fatal are specific, so reserve only for those.

        1. The economy is still hand-to-mouth (fewer than
           ECONOMY_PRIORITY_CHAINS completed chains), or a long unbroken run
           of rounds too poor to buy a harvester. At 0 titanium we cannot buy
           the one building that ends the drought, and nothing else will. This
           is the exact deadlock that produced 7 zero-income games out of 21
           on the ladder. The streak arm covers the case the counter cannot —
           see poor_streak.

           The old threshold was `harvester_count == 0`, one chain too
           generous, and it left the ratchet running in exactly the games
           that mattered. Measured on the five losses to the top ladder team:
           with 1-2 chains alive the reserve was 0 every round, and the floor
           rule alone converted 1,185 titanium into ammunition over 289
           rounds — MORE than the 860 we mined all game, 1,045 of it while
           under 60 Ti. It bought 270 damage to a core they healed 268 of.
        2. The core is damaged. Healing is 1 Ti for 4 HP and needs a nonzero
           balance to happen at all; our core was healed for 510 HP across
           those 21 games, the enemy's for 9,352.

        Otherwise the buffer rule's AMMO_ECONOMY_RESERVE is already guarding
        the economy and the floor can spend freely — a dry turret is a real
        cost too.
        """
        reserve = 0
        if harvester_count < ECONOMY_PRIORITY_CHAINS or self.poor_streak >= DEADLOCK_POOR_ROUNDS:
            reserve = ct.get_harvester_cost()
        if ct.get_hp() < ct.get_max_hp():
            reserve = max(reserve, AMMO_FLOOR_RESERVE)
        if living < target_living:
            # The floor cannot be allowed to spend the exact bank needed for
            # the next workforce slot.  Route work and future income outrank
            # keeping a turret topped up during this phase.
            reserve = max(reserve, ct.get_builder_bot_cost() + SPAWN_RESERVE)
        return reserve

    def _publish_siege(self, ct: Controller, turret: Position | None) -> None:
        """Light the core-distress beacon other units steer by.

        This slot exists because of a pure VISION mismatch that cost us five
        straight losses (see CORE_SIEGE_HP in constants.py). Builders detect
        home threats with their own r^2=20 vision; the sentinels that ground
        our core down sat at dist_sq 25-32 from it, outside that. The core's
        own vision is r^2=36 and saw them the entire time — it just had no way
        to tell anyone. Now it does.

        Both halves matter and are packed into the one reclaimed slot:

          missing HP  tells any builder near home that healing the core
                      (4 HP per titanium, the best exchange rate in the game)
                      outranks whatever else it was doing.
          turret pos  tells a builder where the damage is coming from, so it
                      can go remove the cause instead of only treating the
                      symptom. A sentinel cannot rotate, so approaching off
                      its fixed fire line is safe.
        """
        missing = ct.get_max_hp() - ct.get_hp()
        self.core_missing_hp = missing
        ct.write_store(SLOT_CORE_SIEGE, missing * SIEGE_HP_SHIFT + (pack_pos(turret) if turret else 0))

    def _prune_dead_builders(self, ct: Controller) -> None:
        """Drop any tracked builder id that's confirmed destroyed, so the
        living count driving the spawn cap above is exact rather than a
        "spawned so far" counter that only ever grows (the previous version
        of this bot used such a counter and could get stuck at 1 living
        builder for the rest of a game once it had hit the lifetime cap and
        then lost bots to combat, with no way to trigger a replacement).

        get_hp(id)/get_entity_type(id) are NOT vision-free despite the
        engine's own Controller stub not documenting that — empirically
        (verified directly against the engine) querying an id currently
        outside our vision raises GameError("Position out of vision range"),
        while querying a *destroyed* id raises GameError("Unknown id"). Those
        are distinguishable, so we only prune on the latter; a builder we
        simply can't currently see (e.g. an attacker deep in enemy territory)
        is presumed alive rather than falsely pruned and endlessly
        respawned — which is exactly the failure mode this fix would
        otherwise reintroduce.
        """
        alive = []
        for bid in self.builder_ids:
            try:
                if ct.get_hp(bid) > 0:
                    alive.append(bid)
            except GameError as e:
                if "unknown id" not in str(e).lower():
                    alive.append(bid)  # out of vision or similar — can't confirm death
            except Exception:
                alive.append(bid)  # unrecognised failure shape — don't punish for our own uncertainty
        self.builder_ids = alive

    def _is_cramped(self, ct: Controller) -> bool:
        """True on small maps where the enemy core (and its turrets) sit within a
        short walk, estimated via the 180°-rotation mirror of our own core
        (assumes rotational map symmetry). On these maps combat dominates and
        tempo beats caution, so both defense and spawn policy shift — see
        CRAMPED_CORE_DIST and the *_CRAMPED constants. Core-only (uses
        ct.get_position() directly as the core's own position).
        """
        w, h = ct.get_map_width(), ct.get_map_height()
        pos = ct.get_position()
        mirror = Position(w - 1 - pos.x, h - 1 - pos.y)
        return manhattan(pos, mirror) <= CRAMPED_CORE_DIST

    def _update_defense(self, ct: Controller, cramped: bool) -> bool:
        """Count live home gunners, detect any enemy unit/building currently
        visible to the core, compute a dynamic home-turret cap (2-5) from
        economy + that threat signal, and — if we want another turret — write
        the cap and designate exactly one builder in vision to build it this
        round. Returns whether a threat is currently visible (the core also
        uses this to decide whether to rush ammo).

        The cap is written only here, so
        unlike a counter incremented by many builders in the same round (which
        all see the same stale value before any write lands — see the store
        note in constants.py), this can never overshoot: at most one builder
        is ever authorised per round, and the count is a direct observation,
        not an accumulator.
        """
        team = ct.get_team()
        pos = ct.get_position()
        # Observe newly placed home Gunners and retain their ids across turns.
        # `get_nearby_buildings()` is vision-bounded, so a plain per-turn count
        # forgets a turret as soon as it falls outside that window and turns a
        # target cap into an unbounded production loop.  Unknown ids are pruned
        # when the engine confirms destruction; out-of-vision errors are kept.
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == team and ct.get_entity_type(bid) == EntityType.GUNNER:
                self.gunner_ids.add(bid)
                self.gunner_history.add(bid)
        observed_gunners: set[int] = set()
        for gid in self.gunner_ids:
            try:
                if ct.get_hp(gid) > 0:
                    observed_gunners.add(gid)
            except GameError as exc:
                if "unknown id" not in str(exc).lower():
                    observed_gunners.add(gid)
            except Exception:
                observed_gunners.add(gid)
        self.gunner_ids = observed_gunners
        # Count lifetime placements, not only currently alive/visible turrets.
        # A destroyed home Gunner does not reopen an unlimited spending loop.
        gunner_count = len(self.gunner_history)
        threat = False
        siege_turret = None
        siege_dist = None
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == team:
                continue
            threat = True
            # Remember the nearest enemy TURRET specifically, so the beacon
            # below points at the thing actually doing the damage rather than
            # at a passing conveyor. See _publish_siege.
            if ct.get_entity_type(bid) not in SIEGE_TURRETS:
                continue
            p = ct.get_position(bid)
            d = pos.distance_squared(p)
            if siege_dist is None or d < siege_dist:
                siege_dist = d
                siege_turret = p
        if not threat:
            for uid in ct.get_nearby_units():
                if ct.get_team(uid) != team:
                    threat = True
        self._publish_siege(ct, siege_turret)

        # Cap: 2 baseline, +1 if the economy has titanium to spare beyond its
        # own reserve, +1 on cramped maps (defense matters more there), and
        # straight to the max if anything enemy is visible near the core right
        # now — react to a real threat rather than waiting on the usual gates.
        # While the economy is still hand-to-mouth, defence has to stay
        # proportionate: the threat response below otherwise jumps straight to
        # five turrets and drops the economy reserve the moment ANY enemy is
        # visible, so a single passing scout could buy five gunners out of the
        # harvester budget — measured as one of two reasons chains stalled flat
        # at 2 while titanium sat at ~15. See ECONOMY_PRIORITY_CHAINS.
        economy_young = ct.read_store(SLOT_HARVESTER_COUNT) < ECONOMY_PRIORITY_CHAINS

        cap = MIN_GUNNERS
        if ct.get_global_resources() >= ECONOMY_RICH_THRESHOLD:
            cap += 1
        if cramped:
            cap += 1
        if threat and not economy_young:
            cap = MAX_GUNNERS_CAP
        cap = min(cap, MAX_GUNNERS_CAP)
        ct.write_store(SLOT_GUNNER_CAP, cap)

        min_round = GUNNER_MIN_ROUND_CRAMPED if cramped else GUNNER_MIN_ROUND
        reserve = ECONOMY_RESERVE_CRAMPED if cramped else ECONOMY_RESERVE
        if threat:
            # Under active threat, respond now regardless of round. Once the
            # economy is established we also waive most of the reserve for an
            # urgently-needed turret; before then we keep it, so the response
            # is "a turret or two, if affordable" rather than "spend the
            # harvester budget".
            min_round = 0
            if not economy_young:
                reserve = min(reserve, 20)

        want_more = (
            gunner_count < cap
            and ct.get_current_round() >= min_round
            and ct.get_global_resources() >= ct.get_gunner_cost() + reserve
        )
        if not want_more:
            ct.write_store(SLOT_DEFENDER_ID, 0)
            return threat

        candidates = [
            uid
            for uid in ct.get_nearby_units()
            if ct.get_team(uid) == team and ct.get_entity_type(uid) == EntityType.BUILDER_BOT
        ]
        if not candidates:
            ct.write_store(SLOT_DEFENDER_ID, 0)
            return threat
        candidates.sort()
        chosen = candidates[ct.get_current_round() % len(candidates)]
        ct.write_store(SLOT_DEFENDER_ID, chosen)
        return threat
