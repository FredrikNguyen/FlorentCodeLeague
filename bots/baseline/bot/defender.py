"""DEFENDER builder-bot role: economy first. Explore, build a harvester on
ore, trail a conveyor CHAIN back to the core, and opportunistically build a
home turret when the core has designated this builder as the round's
defender (see core_role.py / SLOT_DEFENDER_ID).

Builder lifecycle (economy sub-mode):
  SCOUT  -> move toward the nearest known ore / explore; build a harvester
            when adjacent to uncovered ore, which switches the bot to CHAIN
  CHAIN  -> walk back toward the core, trailing a connected line of conveyors
            so the new harvester delivers; return to SCOUT once done
"""

import random

from fcode import Controller, Direction, EntityType, Environment, Position

from .constants import (
    BELT_OUT_BELT,
    BELT_OUT_CORE,
    BELT_OUT_DEAD,
    BELT_OUT_GAP,
    BELT_OUT_UNKNOWN,
    BLACKLIST_ROUNDS,
    CARDINALS,
    CHAIN_BLOCKED_LIMIT,
    CHAIN_SLACK,
    DIRECTIONS,
    EARLY_HARVEST_RANGE,
    ECONOMY_PRIORITY_CHAINS,
    EXPLORE_MIN_DIST_SQ,
    GUNNER_MIN_CORE_DIST_SQ,
    GUNNER_NEAR_CORE_DIST_SQ,
    MODE_CHAIN,
    MODE_SCOUT,
    NAV_GIVEUP,
    ORE_CURSOR_MASK,
    ORE_QUEUE_LEN,
    ORE_TURRET_MAX_PER_BUILDER,
    ORE_TURRET_MIN_ROUND,
    ORE_TURRET_RESERVE,
    SLOT_DEFENDER_ID,
    SLOT_HARVESTER_COUNT,
    SLOT_ORE_CURSOR,
    SLOT_ORE_QUEUE_BASE,
    SLOT_PERMA_ATTACKER_ID,
    SLOT_SECOND_ATTACKER_ID,
    ore_cursor_from_packed,
)
from .util import adjacent, in_bounds, manhattan, pack_pos, unpack_pos


class DefenderMixin:
    def _run_defender(self, ct: Controller, danger: set[Position]) -> None:
        # CHAIN mode: extend the conveyor line back to the core, nothing else.
        if self.mode == MODE_CHAIN:
            self._run_chain(ct, danger)
            return

        # SCOUT mode.
        if ct.get_action_cooldown() == 0:
            if self._try_hijack_enemy_harvester(ct, danger):
                return
            # Core ring first: 3 Ti, no travel (only fires if we're already
            # adjacent to a gap), and it's what makes every future chain
            # deliver. Cheap enough to outrank starting a 20 Ti harvester.
            if self._try_build_core_ring(ct):
                return
            if self._try_repair_visible_belt(ct):
                return
            if self._try_reconnect_orphaned_harvester(ct, danger):
                return
            if self._try_build_harvester(ct):
                return  # we just switched to CHAIN; start laying next round
            if self._try_build_ore_turret(ct):
                return
            self._try_build_gunner(ct)

        if ct.get_action_cooldown() == 0:
            self._try_heal(ct)

        self._move_toward_target(ct, danger)

    def _facing_to_core(self, ct: Controller, tile: Position) -> Direction | None:
        """If tile is orthogonally adjacent to our own core, return the direction
        from tile into that core tile (so a conveyor there drains into the core).
        Returns None if tile isn't next to the core — the chain endpoint test.
        """
        team = ct.get_team()
        for d in CARDINALS:
            n = tile.add(d)
            # Vision guard belongs HERE, not just at the call sites. `tile`
            # being visible does not make tile's neighbours visible — a tile
            # on the rim of vision has neighbours one step beyond it, and
            # querying those raises. This bit twice before being fixed at the
            # root: once via _find_core_ring_gap scanning the ring, and it is
            # the same shape as the _run_chain and _find_belt_gap bugs (see
            # README.md). Treating "can't see it" as "not the core" is the
            # conservative answer — we simply don't claim a connection we
            # cannot verify.
            if not in_bounds(ct, n) or not ct.is_in_vision(n):
                continue
            bid = ct.get_tile_building_id(n)
            if bid is not None and ct.get_team(bid) == team and ct.get_entity_type(bid) == EntityType.CORE:
                return d
        return None

    def _find_core_ring_gap(self, ct: Controller) -> Position | None:
        """Nearest empty tile orthogonally adjacent to our core.

        We keep a permanent conveyor ring on every such tile, each facing
        into the core, rebuilt whenever one is missing. It's the single
        highest-leverage thing a builder can construct: a conveyor is 3 Ti,
        and once the ring exists ANY chain that merely reaches the core's
        neighbourhood delivers, instead of having to nail the last tile
        exactly right. It also makes the network self-healing at the point
        where losing one belt otherwise costs the whole chain's output.

        Scanned from the core position rather than the builder's, so a
        builder anywhere nearby can be dispatched to a gap. _facing_to_core
        is the authoritative test for "is this tile on the ring" — it checks
        for a real adjacent core building, so it works regardless of which
        corner of the 2x2 footprint get_position() reports. The 5x5 box is
        wide enough to cover the ring under any corner convention; corners of
        the box are rejected by _facing_to_core (diagonals don't count).
        """
        if self.core_pos is None:
            return None
        pos = ct.get_position()
        best = None
        best_dist = float("inf")
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                tile = Position(self.core_pos.x + dx, self.core_pos.y + dy)
                if not in_bounds(ct, tile) or not ct.is_in_vision(tile):
                    continue
                if not ct.is_tile_empty(tile):
                    continue
                if self._facing_to_core(ct, tile) is None:
                    continue
                d = pos.distance_squared(tile)
                if d < best_dist:
                    best_dist = d
                    best = tile
        return best

    def _try_build_core_ring(self, ct: Controller) -> bool:
        """Opportunistically fill a ring tile we're already standing next to.

        Deliberately free of travel: this fires only when a builder happens
        to be adjacent to a gap, so maintaining the ring costs no detour.
        Builders pass the core constantly (every chain ends there), so the
        ring stays topped up without anyone being assigned to it. Dynamic
        builders additionally treat a ring gap as a repair task and WILL
        walk to it — see dynamic.py's _find_belt_gap.
        """
        if self.core_pos is None or ct.get_action_cooldown() != 0:
            return False
        if ct.get_global_resources() < ct.get_conveyor_cost():
            return False
        pos = ct.get_position()
        for d in CARDINALS:
            tile = pos.add(d)
            if not in_bounds(ct, tile) or not ct.is_in_vision(tile):
                continue
            if not ct.is_tile_empty(tile):
                continue
            facing = self._facing_to_core(ct, tile)
            if facing is None:
                continue
            if ct.can_build_conveyor(tile, facing):
                ct.build_conveyor(tile, facing)
                return True
        return False

    def _would_sever_belt(self, ct: Controller, tile: Position) -> bool:
        """True if some friendly conveyor currently outputs INTO `tile`.

        Building anything solid there severs that belt: harvesters, turrets
        and barriers never accept resources, so the stack simply stops and
        everything upstream stops delivering. A conveyor's facing is always
        valid at the moment it's laid (the builder just walked that way), so
        misdirected-looking belts are really a BUILD-ORDERING problem — the
        obstruction arrives afterwards. Observed in a real match: belts
        pointing into our own harvester and into our own home gunners.

        Callers must check this before committing any non-conveyor build.
        Cheap: 4 neighbours, all within 2 tiles of the builder and therefore
        in vision, but guarded anyway (see the vision notes in README.md).
        """
        team = ct.get_team()
        for d in CARDINALS:
            n = tile.add(d)
            if not in_bounds(ct, n) or not ct.is_in_vision(n):
                continue
            bid = ct.get_tile_building_id(n)
            if bid is None or ct.get_team(bid) != team:
                continue
            if ct.get_entity_type(bid) != EntityType.CONVEYOR:
                continue
            if n.add(ct.get_direction(bid)) == tile:
                return True
        return False

    def _belt_output_status(self, ct: Controller, tile: Position, facing: Direction) -> int:
        """Classify what a conveyor standing at `tile` and facing `facing`
        would deliver its stack into. Returns one of the BELT_OUT_* constants.

        This is the single place that knows what can and cannot accept a
        stack, so the repair finder, the repair validator and the facing
        chooser can never disagree about it (they used to, which is how belts
        aimed at walls stayed invisible: the old severed-belt check tested
        is_tile_empty(), and a wall is not "empty").

        BELT_OUT_UNKNOWN is returned for anything out of vision and callers
        must treat it as "no opinion" — never as damage. Querying an
        out-of-vision tile raises rather than answering (see README.md), and
        a belt we merely can't see is not a belt we know is broken.
        """
        out = tile.add(facing)
        if not in_bounds(ct, out):
            return BELT_OUT_DEAD
        if not ct.is_in_vision(out):
            return BELT_OUT_UNKNOWN
        if ct.get_tile_env(out) == Environment.WALL:
            return BELT_OUT_DEAD
        bid = ct.get_tile_building_id(out)
        if bid is None:
            return BELT_OUT_GAP
        if ct.get_team(bid) != ct.get_team():
            return BELT_OUT_DEAD  # an enemy belt would just gift them the stack
        etype = ct.get_entity_type(bid)
        if etype == EntityType.CORE:
            return BELT_OUT_CORE
        if etype in (EntityType.CONVEYOR, EntityType.SPLITTER):
            # A mutual 2-cycle (we face them, they face us) is a closed loop:
            # the stack shuttles forever and nothing upstream ever delivers.
            # Splitters rotate their output so they can't be one half of a
            # fixed cycle; only conveyors are checked.
            if etype == EntityType.CONVEYOR and out.add(ct.get_direction(bid)) == tile:
                return BELT_OUT_DEAD
            return BELT_OUT_BELT
        # Harvester, barrier or turret: verified never to accept a stack.
        return BELT_OUT_DEAD

    def _best_feed_direction(self, ct: Controller, tile: Position) -> Direction | None:
        """Direction a conveyor at `tile` should face to connect into the
        network: straight into the core if adjacent to it, else None.

        We deliberately do NOT merge into an arbitrary existing conveyor here,
        even though that would produce a more compact network: a conveyor built
        by another still-in-progress chain gives no guarantee it ultimately
        reaches the core — it could belong to a chain that itself later merges
        elsewhere, stalls, or gets abandoned (CHAIN_BLOCKED_LIMIT), leaving its
        last segment facing an arbitrary direction. Chaining into such a segment
        silently produces a conveyor line that looks connected (builds fine,
        the API has no problem with it) but never delivers anything — this was
        a real, hard-to-spot bug: on cramped/contested maps it dropped delivered
        titanium to zero for the whole match. Only the literal core is a
        verified sink, so that's the only thing we treat as "connected".
        """
        return self._facing_to_core(ct, tile)

    def _try_repair_visible_belt(self, ct: Controller) -> bool:
        """Repair a nearby severed or terminally misdirected conveyor."""
        if ct.get_action_cooldown() != 0 or ct.get_global_resources() < ct.get_conveyor_cost():
            return False
        pos = ct.get_position()
        team = ct.get_team()
        gaps: list[tuple[int, Position, Direction]] = []
        dead: list[tuple[int, Position, Direction]] = []
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) != team or ct.get_entity_type(bid) != EntityType.CONVEYOR:
                continue
            tile = ct.get_position(bid)
            facing = ct.get_direction(bid)
            status = self._belt_output_status(ct, tile, facing)
            if status not in (BELT_OUT_GAP, BELT_OUT_DEAD):
                continue
            target = tile if status == BELT_OUT_DEAD else tile.add(facing)
            if not in_bounds(ct, target) or not ct.is_in_vision(target) or not adjacent(pos, target):
                continue
            if hasattr(self, "_someone_working_at") and self._someone_working_at(ct, target):
                continue
            distance = pos.distance_squared(target)
            (gaps if status == BELT_OUT_GAP else dead).append((distance, target, facing))
        if gaps:
            _, target, fallback = min(gaps)
            facing = self._repair_facing(ct, target) if hasattr(self, "_repair_facing") else fallback
            if facing is not None and ct.can_build_conveyor(target, facing):
                ct.build_conveyor(target, facing)
                return True
        if dead:
            _, target, old_facing = min(dead)
            facing = self._repair_facing(ct, target) if hasattr(self, "_repair_facing") else None
            bid = ct.get_tile_building_id(target)
            if facing is not None and bid is not None and facing != old_facing and ct.can_destroy(target):
                ct.destroy(target)
                if ct.can_build_conveyor(target, facing):
                    ct.build_conveyor(target, facing)
                    return True
        return False

    def _is_nearest_orphan_responder(self, ct: Controller, source: Position) -> bool:
        """Assign a visible orphan Harvester to one nearby non-attacker.

        This is deliberately a local ownership rule.  A Builder that cannot
        see the source cannot claim it, and a farther observer must keep doing
        its own work rather than crossing the map to repair it.  A Builder
        standing beside the source is treated as the active chain owner; its
        presence suppresses a duplicate seed while the opening route is still
        being laid.
        """
        my_id = ct.get_id()
        my_pos = ct.get_position()
        fixed_attackers = {
            ct.read_store(SLOT_PERMA_ATTACKER_ID),
            ct.read_store(SLOT_SECOND_ATTACKER_ID),
        }
        for uid in ct.get_nearby_units():
            if uid == my_id or uid in fixed_attackers:
                continue
            if ct.get_team(uid) != ct.get_team() or ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                continue
            other_pos = ct.get_position(uid)
            if other_pos.distance_squared(source) <= 2:
                return False
            other_dist = other_pos.distance_squared(source)
            my_dist = my_pos.distance_squared(source)
            if other_dist < my_dist or (other_dist == my_dist and uid < my_id):
                return False
        return True

    def _harvester_has_accepting_neighbor(self, ct: Controller, source: Position) -> bool:
        """Return whether a visible friendly logistics neighbor accepts `source`.

        A Conveyor accepts from any cardinal side except its fixed output;
        treating every adjacent Conveyor as an outlet falsely hides a belt
        pointed back into the Harvester. A Splitter accepts only at its back
        side, the opposite of its facing direction.
        """
        team = ct.get_team()
        for direction in CARDINALS:
            neighbor = source.add(direction)
            if not in_bounds(ct, neighbor) or not ct.is_in_vision(neighbor):
                continue
            neighbor_id = ct.get_tile_building_id(neighbor)
            if neighbor_id is None or ct.get_team(neighbor_id) != team:
                continue
            entity_type = ct.get_entity_type(neighbor_id)
            if entity_type == EntityType.CONVEYOR:
                if neighbor.add(ct.get_direction(neighbor_id)) != source:
                    return True
            elif entity_type == EntityType.SPLITTER:
                if neighbor.add(ct.get_direction(neighbor_id).opposite()) == source:
                    return True
        return False

    def _try_reconnect_orphaned_harvester(
        self, ct: Controller, danger: set[Position]
    ) -> bool:
        """Seed one visible, completely disconnected own Harvester locally.

        The responder must already be next to the seed site: a disconnected
        source is useful only when this repair is free of a cross-map detour.
        The same local repair is useful after the first route when a belt has
        been destroyed or left pointing into the Harvester. The existing
        seeded-route FSM performs the rest of the connection.
        """
        if (
            self.core_pos is None
            or ct.get_global_resources() < ct.get_conveyor_cost()
        ):
            return False
        team = ct.get_team()
        pos = ct.get_position()
        choices: list[tuple[int, int, int, Position, Position, Direction]] = []
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) != team or ct.get_entity_type(bid) != EntityType.HARVESTER:
                continue
            source = ct.get_position(bid)
            if not self._is_nearest_orphan_responder(ct, source):
                continue
            if self._harvester_has_accepting_neighbor(ct, source):
                continue
            site_info = self._find_hijack_site(ct, source)
            if site_info is None:
                continue
            site, facing = site_info
            choices.append((
                pos.distance_squared(site),
                source.x,
                source.y,
                source,
                site,
                facing,
            ))
        if not choices:
            return False
        _, _, _, _source, site, facing = min(choices)
        if not adjacent(pos, site):
            return False
        if ct.get_action_cooldown() != 0 or not ct.can_build_conveyor(site, facing):
            return False
        ct.build_conveyor(site, facing)
        self.mode = MODE_CHAIN
        self.route_seed = site
        self.route_seed_pending = None
        self.hijack_harvester = None
        self.hijack_build_pos = None
        self.chain_pending = None
        self.chain_len = 0
        self.chain_blocked = 0
        self.chain_tiles = {site}
        self.chain_limit = manhattan(site, self.core_pos) + CHAIN_SLACK
        self.target = None
        return True

    def _harvestable(self, ct: Controller, tile: Position) -> bool:
        """True if tile is close enough to the core to chain home profitably.

        The limit tightens while the economy is young: a chain costs roughly
        one conveyor and TWO ROUNDS per tile of distance, so a far harvester
        is both expensive and slow to start paying. Early on we take only
        short, cheap chains that begin delivering almost immediately; the
        distant ore is still there once we can afford it. See
        EARLY_HARVEST_RANGE / ECONOMY_PRIORITY_CHAINS in constants.py.
        """
        if self.core_pos is None:
            return True
        limit = self.harvest_range
        if ct.read_store(SLOT_HARVESTER_COUNT) < ECONOMY_PRIORITY_CHAINS:
            # A fixed 12-tile opening is appropriate on compact boards but
            # strands the first routes on large maps (Longship/Aurora/Vault).
            # Scale only the early cap with board perimeter; small maps keep
            # the original economy-safe limit.
            board_bonus = max(0, (ct.get_map_width() + ct.get_map_height() - 32) // 4)
            limit = min(limit, EARLY_HARVEST_RANGE + board_bonus)
        return manhattan(tile, self.core_pos) <= limit

    def _try_build_harvester(self, ct: Controller) -> bool:
        """Build a harvester on an adjacent (cardinal) ore tile. On success, flip
        into CHAIN mode so we connect it back to the core.
        """
        if ct.get_global_resources() < ct.get_harvester_cost():
            return False

        pos = ct.get_position()
        for d in CARDINALS:
            build_pos = pos.add(d)
            if not in_bounds(ct, build_pos):
                continue
            if self._yield_ore_to_closer_builder(ct, build_pos):
                continue
            if not self._harvestable(ct, build_pos):
                continue
            if self._would_sever_belt(ct, build_pos):
                continue  # an existing belt feeds this tile; don't plug it
            if ct.can_build_harvester(build_pos):
                ct.build_harvester(build_pos)

                # Enter CHAIN mode: trail conveyors from here to the network.
                self.mode = MODE_CHAIN
                self.chain_pending = None
                self.chain_len = 0
                self.chain_blocked = 0
                self.chain_tiles = set()
                if self.core_pos is not None:
                    self.chain_limit = manhattan(build_pos, self.core_pos) + CHAIN_SLACK
                else:
                    self.chain_limit = CHAIN_SLACK
                self.target = None
                return True
        return False

    def _yield_ore_to_closer_builder(self, ct: Controller, ore: Position) -> bool:
        """Yield a visible ore to a closer economic Builder.

        Store claims are delayed and the store is full, so resolve collisions
        locally: shorter Manhattan approach wins and entity ID breaks ties.
        Permanent attackers are excluded because they do not build harvesters.
        """
        mine = ct.get_position()
        my_distance = manhattan(mine, ore)
        my_id = ct.get_id()
        team = ct.get_team()
        attacker_ids = {
            ct.read_store(SLOT_PERMA_ATTACKER_ID),
            ct.read_store(SLOT_SECOND_ATTACKER_ID),
        }
        for uid in ct.get_nearby_units():
            if uid == my_id or ct.get_team(uid) != team:
                continue
            if ct.get_entity_type(uid) != EntityType.BUILDER_BOT or uid in attacker_ids:
                continue
            other_distance = manhattan(ct.get_position(uid), ore)
            if other_distance < my_distance or (other_distance == my_distance and uid < my_id):
                return True
        return False

    def _run_chain(self, ct: Controller, danger: set[Position]) -> None:
        """Lay a connected conveyor chain from the last harvester straight to the
        core — the only tile we treat as a verified sink (see
        `_best_feed_direction`). We walk toward the core itself, one cardinal
        step at a time, and build on the turn after each step, on the tile we
        just vacated, facing the way we moved. Because we can't move and build
        in the same turn, this alternates move/build — half speed, but
        purposeful. The very first trailed tile sits next to the harvester (we
        can never step onto the harvester itself, so the conveyor never faces
        into it). The chain ends the moment a placed conveyor lands facing
        directly into the core.
        """
        core = self.core_pos
        pos = ct.get_position()

        if self.route_seed is not None:
            self._run_seeded_route(ct, danger)
            return

        if core is None or self.chain_len > self.chain_limit:
            self._end_chain(ct)
            return

        # If we owe a conveyor on a vacated tile, place it before moving on.
        if self.chain_pending is not None:
            if ct.get_action_cooldown() == 0:
                tile, fallback_facing = self.chain_pending
                # Adjacency first, before any vision-sensitive query below —
                # chain_pending can go stale (the tile set 1+ rounds ago, no
                # longer adjacent) if the danger-flee check earlier in
                # _run_builder pulls us away before we get back here, and
                # querying a tile we've lost vision of raises GameError
                # rather than returning a false answer. adjacent() is pure
                # math (no engine call), so it's always safe to check first.
                if not (adjacent(pos, tile) and in_bounds(ct, tile)):
                    self.chain_pending = None  # lost adjacency; skip this segment
                    return
                # If this tile can now feed straight into the core or an existing
                # conveyor, use that facing instead of our walking direction —
                # otherwise the stack never actually drains anywhere.
                feed_dir = self._best_feed_direction(ct, tile)
                facing = feed_dir if feed_dir is not None else fallback_facing
                connects = feed_dir is not None
                # The fallback is just "the way we walked", chosen a round ago.
                # By now that tile can hold a wall we routed around, a building
                # a teammate put up, or the belt we ourselves laid pointing
                # back at us — laying into any of those creates exactly the
                # dead ends the repair pass then has to come and undo. Prefer
                # any direction that still accepts; if none does, skip the
                # segment rather than build a known-dead tile.
                if not connects and self._belt_output_status(ct, tile, facing) == BELT_OUT_DEAD:
                    alt = self._repair_facing(ct, tile)
                    if alt is None:
                        self.chain_pending = None
                        return
                    facing = alt
                if not ct.is_tile_empty(tile):
                    # Something already occupies it (often our own conveyor from an
                    # earlier round) — no need to build, just move past it. Only
                    # treat it as the finish line if it's core-adjacent; otherwise
                    # walking on toward the core (below) continues as normal.
                    self.chain_pending = None
                    if connects:
                        self._end_chain(ct, success=True)
                elif ct.get_global_resources() < ct.get_conveyor_cost():
                    # Can't afford it yet — wait rather than leaving a gap.
                    self.chain_blocked += 1
                    if self.chain_blocked >= CHAIN_BLOCKED_LIMIT:
                        self._end_chain(ct)
                elif ct.can_build_conveyor(tile, facing):
                    ct.build_conveyor(tile, facing)
                    self.chain_len += 1
                    self.chain_tiles.add(tile)
                    self.chain_pending = None
                    self.chain_blocked = 0
                    if connects:
                        self._end_chain(ct, success=True)  # reached the core; done
                else:
                    self.chain_pending = None  # unbuildable here; skip segment
            return

        # THE FINAL BELT. If we're standing on a core-adjacent tile, this tile
        # is the last link in the chain — and finishing it needs a special
        # case, because the normal "walk closer, build on the tile you
        # vacated" rhythm cannot complete here.
        #
        # AGENT.md states that a team's own core tiles are passable. THEY ARE
        # NOT — verified directly against the engine: is_tile_passable() and
        # can_move() both report False for our own core. So from a tile
        # orthogonally adjacent to the core there is no legal step that gets
        # any closer, _navigate() correctly reports no progress, and the chain
        # was abandoned after CHAIN_BLOCKED_LIMIT rounds exactly one belt
        # short of delivering. Measured: 14 of 19 chain failures were stuck at
        # manhattan distance 1 from the core — the "missing last belt" bug.
        #
        # Fix: step ASIDE rather than forward. Any legal neighbour will do —
        # we only need to stop standing on the tile so we can build on it next
        # round, facing into the core.
        finish_dir = self._facing_to_core(ct, pos)
        if finish_dir is not None:
            if not ct.is_tile_empty(pos):
                self._end_chain(ct, success=True)  # already built here; done
                return
            if ct.get_move_cooldown() == 0:
                for d in CARDINALS:
                    step = pos.add(d)
                    if not in_bounds(ct, step) or step in danger:
                        continue
                    if ct.can_move(d):
                        ct.move(d)
                        self.chain_pending = (pos, finish_dir)
                        self.chain_blocked = 0
                        return
            self.chain_blocked += 1
            if self.chain_blocked >= CHAIN_BLOCKED_LIMIT:
                self._end_chain(ct)
            return

        # No pending conveyor: take another step toward the core, trailing a
        # conveyor on the tile we leave. (We keep going until a placed conveyor
        # faces directly into the core; standing adjacent isn't enough on its
        # own — it has to actually output onto a core tile.)
        moved = self._navigate(ct, core, avoid=danger)
        if moved is not None:
            self.chain_pending = (pos, moved)
            self.chain_blocked = 0
        else:
            self.chain_blocked += 1
            if self.chain_blocked >= CHAIN_BLOCKED_LIMIT:
                self._end_chain(ct)

    def _hijack_facing(self, ct: Controller, belt: Position, harvester: Position) -> Direction | None:
        """Choose a conveyor output that avoids pointing back into the source."""
        forbidden = next((d for d in CARDINALS if belt.add(d) == harvester), None)
        team = ct.get_team()
        preferred: list[tuple[int, Direction]] = []
        for d in CARDINALS:
            if d == forbidden:
                continue
            out = belt.add(d)
            if not in_bounds(ct, out) or not ct.is_in_vision(out):
                continue
            bid = ct.get_tile_building_id(out)
            if bid is None or ct.get_team(bid) != team:
                continue
            etype = ct.get_entity_type(bid)
            if etype == EntityType.CORE:
                preferred.append((-1000, d))
            elif etype in (EntityType.CONVEYOR, EntityType.SPLITTER):
                preferred.append((-500 + manhattan(out, self.core_pos), d))
        if preferred:
            return min(preferred, key=lambda item: item[0])[1]
        candidates = [d for d in CARDINALS if d != forbidden]
        if self.core_pos is not None:
            candidates.sort(key=lambda d: manhattan(belt.add(d), self.core_pos))
        return candidates[0] if candidates else None

    def _find_hijack_site(self, ct: Controller, harvester: Position) -> tuple[Position, Direction] | None:
        pos = ct.get_position()
        choices: list[tuple[int, int, Position, Direction]] = []
        for d in CARDINALS:
            site = harvester.add(d)
            if not in_bounds(ct, site) or not ct.is_in_vision(site) or not ct.is_tile_empty(site):
                continue
            facing = self._hijack_facing(ct, site, harvester)
            if facing is None:
                continue
            if adjacent(pos, site) and not ct.can_build_conveyor(site, facing):
                continue
            choices.append((0 if adjacent(pos, site) else 1, pos.distance_squared(site), site, facing))
        if not choices:
            return None
        choices.sort(key=lambda item: (item[0], item[1], manhattan(item[2], self.core_pos) if self.core_pos else 0))
        return choices[0][2], choices[0][3]

    def _try_hijack_enemy_harvester(self, ct: Controller, danger: set[Position]) -> bool:
        """Claim one visible enemy Harvester with an adjacent conveyor."""
        if self.core_pos is None or ct.get_global_resources() < ct.get_conveyor_cost():
            return False
        pos = ct.get_position()
        visible = [
            (pos.distance_squared(ct.get_position(bid)), ct.get_position(bid))
            for bid in ct.get_nearby_buildings()
            if ct.get_team(bid) != ct.get_team() and ct.get_entity_type(bid) == EntityType.HARVESTER
        ]
        if not visible:
            self.hijack_harvester = None
            self.hijack_build_pos = None
            return False
        visible.sort(key=lambda item: (item[0], item[1].x, item[1].y))
        harvester = self.hijack_harvester or visible[0][1]
        if all(harvester != target for _, target in visible):
            harvester = visible[0][1]
            self.hijack_build_pos = None
        self.hijack_harvester = harvester
        site_info = None
        if self.hijack_build_pos is not None:
            site = self.hijack_build_pos
            if (in_bounds(ct, site) and ct.is_in_vision(site) and ct.is_tile_empty(site)
                    and adjacent(site, harvester)):
                facing = self._hijack_facing(ct, site, harvester)
                if facing is not None and ct.can_build_conveyor(site, facing):
                    site_info = (site, facing)
        if site_info is None:
            site_info = self._find_hijack_site(ct, harvester)
            if site_info is None:
                self.hijack_harvester = None
                self.hijack_build_pos = None
                return False
            self.hijack_build_pos = site_info[0]
        site, facing = site_info
        if not adjacent(pos, site):
            if ct.get_move_cooldown() == 0:
                self._navigate(ct, site, avoid=danger)
            return True
        if ct.get_action_cooldown() != 0 or not ct.can_build_conveyor(site, facing):
            return True
        ct.build_conveyor(site, facing)
        self.mode = MODE_CHAIN
        self.route_seed = site
        self.route_seed_pending = None
        self.chain_pending = None
        self.chain_len = 0
        self.chain_blocked = 0
        self.chain_tiles = {site}
        self.chain_limit = manhattan(site, self.core_pos) + CHAIN_SLACK
        self.target = None
        return True

    def _end_seeded_route(self) -> None:
        self.route_seed = None
        self.route_seed_pending = None
        self.hijack_harvester = None
        self.hijack_build_pos = None
        self.mode = MODE_SCOUT
        self.chain_pending = None
        self.chain_len = 0
        self.chain_blocked = 0
        self.chain_tiles = set()
        self.target = None
        self.best_dist = float("inf")
        self.no_progress = 0
        if hasattr(self, "_clear_task"):
            self._clear_task()

    def _run_seeded_route(self, ct: Controller, danger: set[Position]) -> bool:
        """Extend the seeded conveyor until it joins our normal route."""
        seed = self.route_seed
        core = self.core_pos
        if seed is None or core is None:
            self._end_seeded_route()
            return True
        pos = ct.get_position()
        if pos != seed and self.route_seed_pending is None:
            if ct.get_move_cooldown() == 0:
                self._navigate(ct, seed, avoid=danger)
            return True
        if self.route_seed_pending is None:
            if not ct.is_in_vision(seed):
                self._end_seeded_route()
                return True
            seed_id = ct.get_tile_building_id(seed)
            if seed_id is None:
                self._end_seeded_route()
                return True
            if (
                ct.get_team(seed_id) != ct.get_team()
                or ct.get_entity_type(seed_id) != EntityType.CONVEYOR
            ):
                # A stale seeded route must not call get_direction() on a
                # replacement building (Barriers/Gunners have no facing).
                # Drop back to SCOUT so the builder can recover normally.
                self._end_seeded_route()
                return True
            facing = ct.get_direction(seed_id)
            out = seed.add(facing)
            if (self._facing_to_core(ct, seed) is not None
                    or (in_bounds(ct, out) and ct.is_in_vision(out)
                        and ct.get_tile_building_id(out) is not None
                        and ct.get_team(ct.get_tile_building_id(out)) == ct.get_team(ct.get_tile_building_id(seed))
                        and ct.get_entity_type(ct.get_tile_building_id(out)) in (EntityType.CONVEYOR, EntityType.SPLITTER))):
                self._end_seeded_route()
                return True
            if ct.get_move_cooldown() == 0 and ct.can_move(facing):
                ct.move(facing)
                self.route_seed_pending = out
            return True
        pending = self.route_seed_pending
        if pos != pending:
            if ct.get_move_cooldown() == 0:
                self._navigate(ct, pending, avoid=danger)
            return True
        finish_dir = self._facing_to_core(ct, pending)
        if finish_dir is not None:
            for d in CARDINALS:
                step = pending.add(d)
                if in_bounds(ct, step) and step not in danger and ct.can_move(d):
                    ct.move(d)
                    self.route_seed = None
                    self.route_seed_pending = None
                    self.chain_pending = (pending, finish_dir)
                    return True
        moved = self._navigate(ct, core, avoid=danger)
        if moved is not None:
            self.route_seed = None
            self.route_seed_pending = None
            self.chain_pending = (pending, moved)
            return True
        self.chain_blocked += 1
        if self.chain_blocked >= CHAIN_BLOCKED_LIMIT:
            self._end_seeded_route()
        return True

    def _end_chain(self, ct: Controller, success: bool = False) -> None:
        if success:
            # Deliberately multi-writer (see the store note in constants.py) —
            # a same-round race just under-counts by one, which only delays
            # the HARVESTER_MILESTONE trigger by a round at worst.
            ct.write_store(SLOT_HARVESTER_COUNT, ct.read_store(SLOT_HARVESTER_COUNT) + 1)
        self.mode = MODE_SCOUT
        self.chain_pending = None
        self.chain_len = 0
        self.chain_blocked = 0
        self.chain_tiles = set()
        self.target = None
        self.best_dist = float("inf")
        self.no_progress = 0

    def _try_build_gunner(self, ct: Controller) -> bool:
        """Build a home turret, but only if the core has designated this exact
        builder as the round's defender (see core_role._update_defense). That
        serialises turret building to at most one per round, so SLOT_GUNNER_CAP
        is an actual cap instead of a target every nearby builder races to hit
        independently.

        The first completed harvester route is the opening economic milestone.
        Until it exists, leave this conversion budget available for the route
        itself; the core still has its existing emergency response paths, and
        this prevents a home defender from becoming a zero-harvester turret
        shell on cramped maps.

        We also never build on a tile orthogonally adjacent to the core — those 8
        tiles are where conveyor chains need to land to drain into the core, and a
        turret sitting there would permanently block that harvester's chain.
        """
        if self.core_pos is None:
            return False
        if ct.read_store(SLOT_HARVESTER_COUNT) == 0:
            return False
        if ct.read_store(SLOT_DEFENDER_ID) != ct.get_id():
            return False
        pos = ct.get_position()
        dist_sq = pos.distance_squared(self.core_pos)
        if not (GUNNER_MIN_CORE_DIST_SQ <= dist_sq <= GUNNER_NEAR_CORE_DIST_SQ):
            return False
        if ct.get_global_resources() < ct.get_gunner_cost():
            return False

        # Face away from the core, toward incoming enemies. Choose the
        # dominant cardinal axis directly so Builder behavior remains visibly
        # cardinal and does not depend on the generic directional helper.
        dx = pos.x - self.core_pos.x
        dy = pos.y - self.core_pos.y
        if abs(dx) >= abs(dy) and dx:
            facing = Direction.EAST if dx > 0 else Direction.WEST
        elif dy:
            facing = Direction.SOUTH if dy > 0 else Direction.NORTH
        else:
            facing = random.choice(DIRECTIONS)

        for d in CARDINALS:
            build_pos = pos.add(d)
            if not in_bounds(ct, build_pos):
                continue
            # Keep every home turret inside the Core's authoritative vision.
            # A Builder standing on the outer edge of the old placement band
            # could build one step farther out; the Core then forgot it on the
            # next round and authorised another.  Defense that its owner cannot
            # observe is not a cap, so remote placement is refused here.
            if build_pos.distance_squared(self.core_pos) > GUNNER_NEAR_CORE_DIST_SQ:
                continue
            if self._facing_to_core(ct, build_pos) is not None:
                continue  # reserved for the conveyor network, not turrets
            if self._would_sever_belt(ct, build_pos):
                continue  # an existing belt feeds this tile; don't plug it
            if ct.can_build_gunner(build_pos, facing):
                ct.build_gunner(build_pos, facing)
                return True
        return False

    def _try_build_ore_turret(self, ct: Controller) -> bool:
        """Build at most one selective gunner beside contested remote ore."""
        if self.core_pos is None or len(self.ore_turret_sites) >= ORE_TURRET_MAX_PER_BUILDER:
            return False
        enemy_core = self._enemy_core_target(ct)
        if enemy_core is None:
            return False
        cramped = manhattan(self.core_pos, enemy_core) <= 20
        if not cramped and ct.get_current_round() < ORE_TURRET_MIN_ROUND:
            return False
        reserve = 0 if cramped else ORE_TURRET_RESERVE
        if ct.get_global_resources() < ct.get_gunner_cost() + reserve:
            return False
        team = ct.get_team()
        pos = ct.get_position()
        candidates: list[tuple[int, Position, Position]] = []
        for ore in ct.get_nearby_tiles():
            if ct.get_tile_env(ore) != Environment.ORE_TITANIUM:
                continue
            if ct.get_tile_building_id(ore) is not None or ore in self.ore_turret_sites:
                continue
            if manhattan(ore, enemy_core) >= manhattan(ore, self.core_pos) and self._harvestable(ct, ore):
                continue
            for d in CARDINALS:
                site = ore.add(d)
                if not in_bounds(ct, site) or not ct.is_in_vision(site) or not ct.is_tile_empty(site):
                    continue
                if not adjacent(pos, site) or self._would_sever_belt(ct, site):
                    continue
                if any(
                    ct.get_team(bid) == team
                    and ct.get_entity_type(bid) == EntityType.GUNNER
                    and ct.get_position(bid).distance_squared(ore) <= 4
                    for bid in ct.get_nearby_buildings()
                ):
                    continue
                candidates.append((pos.distance_squared(ore), ore, site))
        if not candidates:
            return False
        candidates.sort(key=lambda item: item[0])
        _, ore, site = candidates[0]
        dx = enemy_core.x - site.x
        dy = enemy_core.y - site.y
        if abs(dx) >= abs(dy) and dx:
            facing = Direction.EAST if dx > 0 else Direction.WEST
        elif dy:
            facing = Direction.SOUTH if dy > 0 else Direction.NORTH
        else:
            facing = DIRECTIONS[0]
        if ct.can_build_gunner(site, facing):
            ct.build_gunner(site, facing)
            self.ore_turret_sites.add(ore)
            return True
        return False

    def _try_heal(self, ct: Controller) -> None:
        """Heal a damaged friendly entity on an adjacent tile (1 Ti -> +4 HP)."""
        pos = ct.get_position()
        for d in CARDINALS:
            check = pos.add(d)
            if in_bounds(ct, check) and ct.can_heal(check):
                ct.heal(check)
                return

    # ------------------------------------------------------------------
    # Movement & targeting (SCOUT mode)
    # ------------------------------------------------------------------

    def _move_toward_target(self, ct: Controller, danger: set[Position]) -> None:
        """Navigate toward our current target, picking a new one when we've
        arrived or can't get any closer for a while. Movement only — no building.

        We must never end up standing *on* the ore we want: harvesters are built
        on an adjacent tile, so a bot sitting on its ore can never build it. We
        stop one tile short of ore targets, and dislodge ourselves if we're
        already on uncovered ore.
        """
        if ct.get_move_cooldown() != 0:
            return

        pos = ct.get_position()

        # Dislodge: standing on uncovered ore -> step off so it becomes a
        # buildable neighbour next turn (prefer a non-ore, non-danger tile).
        if ct.get_tile_env(pos) == Environment.ORE_TITANIUM and ct.get_tile_building_id(pos) is None:
            for prefer_safe_non_ore in (True, False):
                for d in CARDINALS:
                    n = pos.add(d)
                    if not in_bounds(ct, n) or not ct.can_move(d):
                        continue
                    if prefer_safe_non_ore and (n in danger or ct.get_tile_env(n) == Environment.ORE_TITANIUM):
                        continue
                    ct.move(d)
                    return
            return

        # (Re)pick a target when we've arrived or don't have one.
        if self.target is None or pos == self.target:
            self._new_target(ct, danger)
        if self.target is None:
            return

        # Track progress; if we can't get closer for a while the target is likely
        # unreachable (walled off) — blacklist it and pick another.
        dist = pos.distance_squared(self.target)
        if dist < self.best_dist:
            self.best_dist = dist
            self.no_progress = 0
        else:
            self.no_progress += 1
            if self.no_progress >= NAV_GIVEUP:
                self.blacklist[self.target] = ct.get_current_round() + BLACKLIST_ROUNDS
                self._new_target(ct, danger)
                if self.target is None:
                    return
                dist = pos.distance_squared(self.target)

        # Stop one tile short of an ore target — the build phase harvests it.
        if dist == 1 and self._is_ore_target(ct, self.target):
            return

        self._navigate(ct, self.target, avoid=danger)

    def _new_target(self, ct: Controller, danger: set[Position]) -> None:
        self.target = self._pick_target(ct, danger)
        self.best_dist = float("inf")
        self.no_progress = 0

    def _is_ore_target(self, ct: Controller, tile: Position) -> bool:
        return ct.is_in_vision(tile) and ct.get_tile_env(tile) == Environment.ORE_TITANIUM

    def _pick_target(self, ct: Controller, danger: set[Position]) -> Position:
        """Choose the next position to navigate toward.

        Priority: nearest visible uncovered ore > nearest ore advertised by a
        teammate that's still uncovered > systematic exploration of our quadrant.
        Never targets a tile sitting in a visible enemy turret's line of fire.
        """
        pos = ct.get_position()
        self._expire_blacklist(ct)

        # 1. Nearest visible uncovered ore.
        best = None
        best_dist = float("inf")
        for tile in ct.get_nearby_tiles():
            if ct.get_tile_env(tile) != Environment.ORE_TITANIUM:
                continue
            if ct.get_tile_building_id(tile) is not None:
                continue
            if (tile in self.blacklist or not self._harvestable(ct, tile)
                    or tile in danger or self._yield_ore_to_closer_builder(ct, tile)):
                continue
            d = pos.distance_squared(tile)
            if 0 < d < best_dist:  # 0 = our own tile; handled by the dislodge logic
                best_dist = d
                best = tile
        if best is not None:
            return best

        # 2. Nearest advertised ore that isn't visibly covered.
        best = None
        best_dist = float("inf")
        for i in range(ORE_QUEUE_LEN):
            cand = unpack_pos(ct.read_store(SLOT_ORE_QUEUE_BASE + i))
            if cand is None or not in_bounds(ct, cand) or cand in self.blacklist:
                continue
            if not self._harvestable(ct, cand) or cand in danger:
                continue
            if ct.is_in_vision(cand) and ct.get_tile_building_id(cand) is not None:
                continue
            d = pos.distance_squared(cand)
            if d > 2 and d < best_dist:  # ignore ore we're basically standing on
                best_dist = d
                best = cand
        if best is not None:
            return best

        # 3. Explore — fan out toward this bot's assigned quadrant.
        return self._explore_target(ct, danger)

    def _expire_blacklist(self, ct: Controller) -> None:
        if not self.blacklist:
            return
        now = ct.get_current_round()
        for tile in [t for t, exp in self.blacklist.items() if exp <= now]:
            del self.blacklist[tile]

    def _explore_target(self, ct: Controller, danger: set[Position]) -> Position:
        """Pick a bounded deterministic frontier target so bots spread out and discover new ore.
        Unreachable picks are abandoned by the progress/blacklist logic.

        Never a tile currently in enemy turret fire, and — since ore beyond
        harvest_range can't be harvested anyway (_harvestable) — biased to stay
        within roughly that range of home rather than wandering blind into
        contested or enemy territory purely for vision.
        """
        w, h = ct.get_map_width(), ct.get_map_height()
        pos = ct.get_position()
        self.explore_cursor += 1
        candidates = []
        for y in range(h):
            for x in range(w):
                cand = Position(x, y)
                if cand in danger or pos.distance_squared(cand) < EXPLORE_MIN_DIST_SQ:
                    continue
                if self.core_pos is not None and manhattan(cand, self.core_pos) > self.harvest_range * 1.3:
                    continue
                candidates.append(cand)
        if candidates:
            # A fixed stride gives every builder a stable, spread-out frontier
            # sequence without sharing the process-global random stream.
            # Blacklist/progress logic still abandons blocked cells.
            candidates.sort(key=lambda p: (p.y, p.x))
            start = (self.explore_cursor * 37 + ct.get_id() * 11) % len(candidates)
            for offset in range(min(len(candidates), 24)):
                cand = candidates[(start + offset * 37) % len(candidates)]
                if cand not in danger:
                    return cand
        return self.core_pos if self.core_pos is not None else pos

    def _share_ore(self, ct: Controller) -> None:
        """Advertise a visible uncovered ore tile into the store ring-buffer so
        teammates can navigate toward ore they haven't seen. Skips duplicates.
        Both roles call this — an attacker passing through can still tip off
        the defenders even though it never harvests anything itself.
        """
        for tile in ct.get_nearby_tiles():
            if ct.get_tile_env(tile) != Environment.ORE_TITANIUM:
                continue
            if ct.get_tile_building_id(tile) is not None:
                continue
            val = pack_pos(tile)
            if any(ct.read_store(SLOT_ORE_QUEUE_BASE + i) == val for i in range(ORE_QUEUE_LEN)):
                return  # already advertised
            packed_cursor = ct.read_store(SLOT_ORE_CURSOR)
            cursor = ore_cursor_from_packed(packed_cursor)
            ct.write_store(SLOT_ORE_QUEUE_BASE + cursor, val)
            # Preserve the Core's high-bit economy phase while advancing the
            # legacy four-entry ore cursor.  Without this, any Builder that
            # advertises ore would erase the income heartbeat in the same
            # delayed Store channel.
            phase_bits = packed_cursor & ~ORE_CURSOR_MASK
            ct.write_store(
                SLOT_ORE_CURSOR,
                phase_bits | ((cursor + 1) % ORE_QUEUE_LEN),
            )
            return
