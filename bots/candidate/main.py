"""Starter bot — economy + two combat roles (Defender / Attacker).

Each unit gets its own Player instance; the engine calls run() once per round.
This file is just the entry point: state + top-level dispatch. The actual
role logic lives in sibling modules so each piece is easier to digest:

  constants.py   tuning knobs, direction tables, communication-store layout
  util.py        stateless helpers (store packing, distance/adjacency math)
  navigation.py  shared BFS pathing + enemy-fire-line detection
  core_role.py   CORE unit: spawning, ammo, dynamic home-turret sizing
  defender.py    DEFENDER builders: economy (ore -> harvester -> conveyor
                 chain to core) + opportunistic home-turret building
  attacker.py    ATTACKER builders: find the enemy core, place the team's
                 one forward sentinel there, then wreck harvesters/belts

Strategy recap:
  1. Core spawns builder bots in two stages: an initial roster of 3
     (1 permanent attacker + 2 defenders), then a second wave up to 6 once
     one completed harvester chain or the bounded round fallback proves the
     economy is moving
     — see core_role.py and constants.py's INITIAL_BUILDER_TARGET /
     REINFORCEMENT_BUILDER_TARGET. It also keeps a small global-ammo buffer
     topped up and computes a dynamic home-turret cap (2-5) each round from
     economy + visible threat. Turrets only ever get built at home, never in
     enemy territory.
  2. Every builder bot picks a role once, deferred to its second round of
     life (see _assign_role): the first builder ever spawned, and the first
     builder of the stage-2 wave, are always ATTACKER regardless of economy
     state; everyone else stays DEFENDER (economy + home defense) until the
     team has completed a couple of harvester chains, after which roughly
     1-in-3 new spawns go ATTACKER too.
  3. An attacker's own priority is: find the enemy core, place the team's
     one forward sentinel there (its facing is permanent once built, unlike
     a gunner's — see attacker.py), THEN start wrecking enemy harvesters and
     conveyor belts.
  4. Bots share every ore tile *and* enemy-core sighting they see through
     small store slots, so intel spreads without everyone re-discovering it.
  5. Gunners rotate to face whatever enemy they can actually line up on
     (verified via can_fire_from, not just guessed from direction) and then
     auto-fire once aligned. Sentinels can't rotate at all, so they just fire
     at whatever's in their fixed line.

See constants.py for the full communication-store slot map and every tuning
constant in one place — that's the file to edit when balancing the bot.
"""


from fcode import Controller, Direction, EntityType, Environment, GameError, Position

from bot.attacker import AttackerMixin
from bot.constants import (CARDINALS, CORE_SIEGE_CRISIS_HP, CORE_SIEGE_HP, CORE_SIEGE_RECALL_SQ, DIRECTIONS, IDLE_ATTACK_RESERVE,
                       HARVEST_RANGE_FRAC, MODE_CHAIN, MODE_SCOUT, ROLE_ATTACKER, ROLE_DEFENDER,
                       ROLE_DYNAMIC, SIEGE_HP_SHIFT, SLOT_CORE_SIEGE, SLOT_CORE_X, SLOT_CORE_Y,
                       SLOT_ENEMY_CORE, SLOT_HARVESTER_COUNT, SLOT_PERMA_ATTACKER_ID, SLOT_PERMA_DEFENDER_ID, SLOT_SECOND_ATTACKER_ID,
                       TASK_NONE)
from bot.core_role import CoreMixin
from bot.defender import DefenderMixin
from bot.dynamic import DynamicMixin
from bot.navigation import NavigationMixin
from bot.util import adjacent, core_footprint, in_bounds, unpack_pos


class Player(CoreMixin, DefenderMixin, AttackerMixin, DynamicMixin, NavigationMixin):
    def __init__(self):
        # Core: ids of builder bots we've spawned that we still believe are
        # alive (pruned every round in core_role._prune_dead_builders — see
        # there for why this is precise rather than a monotonic counter).
        # ramp_established flips True once we've ever reached our initial
        # 3-builder roster — gates whether combat-loss replacement is allowed
        # to skip the spawn Ti reserve (see MIN_BUILDERS_ALIVE in
        # constants.py); it must not apply during the very first ramp-up.
        self.builder_ids: list[int] = []
        # Core-only observation of every home Gunner we have seen.  The old
        # defense loop counted only buildings in the Core's current vision;
        # remote counter-Gunners then made that count forgetful and the Core
        # kept authorising replacements forever.  Keeping ids is conservative
        # when a turret leaves vision, which is the safe side of the cap.
        self.gunner_ids: set[int] = set()
        # Lifetime set for the home-defense budget.  Rebuilding a Gunner every
        # time the previous one dies is another economy loop: on pressured maps
        # the old bot spent hundreds of purchases on a five-turret target.  A
        # turret slot is therefore a strategic investment for this game, not a
        # respawn permission.
        self.gunner_history: set[int] = set()
        self.ramp_established = False

        # Core only: consecutive rounds too poor to afford a harvester, used
        # by core_role._floor_reserve to detect the ammo/economy deadlock.
        self.poor_streak = 0
        # Core only: HP the core is currently missing, mirrored into
        # SLOT_CORE_SIEGE each round for the builders (see _publish_siege).
        self.core_missing_hp = 0
        # Core-only accounting for the income-aware lifetime ammunition cap.
        self.prev_resources: int | None = None
        self.last_conversion = 0
        self.income_seen = 0
        # Core-only delivery heartbeat.  This is deliberately separate from
        # income_seen: a lifetime total cannot tell whether the route is still
        # paying when the historical Harvester milestone releases workers.
        self.income_quiet_rounds = 0
        self.ammo_spent = 0

        # Builder role (decided once, deferred to the builder's second round
        # of life — see _run_builder/_assign_role) and, for DEFENDER, the
        # economy sub-mode.
        self.role: int | None = None
        self.spawn_round: int | None = None
        self.mode = MODE_SCOUT

        # Builder navigation state (shared by both roles).
        self.target: Position | None = None    # where we're trying to walk to
        self.best_dist = float("inf")          # closest we've been to the target
        self.no_progress = 0                    # rounds without getting closer
        self.visited: dict[Position, int] = {}  # per-bot terrain memory (visit counts)
        self.blacklist: dict[Position, int] = {}  # targets we gave up on -> expiry round
        self.explore_cursor = 0

        # Chain-laying state (DEFENDER, CHAIN mode). We trail a line of conveyors
        # behind us as we walk toward the network; chain_pending is the tile we
        # still owe a conveyor (the tile we just vacated) plus the facing it
        # should point. chain_tiles holds tiles this chain has already laid, so
        # the walk goal (nearest network tile) never targets our own freshly-laid
        # trail.
        self.chain_pending: tuple | None = None
        self.chain_len = 0
        self.chain_limit = 0
        self.chain_blocked = 0
        self.chain_tiles: set[Position] = set()

        # A hijack starts with a conveyor built beside an enemy Harvester.
        # The regular chain loop assumes it owns the source Harvester, so a
        # small seeded-route state lets an attacker route stolen output home
        # without counting it as one of our completed chains.
        self.route_seed: Position | None = None
        self.route_seed_pending: Position | None = None
        self.hijack_harvester: Position | None = None
        self.hijack_build_pos: Position | None = None
        self.ore_turret_sites: set[Position] = set()
        self.home_barrier_sites: set[Position] = set()

        # Cached core position (read from the store once, then reused) and the
        # furthest (Manhattan) we'll plant a harvester from it. Ore beyond this
        # can't be chained home before the enemy contests it, and chasing it just
        # overextends bots into the kill zone — so we harvest within range and let
        # the rest go. Set from map size once the core position is known.
        self.core_pos: Position | None = None
        self.harvest_range = 999

        # ATTACKER state: best known/guessed enemy core position, and an enemy
        # economy building we're currently detouring to destroy (if any).
        # The forward-sentinel pool is NOT tracked here — it's re-observed
        # live each round (attacker.py::_count_forward_sentinels) so losses
        # get replaced instead of a one-way flag latching "done" forever.
        self.enemy_core_known: Position | None = None
        self.attack_target: Position | None = None
        # A primary attacker may establish one early home Launcher relay.  The
        # flag belongs to the Builder instance; a destroyed relay is not
        # rebuilt by an unrelated worker.
        self.opening_launcher_built = False

        # ATTACKER forward-sentinel site memory (see the SENTINEL_* block in
        # constants.py). sentinel_watch is the (id, tile, round) of our most
        # recent plant, watched until it either proves durable or dies young;
        # sentinel_sites maps a tile that ate a short-lived sentinel to the
        # round its ban expires. Per-bot: the treadmill was a single attacker
        # rebuilding on one tile, so per-bot memory is where it gets broken.
        self.sentinel_watch: tuple | None = None
        self.sentinel_sites: dict[Position, int] = {}
        self.enemy_barrier_sites: set[Position] = set()

        # DYNAMIC state: the task currently held, what it's aimed at, and the
        # round it was picked (for the commitment floor). See dynamic.py.
        self.task = TASK_NONE
        self.task_target: Position | None = None
        self.task_started = 0

    def run(self, ct: Controller) -> None:
        """Entry point called by the engine every round for each unit.

        Wrapped in a guard so a stray GameError (e.g. an out-of-bounds query at a
        map edge) can never permanently destroy the unit — it would otherwise be
        removed for the rest of the match.
        """
        try:
            etype = ct.get_entity_type()
            if etype == EntityType.CORE:
                self._run_core(ct)
            elif etype == EntityType.BUILDER_BOT:
                self._run_builder(ct)
            elif etype == EntityType.GUNNER:
                self._run_gunner(ct)
            elif etype == EntityType.SENTINEL:
                self._run_sentinel(ct)
            elif etype == EntityType.LAUNCHER:
                self._run_launcher(ct)
        except Exception as e:  # noqa: BLE001 — never let a unit die to an edge case
            return

    def _run_launcher(self, ct: Controller) -> None:
        """Use a stationary Launcher as a bounded control relay.

        Enemy Builders near home are ejected away from our Core first.  When
        there is no infiltrator, only a designated fixed attacker may be
        picked up, and only a destination that strictly approaches the known
        or symmetric enemy Core is considered.  Every throw is authorized by
        ``can_launch``; no destination occupancy or facing is inferred.
        """
        try:
            own_team = ct.get_team()
            launcher_pos = ct.get_position()
            if self.core_pos is None:
                self._read_core_pos(ct)
            own_core = self.core_pos
            enemy_core = self.enemy_core_known or unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
            if enemy_core is None and own_core is not None:
                enemy_core = Position(
                    ct.get_map_width() - 1 - own_core.x,
                    ct.get_map_height() - 1 - own_core.y,
                )
            builders: list[tuple[int, Position, bool]] = []
            for entity_id in tuple(ct.get_nearby_units())[:32]:
                try:
                    if ct.get_entity_type(entity_id) != EntityType.BUILDER_BOT:
                        continue
                    position = ct.get_position(entity_id)
                    team = ct.get_team(entity_id)
                except Exception:
                    continue
                delta_x = abs(position.x - launcher_pos.x)
                delta_y = abs(position.y - launcher_pos.y)
                if max(delta_x, delta_y) > 1:
                    continue
                builders.append((entity_id, position, team == own_team))
            if not builders:
                return

            # Eject an infiltrator before moving our own workforce.  The
            # destination must increase its squared distance from our Core.
            enemy_candidates = [item for item in builders if not item[2]]
            if enemy_candidates and own_core is not None:
                pickup, pickup_pos, _ = min(
                    enemy_candidates,
                    key=lambda item: (item[1].distance_squared(own_core), item[0]),
                )
                destination = self._launcher_destination(
                    ct,
                    launcher_pos,
                    pickup_pos,
                    own_core,
                    enemy_core,
                    enemy=True,
                )
                if destination is not None and ct.can_launch(pickup_pos, destination):
                    ct.launch(pickup_pos, destination)
                return

            fixed_ids = {
                int(ct.read_store(SLOT_PERMA_ATTACKER_ID)),
                int(ct.read_store(SLOT_SECOND_ATTACKER_ID)),
            }
            fixed_ids.discard(0)
            own_candidates = [item for item in builders if item[2] and item[0] in fixed_ids]
            if not own_candidates or enemy_core is None:
                return
            pickup, pickup_pos, _ = min(
                own_candidates,
                key=lambda item: (item[1].distance_squared(enemy_core), item[0]),
            )
            destination = self._launcher_destination(
                ct,
                launcher_pos,
                pickup_pos,
                own_core,
                enemy_core,
                enemy=False,
            )
            if destination is not None and ct.can_launch(pickup_pos, destination):
                ct.launch(pickup_pos, destination)
        except Exception:
            return

    def _launcher_destination(
        self,
        ct: Controller,
        launcher_pos: Position,
        pickup: Position,
        own_core: Position | None,
        enemy_core: Position | None,
        *,
        enemy: bool,
    ) -> Position | None:
        """Choose a bounded strict-progress destination without tile guesses."""
        if enemy and own_core is None:
            return None
        if not enemy and enemy_core is None:
            return None
        candidates: list[tuple[int, int, int, Position]] = []
        for dy in range(-5, 6):
            for dx in range(-5, 6):
                if dx * dx + dy * dy > 26 or (dx == 0 and dy == 0):
                    continue
                target = Position(launcher_pos.x + dx, launcher_pos.y + dy)
                if not in_bounds(ct, target):
                    continue
                if target == pickup:
                    continue
                if enemy:
                    assert own_core is not None
                    before = pickup.distance_squared(own_core)
                    after = target.distance_squared(own_core)
                    if after <= before:
                        continue
                    # Prefer the farthest legal ejection, then deterministic
                    # coordinates.  can_launch is the occupancy authority.
                    candidates.append((after, -target.y, -target.x, target))
                else:
                    assert enemy_core is not None
                    before = pickup.distance_squared(enemy_core)
                    after = target.distance_squared(enemy_core)
                    if after >= before:
                        continue
                    candidates.append((-after, -target.y, -target.x, target))
        if not candidates:
            return None
        candidates.sort(reverse=True)
        for _, _, _, target in candidates:
            try:
                if ct.can_launch(pickup, target):
                    return target
            except Exception:
                continue
        return None

    # ------------------------------------------------------------------
    # Builder bot — role dispatch
    # ------------------------------------------------------------------

    def _run_builder(self, ct: Controller) -> None:
        if self.core_pos is None:
            self._read_core_pos(ct)

        if self.role is None:
            # Defer the role decision by one round after spawning: a store
            # write the core makes the same round it spawns us (e.g. this
            # id being SLOT_PERMA_ATTACKER_ID) isn't visible until next
            # round — see the note in constants.py — so deciding immediately
            # could permanently miss that designation. The delay is harmless;
            # we just do nothing else this first round either.
            if self.spawn_round is None:
                self.spawn_round = ct.get_current_round()
            if ct.get_current_round() <= self.spawn_round:
                return
            self._assign_role(ct)

        # Survival first: if we're standing in a visible enemy turret's line of
        # fire, disengage immediately — building/moving/fighting is worthless
        # if the bot dies next round. Skips the rest of the turn (build/move/
        # fire are mutually exclusive anyway) unless we're fully boxed in with
        # no escape, in which case we fall through to normal behaviour.
        danger = self._danger_tiles(ct)
        if ct.get_position() in danger:
            if self._navigate(ct, None, avoid=danger, flee=True) is not None:
                self._share_ore(ct)
                return

        # Then the core: if we are standing next to it and it is hurt, healing
        # it outranks every role's own agenda. This is role-independent on
        # purpose — whichever builder happens to be home is the one that has
        # to do it, and in the losses that motivated this the builders that
        # were home were defenders and attackers passing through, not the
        # dynamic pool that owns TASK_BASE_REPAIR.
        if self._heal_core(ct):
            self._share_ore(ct)
            return

        # ...and if we're NOT next to it but the core says it's being ground
        # down, go there. The opportunistic version above was the whole
        # response until now, and it is not a response: across five losses our
        # core absorbed 3,572 damage and we healed 1,034 of it, twice healing
        # none at all, because nobody was ever asked to walk home. See
        # CORE_SIEGE_HP and core_role._publish_siege.
        if self._answer_siege(ct, danger):
            self._share_ore(ct)
            return

        # A seeded hijack route outranks the attacker's normal agenda. The
        # first conveyor has already claimed an enemy Harvester's output; the
        # only useful next action is to finish routing it to our Core.
        if self.mode == MODE_CHAIN and self.route_seed is not None:
            self._run_seeded_route(ct, danger)
            self._share_ore(ct)
            return

        if self.role == ROLE_ATTACKER:
            self._run_attacker(ct, danger)
        elif self.role == ROLE_DYNAMIC:
            self._run_dynamic(ct, danger)
        else:
            self._run_defender(ct, danger)
        self._idle_fallback(ct, danger)
        self._share_ore(ct)

    def _heal_core(self, ct: Controller) -> bool:
        """Heal our own core if it is damaged and orthogonally adjacent.

        The exchange rates decide this one. Healing is 4 HP per titanium;
        a builder's attack is 2 damage per 2 titanium, i.e. 1 HP per
        titanium, and an enemy sentinel shot converts 10 of THEIR titanium
        into 18 damage. So a builder standing at the core turns titanium
        into effective core HP four times faster by repairing than by
        punching whatever is shooting at it, and more than twice as fast as
        the attacker can undo.

        The 21 ladder replays are unambiguous about it being worth doing:
        our core was healed for 510 HP across all of them (zero in 13 of the
        21 games) while enemy cores absorbed 13,856 damage from us and were
        healed for 9,352 — they routinely survived three times a core's
        worth of damage, and we never survived one.

        Returns True if it healed, meaning the turn is spent.
        """
        core = self.core_pos
        if core is None or ct.get_action_cooldown() != 0:
            return False
        # core_pos is the footprint anchor of a 2x2 building; can_heal takes
        # any orthogonally adjacent tile and heals every friendly entity on
        # it, so aim at whichever of the four covered tiles we are next to.
        pos = ct.get_position()
        for tile in core_footprint(core):
            if not adjacent(pos, tile):
                continue
            try:
                if ct.can_heal(tile):
                    ct.heal(tile)
                    return True
            except GameError:
                continue
        return False

    def _idle_fallback(self, ct: Controller, danger: set[Position]) -> None:
        """Last resort for a turn that would otherwise be discarded outright.

        This runs for EVERY role, after that role has had its say, and only
        when both cooldowns are still clear — i.e. only on turns the bot was
        about to throw away. Nothing here can therefore cost us a better
        action; the alternative to each of these is literally nothing.

        Measured on the fixed bot over a 66-game sweep: **46% of all ready
        builder turns were wasted** (the baseline was 53%), against 0-4% for
        the team that beat us five times. Crucially it is NOT poverty — the
        idle rate is 42-49% at every titanium balance, and 60% of those turns
        happened with 60+ Ti banked. It is builders with nothing left in
        their repertoire. Instrumenting every wasted turn by role attributed
        86% of them to three dead ends, all the same shape:

           41%  ATTACKER travelling: _run_attacker navigates and RETURNS, so
                a _navigate that can't improve (enemy turret fire lines seal
                the approach) idles the turn, and _attacker_fallback is never
                even reached on that path.
           29%  DYNAMIC holding TASK_HOME_THREAT: already inside
                COUNTER_TURRET_RANGE_SQ, no legal counter-turret tile outside
                the enemy's fire line, and "close in" can't improve either —
                so it stands there for up to TASK_MAX_ROUNDS (40) rounds.
           16%  DEFENDER scouting: same failure, no ore reachable.

        The common cause is that every role treats "_navigate returned None"
        as "nothing to do" rather than as "try something else", so the escape
        below is deliberately escalating and ends in a step that cannot fail
        for any reason short of being physically walled in.
        """
        if ct.get_action_cooldown() != 0 or ct.get_move_cooldown() != 0:
            return  # already acted or moved this turn — not a wasted one

        pos = ct.get_position()
        team = ct.get_team()

        # --- Actions, cheapest-per-titanium first ---------------------------
        # A core-ring gap we're already touching is 3 Ti that unlocks every
        # future delivery (see defender._try_build_core_ring).
        if self._try_build_core_ring(ct):
            return

        neighbours = []
        for d in DIRECTIONS:
            if not d.is_cardinal():
                continue
            n = pos.add(d)
            if not in_bounds(ct, n) or not ct.is_in_vision(n):
                continue
            neighbours.append((n, ct.get_tile_building_id(n)))

        try:
            # Heal a damaged friendly: 1 Ti for 4 HP, the best rate in the game.
            for n, bid in neighbours:
                if bid is None or ct.get_team(bid) != team:
                    continue
                if ct.get_hp(bid) < ct.get_max_hp(bid) and ct.can_heal(n):
                    ct.heal(n)
                    return
            # Bare ore we happen to be standing next to.
            for n, bid in neighbours:
                if bid is not None or ct.get_tile_env(n) != Environment.ORE_TITANIUM:
                    continue
                if self._would_sever_belt(ct, n):
                    continue
                if ct.can_build_harvester(n):
                    ct.build_harvester(n)
                    return
            # Chip an adjacent enemy building only from genuine surplus. This
            # is a poor 1 HP/Ti trade and must not consume route capital.
            if ct.get_global_resources() >= IDLE_ATTACK_RESERVE:
                for n, bid in neighbours:
                    if bid is None or ct.get_team(bid) == team:
                        continue
                    if ct.can_fire(n):
                        ct.fire(n)
                        return
        except GameError:
            pass

        # --- Movement, escalating until something works ---------------------
        # A chain in progress owes a conveyor to a specific vacated tile with
        # a specific facing, so wandering off would strand it. Leave that one
        # case alone — it was only 3% of the waste anyway.
        if self.mode == MODE_CHAIN and self.chain_pending is not None:
            return

        goal = self.task_target or self.target or self.enemy_core_known or self.core_pos
        if goal is not None and self._navigate(ct, goal, avoid=danger) is not None:
            return
        # Same goal, but no longer refusing to cross a turret's fire line.
        # Crossing one risks 18 damage; standing still for 40 rounds is a
        # certainty of contributing nothing, which is the worse deal.
        if goal is not None and self._navigate(ct, goal) is not None:
            return
        if self._navigate(ct, self._far_explore_target(ct)) is not None:
            return
        # Nothing above could improve on standing here. Take ANY legal step,
        # preferring ground we've trodden least — a builder that moves brings
        # new tiles into vision, and a builder that doesn't cannot.
        best = None
        best_visits = None
        for d in CARDINALS:
            n = pos.add(d)
            if not in_bounds(ct, n) or n in danger or not ct.can_move(d):
                continue
            v = self.visited.get(n, 0)
            if best_visits is None or v < best_visits:
                best_visits = v
                best = d
        if best is not None:
            ct.move(best)
            self.visited[pos.add(best)] = self.visited.get(pos.add(best), 0) + 1

    def _answer_siege(self, ct: Controller, danger: set[Position]) -> bool:
        """Walk home when the core is being ground down, and deal with the
        thing grinding it. Returns True if this turn is spent on that.

        Two responses, and the cheap one comes first:

        1. **Heal.** 1 Ti buys 4 core HP; an enemy sentinel spends 10 ammo to
           deal 18 damage every 2 rounds. One builder standing at the core
           therefore neutralises nearly half a besieging sentinel for ~1
           Ti/round, and two neutralise it outright. This is the single best
           titanium-to-survival rate available to us and we were not using it.

        2. **Remove the cause,** if the core told us where it is. Worth doing
           because a SENTINEL CANNOT ROTATE — its fire line is fixed the moment
           it is built — so a builder that approaches from off that line is in
           no danger at all, and `_navigate(avoid=danger)` already refuses to
           route through the line. 15 rounds of builder-fire (30 Ti) then
           removes it permanently. That is a very different trade from the one
           COUNTER_TURRET_RANGE_SQ was written for, which assumed a gunner
           that can turn around and shoot back.

        Who answers is deliberately graded, so a beacon can't empty the map:
        attackers ignore it (they are the offense, and a besieged core is
        often exactly when their pressure matters most) and a builder in the
        middle of laying a chain finishes it, unless the core is in real
        crisis — at which point stranded conveyors are the cheaper loss.
        """
        if self.core_pos is None:
            return False
        packed = ct.read_store(SLOT_CORE_SIEGE)
        if packed == 0:
            return False
        missing = packed // SIEGE_HP_SHIFT
        if missing < CORE_SIEGE_HP:
            return False
        if ct.get_global_resources() < 2:
            return False  # can afford neither a heal (1 Ti) nor a punch (2 Ti)
        crisis = missing >= CORE_SIEGE_CRISIS_HP
        if self.role == ROLE_ATTACKER and not crisis:
            return False
        if self.mode == MODE_CHAIN and not crisis:
            return False
        pos = ct.get_position()
        if pos.distance_squared(self.core_pos) > CORE_SIEGE_RECALL_SQ:
            return False

        # Which of the two responses is this builder's? Whichever it is already
        # closer to. That splits the team the way we want without any
        # coordination: builders caught out in the field intercept the turret,
        # builders near home stay and repair — and it degrades correctly to
        # "everyone heals" when the core never reports a turret at all.
        turret = unpack_pos(packed % SIEGE_HP_SHIFT)
        if turret is not None and pos.distance_squared(turret) < pos.distance_squared(self.core_pos):
            if adjacent(pos, turret):
                if ct.get_action_cooldown() == 0 and ct.get_global_resources() >= 2 and ct.can_fire(turret):
                    ct.fire(turret)
                return True  # in position; don't wander off just because we're on cooldown
            if ct.get_move_cooldown() == 0 and self._navigate(ct, turret, avoid=danger) is not None:
                return True
            return False

        # Head home. _heal_core (checked before us every round) takes over the
        # moment we're adjacent to the core, so the destination is the core
        # itself and arriving is the whole job.
        if ct.get_move_cooldown() == 0 and self._navigate(ct, self.core_pos, avoid=danger) is not None:
            return True
        return False

    def _assign_role(self, ct: Controller) -> None:
        """Decide this builder's role once, for life.

        Three builders hold fixed floor roles, all designated once by the core
        in core_role.py: the first builder ever spawned and the first builder
        of the stage-2 wave are permanent ATTACKERs, and the second builder
        ever spawned is the permanent DEFENDER. Everyone else is DYNAMIC and
        re-picks a *task* every time it's between tasks (see dynamic.py).

        The floors are deliberately fixed designations rather than something
        the greedy pool is trusted to maintain: a greedy rule only holds a
        floor probabilistically (nothing stops every dynamic builder chasing
        the same urgent thing at once), and verifying it centrally would need
        vision-limited counting. See DESIGN_dynamic_builders.md.
        """
        my_id = ct.get_id()
        if my_id in (ct.read_store(SLOT_PERMA_ATTACKER_ID), ct.read_store(SLOT_SECOND_ATTACKER_ID)):
            self.role = ROLE_ATTACKER
        elif my_id == ct.read_store(SLOT_PERMA_DEFENDER_ID):
            self.role = ROLE_DEFENDER
        elif ct.read_store(SLOT_HARVESTER_COUNT) == 0:
            # Until the first route has actually delivered, turn every
            # non-attacker in the opening workforce into an economy floor.
            # A dynamic worker can otherwise spend its early turns on ring
            # repair/advance tasks while no paying route exists; this fallback
            # keeps a second defender exploring and chaining until income is
            # proven. Builders spawned after the first delivery remain dynamic.
            self.role = ROLE_DEFENDER
        else:
            self.role = ROLE_DYNAMIC

    def _read_core_pos(self, ct: Controller) -> None:
        """Read the core position the core publishes each round.

        Both slots are stored with a +1 OFFSET (core_role._run_core writes
        them that way), for the same reason util.pack_pos offsets: an empty
        store slot reads as 0, so a raw 0 is ambiguous between "no data yet"
        and "the coordinate really is 0".

        That ambiguity was a total economy failure, not a nuisance. A core at
        (0, 0) published x=0, y=0, the old `if x > 0 or y > 0` guard read that
        as "not published yet", and self.core_pos stayed None for the whole
        match on every builder. Everything downstream is gated on it:
        _run_chain bails immediately when core is None, so NOT ONE CONVEYOR
        was ever laid; _try_build_core_ring and _find_core_ring_gap both
        return early; and _harvestable loses its range limit, so builders
        wandered off planting unconnectable harvesters. Measured on jackpot:
        39 harvesters built over 1000 rounds, zero conveyors, zero titanium
        delivered.

        Three pool maps put team A's core at (0, 0) — jackpot, sweden, vase.
        Combined with the separate spawn-ring bug (util.core_spawn_ring),
        those were unconditional losses from round 0.
        """
        x = ct.read_store(SLOT_CORE_X)
        y = ct.read_store(SLOT_CORE_Y)
        if x > 0 and y > 0:
            self.core_pos = Position(x - 1, y - 1)
            w, h = ct.get_map_width(), ct.get_map_height()
            self.harvest_range = max(8, int((w + h) * HARVEST_RANGE_FRAC))

    # ------------------------------------------------------------------
    # Gunner
    # ------------------------------------------------------------------

    def _run_gunner(self, ct: Controller) -> None:
        """Fire at the nearest thing in our facing line, if we have ammo —
        and if there's nothing to hit there, rotate to face the nearest
        enemy we can actually line up on, so we're ready to fire next round.

        A gunner is a facing weapon: get_gunner_target() only ever reports
        something along the single direction we're currently pointed, chosen
        once at build time and never revisited. Without ever rotating, a
        turret is completely blind to a threat approaching from any other
        angle — including a builder bot attacking it at point-blank range
        from the "wrong" side, which was the first symptom reported (turrets
        taking damage and never firing back).

        Naively rotating toward a generic directional helper looks right but
        usually isn't: that just rounds to the nearest 45° compass direction,
        which only happens to be exact when the threat is orthogonally
        adjacent (adjacency forces exact alignment by construction). Anything
        farther away is almost never sitting exactly on one of our 8 firing
        lines, so rotating to the "roughly right" direction still never
        connects — which was the second symptom (turrets only ever engaging
        point-blank despite having real range). can_fire_from() is the
        engine's own alignment check (ignores ammo/cooldown, just geometry),
        so we search actual candidate directions against it instead of
        guessing.

        Rotating costs an action (10 Ti, 1 round cooldown, same as reload),
        so this alternates rotate/fire against a stationary threat.

        get_gunner_target() also returns the closest *occupied* tile in the
        line regardless of team — it does not filter friend from foe
        (confirmed in the engine's own Controller stub) — so a turret left
        unchecked will happily gun down a friendly harvester or conveyor that
        ends up in its fire line later (e.g. built after the turret, along
        the same cardinal). We skip firing outright when the nearest thing is
        ours; the line only ever reports that one nearest tile, so whatever
        might be behind it isn't a reachable target this turn anyway.
        """
        target = ct.get_gunner_target()
        if target is not None and not self._is_friendly_tile(ct, target):
            if ct.can_fire(target):
                ct.fire(target)
            return

        if ct.get_action_cooldown() != 0:
            return
        facing = self._best_rotate_facing(ct)
        if facing is not None and facing != ct.get_direction() and ct.can_rotate(facing):
            ct.rotate(facing)

    def _best_rotate_facing(self, ct: Controller) -> Direction | None:
        """Nearest visible enemy first, then the first of our 8 facings that
        can_fire_from confirms would actually line up on it. Skips enemies no
        facing can reach (out of range or unalignable) in favour of a farther
        one we could actually hit.
        """
        team = ct.get_team()
        pos = ct.get_position()
        etype = ct.get_entity_type()
        candidates: list[Position] = []
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) != team:
                candidates.append(ct.get_position(bid))
        for uid in ct.get_nearby_units():
            if ct.get_team(uid) != team:
                candidates.append(ct.get_position(uid))
        candidates.sort(key=lambda p: pos.distance_squared(p))
        for enemy_pos in candidates:
            for d in DIRECTIONS:
                if ct.can_fire_from(pos, d, etype, enemy_pos):
                    return d
        return None

    def _is_friendly_tile(self, ct: Controller, pos: Position) -> bool:
        team = ct.get_team()
        bid = ct.get_tile_building_id(pos)
        if bid is not None:
            return ct.get_team(bid) == team
        bot_id = ct.get_tile_builder_bot_id(pos)
        if bot_id is not None:
            return ct.get_team(bot_id) == team
        return False

    # ------------------------------------------------------------------
    # Sentinel
    # ------------------------------------------------------------------

    def _run_sentinel(self, ct: Controller) -> None:
        """Fire at the nearest enemy in our line, if any — and that's it.

        Unlike a gunner, a sentinel has no rotate()/can_rotate() support at
        all (confirmed in the engine's own Controller stub: rotate is
        documented "Gunner-only"). Its facing is permanent from the moment
        it's built, so there's no reactive behaviour to add here — all the
        actual work is in attacker.py's _try_build_sentinel, which searches
        for a placement that's verified (via can_fire_from) to line up on
        the enemy core before ever committing to one.
        """
        target = self._find_sentinel_target(ct)
        if target is not None and ct.can_fire(target):
            ct.fire(target)

    def _find_sentinel_target(self, ct: Controller) -> Position | None:
        """Nearest enemy-occupied tile in our (fixed) attack pattern.

        get_gunner_target() is gunner-only per the engine stub, so we build
        the equivalent ourselves from get_attackable_tiles() — which does
        work generically for any turret — checking both buildings and
        builder bots per tile, since a conveyor/splitter tile can host both
        a building and a builder bot standing on it at once.
        """
        team = ct.get_team()
        pos = ct.get_position()
        tiles = sorted(ct.get_attackable_tiles(), key=lambda t: pos.distance_squared(t))
        for tile in tiles:
            bid = ct.get_tile_building_id(tile)
            if bid is not None and ct.get_team(bid) != team:
                return tile
            bot_id = ct.get_tile_builder_bot_id(tile)
            if bot_id is not None and ct.get_team(bot_id) != team:
                return tile
        return None
