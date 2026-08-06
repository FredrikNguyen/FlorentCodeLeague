
from __future__ import annotations

from dataclasses import dataclass, field

from fcode import Direction, EntityType, Environment, GameConstants, Position

from .actions import TurnActions, cpu_is_safe
from .comms import PROJECT_COUNT, SCHEMA_VERSION, Slot, _store, _write, assignment_is_fresh, encode_global_strategy, encode_strategy, epoch_distance, read_assignment, read_project, write_assignment, write_project
from .defense import DefenseState, choose_defenders, required_defender_count, update_defense_overlay
from .economy import (
    EMERGENCY_LIQUIDITY_RESERVE,
    MAX_SIMULTANEOUS_BUILD_PROJECTS,
    choose_economy_phase,
    compute_desired_builders,
    free_titanium_after_reserves,
)
from .feature_flags import ENABLE_DEFENSIVE_BUILDING, ENABLE_PHASE_STRATEGY
from .offense import read_verified_enemy_core
from .policy import allocate_roles, choose_opening, choose_phase, choose_strategy_phase, describe_opening, persistent_defender_count, required_route_count
from .types import Budget, DefenseMode, EconomyPhase, EconomySnapshot, Opening, Phase, ProjectState, Role, StrategyPhase


@dataclass(slots=True)
class CoreState:
    opening: Opening = Opening.BALANCED_ECONOMY; phase: Phase = Phase.OPENING; spawned_ids: list[int] = field(default_factory=list); claim_owners: dict[int, int] = field(default_factory=dict)
    claim_initialized: bool = False; schema_written: bool = False; last_budget: Budget = field(default_factory=Budget); spawn_cursor: int = 0; near_term_core_kill: bool = False; opening_observed_round: int | None = None; pending_assignments: dict[int, tuple[int, int]] = field(default_factory=dict); failed_ore_cooldowns: dict[Position, int] = field(default_factory=dict); failed_project_positions: dict[int, Position] = field(default_factory=dict); releasing_projects: set[int] = field(default_factory=set)
    economy_phase: EconomyPhase = EconomyPhase.BOOTSTRAP; snapshot: EconomySnapshot = field(default_factory=EconomySnapshot); opening_descriptor: object | None = None; defense_state: DefenseState = field(default_factory=DefenseState); strategy_phase: StrategyPhase = StrategyPhase.BOOTSTRAP_ECON; strategy_epoch: int = 0; economy_ready_rounds: int = 0; role_assignments: dict[int, Role] = field(default_factory=dict)
    explored_tiles: set[Position] = field(default_factory=set); reachable_ore_positions: set[Position] = field(default_factory=set); exploration_complete: bool = False


def _get(ct: object, name: str, default: int = 0) -> int:
    try: return int(getattr(ct, name)())
    except (AttributeError, TypeError, ValueError): return default


def _cost(ct: object, name: str, default: int) -> int:
    return max(0, _get(ct, name, default))


def compute_budget(ct: object, *, route_projects: int = 0) -> Budget:
    resources = _get(ct, "get_global_resources", 0); builder = _cost(ct, "get_builder_bot_cost", GameConstants.BUILDER_BOT_BASE_COST); harvester = _cost(ct, "get_harvester_cost", GameConstants.HARVESTER_BASE_COST); conveyor = _cost(ct, "get_conveyor_cost", GameConstants.CONVEYOR_BASE_COST); gunner = _cost(ct, "get_gunner_cost", GameConstants.GUNNER_BASE_COST); sentinel = _cost(ct, "get_sentinel_cost", GameConstants.SENTINEL_BASE_COST)
    construction = harvester + (4 + max(0, int(route_projects))) * conveyor
    # Keep a small standing reserve, then let the event-driven overlay raise
    # spending only for a fresh active/critical threat.  A permanent 20% hold
    # starves the first route on compact maps.
    defense = min(max(0, resources // 50), max(gunner, sentinel)) if ENABLE_DEFENSIVE_BUILDING else 0
    liquidity = max(builder, harvester, EMERGENCY_LIQUIDITY_RESERVE)
    ammo = max(0, min(resources // 50, 2 * GameConstants.GUNNER_AMMO_COST + GameConstants.SENTINEL_AMMO_COST)) if ENABLE_DEFENSIVE_BUILDING else 0
    expansion = max(0, resources - construction - defense - liquidity - ammo)
    return Budget(construction, defense, ammo, expansion, liquidity)


def _visible_counts(ct: object) -> tuple[int, int]:
    try:
        ids = tuple(ct.get_nearby_buildings())
    except Exception: ids = ()
    types = tuple(_entity_type(ct, entity_id) for entity_id in ids); return sum(entity_type == EntityType.GUNNER for entity_type in types), sum(entity_type == EntityType.SENTINEL for entity_type in types)


def _entity_type(ct: object, entity_id: int):
    try: return ct.get_entity_type(entity_id)
    except Exception: return None


def desired_ammo(ct: object, *, horizon_rounds: int = 6, emergency_buffer: int = 0) -> int:
    gunner_count, sentinel_count = _visible_counts(ct)
    gunner_shots = max(0, int(horizon_rounds) // max(1, GameConstants.GUNNER_FIRE_COOLDOWN)); sentinel_shots = max(0, int(horizon_rounds) // max(1, GameConstants.SENTINEL_FIRE_COOLDOWN))
    return gunner_count * gunner_shots * GameConstants.GUNNER_AMMO_COST + sentinel_count * sentinel_shots * GameConstants.SENTINEL_AMMO_COST + max(0, int(emergency_buffer))


def _write_store(ct: object, slot: Slot, value: int) -> None:
    _write(ct, slot, max(0, min(0xFFFFFFFF, int(value))))


def _spawn_positions(ct: object) -> tuple[Position, ...]:
    try:
        positions = tuple(ct.get_nearby_tiles(dist_sq=GameConstants.CORE_SPAWNING_RADIUS_SQ)); return tuple(sorted(positions, key=lambda pos: (pos.y, pos.x)))
    except Exception: return ()


def _observed_opening(ct: object):
    width, height = _get(ct, "get_map_width", 1), _get(ct, "get_map_height", 1)
    try:
        origin = ct.get_position(); tiles = tuple(ct.get_nearby_tiles())[: max(1, width * height)]
    except Exception: origin, tiles = Position(0, 0), ()
    walls: set[Position] = set(); ore: list[Position] = []; passable: set[Position] = set()
    for tile in tiles:
        if not cpu_is_safe(ct): break
        try:
            environment = ct.get_tile_env(tile); walls.update((tile,) if environment == Environment.WALL else ()); ore.extend((tile,) if environment == Environment.ORE_TITANIUM else ()); passable.update((tile,) if ct.is_tile_passable(tile) else ())
        except Exception: continue
    low_degree = exposed = 0
    for tile in tuple(sorted(passable, key=lambda pos: (pos.y, pos.x))):
        if not cpu_is_safe(ct): break
        neighbours = tuple(tile.add(direction) for direction in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST))
        degree = sum(neighbour in passable for neighbour in neighbours); low_degree += degree <= 1; exposed += any(neighbour in walls for neighbour in neighbours)
    enemy_distance = 999
    try:
        own_team = ct.get_team()
        for entity_id in tuple(ct.get_nearby_buildings())[: max(64, width * height)]:
            if not cpu_is_safe(ct): break
            if ct.get_entity_type(entity_id) == EntityType.CORE and ct.get_team(entity_id) != own_team: position = ct.get_position(entity_id); enemy_distance = min(enemy_distance, abs(position.x - origin.x) + abs(position.y - origin.y))
    except Exception: pass
    return describe_opening(width, height, nearby_ore_count=len(ore), nearest_ore_distance=min((abs(position.x - origin.x) + abs(position.y - origin.y) for position in ore), default=999), wall_density=len(walls) / max(1, len(tiles)), low_degree_passable_tiles=low_degree, route_exposure=exposed / max(1, len(passable)), estimated_enemy_distance=enemy_distance)


def _update_exploration_progress(ct: object, state: CoreState, width: int, height: int) -> None:
    try:
        tiles = tuple(ct.get_nearby_tiles())[: max(1, min(width * height, 4096))]
    except Exception:
        tiles = ()
    for position in tiles:
        if not (0 <= position.x < width and 0 <= position.y < height):
            continue
        state.explored_tiles.add(position)
        try:
            if ct.get_tile_env(position) == Environment.ORE_TITANIUM:
                state.reachable_ore_positions.add(position)
        except Exception:
            continue
    state.exploration_complete = len(state.explored_tiles) >= max(1, width * height)


def _project_states(ct: object) -> tuple[ProjectState, ...]:
    return tuple((project.state if (project := read_project(ct, index)) is not None else ProjectState.IDLE) for index in range(PROJECT_COUNT))


def _builder_ids(ct: object) -> tuple[int, ...]:
    try:
        ids = tuple(ct.get_nearby_units())
    except Exception:
        try: ids = tuple(ct.get_nearby_entities())
        except Exception: ids = ()
    own_team = None
    try: own_team = ct.get_team()
    except Exception: pass
    result: list[int] = []
    for entity_id in ids:
        try:
            if ct.get_entity_type(entity_id) != EntityType.BUILDER_BOT or own_team is not None and ct.get_team(entity_id) != own_team: continue
            result.append(int(entity_id))
        except Exception: continue
    return tuple(sorted(set(result)))


def _healthy_heartbeat(ct: object, index: int, round_no: int) -> bool:
    project = read_project(ct, index)
    return project is not None and project.state == ProjectState.MAINTAIN and epoch_distance(round_no & 63, project.epoch) <= 16


def _next_project_slot(ct: object, state: CoreState, round_no: int) -> int | None:
    states = _project_states(ct)
    def reusable(index: int) -> bool:
        project = read_project(ct, index)
        if project is None or project.state in (ProjectState.IDLE, ProjectState.FAILED):
            return True
        assignment = read_assignment(ct, index)
        return assignment is None or not assignment_is_fresh(assignment, round_no & 63)

    if 0 not in state.claim_owners and 0 not in state.pending_assignments and 0 not in state.releasing_projects and reusable(0):
        return 0
    if not _healthy_heartbeat(ct, 0, round_no):
        return None
    secondary_building = sum(
        states[index] in (ProjectState.CLAIMED, ProjectState.PLANNING, ProjectState.BUILDING, ProjectState.VERIFYING, ProjectState.DELIVERING)
        or index in state.pending_assignments
        or states[index] == ProjectState.IDLE and index in state.claim_owners
        for index in range(1, PROJECT_COUNT)
    )
    if secondary_building >= MAX_SIMULTANEOUS_BUILD_PROJECTS:
        return None
    for index in range(1, PROJECT_COUNT):
        if index in state.claim_owners or index in state.pending_assignments or index in state.releasing_projects:
            continue
        project = read_project(ct, index)
        if not reusable(index):
            continue
        if project is not None and project.position in state.failed_ore_cooldowns and round_no < state.failed_ore_cooldowns[project.position]:
            continue
        return index
    return None


def _assign_waiting_builder(ct: object, state: CoreState, round_no: int) -> None:
    index = _next_project_slot(ct, state, round_no)
    if index is None:
        return
    assigned = set(state.claim_owners.values()) | {owner for owner, _ in state.pending_assignments.values()}
    candidates = tuple(builder_id for builder_id in tuple(state.spawned_ids) + _builder_ids(ct) if builder_id not in assigned)
    if not candidates:
        return
    owner_id = min(candidates)
    generation = round_no & 63
    if write_assignment(ct, index, owner_id, generation):
        state.claim_owners[index] = owner_id
        state.pending_assignments[index] = (owner_id, generation)


def _snapshot(ct: object, *, desired_builders: int, round_no: int) -> EconomySnapshot:
    states = _project_states(ct)
    active = sum(state not in (ProjectState.IDLE, ProjectState.FAILED) for state in states)
    maintaining = sum(state == ProjectState.MAINTAIN for state in states)
    building = sum(state in (ProjectState.CLAIMED, ProjectState.PLANNING, ProjectState.BUILDING, ProjectState.VERIFYING, ProjectState.DELIVERING) for state in states)
    failed = sum(state == ProjectState.FAILED for state in states)
    resources = _get(ct, "get_global_resources", 0); ammo = _get(ct, "get_global_ammo", 0); scale = max(0, int(_get(ct, "get_scale_percent", 100)))
    conveyor = _cost(ct, "get_conveyor_cost", GameConstants.CONVEYOR_BASE_COST); harvester = _cost(ct, "get_harvester_cost", GameConstants.HARVESTER_BASE_COST)
    completion_reserve = max(0, building * (4 * conveyor + harvester)); repair_reserve = max(2 * conveyor, (completion_reserve + 9) // 10) if active else 0
    budget = compute_budget(ct, route_projects=building)
    free = free_titanium_after_reserves(resources, completion_reserve=completion_reserve, repair_reserve=repair_reserve, liquidity_reserve=EMERGENCY_LIQUIDITY_RESERVE, defense_reserve=budget.defense, ammo_reserve=budget.ammo)
    try: live_units = _get(ct, "get_unit_count", 0)
    except Exception: live_units = 0
    return EconomySnapshot(round_no, resources, ammo, scale, live_units, desired_builders, active, maintaining, building, failed, failed, completion_reserve, repair_reserve, budget.defense, budget.ammo, free)


def _free_builder_ids(ct: object, state: CoreState) -> tuple[int, ...]:
    assigned = set(state.claim_owners.values()) | {owner for owner, _ in state.pending_assignments.values()}
    return tuple(builder_id for builder_id in _builder_ids(ct) if builder_id not in assigned)


def _free_builder_candidates(ct: object, state: CoreState) -> tuple[tuple[int, Position, int, bool], ...]:
    candidates: list[tuple[int, Position, int, bool]] = []
    for builder_id in _free_builder_ids(ct, state):
        try:
            position = ct.get_position(builder_id)
            hp = int(ct.get_hp(builder_id))
        except Exception:
            continue
        candidates.append((builder_id, position, hp, False))
    return tuple(candidates)


def _synchronize_claim_owners(ct: object, state: CoreState, width: int, height: int, round_no: int) -> None:
    for index in range(PROJECT_COUNT):
        assignment = read_assignment(ct, index); project = read_project(ct, index); pending = state.pending_assignments.get(index)
        if assignment is None and pending is not None: state.claim_owners[index] = pending[0]; continue
        owner = state.claim_owners.get(index)
        heartbeat = project.epoch if project is not None and project.state.value != "idle" else assignment.generation if assignment is not None else -1
        live = assignment is not None and assignment.owner_id > 0 and epoch_distance(round_no & 63, heartbeat) <= 31
        if live:
            state.pending_assignments.pop(index, None)
            if owner != assignment.owner_id: state.claim_owners[index] = assignment.owner_id
        if project is not None and project.state == ProjectState.FAILED:
            if project.position is not None:
                state.failed_ore_cooldowns.setdefault(project.position, round_no + 16)
                state.failed_project_positions[index] = project.position
            expiry = state.failed_ore_cooldowns.get(project.position) if project.position is not None else round_no
            if expiry is not None and round_no < expiry:
                continue
            if index not in state.releasing_projects:
                state.pending_assignments.pop(index, None)
                write_assignment(ct, index, None, round_no & 63)
                write_project(ct, index, None, round_no & 63, ProjectState.IDLE, width, height, writer=index)
                state.releasing_projects.add(index)
                continue
            if assignment is None and (project is None or project.state == ProjectState.IDLE):
                state.claim_owners.pop(index, None); state.pending_assignments.pop(index, None); state.releasing_projects.discard(index)
                failed_position = state.failed_project_positions.pop(index, None)
                if failed_position is not None: state.failed_ore_cooldowns.pop(failed_position, None)
                continue
        if project is None or project.state != ProjectState.FAILED:
            if live: continue
        if owner is not None: state.claim_owners.pop(index, None)


def run_core(ct: object, state: CoreState | None = None, actions: TurnActions | None = None) -> CoreState:
    state = state or CoreState(); turn = actions or TurnActions(ct); round_no = _get(ct, "get_current_round", 0)
    width = _get(ct, "get_map_width", 1); height = _get(ct, "get_map_height", 1); resources = _get(ct, "get_global_resources", 0)
    _update_exploration_progress(ct, state, width, height)
    state.last_budget = compute_budget(ct, route_projects=0); _synchronize_claim_owners(ct, state, width, height, round_no)
    schema = _store(ct, Slot.SCHEMA_VERSION) or 0
    if schema != SCHEMA_VERSION or not state.schema_written:
        _write_store(ct, Slot.SCHEMA_VERSION, SCHEMA_VERSION); state.schema_written = True
    if state.opening_descriptor is None:
        state.opening_descriptor = _observed_opening(ct)
        state.opening_observed_round = round_no
    descriptor = state.opening_descriptor
    if ENABLE_DEFENSIVE_BUILDING:
        state.defense_state = update_defense_overlay(ct, state.defense_state)
    state.opening = choose_opening(descriptor)
    project_states = _project_states(ct)
    known_ore_count = max(int(getattr(descriptor, "nearby_ore_count", 0)), len(state.reachable_ore_positions))
    preliminary_desired = compute_desired_builders(active_building_projects=sum(value in (ProjectState.CLAIMED, ProjectState.PLANNING, ProjectState.BUILDING, ProjectState.VERIFYING, ProjectState.DELIVERING) for value in project_states), maintaining_routes=sum(value == ProjectState.MAINTAIN for value in project_states), known_ore_count=known_ore_count)
    state.snapshot = _snapshot(ct, desired_builders=preliminary_desired, round_no=round_no)
    state.economy_phase = choose_economy_phase(project_states, round_no=round_no, profitable_expansion=round_no < 820 and state.snapshot.free_titanium >= 0)
    required_routes = required_route_count(reachable_ore_count=len(state.reachable_ore_positions), exploration_complete=state.exploration_complete)
    fresh_maintaining_routes = sum(_healthy_heartbeat(ct, index, round_no) for index in range(PROJECT_COUNT))
    healthy_gate = fresh_maintaining_routes >= required_routes and state.snapshot.broken_routes == 0
    free_builder_ids = _free_builder_ids(ct, state)
    if ENABLE_PHASE_STRATEGY:
        # The offensive clock starts only after every required route has a
        # fresh delivery heartbeat.  Until exhaustive exploration proves a
        # smaller reachable ore set, that means all four route slots.
        if healthy_gate:
            state.economy_ready_rounds += 1
        else:
            state.economy_ready_rounds = 0
        enemy_core_fresh = read_verified_enemy_core(ct, max_age=24) is not None
        state.strategy_phase = choose_strategy_phase(
            state.snapshot,
            defense_mode=state.defense_state.mode,
            enemy_core_fresh=enemy_core_fresh,
            free_builders=len(free_builder_ids),
            required_routes=required_routes,
            stable_rounds=state.economy_ready_rounds,
        )
        state.role_assignments = allocate_roles(
            free_builder_ids,
            phase=state.strategy_phase,
            defenders=persistent_defender_count(map_area=width * height, recent_threat=state.defense_state.last_threat_round >= 0 and round_no - state.defense_state.last_threat_round <= 16),
            maintenance_workers=max(1, (state.snapshot.maintaining_routes + 1) // 2),
            scouts=1,
        )
        required_defenders = required_defender_count(
            state.defense_state.mode,
            state.defense_state.threat.severity if state.defense_state.threat is not None else 0,
            map_area=width * height,
        ) if state.strategy_phase == StrategyPhase.DEFENSE_ALERT else 0
        state.defense_state.defenders = choose_defenders(
            _free_builder_candidates(ct, state),
            required_defenders,
            threat_position=state.defense_state.threat.position if state.defense_state.threat is not None else None,
            critical_route_owners=frozenset(state.claim_owners.values()),
        ) if required_defenders else ()
        state.strategy_epoch = round_no & 63
    if state.strategy_phase in (StrategyPhase.DEFENSE_ALERT,):
        state.phase = Phase.DEFENSE
    elif state.strategy_phase in (StrategyPhase.ATTACK_PREPARATION, StrategyPhase.OFFENSIVE_PRESSURE, StrategyPhase.CORE_SIEGE):
        state.phase = Phase.OFFENSE
    elif state.strategy_phase == StrategyPhase.ENDGAME:
        state.phase = Phase.ENDGAME
    else:
        state.phase = choose_phase(round_no, opening=state.opening, verified_enemy_core=descriptor.estimated_enemy_distance < 999, economy_ready=healthy_gate and state.economy_ready_rounds >= 8)
    target_ammo = desired_ammo(ct, emergency_buffer=0) if ENABLE_DEFENSIVE_BUILDING and (state.strategy_phase in (StrategyPhase.ATTACK_PREPARATION, StrategyPhase.OFFENSIVE_PRESSURE, StrategyPhase.CORE_SIEGE) or state.defense_state.mode == DefenseMode.CRITICAL) else 0
    strategy_word = encode_global_strategy(state.strategy_phase, state.phase, state.opening) if ENABLE_PHASE_STRATEGY else encode_strategy(state.phase, state.opening)
    _write_store(ct, Slot.STRATEGY, strategy_word); _write_store(ct, Slot.DIAGNOSTICS, tuple(EconomyPhase).index(state.economy_phase)); _write_store(ct, Slot.AMMO_TARGET, target_ammo)

    desired_builders = compute_desired_builders(active_building_projects=state.snapshot.building_routes, maintaining_routes=state.snapshot.maintaining_routes, known_ore_count=known_ore_count)
    state.snapshot = _snapshot(ct, desired_builders=desired_builders, round_no=round_no)
    _write_store(ct, Slot.DESIRED_BUILDERS, desired_builders)
    unit_count = _get(ct, "get_unit_count", desired_builders + 1)
    builder_cost = _cost(ct, "get_builder_bot_cost", GameConstants.BUILDER_BOT_BASE_COST)
    if unit_count < desired_builders + 1 and state.snapshot.free_titanium >= builder_cost and not turn.acted:
        positions = _spawn_positions(ct)
        if positions:
            start = state.spawn_cursor % len(positions); ordered = positions[start:] + positions[:start]
            for position in ordered:
                builder_id = turn.spawn(position)
                if builder_id is not None:
                    state.spawn_cursor = (start + 1) % len(positions); state.spawned_ids.append(int(builder_id)); break

    if not state.claim_initialized and len(state.claim_owners) >= PROJECT_COUNT: state.claim_initialized = True
    _assign_waiting_builder(ct, state, round_no)

    current_ammo = _get(ct, "get_global_ammo", 0); deficit = max(0, target_ammo - current_ammo); current_resources = _get(ct, "get_global_resources", 0); current_budget = compute_budget(ct, route_projects=state.snapshot.building_routes)
    if ENABLE_DEFENSIVE_BUILDING and round_no < 850 and deficit and state.phase != Phase.OPENING:
        amount = min(deficit, free_titanium_after_reserves(current_resources, completion_reserve=current_budget.construction, repair_reserve=state.snapshot.emergency_repair_reserve, liquidity_reserve=current_budget.liquidity, defense_reserve=current_budget.defense))
        if amount and not turn.acted:
            turn.convert_ammo(amount)
    return state
