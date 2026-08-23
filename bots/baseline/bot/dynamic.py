"""DYNAMIC builder-bot role: greedy per-task selection.

Most builders are dynamic. Rather than being locked to economy or offense
for life, a dynamic builder re-picks a TASK from a strict priority list
whenever it's between tasks, taking the highest-priority thing it can
personally see. See DESIGN_dynamic_builders.md for the full rationale;
the short version:

  TASK_HOME_THREAT  enemy near our core (turret > harvester > anything else)
  TASK_BELT_REPAIR  a gap in our conveyor network
  TASK_HARVEST      the normal economy loop (delegates to defender.py)
  TASK_RETIRE_GUNNER remove one surplus home Gunner only during a cash shortfall
  TASK_RAID         a surplus-funded raid on visible enemy logistics
  TASK_ORE_DENIAL   barrier an ore tile on the enemy's half of the map
  TASK_ADVANCE      fallback: march on the enemy core, harass it on arrival

Three things keep greedy selection from thrashing:

  * Tasks end on their own termination condition (achieved / confirmed
    gone), not a timer — TASK_MAX_ROUNDS is only a runaway backstop.
  * A task is preempted only by a STRICTLY higher priority. Since the
    priorities are discrete, that gives tie-hysteresis with no tuning.
  * Commitment scales with sunk investment: a chain in progress is
    effectively non-preemptible (abandoning it strands conveyors that
    deliver nothing), while merely walking somewhere is cheap to drop.

Proximity gating is free: every detector below works off this builder's own
vision, so a builder that can't see a threat never bids on it. TASK_HOME_THREAT
therefore recruits builders already near home instead of yanking the whole
pool back across the map.
"""

from fcode import Controller, Direction, EntityType, Environment, Position

from .constants import (
    BELT_OUT_BELT,
    BELT_OUT_CORE,
    BELT_OUT_DEAD,
    BELT_OUT_GAP,
    BELT_OUT_UNKNOWN,
    CARDINALS,
    COMMIT_FLOOR_MIN,
    COMMIT_FLOOR_SPREAD,
    CORE_SIEGE_HP,
    DYNAMIC_ECONOMY_FLOOR,
    ECONOMY_PHASE_CONVERTING,
    ECONOMY_PHASE_CRISIS,
    ECONOMY_PHASE_OPENING,
    ECONOMY_PHASE_PRESSURE,
    HOME_THREAT_RADIUS_SQ,
    IDLE_ATTACK_RESERVE,
    MIN_GUNNERS,
    MODE_CHAIN,
    OFFENSE_MIN_HARVESTERS,
    ORE_QUEUE_LEN,
    SIEGE_HP_SHIFT,
    SLOT_CORE_SIEGE,
    SLOT_HARVESTER_COUNT,
    SLOT_ORE_CURSOR,
    SLOT_ORE_QUEUE_BASE,
    SLOT_PERMA_ATTACKER_ID,
    SLOT_PERMA_DEFENDER_ID,
    SLOT_SECOND_ATTACKER_ID,
    SENTINEL_POOL_TARGET,
    TASK_ADVANCE,
    TASK_BASE_REPAIR,
    TASK_BELT_REPAIR,
    TASK_HARVEST,
    TASK_HIJACK,
    TASK_HOME_THREAT,
    TASK_MAX_ROUNDS,
    TASK_NONE,
    TASK_ORE_DENIAL,
    TASK_RAID,
    TASK_RETIRE_GUNNER,
    economy_phase_from_cursor,
)
from .util import adjacent, in_bounds, manhattan, unpack_pos

# Enemy buildings that count as a turret threat (ranked worst-first inside
# _find_home_threat). Launchers are included: they throw our builders around,
# which is disruptive enough to treat like a turret.
THREAT_TURRETS = (EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER)


class DynamicMixin:
    def _run_dynamic(self, ct: Controller, danger: set[Position]) -> None:
        # A chain in progress is effectively non-preemptible — see the module
        # docstring. (The flee check upstream in _run_builder still overrides.)
        if self.mode == MODE_CHAIN:
            self._run_chain(ct, danger)
            return

        self._validate_task(ct)
        self._maybe_switch_task(ct)
        self._execute_task(ct, danger)

    # ------------------------------------------------------------------
    # Task bookkeeping
    # ------------------------------------------------------------------

    def _commit_floor(self, ct: Controller) -> int:
        """Rounds before this builder will consider preempting its own task.
        Varied by id so the pool doesn't re-evaluate in lockstep."""
        return COMMIT_FLOOR_MIN + (ct.get_id() % COMMIT_FLOOR_SPREAD)

    def _set_task(self, ct: Controller, task: int, target: Position | None) -> None:
        self.task = task
        self.task_target = target
        self.task_started = ct.get_current_round()

    def _clear_task(self) -> None:
        self.task = TASK_NONE
        self.task_target = None

    def _validate_task(self, ct: Controller) -> None:
        """Drop the current task once it's achieved, confirmed impossible, or
        has run past the runaway backstop.

        Every tile query here is guarded by is_in_vision first: task_target is
        a remembered position that is very often out of vision while we're
        still walking to it, and querying such a position raises GameError
        rather than returning a falsy answer (see README.md). "Can't see it"
        must mean "keep going", never "give up".
        """
        if self.task == TASK_NONE:
            return
        target = self.task_target
        if target is None or not in_bounds(ct, target):
            self._clear_task()
            return
        if ct.get_current_round() - self.task_started >= TASK_MAX_ROUNDS:
            self._clear_task()
            return
        if self.task == TASK_ADVANCE or not ct.is_in_vision(target):
            return  # ADVANCE never "completes"; unseen targets stay committed

        if self.task == TASK_HOME_THREAT:
            if ct.get_tile_building_id(target) is None and ct.get_tile_builder_bot_id(target) is None:
                self._clear_task()  # killed it, or it moved on
        elif self.task == TASK_BELT_REPAIR:
            # Deliberately the same classifier the finder used, not a separate
            # "is it empty" test: the task now covers two defect shapes (a gap
            # to fill AND a conveyor to re-point), and an occupied tile means
            # "done" for the first but "still broken" for the second. Testing
            # emptiness here would abandon every re-point task on arrival.
            bid = ct.get_tile_building_id(target)
            if bid is None:
                pass  # still a gap — keep going
            elif (ct.get_team(bid) != ct.get_team()
                  or ct.get_entity_type(bid) != EntityType.CONVEYOR
                  or self._belt_output_status(ct, target, ct.get_direction(bid)) != BELT_OUT_DEAD):
                self._clear_task()  # filled, re-pointed, or no longer ours
        elif self.task == TASK_BASE_REPAIR:
            bid = ct.get_tile_building_id(target)
            if bid is None or ct.get_hp(bid) >= ct.get_max_hp(bid):
                self._clear_task()  # healed to full, or lost it
        elif self.task == TASK_RETIRE_GUNNER:
            bid = ct.get_tile_building_id(target)
            if (
                bid is None
                or ct.get_team(bid) != ct.get_team()
                or ct.get_entity_type(bid) != EntityType.GUNNER
                or not self._low_liquidity_retirement_allowed(ct)
            ):
                self._clear_task()
        elif self.task == TASK_ORE_DENIAL:
            if ct.get_tile_building_id(target) is not None:
                self._clear_task()  # someone built there first
        elif self.task == TASK_HARVEST:
            if ct.get_tile_building_id(target) is not None:
                self._clear_task()  # ore got claimed
        elif self.task == TASK_HIJACK:
            bid = ct.get_tile_building_id(target)
            if bid is None or ct.get_team(bid) == ct.get_team() or ct.get_entity_type(bid) != EntityType.HARVESTER:
                self._clear_task()
        elif self.task == TASK_RAID:
            bid = ct.get_tile_building_id(target)
            if (
                bid is None
                or ct.get_team(bid) == ct.get_team()
                or ct.get_entity_type(bid) not in self.ECONOMY_TARGET_TYPES
            ):
                # A raid ending is a state transition, not a license to pick
                # another offensive target immediately. The destroyed tile
                # often exposed a route gap or a damaged home belt; claim one
                # visible repair before returning to the normal greedy pool.
                # This is bounded by the ordinary repair task backstop and is
                # only entered after the target is confirmed gone, so it
                # cannot pull a raider off an active attack or interrupt a
                # route owner in CHAIN mode.
                repair = self._find_belt_gap(ct)
                if repair is not None:
                    self._set_task(ct, TASK_BELT_REPAIR, repair)
                else:
                    damaged = self._find_damaged_building(ct)
                    if damaged is not None:
                        self._set_task(ct, TASK_BASE_REPAIR, damaged)
                    else:
                        self._clear_task()

    def _maybe_switch_task(self, ct: Controller) -> None:
        """Greedy pick, with strict-preemption hysteresis."""
        best = self._best_task(ct)
        if best is None:
            return
        priority, target = best
        if self.task == TASK_NONE:
            self._set_task(ct, priority, target)
            return
        if priority < self.task:
            # Strictly higher priority only — equal priority never preempts,
            # which is what stops two near-tied options from trading places.
            if ct.get_current_round() - self.task_started >= self._commit_floor(ct):
                self._set_task(ct, priority, target)
        elif priority == self.task and self.task_target is None:
            self._set_task(ct, priority, target)

    def _best_task(self, ct: Controller) -> tuple[int, Position | None] | None:
        target = self._find_home_threat(ct)
        # A nearby enemy Harvester is an income opportunity, not a combat
        # threat; reserve it for the hijack route below.
        if target is not None and self._is_nearest_home_responder(ct, target) and (
            not ct.is_in_vision(target)
            or ct.get_tile_building_id(target) is None
            or ct.get_entity_type(ct.get_tile_building_id(target)) != EntityType.HARVESTER
        ):
            return (TASK_HOME_THREAT, target)
        target = self._find_belt_gap(ct)
        if target is not None:
            return (TASK_BELT_REPAIR, target)
        target = self._find_enemy_harvester(ct)
        if target is not None:
            return (TASK_HIJACK, target)
        target = self._find_damaged_building(ct)
        if target is not None:
            return (TASK_BASE_REPAIR, target)
        if self._should_harvest(ct):
            return (TASK_HARVEST, None)  # defender.py picks its own ore target
        target = self._find_low_liquidity_gunner(ct)
        if target is not None:
            return (TASK_RETIRE_GUNNER, target)
        target = self._find_raid_target(ct)
        if target is not None:
            return (TASK_RAID, target)
        target = self._find_denial_target(ct)
        if target is not None:
            return (TASK_ORE_DENIAL, target)
        return (TASK_ADVANCE, self._enemy_core_target(ct))

    def _offense_unlocked(self, ct: Controller) -> bool:
        """Has the team earned the right to send dynamic builders on offense?

        See OFFENSE_MIN_HARVESTERS — without this gate the pool defaulted to
        attacking whenever ore wasn't already in sight, and the bot reliably
        out-aggressed itself into losing on resources.
        """
        return ct.read_store(SLOT_HARVESTER_COUNT) >= OFFENSE_MIN_HARVESTERS

    # ------------------------------------------------------------------
    # Task execution
    # ------------------------------------------------------------------

    def _execute_task(self, ct: Controller, danger: set[Position]) -> None:
        if self.task == TASK_HARVEST:
            self._run_defender(ct, danger)  # full SCOUT/CHAIN economy loop
            return
        if self.task == TASK_HOME_THREAT:
            self._execute_strike(ct, danger)
            return
        if self.task == TASK_HIJACK:
            self._execute_hijack(ct, danger)
            return
        if self.task == TASK_BELT_REPAIR:
            self._execute_belt_repair(ct, danger)
            return
        if self.task == TASK_BASE_REPAIR:
            self._execute_base_repair(ct, danger)
            return
        if self.task == TASK_RETIRE_GUNNER:
            self._execute_retire_gunner(ct, danger)
            return
        if self.task == TASK_RAID:
            self._execute_raid(ct, danger)
            return
        if self.task == TASK_ORE_DENIAL:
            self._execute_denial(ct, danger)
            return
        self._execute_advance(ct, danger)

    def _execute_hijack(self, ct: Controller, danger: set[Position]) -> None:
        """Seed a route from one visible enemy Harvester."""
        if self.task_target is None:
            self._clear_task()
            return
        self.hijack_harvester = self.task_target
        if self._try_hijack_enemy_harvester(ct, danger):
            return
        self._clear_task()

    def _execute_strike(self, ct: Controller, danger: set[Position]) -> None:
        """Answer a home threat.

        Against an enemy TURRET, build a counter-gunner and leave rather than
        trading punches: builder-fire is 2 dmg/hit, so grinding down a 30 HP
        sentinel means 15 rounds parked in its kill zone, and it kills the
        40 HP builder in 4. A gunner does 10 dmg on reload 1 and fights on
        after we've walked away. See COUNTER_TURRET_RANGE_SQ.

        Against anything softer (a harvester, an enemy builder) plain
        builder-fire is fine — those don't shoot back nearly as hard, and a
        turret would be an over-investment.
        """
        target = self.task_target
        if target is None:
            return
        if not self._is_nearest_home_responder(ct, target):
            # Home-threat detection is local, so several dynamic Builders can
            # see the same turret/harvester.  Allocate the response to one
            # nearest non-attacker instead of letting every observer spend a
            # turn travelling or build duplicate counter-Gunners.
            self._clear_task()
            return
        pos = ct.get_position()

        if self._is_enemy_turret(ct, target):
            # Do not build a remote counter-Gunner here.  The old response was
            # locally sensible but globally unbounded: every Builder that could
            # see the same enemy turret independently bought a new Gunner, while
            # the Core could only count home-visible Gunners.  In live losses
            # this produced 15--59 Gunners, 1--10 Harvesters, and a starved
            # workforce.  A Builder already beside the threat can trade its
            # cheap adjacent attack; otherwise it closes in and lets the
            # Core-designated home defense handle the base.  This is a strategy
            # boundary, not a smaller counter-turret cap.
            if adjacent(pos, target):
                if ct.get_action_cooldown() == 0 and ct.can_fire(target):
                    ct.fire(target)
                return
            # Not in position (or couldn't place yet) — close in, but never
            # through the turret's own fire line (_navigate avoids danger).
            if ct.get_move_cooldown() == 0:
                self._navigate(ct, target, avoid=danger)
            return

        if adjacent(pos, target):
            if ct.get_action_cooldown() == 0 and ct.can_fire(target):
                ct.fire(target)
            return
        if ct.get_move_cooldown() == 0:
            self._navigate(ct, target, avoid=danger)

    def _is_nearest_home_responder(self, ct: Controller, target: Position) -> bool:
        """Return whether this dynamic Builder owns the local home response.

        The old task picker was greedy per unit: all Builders with the same
        vision independently claimed one threat, and each could construct a
        counter-Gunner before any of the others observed it.  The Core cannot
        cheaply publish a per-threat assignment, but every responder can make
        the same deterministic nearest-distance decision from shared vision.
        Permanent attackers are excluded because their role does not execute
        TASK_HOME_THREAT; the permanent defender remains eligible.
        """
        my_id = ct.get_id()
        my_dist = ct.get_position().distance_squared(target)
        fixed_attackers = {
            ct.read_store(SLOT_PERMA_ATTACKER_ID),
            ct.read_store(SLOT_SECOND_ATTACKER_ID),
        }
        for uid in ct.get_nearby_units():
            if uid == my_id or uid in fixed_attackers:
                continue
            if ct.get_team(uid) != ct.get_team() or ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                continue
            other_dist = ct.get_position(uid).distance_squared(target)
            if other_dist < my_dist or (other_dist == my_dist and uid < my_id):
                return False
        return True

    def _is_enemy_turret(self, ct: Controller, pos: Position) -> bool:
        if not in_bounds(ct, pos) or not ct.is_in_vision(pos):
            return False
        bid = ct.get_tile_building_id(pos)
        if bid is None or ct.get_team(bid) == ct.get_team():
            return False
        return ct.get_entity_type(bid) in THREAT_TURRETS

    def _try_build_counter_turret(
        self, ct: Controller, target: Position, danger: set[Position]
    ) -> int | None:
        """Legacy hook retained for callers/tests; remote counter-Gunners are retired.

        Remote turret construction was removed from the strategy because a
        per-Builder visibility decision had no global ownership or lifetime
        accounting. Keeping the method as a no-op makes that invariant explicit
        and prevents a future task branch from silently reintroducing the
        runaway Gunner loop.
        """
        return None

    def _execute_base_repair(self, ct: Controller, danger: set[Position]) -> None:
        """Heal a damaged friendly building (1 Ti -> +4 HP). Cheap way to keep
        harvesters, belts and turrets alive instead of letting chip damage
        accumulate until they're destroyed and have to be rebuilt outright.
        """
        target = self.task_target
        if target is None:
            return
        if adjacent(ct.get_position(), target):
            if ct.get_action_cooldown() == 0 and ct.can_heal(target):
                ct.heal(target)
            return
        if ct.get_move_cooldown() == 0:
            self._navigate(ct, target, avoid=danger)

    def _low_liquidity_retirement_allowed(self, ct: Controller) -> bool:
        """Return whether removing one surplus home Gunner is safe now.

        This is deliberately a liquidity escape hatch, not a general defense
        policy.  It only opens after four completed routes, while the bank
        cannot fund the next Harvester, and while the
        Core has neither a fresh siege beacon nor a visible enemy near home.
        The three-Gunner floor remains the hard safety boundary.
        """
        core = getattr(self, "core_pos", None)
        if core is None:
            return False
        if ct.read_store(SLOT_HARVESTER_COUNT) < OFFENSE_MIN_HARVESTERS + 1:
            return False
        if ct.get_global_resources() >= ct.get_harvester_cost():
            return False
        if ct.read_store(SLOT_CORE_SIEGE) // SIEGE_HP_SHIFT >= CORE_SIEGE_HP:
            return False

        team = ct.get_team()
        gunners = []
        for bid in ct.get_nearby_buildings():
            entity_team = ct.get_team(bid)
            position = ct.get_position(bid)
            if entity_team == team:
                if ct.get_entity_type(bid) == EntityType.GUNNER:
                    gunners.append((position.distance_squared(core), bid, position))
                continue
            if position.distance_squared(core) <= HOME_THREAT_RADIUS_SQ:
                return False
        for uid in ct.get_nearby_units():
            if ct.get_team(uid) != team and ct.get_position(uid).distance_squared(core) <= HOME_THREAT_RADIUS_SQ:
                return False
        if len(gunners) <= MIN_GUNNERS + 1:
            return False

        # Retire the outermost visible Gunner, assigning it to one deterministic
        # nearby non-attacker.  The live count is rechecked next round, so two
        # observers cannot remove below the floor even with delayed Store data.
        gunners.sort(key=lambda item: (-item[0], item[1]))
        for _, _bid, position in gunners:
            if self._is_nearest_home_responder(ct, position):
                return True
        return False

    def _find_low_liquidity_gunner(self, ct: Controller) -> Position | None:
        """Find the outermost safe home Gunner eligible for retirement."""
        core = getattr(self, "core_pos", None)
        if not self._low_liquidity_retirement_allowed(ct) or core is None:
            return None
        team = ct.get_team()
        gunners = []
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) != team or ct.get_entity_type(bid) != EntityType.GUNNER:
                continue
            position = ct.get_position(bid)
            gunners.append((position.distance_squared(core), bid, position))
        gunners.sort(key=lambda item: (-item[0], item[1]))
        for _, _bid, position in gunners:
            if not adjacent(ct.get_position(), position):
                continue
            if self._is_nearest_home_responder(ct, position):
                return position
        return None

    def _execute_retire_gunner(self, ct: Controller, danger: set[Position]) -> None:
        """Walk to and legally destroy one safe surplus home Gunner."""
        target = self.task_target
        if target is None:
            self._clear_task()
            return
        if not self._low_liquidity_retirement_allowed(ct):
            self._clear_task()
            return
        if adjacent(ct.get_position(), target):
            bid = ct.get_tile_building_id(target)
            if (
                bid is not None
                and ct.get_team(bid) == ct.get_team()
                and ct.get_entity_type(bid) == EntityType.GUNNER
                and ct.can_destroy(target)
            ):
                ct.destroy(target)
            self._clear_task()
            return
        if ct.get_move_cooldown() == 0:
            self._navigate(ct, target, avoid=danger)

    def _execute_belt_repair(self, ct: Controller, danger: set[Position]) -> None:
        """Fix the belt defect at task_target: build into a gap, or re-point a
        conveyor that's aimed somewhere no stack can go.

        Re-pointing needs destroy-then-build in the SAME turn, which is legal
        because destroy() costs no action, has no cooldown and is unlimited
        per turn, while only the rebuild consumes the action. Everything that
        could make the rebuild fail is therefore checked BEFORE the destroy —
        affordability, a viable facing, and that the facing is actually
        different — because a destroy we can't follow through on would leave
        the network strictly worse than we found it.
        """
        target = self.task_target
        if target is None:
            return
        pos = ct.get_position()
        if not adjacent(pos, target):
            if ct.get_move_cooldown() == 0:
                self._navigate(ct, target, avoid=danger)
            return
        if ct.get_action_cooldown() != 0 or ct.get_global_resources() < ct.get_conveyor_cost():
            return

        facing = self._repair_facing(ct, target)
        if facing is None:
            self._clear_task()  # nothing here would help; go find other work
            return

        bid = ct.get_tile_building_id(target)
        if bid is None:
            if ct.can_build_conveyor(target, facing):
                ct.build_conveyor(target, facing)
            self._clear_task()
            return

        # Occupied: only ever our own misdirected conveyor (the finder rejects
        # everything else). Leave it alone if the facing wouldn't change.
        if ct.get_direction(bid) == facing or not ct.can_destroy(target):
            self._clear_task()
            return
        ct.destroy(target)
        if ct.can_build_conveyor(target, facing):
            ct.build_conveyor(target, facing)
        self._clear_task()

    def _execute_denial(self, ct: Controller, danger: set[Position]) -> None:
        """Barrier an ore tile so the enemy can never harvest it."""
        target = self.task_target
        if target is None:
            return
        pos = ct.get_position()
        if adjacent(pos, target):
            if ct.get_action_cooldown() != 0 or ct.get_global_resources() < ct.get_barrier_cost():
                return
            if not self._would_sever_belt(ct, target) and ct.can_build_barrier(target):
                ct.build_barrier(target)
            self._clear_task()
            return
        if ct.get_move_cooldown() == 0:
            self._navigate(ct, target, avoid=danger)

    def _execute_raid(self, ct: Controller, danger: set[Position]) -> None:
        """Spend the fixed surplus reserve to break one enemy logistics tile.

        The target is selected only after the economy gate and is owned by the
        nearest visible builder, so a shared sighting produces one raid lane
        rather than every dynamic builder queueing on the same conveyor.  The
        attacker primitive handles cardinal approach, visibility-safe target
        validation, and the two-titanium builder-fire action.
        """
        target = self.task_target
        if target is None or ct.get_global_resources() < IDLE_ATTACK_RESERVE:
            self._clear_task()
            return
        self.attack_target = target
        if self._handle_attack_target(ct, danger):
            return
        self.attack_target = None
        self._clear_task()

    def _execute_advance(self, ct: Controller, danger: set[Position]) -> None:
        """Fallback so a dynamic builder is never idle: head for the enemy
        core, planting a forward sentinel if the pool still has room, else
        chipping at the core on arrival.

        Dynamic builders help fill the sentinel pool rather than leaving it
        to the two floor attackers alone — three sentinels placed by round
        ~100 is the actual win condition, and two attackers walking there
        one at a time is too slow to hit it. _try_build_sentinel enforces
        the pool cap and the confirmed-sighting requirement itself, so this
        can't overbuild. It is still gated on the economy having earned it
        (OFFENSE_MIN_HARVESTERS): a 30 Ti sentinel bought before we have
        harvesters is exactly the over-aggression this class of builder was
        found guilty of.
        """
        enemy_core = self.task_target
        if enemy_core is None:
            enemy_core = self._enemy_core_target(ct)
        if enemy_core is None:
            if ct.get_move_cooldown() == 0:
                self._navigate(ct, self._far_explore_target(ct), avoid=danger)
            return
        if self._offense_unlocked(ct) and self._try_build_sentinel(ct, enemy_core) is not None:
            return
        self._harass(ct, enemy_core, danger)

    # ------------------------------------------------------------------
    # Detectors (all vision-based — that's what gives us proximity gating)
    # ------------------------------------------------------------------

    def _find_enemy_harvester(self, ct: Controller) -> Position | None:
        """Find one visible enemy Harvester, preferring an orphaned source."""
        team = ct.get_team()
        pos = ct.get_position()
        candidates: list[tuple[int, int, int, int, Position]] = []
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == team or ct.get_entity_type(bid) != EntityType.HARVESTER:
                continue
            harvester = ct.get_position(bid)
            outlets = 0
            for d in CARDINALS:
                n = harvester.add(d)
                if not in_bounds(ct, n) or not ct.is_in_vision(n):
                    continue
                other = ct.get_tile_building_id(n)
                if other is not None and ct.get_team(other) == team and ct.get_entity_type(other) in (EntityType.CONVEYOR, EntityType.SPLITTER):
                    outlets += 1
            candidates.append((outlets, pos.distance_squared(harvester), harvester.x, harvester.y, harvester))
        if not candidates:
            return None
        candidates.sort(key=lambda item: item[:4])
        return candidates[0][4]

    def _find_home_threat(self, ct: Controller) -> Position | None:
        """Nearest enemy near our own core, ranked: turret > harvester >
        anything else hostile. A turret is doing ongoing ranged damage, so it
        outranks an economy building, which outranks a plain brawl.
        """
        if self.core_pos is None:
            return None
        team = ct.get_team()
        pos = ct.get_position()
        best: list[tuple[float, Position] | None] = [None, None, None]

        def offer(rank: int, p: Position) -> None:
            d = pos.distance_squared(p)
            if best[rank] is None or d < best[rank][0]:
                best[rank] = (d, p)

        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == team:
                continue
            etype = ct.get_entity_type(bid)
            if etype == EntityType.CORE:
                continue  # that's their base, not a threat to ours
            p = ct.get_position(bid)
            if p.distance_squared(self.core_pos) > HOME_THREAT_RADIUS_SQ:
                continue
            if etype in THREAT_TURRETS:
                offer(0, p)
            elif etype == EntityType.HARVESTER:
                offer(1, p)
            # Anything ELSE the enemy owns — conveyors, splitters, barriers —
            # is deliberately NOT a home threat. It cannot hurt our core, and
            # treating it as one was measured to wreck the whole dynamic pool:
            # 48% of all dynamic builder-rounds went to HOME_THREAT, with
            # ORE_DENIAL and ADVANCE never firing even once, because there is
            # always some enemy belt within range and each one takes ~10
            # rounds of builder-fire to chew through. Wrecking enemy belts is
            # OFFENSE (attacker.py's job, and TASK_ORE_DENIAL's), not defence.

        for uid in ct.get_nearby_units():
            if ct.get_team(uid) == team:
                continue
            if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                continue  # turrets already counted via get_nearby_buildings
            p = ct.get_position(uid)
            if p.distance_squared(self.core_pos) <= HOME_THREAT_RADIUS_SQ:
                offer(2, p)

        for entry in best:
            if entry is not None:
                return entry[1]
        return None

    def _find_damaged_building(self, ct: Controller) -> Position | None:
        """Nearest friendly building at home that's taken damage.

        Healing is 1 Ti for +4 HP — far cheaper than letting chip damage
        accumulate until the building dies and the whole thing (harvester,
        belt run, turret) has to be rebuilt from scratch. Restricted to our
        own base area so builders don't wander off healing forward sentinels.
        """
        if self.core_pos is None:
            return None
        team = ct.get_team()
        pos = ct.get_position()
        best = None
        best_dist = float("inf")
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) != team:
                continue
            p = ct.get_position(bid)
            if p.distance_squared(self.core_pos) > HOME_THREAT_RADIUS_SQ:
                continue
            if ct.get_hp(bid) >= ct.get_max_hp(bid):
                continue
            d = pos.distance_squared(p)
            if d < best_dist:
                best_dist = d
                best = p
        return best

    def _find_belt_gap(self, ct: Controller) -> Position | None:
        """Where the conveyor network is broken and needs a tile rebuilt.

        Checked in value order:

        1. A missing tile on the CORE RING — the permanent ring of conveyors
           on every core-adjacent tile, each facing in. Highest leverage in
           the game for 3 Ti: with the ring intact, any chain that reaches
           the core's neighbourhood delivers, instead of having to land its
           final tile exactly right. Worth walking to, unlike the
           opportunistic version in defender.py.
        2. A friendly conveyor whose output tile is empty — the chain is
           severed exactly there.

        Local and memoryless on purpose: the builder that laid a chain may be
        long dead, and per-unit state isn't shared. A conveyor pointing into
        the core or a wall is not a false positive (neither tile reads as
        empty). Repairs self-propagate — the rebuilt conveyor faces onward,
        so if its own output is also empty that's detected next round.
        """
        ring_gap = self._find_core_ring_gap(ct)
        if ring_gap is not None and not self._someone_working_at(ct, ring_gap):
            return ring_gap
        team = ct.get_team()
        pos = ct.get_position()
        best = None
        best_dist = float("inf")
        misdirected = None
        misdirected_dist = float("inf")
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) != team:
                continue
            if ct.get_entity_type(bid) != EntityType.CONVEYOR:
                continue
            p = ct.get_position(bid)
            status = self._belt_output_status(ct, p, ct.get_direction(bid))
            if status == BELT_OUT_GAP:
                gap = p.add(ct.get_direction(bid))
                if self.core_pos is not None and manhattan(gap, self.core_pos) > self.harvest_range:
                    continue  # out of our economic footprint; not worth chasing
                if self._someone_working_at(ct, gap):
                    continue  # an active chain's frontier, or a teammate on it
                d = pos.distance_squared(gap)
                if d < best_dist:
                    best_dist = d
                    best = gap
            elif status == BELT_OUT_DEAD:
                # Case 3: terminally misdirected. Unlike a gap this tile is
                # already occupied — the repair is to re-point it (destroy +
                # rebuild facing somewhere that accepts), see
                # _execute_belt_repair. Only worth claiming if a better facing
                # actually exists from here, otherwise we'd walk over, fail,
                # and re-pick it forever.
                if self.core_pos is not None and manhattan(p, self.core_pos) > self.harvest_range:
                    continue
                if self._someone_working_at(ct, p):
                    continue
                if self._repair_facing(ct, p) is None:
                    continue
                d = pos.distance_squared(p)
                if d < misdirected_dist:
                    misdirected_dist = d
                    misdirected = p
        # Severed belts first: they're one 3 Ti build from delivering, whereas
        # re-pointing spends a conveyor to reclaim one. Both are cheap and the
        # misdirected case is only reachable once no gap is in view.
        return best if best is not None else misdirected

    def _someone_working_at(self, ct: Controller, gap: Position) -> bool:
        """Is a friendly builder already standing next to this gap?

        Two false positives collapse into one cheap check. A chain that is
        still BEING LAID always has a leading conveyor pointing at an empty
        tile — indistinguishable, locally, from a severed belt — so the
        chain-layer's own frontier reads as damage and every idle builder
        piles onto it. Measured: belt repair ballooned to 50% of all dynamic
        builder-rounds. The same check also stops two builders being
        dispatched to the same genuine gap.

        Whoever is adjacent gets to finish; we go find something else.
        """
        team = ct.get_team()
        for d in CARDINALS:
            n = gap.add(d)
            if not in_bounds(ct, n) or not ct.is_in_vision(n):
                continue
            bot = ct.get_tile_builder_bot_id(n)
            if bot is not None and bot != ct.get_id() and ct.get_team(bot) == team:
                return True
        return False

    def _repair_facing(self, ct: Controller, tile: Position) -> Direction | None:
        """Which way a conveyor at `tile` should point — for a rebuild into a
        gap, or a re-point of a misdirected belt.

        Ranked: straight into the core, else the adjacent friendly belt that
        is strictly closer to home than we are, else a bare step homeward.
        Every candidate is screened through _belt_output_status, so this can
        never hand back a direction that is itself terminally dead (a wall,
        a harvester, or the other half of a mutual loop) — which is exactly
        how a "repair" used to be able to recreate the defect it was sent to
        fix. Returns None when no direction is any good; the caller then
        leaves the tile alone rather than spending a conveyor to no effect.
        """
        best = None
        best_dist = None
        homeward_fallback = None
        for d in CARDINALS:
            status = self._belt_output_status(ct, tile, d)
            if status == BELT_OUT_CORE:
                return d
            if status == BELT_OUT_BELT and self.core_pos is not None:
                out = tile.add(d)
                dist = manhattan(out, self.core_pos)
                if dist < manhattan(tile, self.core_pos) and (best_dist is None or dist < best_dist):
                    best_dist = dist
                    best = d
            elif status in (BELT_OUT_GAP, BELT_OUT_UNKNOWN) and self.core_pos is not None:
                # Not a sink yet, but a legal place for the chain to continue;
                # the next repair round detects and fills it in turn.
                out = tile.add(d)
                if manhattan(out, self.core_pos) < manhattan(tile, self.core_pos):
                    homeward_fallback = d
        if best is not None:
            return best
        return homeward_fallback

    def _should_harvest(self, ct: Controller) -> bool:
        """Should this builder be doing economy right now?

        Two ways to answer yes, and the second one matters more than it looks:

        1. Ore is already visible or teammate-advertised — the obvious case.
        2. The team hasn't hit OFFENSE_MIN_HARVESTERS yet — in which case we
           take the harvest task EVEN WITH NO ORE IN SIGHT, because
           _run_defender explores to find some. Without this clause a dynamic
           builder standing anywhere without ore in its r²=20 vision fell
           straight through to TASK_ADVANCE and left home for good; the pool
           self-converted into attackers and the economy never got built.
        """
        route_count = ct.read_store(SLOT_HARVESTER_COUNT)
        phase = economy_phase_from_cursor(ct.read_store(SLOT_ORE_CURSOR))
        # A historical route count is not proof that titanium is arriving.
        # Until the Core publishes a pressure phase, keep every dynamic worker
        # on the existing SCOUT/CHAIN loop. Crisis is intentionally included:
        # when a route is cut or income goes quiet, more raids only deepen the
        # deficit; a fresh route is the recovery action.
        if phase in (
            ECONOMY_PHASE_OPENING,
            ECONOMY_PHASE_CONVERTING,
            ECONOMY_PHASE_CRISIS,
        ):
            return True
        if route_count < OFFENSE_MIN_HARVESTERS:
            return True
        # A route count is historical: it does not fall when an infiltrator or
        # a forward attack destroys a Harvester.  Keep one dynamic worker in
        # the economy loop through the five-route milestone while liquidity is
        # actually too low to rebuild that route.  Once the bank can fund the
        # replacement plus two short path links and the fixed attack reserve,
        # release the pool to the normal raid/advance ladder immediately.  The
        # fixed attackers are unaffected, so pressure remains continuous.
        if route_count < DYNAMIC_ECONOMY_FLOOR:
            replacement_budget = (
                ct.get_harvester_cost()
                + 2 * ct.get_conveyor_cost()
                + IDLE_ATTACK_RESERVE
            )
            if (
                ct.get_global_resources() < replacement_budget
                and self._owns_liquidity_floor(ct)
            ):
                return True
        # Keep one *local* dynamic Builder on the economy loop even after the
        # healthy-pressure handoff.  The permanent Defender is a floor, but it
        # can be dead, sieged, or trapped in a long chain; once the other
        # workers are released, a quiet home area otherwise has no one
        # exploring for the next source.  Reuse the deterministic nearest-home
        # lease so this does not turn the entire pressure pool back into
        # harvesters: only a Builder inside the home response radius, and only
        # the nearest non-fixed worker there, owns the steward slot.  The
        # nearest-home guard is deliberately local because the engine does not
        # expose a global Builder roster to a Builder unit.
        if (
            phase == ECONOMY_PHASE_PRESSURE
            and self._owns_liquidity_floor(ct)
        ):
            return True
        return self._harvest_available(ct)

    def _owns_liquidity_floor(self, ct: Controller) -> bool:
        """Assign the low-bank recovery lease to one nearby dynamic Builder.

        The floor is a route-safety reserve, not a command for the whole
        workforce to stop attacking.  Use the same deterministic local
        nearest-owner pattern as home threats and raids, excluding the three
        fixed roles.  Visibility is intentionally local: a distant dynamic
        Builder cannot be pulled home just to satisfy a bookkeeping lease,
        while nearby observers converge on one owner through distance/ID
        tie-breaking.
        """
        fixed = {
            ct.read_store(SLOT_PERMA_ATTACKER_ID),
            ct.read_store(SLOT_SECOND_ATTACKER_ID),
            ct.read_store(SLOT_PERMA_DEFENDER_ID),
        }
        fixed.discard(0)
        my_id = ct.get_id()
        core_pos = getattr(self, "core_pos", None)
        if core_pos is None:
            return False
        home = core_pos or ct.get_position()
        my_dist = ct.get_position().distance_squared(home)
        # The pressure steward is a home-side lease, not a license for every
        # isolated forward Builder to rediscover the economy task.  A Builder
        # beyond the local home radius leaves the persistent economy floor to
        # the nearest worker that can actually observe and service it.
        if core_pos is not None and my_dist > HOME_THREAT_RADIUS_SQ:
            return False
        for uid in ct.get_nearby_units():
            if uid == my_id or uid in fixed:
                continue
            if ct.get_team(uid) != ct.get_team() or ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                continue
            other_dist = ct.get_position(uid).distance_squared(home)
            if other_dist < my_dist or (other_dist == my_dist and uid < my_id):
                return False
        return True

    def _find_raid_target(self, ct: Controller) -> Position | None:
        """Find one high-value logistics target after the economy is funded.

        This deliberately reuses the attacker's ranked harvester/splitter/
        conveyor selector, but adds a nearest-builder claim.  A dynamic unit
        may raid only while it can leave the fixed combat reserve untouched;
        otherwise it remains available for repair or the core assault.
        """
        if not self._offense_unlocked(ct):
            return None
        # Dynamic builders are also the only scalable source of forward
        # Sentinels. Normally the assault shell remains the hard prerequisite,
        # but a *loaded* enemy belt is a short-lived income window: after one
        # Sentinel and three completed chains, let exactly the nearest dynamic
        # builder break that loaded tile rather than walking past it. Empty
        # logistics still wait for the full shell, so this cannot turn into a
        # broad pre-sentinel economy detour.
        enemy_core = self._enemy_core_target(ct)
        if enemy_core is None:
            return None
        sentinel_count = self._count_forward_sentinels(ct, enemy_core)
        if ct.get_global_resources() < IDLE_ATTACK_RESERVE:
            return None
        target = self._find_enemy_economy_target(ct)
        if target is None or not self._is_nearest_raid_responder(ct, target):
            return None
        if sentinel_count < SENTINEL_POOL_TARGET:
            if sentinel_count < 1 or not self._is_loaded_raid_target(ct, target):
                return None
        return target

    def _is_loaded_raid_target(self, ct: Controller, target: Position) -> bool:
        """Return whether a visible enemy conveyor/splitter carries income."""
        if not ct.is_in_vision(target):
            return False
        bid = ct.get_tile_building_id(target)
        if bid is None or ct.get_team(bid) == ct.get_team():
            return False
        if ct.get_entity_type(bid) not in (EntityType.CONVEYOR, EntityType.SPLITTER):
            return False
        try:
            return ct.get_stored_resource(bid) is not None
        except Exception:
            return False

    def _is_nearest_raid_responder(self, ct: Controller, target: Position) -> bool:
        """Assign a visible logistics raid to one deterministic builder."""
        my_id = ct.get_id()
        my_dist = ct.get_position().distance_squared(target)
        for uid in ct.get_nearby_units():
            if uid == my_id or ct.get_team(uid) != ct.get_team():
                continue
            if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                continue
            other_dist = ct.get_position(uid).distance_squared(target)
            if other_dist < my_dist or (other_dist == my_dist and uid < my_id):
                return False
        return True

    def _harvest_available(self, ct: Controller) -> bool:
        """Is there ore actually worth going for right now? Mirrors
        defender.py's own target priorities (visible uncovered ore, then
        teammate-advertised ore), since _run_defender executes this task.
        """
        for tile in ct.get_nearby_tiles():
            if ct.get_tile_env(tile) != Environment.ORE_TITANIUM:
                continue
            if ct.get_tile_building_id(tile) is not None:
                continue
            if self._harvestable(ct, tile):
                return True
        for i in range(ORE_QUEUE_LEN):
            cand = unpack_pos(ct.read_store(SLOT_ORE_QUEUE_BASE + i))
            if cand is None or not in_bounds(ct, cand):
                continue
            if not self._harvestable(ct, cand):
                continue
            if ct.is_in_vision(cand) and ct.get_tile_building_id(cand) is not None:
                continue
            return True
        return False

    def _find_denial_target(self, ct: Controller) -> Position | None:
        """An uncovered ore tile on the enemy's half — barrier it and they can
        never build a harvester there (harvesters need a bare ore tile).
        Skips ore inside our own economic range, which we'd rather harvest.
        """
        if self.core_pos is None:
            return None
        enemy_core = self._enemy_core_target(ct)
        if enemy_core is None:
            return None
        pos = ct.get_position()
        best = None
        best_dist = float("inf")
        for tile in ct.get_nearby_tiles():
            if ct.get_tile_env(tile) != Environment.ORE_TITANIUM:
                continue
            if ct.get_tile_building_id(tile) is not None:
                continue
            if manhattan(tile, enemy_core) >= manhattan(tile, self.core_pos):
                continue  # not their half
            if self._harvestable(ct, tile):
                continue  # close enough that we'd rather mine it ourselves
            d = pos.distance_squared(tile)
            if 0 < d < best_dist:
                best_dist = d
                best = tile
        return best
