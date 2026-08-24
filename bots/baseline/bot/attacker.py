"""ATTACKER builder-bot role: find the enemy core, ring it with sentinels,
and wreck their economy.

Priority order each round, strict — later steps don't happen until earlier
ones are satisfied:
  1. Update/share intel on the enemy core (cheap, always).
  2. Plant a forward sentinel aimed at the core, if the pool isn't full and
     we're anywhere within sentinel range (r²=32).
  3. Travel toward the enemy core. No economy detours while travelling.
  4. Once on top of it: destroy enemy harvesters and conveyors/splitters of
     opportunity, falling back to punching the core with builder-fire.

Note step 2 comes BEFORE travelling: if a sentinel can already be planted
from here, planting it at standoff beats walking into point-blank danger
first.

Forward sentinels are the win condition — observed Gold League games are
decided around round 100 by exactly this. Two properties make a sentinel
worth planting in enemy territory where a *gunner* isn't: attack radius
r²=32 (vs a gunner's 13) and a line-shot that ignores obstacles, so it
threatens the core from well outside the defended ring instead of needing
to sit adjacent to anything. Gunners stay home-only: one alone out here
just gets picked off (see core_role.py's home-turret cap).

Its facing is PERMANENT — the engine has no rotate() for sentinels at all,
gunner-only — so _try_build_sentinel only ever commits to a placement
verified via can_fire_from(), the same lesson learned from the gunner
rotation bug.
"""

import random

from fcode import Controller, EntityType, GameError, Position

from .constants import (
    CARDINALS,
    DIRECTIONS,
    ECONOMY_PHASE_PRESSURE,
    ECONOMY_STRONG_CHAINS,
    ENEMY_CORE_BARRIER_CAP,
    HARASS_RANGE_SQ,
    IDLE_ATTACK_RESERVE,
    MODE_SCOUT,
    OFFENSE_MIN_HARVESTERS,
    ROLE_ATTACKER,
    SENTINEL_MIN_LIFETIME,
    SENTINEL_POOL_TARGET,
    SENTINEL_POOL_TARGET_EARLY,
    SENTINEL_RANGE_SQ,
    SENTINEL_SITE_BLACKLIST,
    SIEGE_BARRIER_CAP,
    SLOT_ENEMY_CORE,
    SLOT_HARVESTER_COUNT,
    SLOT_ORE_CURSOR,
    SLOT_PERMA_ATTACKER_ID,
    SLOT_SECOND_ATTACKER_ID,
    SLOT_SENTINEL_COUNT,
    economy_phase_from_cursor,
)
from .util import adjacent, in_bounds, manhattan, pack_pos, unpack_pos


class AttackerMixin:
    def _enemy_core_barrier_cap(self, ct: Controller) -> int:
        """Return the cage depth allowed by the shared economy phase."""
        if (
            ct.read_store(SLOT_HARVESTER_COUNT) >= ECONOMY_STRONG_CHAINS
            and economy_phase_from_cursor(ct.read_store(SLOT_ORE_CURSOR))
            == ECONOMY_PHASE_PRESSURE
        ):
            return SIEGE_BARRIER_CAP
        return ENEMY_CORE_BARRIER_CAP

    def _try_build_opening_launcher(self, ct: Controller) -> bool:
        """Establish one home mobility relay for the primary attacker.

        Top-team openings use a Launcher as a control/topology primitive before
        a large combat shell exists.  The old candidate had no Launcher
        lifecycle at all, so its first attacker spent the same opening rounds
        walking through the centre while the opponent could reposition freely.
        This is deliberately a single, primary-attacker-owned relay: it keeps
        a Harvester plus two Conveyor links affordable, builds only in the
        Core's local ring, and never interrupts an active chain.
        """
        if getattr(self, "role", None) != ROLE_ATTACKER:
            return False
        if getattr(self, "opening_launcher_built", False):
            return False
        if getattr(self, "mode", 0) != MODE_SCOUT:
            return False
        try:
            if ct.get_action_cooldown() != 0 or self.core_pos is None:
                return False
            primary_id = int(ct.read_store(SLOT_PERMA_ATTACKER_ID))
            if primary_id and int(ct.get_id()) != primary_id:
                return False
            current = ct.get_position()
            if current.distance_squared(self.core_pos) > 25:
                return False
            own_team = ct.get_team()
            for building_id in tuple(ct.get_nearby_buildings())[:64]:
                try:
                    if (
                        ct.get_team(building_id) == own_team
                        and ct.get_entity_type(building_id) == EntityType.LAUNCHER
                        and ct.get_position(building_id).distance_squared(self.core_pos) <= 36
                    ):
                        return False
                except Exception:
                    continue
            launcher_cost = max(0, int(ct.get_launcher_cost()))
            harvester_cost = max(0, int(ct.get_harvester_cost()))
            conveyor_cost = max(0, int(ct.get_conveyor_cost()))
            # Preserve the opening source and a short route shell.  Query all
            # prices dynamically; the scale multiplier is part of the game.
            reserve = harvester_cost + 2 * conveyor_cost
            if ct.get_global_resources() < launcher_cost + reserve:
                return False
            for direction in CARDINALS:
                site = current.add(direction)
                if not in_bounds(ct, site) or self._would_sever_belt(ct, site):
                    continue
                if not ct.can_build_launcher(site):
                    continue
                ct.build_launcher(site)
                self.opening_launcher_built = True
                return True
        except Exception:
            return False
        return False

    def _run_attacker(self, ct: Controller, danger: set[Position]) -> None:
        self._update_enemy_intel(ct)
        self._watch_sentinel(ct)

        # A single early mobility relay is the control-first opening primitive.
        # It runs before Core intel/sentinel work so a newly spawned primary
        # attacker can be thrown forward on the next round.
        if self._try_build_opening_launcher(ct):
            return

        enemy_core = self._enemy_core_target(ct)
        # On cramped maps the two cores are close enough that the symmetric
        # target is reliable before direct vision; plant an early sentinel
        # rather than spending the opening walk in the opponent's fire lane.
        if enemy_core is not None and self._cramped_map(ct):
            if self._try_build_sentinel(ct, enemy_core) is not None:
                return

        # Fixed attackers stay on the direct core/sentinel lane. Defender and
        # dynamic workers still own opportunistic harvester hijacks; allowing
        # the guaranteed attacker to seed a long route here delayed the first
        # combat shell in the loss replays (opponents placed sentinels while
        # our attacker was still routing stolen output).
        if enemy_core is None:
            # No guess yet (core_pos not learned this early) — head out into
            # the map until we do. No economy detours yet either: finding
            # the core comes first.
            if ct.get_move_cooldown() == 0:
                self._navigate(ct, self._far_explore_target(ct), avoid=danger)
            return

        # Sentinels first, from as far out as the sentinel can actually
        # shoot — this is the win condition, and its reach is 6x the
        # builder-fire harassment range below. Deliberately attempted BEFORE
        # closing distance: if we can already plant one from here, planting
        # it from standoff beats walking into point-blank danger first.
        if self._try_build_sentinel(ct, enemy_core) is not None:
            return

        # Top ladder teams consistently turn cheap Barriers into offensive
        # topology: ring the Core so enemy Builders cannot freely reach repair
        # tiles, while our Sentinels keep firing through the cage. This comes
        # after the Sentinel attempt, so it never spends the action that could
        # have established the actual damage source.
        if self._try_build_enemy_core_barrier(ct, enemy_core):
            return

        # Once the forward-sentinel slot is satisfied, use the permanent
        # attackers to convert surplus titanium into a concrete raid instead of
        # sending the economy pool off course. Top-team replays consistently
        # cut harvesters and loaded logistics before committing to the core.
        if self._try_sabotage_with_attacker(ct, danger):
            return

        pos = ct.get_position()
        if pos.distance_squared(enemy_core) > HARASS_RANGE_SQ:
            if ct.get_move_cooldown() == 0:
                self._navigate(ct, enemy_core, avoid=danger)
            return

        # Right on top of the core: wreck their economy, else punch the core.
        victim = self._find_enemy_economy_target(ct)
        if victim is not None:
            self.attack_target = victim
        if self.attack_target is not None and self._handle_attack_target(ct, danger):
            return
        self._harass(ct, enemy_core, danger)
        self._attacker_fallback(ct, danger)

    def _try_build_enemy_core_barrier(self, ct: Controller, enemy_core: Position) -> bool:
        """Build a bounded, escape-safe barrier cage around a confirmed Core."""
        if self.enemy_core_known is None or ct.get_action_cooldown() != 0:
            return False
        if ct.read_store(SLOT_HARVESTER_COUNT) == 0:
            return False
        # SLOT_HARVESTER_COUNT is historical: it never falls when a route is
        # destroyed. Preserve enough current titanium to replace one Harvester
        # before spending on siege topology, or a broken economy can keep
        # buying cheap Barriers while being unable to restart delivery.
        if ct.get_global_resources() < ct.get_barrier_cost() + ct.get_harvester_cost():
            return False

        team = ct.get_team()
        visible_cage = {
            ct.get_position(building_id)
            for building_id in ct.get_nearby_buildings()
            if (
                ct.get_team(building_id) == team
                and ct.get_entity_type(building_id) == EntityType.BARRIER
                and ct.get_position(building_id).distance_squared(enemy_core) <= 13
            )
        }
        known_cage = visible_cage | self.enemy_barrier_sites
        if len(known_cage) >= self._enemy_core_barrier_cap(ct):
            return False

        pos = ct.get_position()
        # Never use the last legal exit from our own tile. A cage that traps
        # the Builder which is constructing it sacrifices the next sabotage
        # turn and makes later repairs impossible.
        exits = {
            direction
            for direction in CARDINALS
            if ct.can_move(direction)
        }
        candidates: list[tuple[int, int, int, Position]] = []
        for index, direction in enumerate(CARDINALS):
            site = pos.add(direction)
            if direction in exits and len(exits) <= 1:
                continue
            if not in_bounds(ct, site) or site in known_cage:
                continue
            distance = site.distance_squared(enemy_core)
            if not (1 <= distance <= 13):
                continue
            if ct.can_build_barrier(site):
                candidates.append((distance, index, site.y, site))
        if not candidates:
            return False
        site = min(candidates)[3]
        ct.build_barrier(site)
        self.enemy_barrier_sites.add(site)
        return True

    def _cramped_map(self, ct: Controller) -> bool:
        if self.core_pos is None:
            return False
        mirror = Position(ct.get_map_width() - 1 - self.core_pos.x,
                          ct.get_map_height() - 1 - self.core_pos.y)
        return manhattan(self.core_pos, mirror) <= 20

    def _attacker_fallback(self, ct: Controller, danger: set[Position]) -> None:
        """Last resort, so an attacker never burns a turn doing nothing.

        Measured on 5 games with the whole builder fleet instrumented: 53% of
        all READY builder turns (cooldowns clear, yet no move/build/attack/
        heal) were wasted, and the attacker alone was 49% of that waste —
        by far the largest single sink. Almost none of it was pathing failure
        (3 turns out of ~2200): the attacker simply arrives at the enemy core,
        finds the sentinel pool full and no economy target in reach, and has
        nothing left in its repertoire.

        Detecting "we did nothing" by re-reading both cooldowns is deliberate.
        The alternative is threading a did-act boolean back through every
        branch of _run_attacker, _handle_attack_target and _harass, which is
        exactly the kind of bookkeeping that goes stale the next time someone
        adds a branch. The engine's own cooldowns cannot go stale.

        Order is by titanium efficiency, not aggression:
          1. HEAL a damaged friendly — 1 Ti for 4 HP is the best ratio in the
             game, and in practice the thing standing next to an attacker is
             the forward sentinel it just planted, whose median lifetime under
             fire was 5 rounds. Out-repairing the incoming fire is worth far
             more than 2 points of chip damage.
          2. ATTACK adjacent enemy ECONOMY (harvester/conveyor/splitter) — 2 Ti
             for 2 damage is a poor trade in general, but a 20 HP conveyor dies
             fast and severs everything upstream of it.
          3. ATTACK any other adjacent enemy building, turrets included. Noted
             as a losing trade in constants.py and it still is — but that
             judgement is about what to CHOOSE to do, and this only runs on a
             turn that would otherwise be discarded outright.
          4. Reposition, so a boxed-in attacker goes and finds another angle
             instead of standing still forever.
        """
        if ct.get_action_cooldown() != 0 or ct.get_move_cooldown() != 0:
            return  # we already acted or moved this turn
        pos = ct.get_position()
        team = ct.get_team()

        neighbours = []
        for d in CARDINALS:
            n = pos.add(d)
            if not in_bounds(ct, n) or not ct.is_in_vision(n):
                continue
            bid = ct.get_tile_building_id(n)
            if bid is not None:
                neighbours.append((n, bid))

        for n, bid in neighbours:
            if ct.get_team(bid) != team:
                continue
            if ct.get_hp(bid) < ct.get_max_hp(bid) and ct.can_heal(n):
                ct.heal(n)
                return

        for economy_only in (True, False):
            for n, bid in neighbours:
                if ct.get_team(bid) == team:
                    continue
                if economy_only and ct.get_entity_type(bid) not in self.ECONOMY_TARGET_TYPES:
                    continue
                if ct.can_fire(n):
                    ct.fire(n)
                    return

        # Nothing to hit or mend from here. Walk to the nearest enemy building
        # we are NOT already touching — a concrete goal, so a boxed-in attacker
        # tries another angle rather than re-deriving the same stuck position.
        # A random explore target would also break the deadlock, but re-rolled
        # every round it just produces a random walk.
        adjacent_ids = {bid for _, bid in neighbours}
        goal = None
        goal_dist = float("inf")
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == team or bid in adjacent_ids:
                continue
            p = ct.get_position(bid)
            d = pos.distance_squared(p)
            if d < goal_dist:
                goal_dist = d
                goal = p
        self._navigate(ct, goal if goal is not None else self._far_explore_target(ct), avoid=danger)

    def _try_build_sentinel(self, ct: Controller, enemy_core: Position) -> int | None:
        """Plant a forward sentinel aimed at the enemy core, if the pool isn't
        already full. Returns the new sentinel's id on success, else None
        (pool full, out of range, unaffordable, or no aligned spot this round
        — the caller just retries next round).

        Placement is gated on a CONFIRMED sighting (self.enemy_core_known),
        never the symmetry guess in _enemy_core_target: a sentinel's facing is
        permanent, so aiming one at a guessed position we've never actually
        seen risks paying 30 Ti for a turret pointed at empty ground forever.

        Range is the sentinel's own r²=32, not the builder's r²=20 vision —
        can_fire_from() is purely geometric and works fine on a target we
        can't currently see (verified empirically; see constants.py). So we
        can plant at standoff, well outside the core's own defended ring.

        We don't know which corner of the enemy core's 2x2 footprint
        get_position() reported, so alignment is checked against all 4
        plausible footprint tiles rather than just the anchor — cheap (4
        cardinal build tiles x 8 facings, short-circuited) and correct
        regardless of the engine's corner convention.
        """
        if self.enemy_core_known is None and not self._cramped_map(ct):
            return None
        if ct.get_action_cooldown() != 0 or ct.get_global_resources() < ct.get_sentinel_cost():
            return None
        round_now = ct.get_current_round()
        pos = ct.get_position()
        if pos.distance_squared(enemy_core) > SENTINEL_RANGE_SQ:
            return None
        # Require one completed harvester chain before buying even the first
        # forward Sentinel.  On compact server maps an early 30-Ti Sentinel
        # displaced the first route and left the team with a delivery only at
        # turn 157; a completed chain is the smallest team-wide proof that the
        # opening economy is paying back.  Once it exists, retain the normal
        # two-sentinel early shell and the full economy-gated pool.
        if ct.read_store(SLOT_HARVESTER_COUNT) == 0:
            return None
        harvester_count = ct.read_store(SLOT_HARVESTER_COUNT)
        pool = (SENTINEL_POOL_TARGET
                if harvester_count >= ECONOMY_STRONG_CHAINS
                else SENTINEL_POOL_TARGET_EARLY)
        if self._count_forward_sentinels(ct, enemy_core) >= pool:
            return None

        core_tiles = [Position(enemy_core.x + dx, enemy_core.y + dy) for dx in (0, 1) for dy in (0, 1)]
        for d in CARDINALS:
            build_pos = pos.add(d)
            if not in_bounds(ct, build_pos):
                continue
            # Don't re-plant on a tile that already ate a sentinel. The
            # placement search is deterministic given the same geometry, so
            # without this memory it re-derives the same doomed tile forever —
            # 140 of 143 rebuilds landed on one tile in the snowflake replay.
            if self.sentinel_sites.get(build_pos, 0) > round_now:
                continue
            if build_pos.distance_squared(enemy_core) > SENTINEL_RANGE_SQ:
                continue
            for facing in DIRECTIONS:
                if not any(ct.can_fire_from(build_pos, facing, EntityType.SENTINEL, t) for t in core_tiles):
                    continue
                if ct.can_build_sentinel(build_pos, facing):
                    sid = ct.build_sentinel(build_pos, facing)
                    self.sentinel_watch = (sid, build_pos, round_now)
                    return sid
        return None

    def _watch_sentinel(self, ct: Controller) -> None:
        """Track the sentinel this builder most recently planted, and ban its
        tile if it died fast.

        "Died fast" is the signal that the placement — not the strategy — was
        wrong: the tile sits inside something's kill zone, and rebuilding
        there buys another ~5 rounds of nothing. We only watch our own most
        recent plant — the treadmill was one builder re-deriving one doomed
        tile, so one slot of memory is where it actually breaks.

        Uses the same GameError discrimination as
        core_role._prune_dead_builders: querying a DESTROYED id raises
        "Unknown id", while an id merely outside our vision raises "Position
        out of vision range". Only the former is proof of death — an attacker
        that has walked away from its own sentinel must not conclude the
        sentinel died just because it can no longer see it.
        """
        if self.sentinel_watch is None:
            return
        sid, site, built = self.sentinel_watch
        age = ct.get_current_round() - built
        try:
            if ct.get_hp(sid) > 0:
                if age >= SENTINEL_MIN_LIFETIME:
                    self.sentinel_watch = None  # survived; the site is fine
                return
        except GameError as e:
            if "unknown id" not in str(e).lower():
                return  # out of vision — presume alive, keep watching
        except Exception:
            return  # unrecognised failure shape — don't act on our own uncertainty

        if age < SENTINEL_MIN_LIFETIME:
            self.sentinel_sites[site] = ct.get_current_round() + SENTINEL_SITE_BLACKLIST
        self.sentinel_watch = None

    def _count_forward_sentinels(self, ct: Controller, enemy_core: Position) -> int:
        """Live count of friendly sentinels covering the enemy core, observed
        fresh each round rather than latched — so a destroyed sentinel is
        naturally replaced instead of leaving a permanent hole.

        Also republishes the count (SLOT_SENTINEL_COUNT) so the core knows to
        bank siege ammo. Only written when we're ourselves close enough to
        have actually seen the cluster; otherwise a distant attacker that can
        see none would zero the count and starve the siege of ammo.
        """
        team = ct.get_team()
        count = 0
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) != team or ct.get_entity_type(bid) != EntityType.SENTINEL:
                continue
            if ct.get_position(bid).distance_squared(enemy_core) <= SENTINEL_RANGE_SQ:
                count += 1
        if ct.get_position().distance_squared(enemy_core) <= SENTINEL_RANGE_SQ:
            ct.write_store(SLOT_SENTINEL_COUNT, count)
        return count

    def _update_enemy_intel(self, ct: Controller) -> None:
        """Record the enemy core's position the moment we see it ourselves, and
        broadcast it; otherwise pick up a sighting a teammate already broadcast.
        """
        if self.enemy_core_known is not None:
            return
        team = ct.get_team()
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) != team and ct.get_entity_type(bid) == EntityType.CORE:
                self.enemy_core_known = ct.get_position(bid)
                ct.write_store(SLOT_ENEMY_CORE, pack_pos(self.enemy_core_known))
                return
        stored = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        if stored is not None:
            self.enemy_core_known = stored

    def _enemy_core_target(self, ct: Controller) -> Position | None:
        """Best current guess at the enemy core: a confirmed sighting (ours or a
        teammate's) if we have one, else the 180°-rotation mirror of our own
        core (maps are symmetric — same trick as core_role._is_cramped).
        """
        if self.enemy_core_known is not None:
            return self.enemy_core_known
        if self.core_pos is None:
            return None
        w, h = ct.get_map_width(), ct.get_map_height()
        return Position(w - 1 - self.core_pos.x, h - 1 - self.core_pos.y)

    ECONOMY_TARGET_TYPES = (EntityType.HARVESTER, EntityType.CONVEYOR, EntityType.SPLITTER)

    def _find_enemy_economy_target(self, ct: Controller) -> Position | None:
        team = ct.get_team()
        pos = ct.get_position()
        best: tuple[int, int, int, int, Position] | None = None
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == team or ct.get_entity_type(bid) not in self.ECONOMY_TARGET_TYPES:
                continue
            p = ct.get_position(bid)
            etype = ct.get_entity_type(bid)
            try:
                loaded = etype in (EntityType.CONVEYOR, EntityType.SPLITTER) and ct.get_stored_resource(bid) is not None
            except Exception:
                loaded = False
            # A loaded line is the opponent's income in flight.  Breaking it
            # removes the carried titanium immediately and often disconnects
            # every source upstream; that is a better raid conversion than
            # walking past it to chip one Harvester.  Empty lines retain a
            # lower priority, while a Harvester remains the best persistent
            # target if no delivery is currently visible.
            score = {
                EntityType.HARVESTER: 300,
                EntityType.SPLITTER: 250,
                EntityType.CONVEYOR: 200,
            }[etype] + (200 if loaded else 0)
            distance = pos.distance_squared(p)
            candidate = (score, -distance, -p.y, -p.x, p)
            if best is None or candidate[:4] > best[:4]:
                best = candidate
        return best[4] if best is not None else None

    def _try_sabotage_with_attacker(self, ct: Controller, danger: set[Position]) -> bool:
        """Pulse one funded fixed attacker through enemy logistics.

        The direct siege lane remains the default.  A detour is earned only
        after the economy and the first forward Sentinel are real, and only
        the nearer of the two designated attackers claims the visible target.
        This turns the existing no-op hook into the top-team behavior seen in
        replay: cut a Harvester or loaded belt, then return to pressure, rather
        than leaving an attacker idle at a completed Sentinel shell.
        """
        if self.attack_target is None:
            enemy_core = self.enemy_core_known
            if enemy_core is None:
                return False
            if ct.read_store(SLOT_HARVESTER_COUNT) < OFFENSE_MIN_HARVESTERS:
                return False
            if ct.get_global_resources() < IDLE_ATTACK_RESERVE:
                return False
            # Do not divert the opening attacker before a real forward damage
            # source exists.  The live count is authoritative when this unit
            # is near the enemy Core; stale Store values are not enough.
            if self._count_forward_sentinels(ct, enemy_core) < 1:
                return False
            target = self._find_enemy_economy_target(ct)
            if target is None or not self._is_nearest_fixed_attacker(ct, target):
                return False
            self.attack_target = target

        if self._handle_attack_target(ct, danger):
            return True
        # A visible gone/stale target is not a reason to abandon the siege
        # lane forever; clear it and let the caller continue normally.
        self.attack_target = None
        return False

    def _is_nearest_fixed_attacker(self, ct: Controller, target: Position) -> bool:
        """Assign one visible fixed attacker to a logistics pulse."""
        fixed = {
            ct.read_store(SLOT_PERMA_ATTACKER_ID),
            ct.read_store(SLOT_SECOND_ATTACKER_ID),
        }
        fixed.discard(0)
        my_id = ct.get_id()
        # Lightweight probes and the first Store-write round have no
        # designation yet; in that case the caller is the only claimant.
        if fixed and my_id not in fixed:
            return False
        my_dist = ct.get_position().distance_squared(target)
        for uid in ct.get_nearby_units():
            if uid == my_id or uid not in fixed:
                continue
            if ct.get_team(uid) != ct.get_team():
                continue
            other_dist = ct.get_position(uid).distance_squared(target)
            if other_dist < my_dist or (other_dist == my_dist and uid < my_id):
                return False
        return True

    def _handle_attack_target(self, ct: Controller, danger: set[Position]) -> bool:
        """Walk to and destroy self.attack_target (an enemy harvester/
        conveyor/splitter). Returns True if this consumed our turn — the
        caller should fall through to normal harass/travel behaviour on
        False (target destroyed or confirmed gone).

        self.attack_target is a remembered position from whenever we (or a
        teammate's sighting) last saw it — by the time we're chasing it down
        it's very often outside our *current* vision again, so unlike an
        adjacent-tile check this needs the same is_in_vision guard defender.py
        uses before any tile query: querying an out-of-vision position raises
        GameError("Position out of vision range") rather than just returning
        a false answer. We only give up on the target once we can actually
        see it's gone; otherwise we keep closing in on the last-known spot.
        """
        pos = ct.get_position()
        target = self.attack_target
        if not in_bounds(ct, target):
            self.attack_target = None
            return False
        if ct.is_in_vision(target):
            bid = ct.get_tile_building_id(target)
            if (
                bid is None
                or ct.get_team(bid) == ct.get_team()
                or ct.get_entity_type(bid) not in self.ECONOMY_TARGET_TYPES
            ):
                self.attack_target = None
                return False
        if adjacent(pos, target):
            if ct.get_action_cooldown() == 0 and ct.can_fire(target):
                ct.fire(target)
            return True
        if ct.get_move_cooldown() == 0:
            self._navigate(ct, target, avoid=danger)
        return True

    def _harass(self, ct: Controller, enemy_core: Position, danger: set[Position]) -> None:
        """Next to the (guessed or confirmed) enemy core: chip at it with
        builder-fire if adjacent, otherwise keep closing the distance. No
        turret-building out here — see the module docstring.
        """
        pos = ct.get_position()
        if adjacent(pos, enemy_core):
            if ct.get_action_cooldown() == 0 and ct.can_fire(enemy_core):
                ct.fire(enemy_core)
            return
        if ct.get_move_cooldown() == 0:
            self._navigate(ct, enemy_core, avoid=danger)

    def _far_explore_target(self, ct: Controller) -> Position:
        w, h = ct.get_map_width(), ct.get_map_height()
        return Position(random.randrange(w), random.randrange(h))
