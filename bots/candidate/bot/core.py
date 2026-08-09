from __future__ import annotations

from dataclasses import dataclass, field

from fcode import EntityType, Environment, Position, Team

from .actions import TurnActions
from .comms import (
    SCHEMA_VERSION,
    Slot,
    claim_is_fresh,
    claim_slot,
    decode_defense_alert,
    decode_rally,
    encode_budget,
    encode_defense_alert,
    encode_epoch_pulse,
    encode_strategy,
    pack_claim,
    unpack_claim,
)
from .policy import assign_role, choose_opening, describe_opening
from .types import Budget, Opening, Phase, Scenario, ThreatKind

# Current documented non-scaled rules. Scaled construction prices are always
# queried through Controller cost getters; these values are fallback-only.
BASE_BUILDER_COST = 30
BASE_HARVESTER_COST = 20
BASE_CONVEYOR_COST = 3
BASE_GUNNER_COST = 20
BASE_SENTINEL_COST = 30
CORE_SPAWN_RADIUS_SQ = 2
MAX_TEAM_UNITS = 50
MAX_MATCH_AMMO_CONVERSION = 640  # non-terminal safety cap; terminal Core assaults may exceed it


PROJECT_STATUS_SLOTS = (
    Slot.PRIMARY_ORE,
    Slot.LOGISTICS,
    Slot.THREAT,
    Slot.ENEMY_CORE,
)


@dataclass(slots=True)
class CoreState:
    opening: Opening = Opening.BALANCED_ECONOMY
    phase: Phase = Phase.OPENING
    claim_owners: dict[int, int] = field(default_factory=dict)
    schema_written: bool = False
    last_budget: Budget = field(default_factory=Budget)
    spawn_cursor: int = 0
    opening_observed_round: int | None = None
    cached_descriptor: object | None = None
    route_target: int = 0
    route_capacity: int = 4
    scenario: Scenario = Scenario.STANDARD
    best_claimed_ore: int = 0
    best_active_projects: int = 0
    best_maintaining_routes: int = 0
    last_claimed_ore: int = 0
    last_active_projects: int = 0
    last_maintaining_routes: int = 0
    last_route_progress_round: int = 0
    offense_committed: bool = False
    ammo_converted_total: int = 0
    last_builder_spawn_round: int = -999
    last_route_capacity_expand_round: int = -999
    last_core_hp: int | None = None


def _get(ct: object, name: str, default: int = 0) -> int:
    try:
        return int(getattr(ct, name)())
    except (AttributeError, TypeError, ValueError):
        return default
    except Exception:
        return default


def _cost(ct: object, name: str, default: int) -> int:
    return max(0, _get(ct, name, default))


def _cpu_safe(ct: object) -> bool:
    try:
        return int(ct.get_cpu_time_elapsed()) < 7000
    except Exception:
        return True


def compute_budget(
    ct: object,
    *,
    route_projects: int = 0,
    maintaining_routes: int = 0,
    phase: Phase = Phase.ECONOMY,
) -> Budget:
    """Reserve the next economic step before any optional combat spend.

    Economy is a permanent background process, not a phase that can be completed.
    Every macro state protects one Harvester plus a useful Conveyor segment. Live
    unfinished primary projects may raise that reserve, but OFFENSE/ENDGAME never
    zero it. Defense receives a separate envelope only when a real DEFENSE phase
    has been triggered by a fresh threat.
    """
    resources = _get(ct, "get_global_resources", 0)
    harvester = _cost(ct, "get_harvester_cost", BASE_HARVESTER_COST)
    conveyor = _cost(ct, "get_conveyor_cost", BASE_CONVEYOR_COST)
    gunner = _cost(ct, "get_gunner_cost", BASE_GUNNER_COST)
    sentinel = _cost(ct, "get_sentinel_cost", BASE_SENTINEL_COST)

    projects = max(0, min(4, int(route_projects)))
    maintained = max(0, min(projects, int(maintaining_routes)))
    unfinished = max(0, projects - maintained)

    # One future producer is always protected. Six links is deliberately a
    # rolling construction seed rather than a prepaid full route: existing
    # Harvesters keep earning while a pioneer walks/builds the rest.
    next_seed = harvester + 6 * conveyor
    unfinished_seed = (
        harvester + min(18, 6 + 4 * unfinished) * conveyor
        if unfinished
        else 0
    )
    construction = max(next_seed, unfinished_seed)

    # No standing-defense tax. A real alarm changes the phase to DEFENSE, at
    # which point reserve enough for one useful turret and a compact magazine.
    if phase == Phase.DEFENSE:
        defense = min(max(gunner, sentinel), max(0, resources // 5))
        ammo = min(24, max(0, resources // 10))
    else:
        defense = 0
        ammo = 0

    # Small liquid floor for repairs / action costs. The economic seed above is
    # the real strategic reserve, so do not double-reserve another Harvester.
    liquidity = 20
    expansion = max(0, resources - construction - defense - ammo - liquidity)
    return Budget(construction, defense, ammo, expansion, liquidity)


def _write_store(ct: object, slot: Slot, value: int) -> None:
    try:
        ct.write_store(int(slot), max(0, min(0xFFFFFFFF, int(value))))
    except Exception:
        pass


_TEAM_A_OPENING_GEOMETRIES = frozenset({(26, 26), (21, 8)})
_TEAM_B_OPENING_GEOMETRIES = frozenset(
    {(14, 18), (18, 18), (10, 10), (25, 15), (20, 26), (24, 24)}
)


def _opening_position_key(ct: object, position: Position) -> tuple[int, int]:
    """Canonical tie-break matching the stronger orientation for this geometry.

    The live pool is rotationally symmetric, but absolute ``(y, x)`` ties make
    the two starts choose different spawn/ore lanes.  For geometries whose local
    control profile has a consistent orientation winner, rotate only the weaker
    side's equal-score choices by 180 degrees.  Ambiguous geometries retain the
    baseline order.
    """
    try:
        geometry = (int(ct.get_map_width()), int(ct.get_map_height()))
        team = ct.get_team()
        origin = ct.get_position()
    except Exception:
        return position.y, position.x
    if geometry == (16, 16):
        # The legacy cross-corner arena and the current same-corner arenas share
        # dimensions but have opposite strong orientations. Their Core quadrant
        # relation is locally observable and distinguishes the geometry without
        # a map-name lookup.
        cross_diagonal = (origin.x < 8) != (origin.y < 8)
        preferred = Team.A if cross_diagonal else Team.B
    elif geometry == (25, 25):
        # The open same-quadrant geometry benefits from Team A's opening order;
        # the cross-diagonal geometry is seed-balanced under baseline behavior
        # and regresses when forcibly rotated.
        cross_diagonal = (origin.x < 12) != (origin.y < 12)
        preferred = None if cross_diagonal else Team.A
    else:
        preferred = (
            Team.A
            if geometry in _TEAM_A_OPENING_GEOMETRIES
            else Team.B
            if geometry in _TEAM_B_OPENING_GEOMETRIES
            else None
        )
    if preferred is not None and team != preferred:
        width, height = geometry
        return height - 1 - position.y, width - 1 - position.x
    return position.y, position.x


def _spawn_positions(ct: object) -> tuple[Position, ...]:
    try:
        positions = tuple(ct.get_nearby_tiles(dist_sq=CORE_SPAWN_RADIUS_SQ))
    except Exception:
        return ()
    return tuple(sorted(positions, key=lambda pos: _opening_position_key(ct, pos)))


def _core_builder_congestion(ct: object) -> int:
    """Count unique friendly Builders occupying the Core exit neighbourhood."""
    try:
        from fcode import Direction
        cardinals = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
        cells = set(_spawn_positions(ct))
        for cell in tuple(cells):
            for direction in cardinals:
                cells.add(cell.add(direction))
        builder_ids: set[int] = set()
        for cell in cells:
            try:
                builder_id = ct.get_tile_builder_bot_id(cell)
            except Exception:
                continue
            if builder_id is not None:
                builder_ids.add(int(builder_id))
        return min(15, len(builder_ids))
    except Exception:
        return 0


def _spawn_lane_score(
    ct: object,
    position: Position,
    *,
    target: Position | None = None,
) -> tuple[int, int, int, int, int]:
    """Prefer spawn cells that open into traffic-free lanes.

    The Core has real local vision, so it can avoid creating a Builder directly
    behind another Builder even though the rest of the map is partially known.
    Route owners still bias toward their ore target; generic workers prioritize
    exit freedom and low nearby Builder density.
    """
    from fcode import Direction
    cardinals = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
    freedom = 0
    congestion = 0
    for direction in cardinals:
        neighbour = position.add(direction)
        try:
            builder_id = ct.get_tile_builder_bot_id(neighbour)
        except Exception:
            builder_id = None
        if builder_id is not None:
            congestion += 1
            continue
        try:
            if ct.is_tile_passable(neighbour):
                freedom += 1
        except Exception:
            continue
    target_distance = (
        abs(position.x - target.x) + abs(position.y - target.y)
        if target is not None
        else 0
    )
    # Route-target distance is primary only for a real newly assigned owner.
    # Otherwise leave a clear exit lane before caring about coordinate order.
    tie_y, tie_x = _opening_position_key(ct, position)
    if target is not None:
        return (target_distance, congestion, -freedom, tie_y, tie_x)
    return (congestion, -freedom, target_distance, tie_y, tie_x)


def _observed_opening(ct: object):
    width = _get(ct, "get_map_width", 1)
    height = _get(ct, "get_map_height", 1)
    try:
        origin = ct.get_position()
        tiles = tuple(ct.get_nearby_tiles())[:256]
    except Exception:
        origin, tiles = Position(0, 0), ()
    walls: set[Position] = set()
    ore: list[Position] = []
    passable: set[Position] = set()
    for tile in tiles:
        if not _cpu_safe(ct):
            break
        try:
            environment = ct.get_tile_env(tile)
            if environment == Environment.WALL:
                walls.add(tile)
            elif environment == Environment.ORE_TITANIUM:
                ore.append(tile)
            if ct.is_tile_passable(tile):
                passable.add(tile)
        except Exception:
            continue
    low_degree = 0
    exposed = 0
    from fcode import Direction

    cardinals = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
    for tile in tuple(sorted(passable, key=lambda pos: (pos.y, pos.x))):
        if not _cpu_safe(ct):
            break
        neighbours = tuple(tile.add(direction) for direction in cardinals)
        degree = sum(neighbour in passable for neighbour in neighbours)
        low_degree += degree <= 1
        exposed += any(neighbour in walls for neighbour in neighbours)
    enemy_distance = 999
    try:
        own_team = ct.get_team()
        for entity_id in tuple(ct.get_nearby_buildings())[:64]:
            if not _cpu_safe(ct):
                break
            if ct.get_entity_type(entity_id) == EntityType.CORE and ct.get_team(entity_id) != own_team:
                position = ct.get_position(entity_id)
                enemy_distance = min(
                    enemy_distance,
                    abs(position.x - origin.x) + abs(position.y - origin.y),
                )
    except Exception:
        pass
    return describe_opening(
        width,
        height,
        nearby_ore_count=len(ore),
        nearest_ore_distance=min(
            (abs(position.x - origin.x) + abs(position.y - origin.y) for position in ore),
            default=999,
        ),
        wall_density=len(walls) / max(1, len(tiles)),
        low_degree_passable_tiles=low_degree,
        route_exposure=exposed / max(1, len(passable)),
        estimated_enemy_distance=enemy_distance,
    )


def _route_target(opening: Opening, area: int) -> int:
    """Four Store-backed producers are the universal primary-economy target.

    Map size and enemy proximity may change *when combat starts*, but never lower
    the economic objective. Reactive defense can interrupt a Builder locally; it
    does not redefine a small map as a two-Harvester game.
    """
    del opening, area
    return 4


def _fresh_claims(ct: object, width: int, height: int, round_no: int, limit: int):
    result = []
    for index in range(max(0, min(4, int(limit)))):
        try:
            claim = unpack_claim(ct.read_store(int(claim_slot(index))), width, height)
        except Exception:
            claim = None
        if claim is not None and claim_is_fresh(claim, round_no & 63):
            result.append((index, claim))
    return result


def _synchronize_claim_owners(
    ct: object,
    state: CoreState,
    width: int,
    height: int,
    round_no: int,
) -> None:
    fresh = dict(_fresh_claims(ct, width, height, round_no, state.route_capacity))
    for index in range(4):
        claim = fresh.get(index) if index < state.route_capacity else None
        if claim is None:
            state.claim_owners.pop(index, None)
        else:
            state.claim_owners[index] = claim.owner_id


def _project_counts(ct: object, claims, round_no: int) -> tuple[int, int, int]:
    active = maintain = producer_ready = 0
    claim_by_index = dict(claims)
    for index, slot in enumerate(PROJECT_STATUS_SLOTS):
        claim = claim_by_index.get(index)
        if claim is None:
            continue
        try:
            value = int(ct.read_store(int(slot)))
        except Exception:
            continue
        owner = value >> 8
        epoch = (value >> 2) & 63
        status = value & 3
        if owner != claim.owner_id or ((round_no & 63) - epoch) & 63 > 12:
            continue
        active += status >= 1
        maintain += status == 2
        producer_ready += status == 3
    return active, maintain, producer_ready


def _fresh_defense_alert(
    ct: object,
    width: int,
    height: int,
    round_no: int,
) -> tuple[Position | None, int]:
    try:
        decoded = decode_defense_alert(
            ct.read_store(int(Slot.DEFENSE_ALERT)), width, height
        )
    except Exception:
        return None, 0
    if decoded is None:
        return None, 0
    position, expires, severity, _kind = decoded
    if position is None:
        return None, 0
    forward = (int(expires) - (round_no & 63)) & 63
    return (position, max(1, int(severity))) if forward <= 12 else (None, 0)


def _local_core_threat(ct: object, area: int) -> tuple[Position | None, int, ThreatKind]:
    """Return the most dangerous visible hostile around the Core.

    The Core publishes this itself so a long-range attacker cannot rely on a
    one-round Builder report delay. The exact hostile position is more useful
    than publishing the Core tile: remote responders travel toward the shooter.
    """
    try:
        own_team = ct.get_team()
        origin = ct.get_position()
        ids = tuple(ct.get_nearby_units())[:48] + tuple(ct.get_nearby_buildings())[:96]
    except Exception:
        return None, 0, ThreatKind.UNKNOWN
    compact = int(area) <= 196
    builder_limit = 81 if compact else 49
    structure_limit = 121 if compact else 100
    best: tuple[int, int, Position, ThreatKind] | None = None
    seen: set[int] = set()
    for entity_id in ids:
        try:
            entity_id = int(entity_id)
            if entity_id in seen or ct.get_team(entity_id) == own_team:
                continue
            seen.add(entity_id)
            entity_type = ct.get_entity_type(entity_id)
            position = ct.get_position(entity_id)
            distance = origin.distance_squared(position)
        except Exception:
            continue
        severity = 0
        kind = ThreatKind.UNKNOWN
        if entity_type == EntityType.BUILDER_BOT and distance <= builder_limit:
            severity = 15 if distance <= 25 else 12
            kind = ThreatKind.BUILDER_RUSH
        elif entity_type in (EntityType.GUNNER, EntityType.SENTINEL) and distance <= structure_limit:
            severity = 15
            kind = ThreatKind.SENTINEL_FIRE if entity_type == EntityType.SENTINEL else ThreatKind.GUNNER_FIRE
        elif entity_type == EntityType.LAUNCHER and distance <= structure_limit:
            severity = 12
            kind = ThreatKind.FIRING_LINE
        if severity:
            candidate=(severity, -distance, position, kind)
            if best is None or candidate[:2] > best[:2]:
                best=candidate
    if best is None:
        return None, 0, ThreatKind.UNKNOWN
    return best[2], best[0], best[3]


def _visible_ore_positions(ct: object) -> tuple[Position, ...]:
    """Return ore currently visible to the Core, nearest first."""
    try:
        origin = ct.get_position()
        tiles = tuple(ct.get_nearby_tiles())[:256]
    except Exception:
        return ()
    ores: list[Position] = []
    for tile in tiles:
        if not _cpu_safe(ct):
            break
        try:
            if ct.get_tile_env(tile) != Environment.ORE_TITANIUM:
                continue
            if ct.get_tile_building_id(tile) is not None:
                continue
        except Exception:
            continue
        ores.append(tile)
    return tuple(
        sorted(
            set(ores),
            key=lambda position: (
                abs(position.x - origin.x) + abs(position.y - origin.y),
                *_opening_position_key(ct, position),
            ),
        )
    )


def _fresh_rally_priority(ct: object, width: int, height: int, round_no: int) -> int:
    try:
        decoded = decode_rally(ct.read_store(int(Slot.RALLY)), width, height)
    except Exception:
        return 0
    if decoded is None:
        return 0
    position, expires, priority = decoded
    if position is None:
        return 0
    forward = (int(expires) - (round_no & 63)) & 63
    # Core rallies are deliberately sticky on large maps: once the enemy Core is
    # found, losing vision for eight travel rounds must not dissolve the assault.
    horizon = 30 if int(priority) >= 15 else 8
    return int(priority) if forward <= horizon else 0


def _select_phase(
    round_no: int,
    *,
    fresh_claim_count: int,
    maintaining_routes: int,
    route_target: int,
    no_progress_rounds: int,
    workforce_ready: bool,
    defense_alert: bool,
    offense_committed: bool,
    attack_objective_priority: int = 0,
    opening: Opening = Opening.BALANCED_ECONOMY,
    area: int = 0,
) -> Phase:
    """Economy-first macro with combat as an interrupt/opportunity.

    Expansion is never a phase transition: route owners keep building in every
    phase. DEFENSE is entered for a real fresh alarm, OFFENSE for a verified
    valuable enemy objective (or a very late anti-timeout fallback), otherwise
    the team remains in the economy/map-control state.
    """
    del offense_committed, opening, area
    # A real attack is an interrupt at *any* round, including the endgame.
    if defense_alert:
        return Phase.DEFENSE
    # Confirming the enemy Core is qualitatively different from seeing another
    # conveyor. Once even one producer is stable, begin the assault immediately
    # while the permanent satellite/economy lane continues in parallel. This is
    # intentionally checked before the old round-60 opening gate: on compact maps
    # a Builder that physically reaches the Core has already solved localization.
    if attack_objective_priority >= 15 and maintaining_routes >= 1:
        return Phase.OFFENSE
    if round_no >= 850:
        return Phase.ENDGAME
    if fresh_claim_count == 0 or round_no < 60:
        return Phase.OPENING
    if maintaining_routes <= 0 or not workforce_ready:
        return Phase.ECONOMY
    if attack_objective_priority >= 11 and maintaining_routes >= min(2, route_target):
        return Phase.OFFENSE
    if round_no >= 700 and maintaining_routes >= 2:
        return Phase.OFFENSE
    return Phase.ECONOMY

def _operating_builder_floor(
    opening: Opening,
    area: int,
    route_target: int,
    nearby_ore_count: int = 0,
    nearest_ore_distance: int = 999,
) -> int:
    """Funded opening crew: enough parallelism to win ore without blind spam.

    v0043 over-corrected worker bloat by falling to 2/3 Builders on compact/medium
    maps. With one route owner that leaves only one or two independent discovery
    lanes, which is too slow to reveal and claim symmetric ore before an opponent.
    The spawn path still protects a complete first-producer seed, so this is a
    *target* crew rather than an unconditional purchase schedule.
    """
    del opening, route_target
    area = max(1, int(area))
    nearby_ore_count = max(0, int(nearby_ore_count))
    nearest_ore_distance = max(0, int(nearest_ore_distance))
    if area <= 196:
        crew, far_threshold = 3, 7
    elif area < 500:
        crew, far_threshold = 4, 9
    else:
        crew, far_threshold = 5, 12
    # Poor initial information earns exactly one extra survey lane.  Do not turn
    # enemy proximity into a speculative defender purchase: defense is reactive.
    if nearby_ore_count <= 0 or nearest_ore_distance > far_threshold:
        crew += 1
    return max(3, min(6, crew))

def _desired_builders(
    phase: Phase,
    opening: Opening,
    area: int,
    route_target: int,
    route_capacity: int | None = None,
    *,
    maintaining_routes: int = 0,
    active_projects: int = 0,
    attack_objective_priority: int = 0,
    defense_severity: int = 0,
    no_progress_rounds: int = 0,
    nearby_ore_count: int = 0,
    nearest_ore_distance: int = 999,
    resource_workers: int = 0,
) -> int:
    """Demand-driven workforce: fund economy first, then scale from surplus.

    The key accounting rule is that a completed primary-route owner is *already a
    mobile Builder*.  v0041 freed those units in the role system but still counted
    route owners, repairers and frontier workers as separate bodies here, which
    over-spawned compact maps.  This function counts concurrent jobs instead.

    ``resource_workers`` is cost-aware capacity backed by titanium left after the
    rolling Harvester/Conveyor reserve.  It is deliberately not a fixed map cap.
    """
    area = max(1, int(area))
    route_target = max(1, min(4, int(route_target)))
    route_capacity = route_target if route_capacity is None else max(1, min(4, int(route_capacity)))
    maintaining_routes = max(0, int(maintaining_routes))
    active_projects = max(0, int(active_projects))
    defense_severity = max(0, int(defense_severity))
    attack_objective_priority = max(0, int(attack_objective_priority))
    resource_workers = max(0, int(resource_workers))

    bootstrap = _operating_builder_floor(
        opening, area, route_target, nearby_ore_count, nearest_ore_distance
    )
    if maintaining_routes <= 0:
        # Before income, titanium belongs to the first producer.  A stalled map
        # can add one extra probe, but never a map-size-derived worker flood.
        floor = bootstrap + (1 if active_projects == 0 and no_progress_rounds >= 80 else 0)
        return min(6, floor)

    # Route owners and mobile specialists are concurrent jobs while the primary
    # network is still being laid.  Counting only route_capacity (v0043/v0044)
    # could leave every live Builder committed to a pipeline and silently erase
    # the scout/saboteur lane exactly when the opponent is racing for outer ore.
    # Keep two genuinely free information/frontier bodies after first income;
    # completed route owners are reusable, so this is still much leaner than one
    # permanent guard per Harvester.
    unfinished = max(0, route_capacity - maintaining_routes)
    mobile_frontier = 2  # persistent survey + sabotage lane
    economy_bodies = max(
        bootstrap,
        route_capacity + mobile_frontier,
        maintaining_routes + unfinished + mobile_frontier,
    )
    # Once the four primary channels exist, retain one additional claimless
    # satellite/capture pioneer.  It is the worker that turns new discoveries
    # into route 5/6/... while the scout and saboteur keep moving.
    if route_capacity >= 4:
        economy_bodies = max(economy_bodies, 7)

    # A genuinely stalled economy gets one more explorer even without a rich bank.
    if no_progress_rounds >= 120:
        economy_bodies += 1

    # Defense is purely reactive and represents concurrent work that cannot be
    # supplied by the same Builder currently laying a route.
    defenders = 0
    if defense_severity >= 10:
        defenders = 2 if area < 500 else 3
        if defense_severity >= 14:
            defenders += 1

    # Offense ramps with verified objectives while economy remains staffed.
    attackers = 0
    if maintaining_routes >= min(2, route_target) and defense_severity < 11:
        if attack_objective_priority >= 15:
            attackers = 4 if area <= 196 else (6 if area < 500 else 8)
        elif phase == Phase.ENDGAME:
            attackers = 2 if area <= 196 else (3 if area < 500 else 4)
        elif attack_objective_priority >= 13:
            attackers = 2 if area < 500 else 3
        elif attack_objective_priority >= 11:
            attackers = 1 if area <= 196 else 2

    # ``resource_workers`` is the only quiet-state growth term.  A compact map
    # with a poor treasury therefore stays lean; the same map can still build a
    # large army later if its Harvester network can actually pay for one.
    desired = economy_bodies + defenders + attackers + resource_workers
    return min(MAX_TEAM_UNITS - 1, max(bootstrap, desired))

def _trim_optional_route_capacity(state: CoreState) -> None:
    """Drop dead/unassigned expansion channels without touching required routes."""
    while state.route_capacity > state.route_target:
        index = state.route_capacity - 1
        if index in state.claim_owners:
            break
        state.route_capacity -= 1


def _maybe_open_expansion_route(
    ct: object,
    state: CoreState,
    *,
    round_no: int,
    maintaining_routes: int,
    active_projects: int,
    producer_ready_projects: int,
    attack_priority: int,
    defense_severity: int,
    budget: Budget,
) -> bool:
    """Keep filling the four reliable economy channels behind every strategy.

    ``route_target`` is only the *minimum income needed before pressure is allowed*.
    It is not an instruction to stop the economy at two or three Harvesters. Once
    the first line is delivering, the Core keeps promoting the remaining Store-
    backed channels with at most two unfinished pipelines. OFFENSE never disables
    this; only a critical home emergency briefly pauses new construction starts.
    """
    del attack_priority  # combat permission must not turn the economy off
    if state.route_capacity >= 4 or round_no >= 970:
        return False
    # Never stack empty route channels. A newly opened slot must receive a live
    # owner before another channel is released.
    if any(index not in state.claim_owners for index in range(state.route_capacity)):
        return False
    if producer_ready_projects > 0 or defense_severity >= 14:
        return False

    unfinished = max(0, int(active_projects) - int(maintaining_routes))
    if unfinished >= 2:
        return False

    area = int(getattr(state.cached_descriptor, "area", 0) or 0)
    resources = _get(ct, "get_global_resources", 0)
    builder = _cost(ct, "get_builder_bot_cost", BASE_BUILDER_COST)
    harvester = _cost(ct, "get_harvester_cost", BASE_HARVESTER_COST)
    conveyor = _cost(ct, "get_conveyor_cost", BASE_CONVEYOR_COST)

    # Rich medium/large openings may launch a second independent route before the
    # first producer ticks. v0041 already had construction logic for this but the
    # Core never opened slot 1, making that branch unreachable. Compact maps are
    # stricter: only an obviously rich bank can justify another pre-income body.
    if maintaining_routes <= 0:
        if state.route_capacity != 1 or active_projects < 1 or round_no < 3:
            return False
        extra_seed = builder + harvester + 6 * conveyor
        reserve = budget.construction + max(20, budget.liquidity) + budget.defense
        # A second *productive* route owner is more valuable than another generic
        # worker. Compact/medium maps therefore admit this parallel pipeline sooner
        # when cash really covers it, while still preserving the first-line seed.
        compact_cushion = 40 if area <= 196 else (15 if area < 500 else 10)
        if resources < reserve + extra_seed + compact_cushion:
            return False
        state.route_capacity += 1
        state.last_route_capacity_expand_round = round_no
        return True

    # After income, release channels quickly but never fragment more than two
    # unfinished pipelines. Route 4 still waits for two live producers.
    required_live = 1 if state.route_capacity <= 2 else 2
    if maintaining_routes < required_live:
        return False

    interval = 3 if area < 500 else 4
    if round_no - state.last_route_capacity_expand_round < interval:
        return False

    # Capacity is only a work slot. Do not pre-bind it to a guessed owner: the
    # normal spawn path below sees the missing slot and creates a confirmed-live
    # route owner, keeping ownership explicit after casualties.
    seed = builder + harvester + 4 * conveyor
    reserve = max(20, budget.liquidity) + budget.defense
    if resources < seed + reserve:
        return False

    state.route_capacity += 1
    state.last_route_capacity_expand_round = round_no
    return True

def _resource_backed_workers(
    ct: object,
    budget: Budget,
    *,
    maintaining_routes: int,
    defense_severity: int,
    round_no: int,
    terminal_assault: bool = False,
) -> int:
    """How many *optional* Builders the current treasury can genuinely fund.

    This replaces v0041's map-size caps and 0..3 richness tier.  The count grows
    naturally with titanium after the next Harvester/Conveyor seed is reserved.
    On a poor compact opening it is zero; if the economy later becomes rich the
    same compact map is free to field many workers.
    """
    if maintaining_routes < 1 or defense_severity >= 10:
        return 0
    resources = _get(ct, "get_global_resources", 0)
    builder = _cost(ct, "get_builder_bot_cost", BASE_BUILDER_COST)
    harvester = _cost(ct, "get_harvester_cost", BASE_HARVESTER_COST)
    conveyor = _cost(ct, "get_conveyor_cost", BASE_CONVEYOR_COST)
    spendable = max(0, resources - budget.reserved)
    if terminal_assault:
        # Once the enemy Core is confirmed, surplus workers are attack capacity.
        step = max(1, builder + 20)
        return max(0, spendable // step)

    # Optional bodies are still bought only from money *after* the rolling next
    # Harvester/Conveyor seed.  The marginal backing requirement falls as passive
    # producers come online: one-Harvester teams stay conservative, whereas a
    # 3/4-Harvester network should turn excess bank into many parallel expansion
    # and attack bodies instead of hoarding titanium.
    route_seed = harvester + 6 * conveyor
    if maintaining_routes <= 1:
        cushion = 70
        step = builder + route_seed + 20
    elif maintaining_routes == 2:
        cushion = 40
        step = builder + max(18, route_seed // 2) + 15
    elif maintaining_routes == 3:
        cushion = 25
        step = builder + max(14, route_seed // 3) + 10
    else:
        cushion = 15
        step = builder + max(10, route_seed // 4) + 8
    return max(0, (spendable - cushion) // max(1, step))

def _ammo_target(
    phase: Phase,
    maintaining_routes: int,
    scenario: Scenario = Scenario.STANDARD,
    *,
    attack_priority: int = 0,
    defense_severity: int = 0,
) -> int:
    """Buy ammunition in proportion to an actual firing job.

    v0019 pre-bought a full offensive magazine as soon as OFFENSE began, even
    when the enemy was still unlocalized and no turret had a useful target.
    That is exactly when titanium should stay liquid for another Harvester,
    repairs, or the next Builder.  Keep a small blind-assault magazine, then
    scale immediately once a combat structure / Harvester / Core objective is
    verified.
    """
    routes = max(0, int(maintaining_routes))
    priority = max(0, int(attack_priority))
    severity = max(0, int(defense_severity))
    if scenario == Scenario.ECONOMY_RESCUE:
        return 0
    if phase == Phase.DEFENSE or scenario == Scenario.CONTESTED:
        extra = 8 if severity >= 13 else (4 if severity >= 10 else 0)
        return min(48, 18 + 6 * routes + extra)
    if scenario == Scenario.EXPANSION:
        # Quiet expansion keeps titanium liquid. Ammo is bought only after a real
        # threat or a verified offensive objective exists.
        return 0
    if phase in (Phase.OFFENSE, Phase.ENDGAME) or scenario in (Scenario.SIEGE, Scenario.ENDGAME):
        if priority >= 15:
            # Confirmed Core: unused titanium should become real firing capacity.
            return min(320, 96 + 28 * max(1, routes))
        if priority >= 13:
            return min(128, 32 + 12 * max(1, routes))
        if (phase == Phase.ENDGAME or scenario == Scenario.ENDGAME) and priority < 9:
            # While the Core is still unlocalized, spend the bank primarily on
            # mobile search bodies. Keep only a starter magazine until a real
            # target appears, then the branches above scale ammo immediately.
            return min(48, 16 + 6 * max(1, routes))
        if priority >= 9:
            # Defended infrastructure / useful firing line: enough for a real
            # engagement, but do not finance a long blind siege in advance.
            return min(64, 16 + 8 * max(1, routes))
        # Blind pressure: launchers and Builders can advance while a compact
        # magazine waits for an actual target. A fresh rally raises this next turn.
        return min(28, 8 + 4 * max(1, routes))
    return 0


def _select_scenario(
    round_no: int,
    *,
    phase: Phase,
    maintaining_routes: int,
    route_target: int,
    no_progress_rounds: int,
    defense_alert: bool,
    defense_severity: int,
    attack_objective_priority: int,
) -> Scenario:
    # Defense is an interrupt even in the last 150 rounds.
    if defense_alert and (
        defense_severity >= 10 or maintaining_routes < 2 or phase == Phase.DEFENSE
    ):
        return Scenario.CONTESTED
    if round_no >= 850 or phase == Phase.ENDGAME:
        # Never play for the titanium tiebreak. If the Core is not known yet,
        # ENDGAME means hunt/localize it; once priority 15 appears, the same
        # scenario becomes the terminal all-in assault.
        return Scenario.ENDGAME
    # The rescue state is intentionally independent of phase commitment. If an
    # earlier attack loses every route, surveyors return to ore duty instead of
    # continuing a bankrupt march across the map.
    if round_no >= 100 and maintaining_routes == 0:
        return Scenario.ECONOMY_RESCUE
    if maintaining_routes < min(2, route_target) and no_progress_rounds >= 80:
        return Scenario.ECONOMY_RESCUE
    if phase == Phase.OFFENSE:
        return Scenario.SIEGE
    if maintaining_routes >= route_target:
        return Scenario.EXPANSION
    return Scenario.STANDARD


def _update_route_progress(
    state: CoreState,
    round_no: int,
    claimed_ore: int,
    active_projects: int,
    maintaining_routes: int,
) -> None:
    # Count both new all-time milestones and recovery after a route was cut.
    # The old max-only tracker treated rebuilding back to the previous count as
    # "no progress" and could release offense while repair was succeeding.
    progressed = (
        claimed_ore > state.last_claimed_ore
        or active_projects > state.last_active_projects
        or maintaining_routes > state.last_maintaining_routes
    )
    state.best_claimed_ore = max(state.best_claimed_ore, claimed_ore)
    state.best_active_projects = max(state.best_active_projects, active_projects)
    state.best_maintaining_routes = max(state.best_maintaining_routes, maintaining_routes)
    state.last_claimed_ore = claimed_ore
    state.last_active_projects = active_projects
    state.last_maintaining_routes = maintaining_routes
    if progressed or state.last_route_progress_round == 0:
        state.last_route_progress_round = round_no


def run_core(
    ct: object,
    state: CoreState | None = None,
    actions: TurnActions | None = None,
) -> CoreState:
    state = state or CoreState()
    turn = actions or TurnActions(ct)
    round_no = _get(ct, "get_current_round", 0)
    width = _get(ct, "get_map_width", 1)
    height = _get(ct, "get_map_height", 1)
    area = max(1, width * height)
    resources = _get(ct, "get_global_resources", 0)
    current_core_hp = _get(ct, "get_hp", 500)
    previous_core_hp = state.last_core_hp
    core_damage = (
        previous_core_hp is not None and current_core_hp < previous_core_hp
    )
    core_damage_delta = (
        max(1, int(previous_core_hp) - int(current_core_hp)) if core_damage else 0
    )
    state.last_core_hp = current_core_hp

    if not state.schema_written:
        _write_store(ct, Slot.SCHEMA_VERSION, SCHEMA_VERSION)
        state.schema_written = True

    if (
        state.cached_descriptor is None
        or state.opening_observed_round is None
        or round_no - state.opening_observed_round >= 32
    ):
        state.cached_descriptor = _observed_opening(ct)
        state.opening = choose_opening(state.cached_descriptor)
        state.opening_observed_round = round_no
    if state.route_target <= 0:
        state.route_target = _route_target(state.opening, area)
        # Straight-line bootstrap: exactly one Store-backed owner until the first
        # producer is actually maintaining. Future owners are created only when
        # their pipeline can be funded, keeping Builder scale low.
        state.route_capacity = 1

    _synchronize_claim_owners(ct, state, width, height, round_no)
    _trim_optional_route_capacity(state)
    claims = _fresh_claims(ct, width, height, round_no, state.route_capacity)
    claimed_ore = sum(claim.position is not None for _, claim in claims)
    active_projects, maintaining_routes, producer_ready_projects = _project_counts(
        ct, claims, round_no
    )
    _update_route_progress(state, round_no, claimed_ore, active_projects, maintaining_routes)

    descriptor = state.cached_descriptor
    nearby_ore_count = int(getattr(descriptor, "nearby_ore_count", 0) or 0)
    nearest_ore_distance = int(getattr(descriptor, "nearest_ore_distance", 999) or 999)
    operating_floor = _operating_builder_floor(
        state.opening, area, state.route_target, nearby_ore_count, nearest_ore_distance
    )
    # Controller distinguishes mobile units from buildings.  get_unit_count()
    # therefore gives the live Core+Builder population. Base workforce decisions on
    # the live count so a killed free Scout/Saboteur is actually replaced.
    unit_count = _get(ct, "get_unit_count", 1)
    live_builders = max(0, unit_count - 1)  # the Core itself occupies one unit slot
    workforce_ready = live_builders >= operating_floor
    no_progress = max(0, round_no - state.last_route_progress_round)
    defense_target, shared_defense_severity = _fresh_defense_alert(
        ct, width, height, round_no
    )
    local_defense_target, local_defense_severity, local_defense_kind = _local_core_threat(ct, area)
    # Damage is authoritative even when the shooter is outside vision or a
    # Sentinel fires through a wall. Publishing the Core tile still gives remote
    # responders a useful destination; local sensing will identify the attacker as
    # soon as somebody reaches the area.
    if core_damage:
        try:
            damage_target = ct.get_position()
        except Exception:
            damage_target = Position(0, 0)
        if local_defense_severity < 15:
            local_defense_target = damage_target
            local_defense_severity = 15
            if core_damage_delta in (2, 4, 6):
                local_defense_kind = ThreatKind.BUILDER_RUSH
            elif core_damage_delta in (18, 36) or core_damage_delta >= 15:
                local_defense_kind = ThreatKind.SENTINEL_FIRE
            elif core_damage_delta in (7, 14, 21, 28) or core_damage_delta >= 6:
                local_defense_kind = ThreatKind.GUNNER_FIRE
            else:
                local_defense_kind = ThreatKind.CORE_DAMAGE
    if local_defense_target is not None and local_defense_severity > 0:
        # Core-authored alarms persist long enough for a large-map responder to
        # cross several rooms. Prefer the actual hostile tile over the Core tile.
        try:
            ct.write_store(
                int(Slot.DEFENSE_ALERT),
                encode_defense_alert(
                    local_defense_target,
                    width,
                    (round_no + 12) & 63,
                    local_defense_severity,
                    local_defense_kind,
                ),
            )
        except Exception:
            pass
    defense_severity = max(shared_defense_severity, local_defense_severity)
    defense_alert = defense_severity >= 10
    attack_priority = _fresh_rally_priority(ct, width, height, round_no)
    # A fully collapsed economy cancels a previous offensive commitment so the
    # team can recover instead of remaining locked in attack mode forever.
    if maintaining_routes == 0 and no_progress >= 64:
        state.offense_committed = False
    state.phase = _select_phase(
        round_no,
        fresh_claim_count=len(claims),
        maintaining_routes=maintaining_routes,
        route_target=state.route_target,
        no_progress_rounds=no_progress,
        workforce_ready=workforce_ready,
        defense_alert=defense_alert,
        offense_committed=state.offense_committed,
        attack_objective_priority=attack_priority,
        opening=state.opening,
        area=area,
    )
    # Offense is recomputed from current contact instead of becoming a hidden
    # permanent macro state. The sticky field is kept for state compatibility only.
    state.offense_committed = False
    state.scenario = _select_scenario(
        round_no,
        phase=state.phase,
        maintaining_routes=maintaining_routes,
        route_target=state.route_target,
        no_progress_rounds=no_progress,
        defense_alert=defense_alert,
        defense_severity=defense_severity,
        attack_objective_priority=attack_priority,
    )

    desired = _desired_builders(
        state.phase,
        state.opening,
        area,
        state.route_target,
        state.route_capacity,
        maintaining_routes=maintaining_routes,
        active_projects=active_projects,
        attack_objective_priority=attack_priority,
        defense_severity=defense_severity,
        no_progress_rounds=no_progress,
        nearby_ore_count=nearby_ore_count,
        nearest_ore_distance=nearest_ore_distance,
    )
    budget_phase = state.phase
    if state.scenario == Scenario.ECONOMY_RESCUE:
        budget_phase = Phase.ECONOMY
    elif state.scenario == Scenario.CONTESTED or defense_severity >= 8:
        budget_phase = Phase.DEFENSE
    budget = compute_budget(
        ct,
        route_projects=active_projects,
        maintaining_routes=maintaining_routes,
        phase=budget_phase,
    )
    if maintaining_routes == 0 and active_projects > 0:
        # During first-income bootstrap, a scaled future Builder must not become
        # the liquidity floor that blocks every Conveyor and Harvester. The
        # route builders separately preserve the current producer cost.
        harvester_seed = max(20, _cost(ct, "get_harvester_cost", BASE_HARVESTER_COST))
        budget = Budget(
            construction=budget.construction,
            defense=budget.defense,
            ammo=budget.ammo,
            expansion=budget.expansion,
            liquidity=min(budget.liquidity, harvester_seed),
        )
    terminal_assault = bool(
        defense_severity < 10
        and maintaining_routes >= 2
        and (state.phase == Phase.ENDGAME or attack_priority >= 15)
    )
    resource_workers = _resource_backed_workers(
        ct,
        budget,
        maintaining_routes=maintaining_routes,
        defense_severity=defense_severity,
        round_no=round_no,
        terminal_assault=terminal_assault,
    )
    _maybe_open_expansion_route(
        ct,
        state,
        round_no=round_no,
        maintaining_routes=maintaining_routes,
        active_projects=active_projects,
        producer_ready_projects=producer_ready_projects,
        attack_priority=attack_priority,
        defense_severity=defense_severity,
        budget=budget,
    )
    # Capacity promotion changes next round's desired owner count; keep this
    # round's Store target internally consistent as well.
    desired = _desired_builders(
        state.phase,
        state.opening,
        area,
        state.route_target,
        state.route_capacity,
        maintaining_routes=maintaining_routes,
        active_projects=active_projects,
        attack_objective_priority=attack_priority,
        defense_severity=defense_severity,
        no_progress_rounds=no_progress,
        nearby_ore_count=nearby_ore_count,
        nearest_ore_distance=nearest_ore_distance,
        resource_workers=resource_workers,
    )
    state.last_budget = budget
    ammo_target = _ammo_target(
        state.phase,
        maintaining_routes,
        state.scenario,
        attack_priority=attack_priority,
        defense_severity=defense_severity,
    )
    _write_store(
        ct,
        Slot.STRATEGY,
        encode_strategy(
            state.phase,
            state.opening,
            state.scenario,
            route_target=state.route_target,
            route_capacity=state.route_capacity,
            maintaining_routes=maintaining_routes,
            active_projects=active_projects,
            defense_severity=defense_severity,
            attack_priority=attack_priority,
        ),
    )
    _write_store(ct, Slot.DESIRED_BUILDERS, desired)
    _write_store(ct, Slot.AMMO_TARGET, ammo_target)
    _write_store(ct, Slot.BUDGET, encode_budget(budget))
    _write_store(
        ct,
        Slot.EPOCH,
        encode_epoch_pulse(
            round_no & 63,
            route_progress_age=min(63, no_progress),
            core_congestion=_core_builder_congestion(ct),
        ),
    )

    max_units = MAX_TEAM_UNITS
    builder_cost = _cost(ct, "get_builder_bot_cost", BASE_BUILDER_COST)
    missing_owner = next(
        (index for index in range(state.route_capacity) if index not in state.claim_owners),
        None,
    )
    # Live workforce is authoritative.  This is both simpler and fixes a real
    # attrition bug: a historical spawn counter could say we had ten Builders
    # after three had died, suppressing free-scout/attacker replacement forever.
    need_builder = live_builders < desired or missing_owner is not None
    # Spawn only against concrete work.  Before first delivery we buy the small
    # operating floor quickly, then freeze Builder growth while any route is
    # waiting for its Harvester.  After income starts, optional workers are
    # staggered so a temporary resource spike cannot turn into a Builder flood.
    bootstrap_floor = _operating_builder_floor(
        state.opening, area, state.route_target, nearby_ore_count, nearest_ore_distance
    )
    if live_builders < min(desired, bootstrap_floor):
        # Protect a complete first producer seed while forming the opening crew.
        harvester_seed = _cost(ct, "get_harvester_cost", BASE_HARVESTER_COST)
        conveyor_seed = _cost(ct, "get_conveyor_cost", BASE_CONVEYOR_COST)
        spawn_reserve = max(
            budget.construction,
            harvester_seed + 6 * conveyor_seed,
        )
    else:
        # Every extra body is bought *after* the next economic step is funded.
        # This is invariant across ECONOMY/OFFENSE/DEFENSE/ENDGAME; combat may
        # scale from surplus but never consumes the expansion seed.
        spawn_reserve = budget.liquidity + budget.construction + budget.defense


    if producer_ready_projects > 0:
        need_builder = False
    if (
        maintaining_routes == 0
        and live_builders >= min(desired, bootstrap_floor)
        and active_projects > 0
    ):
        need_builder = False

    if maintaining_routes <= 0 or terminal_assault:
        spawn_interval = 1
    elif resource_workers >= 1:
        # A genuinely capitalised team should turn the bank into map tempo
        # quickly; resource_workers is computed only after the expansion reserve.
        spawn_interval = 1
    elif active_projects > maintaining_routes or state.route_capacity < state.route_target:
        # While the four primary producers are still coming online, add funded
        # concurrency every other round instead of waiting four rounds per body.
        spawn_interval = 2
    elif defense_severity >= 12 or attack_priority >= 13:
        spawn_interval = 2
    else:
        spawn_interval = 3
    if round_no - state.last_builder_spawn_round < spawn_interval:
        need_builder = False
    if need_builder and unit_count < max_units and resources >= builder_cost + spawn_reserve:
        positions = _spawn_positions(ct)
        if positions:
            visible_ore = _visible_ore_positions(ct)
            claimed_positions = {
                claim.position for _, claim in claims if claim.position is not None
            }
            owner_index = next(
                (candidate for candidate in range(state.route_capacity) if candidate not in state.claim_owners),
                None,
            )
            owner_target = (
                next(
                    (position for position in visible_ore if position not in claimed_positions),
                    None,
                )
                if owner_index == 0
                else None
            )
            positions = tuple(
                sorted(
                    positions,
                    key=lambda position: _spawn_lane_score(
                        ct, position, target=owner_target
                    ),
                )
            )
            # Rotate only across the best few exits. The old full-list rotation
            # eventually spawned directly into the most congested Core pocket
            # even when several clear lanes were available.
            preferred_count = min(3, len(positions))
            start = state.spawn_cursor % preferred_count
            preferred = positions[:preferred_count]
            ordered = preferred[start:] + preferred[:start] + positions[preferred_count:]
            for offset, position in enumerate(ordered):
                builder_id = turn.spawn(position)
                if builder_id is None:
                    continue
                state.spawn_cursor = (start + offset + 1) % preferred_count
                state.last_builder_spawn_round = round_no
                if owner_index is not None:
                    state.claim_owners[owner_index] = int(builder_id)
                    try:
                        _write_store(
                            ct,
                            claim_slot(owner_index),
                            pack_claim(owner_target, width, round_no, int(builder_id), height),
                        )
                    except ValueError:
                        pass
                break

    current_ammo = _get(ct, "get_global_ammo", 0)
    deficit = max(0, ammo_target - current_ammo)
    current_resources = _get(ct, "get_global_resources", 0)
    protected = budget.liquidity + budget.construction + budget.defense
    if deficit > 0:
        # A bot that cannot establish a real firing line must not convert the
        # Outside terminal assault, keep a lifetime safety cap so a blind firing
        # line cannot eat the whole economy. Terminal Core assault bypasses this
        # cap deliberately: the remaining bank is fuel for the primary win.
        conversion_left = (
            max(0, current_resources - protected)
            if terminal_assault
            else max(0, MAX_MATCH_AMMO_CONVERSION - state.ammo_converted_total)
        )
        amount = min(deficit, max(0, current_resources - protected), conversion_left)
        if amount > 0 and turn.convert_ammo(amount):
            state.ammo_converted_total += amount
    return state
