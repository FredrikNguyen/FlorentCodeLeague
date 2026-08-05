
from __future__ import annotations

from dataclasses import dataclass, field

from fcode import Direction, EntityType, Environment, GameConstants, Position

from .actions import TurnActions, cpu_is_safe
from .comms import SCHEMA_VERSION, Slot, _store, _write, encode_strategy, epoch_distance, read_assignment, read_project, write_assignment
from .policy import choose_opening, describe_opening, choose_phase
from .types import Budget, Opening, Phase


@dataclass(slots=True)
class CoreState:
    opening: Opening = Opening.BALANCED_ECONOMY; phase: Phase = Phase.OPENING; spawned_ids: list[int] = field(default_factory=list); claim_owners: dict[int, int] = field(default_factory=dict)
    claim_initialized: bool = False; schema_written: bool = False; last_budget: Budget = field(default_factory=Budget); spawn_cursor: int = 0; near_term_core_kill: bool = False; opening_observed_round: int | None = None; pending_assignments: dict[int, tuple[int, int]] = field(default_factory=dict)


def _get(ct: object, name: str, default: int = 0) -> int:
    try: return int(getattr(ct, name)())
    except (AttributeError, TypeError, ValueError): return default


def _cost(ct: object, name: str, default: int) -> int:
    return max(0, _get(ct, name, default))


def compute_budget(ct: object, *, route_projects: int = 0) -> Budget:
    resources = _get(ct, "get_global_resources", 0); builder = _cost(ct, "get_builder_bot_cost", GameConstants.BUILDER_BOT_BASE_COST); harvester = _cost(ct, "get_harvester_cost", GameConstants.HARVESTER_BASE_COST); conveyor = _cost(ct, "get_conveyor_cost", GameConstants.CONVEYOR_BASE_COST); gunner = _cost(ct, "get_gunner_cost", GameConstants.GUNNER_BASE_COST); sentinel = _cost(ct, "get_sentinel_cost", GameConstants.SENTINEL_BASE_COST)
    construction = harvester + 4 * conveyor + max(0, int(route_projects)) * conveyor; defense = min(max(0, resources // 5), max(gunner, sentinel)); liquidity = max(builder, harvester, 20); ammo = max(0, min(resources // 8, 2 * GameConstants.GUNNER_AMMO_COST + GameConstants.SENTINEL_AMMO_COST)); expansion = max(0, resources - construction - defense - liquidity - ammo)
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


def _synchronize_claim_owners(ct: object, state: CoreState, width: int, height: int, round_no: int) -> None:
    for index in range(3):
        assignment = read_assignment(ct, index); project = read_project(ct, index); pending = state.pending_assignments.get(index)
        if assignment is None and pending is not None: state.claim_owners[index] = pending[0]; continue
        owner = state.claim_owners.get(index)
        heartbeat = project.epoch if project is not None and project.state.value != "idle" else assignment.generation if assignment is not None else -1
        live = assignment is not None and assignment.owner_id > 0 and epoch_distance(round_no & 63, heartbeat) <= 31
        if live:
            state.pending_assignments.pop(index, None)
            if owner != assignment.owner_id: state.claim_owners[index] = assignment.owner_id
        if project is None or project.state.value != "failed":
            if live: continue
        if project is not None and project.state.value == "failed":
            state.claim_owners.pop(index, None); state.pending_assignments.pop(index, None); continue
        if owner is not None: state.claim_owners.pop(index, None)


def run_core(ct: object, state: CoreState | None = None, actions: TurnActions | None = None) -> CoreState:
    state = state or CoreState(); turn = actions or TurnActions(ct); round_no = _get(ct, "get_current_round", 0)
    width = _get(ct, "get_map_width", 1); height = _get(ct, "get_map_height", 1); resources = _get(ct, "get_global_resources", 0)
    budget = compute_budget(ct, route_projects=0)
    state.last_budget = budget; _synchronize_claim_owners(ct, state, width, height, round_no)
    schema = _store(ct, Slot.SCHEMA_VERSION) or 0
    if schema != SCHEMA_VERSION or not state.schema_written:
        _write_store(ct, Slot.SCHEMA_VERSION, SCHEMA_VERSION); state.schema_written = True
    descriptor = _observed_opening(ct)
    state.opening = choose_opening(descriptor); state.phase = choose_phase(round_no, opening=state.opening, verified_enemy_core=descriptor.estimated_enemy_distance < 999, economy_ready=resources >= budget.construction + budget.liquidity)
    _write_store(ct, Slot.STRATEGY, encode_strategy(state.phase, state.opening)); _write_store(ct, Slot.AMMO_TARGET, desired_ammo(ct, emergency_buffer=0)); _write_store(ct, Slot.EPOCH, round_no & 63)
    state.opening_observed_round = round_no

    desired_builders = {Opening.COMPACT_PRESSURE: 3, Opening.ANTI_RUSH: 4, Opening.CHOKEPOINT_CONTROL: 4, Opening.WIDE_EXPANSION: 5, Opening.BALANCED_ECONOMY: 4}.get(state.opening, 4)
    _write_store(ct, Slot.DESIRED_BUILDERS, desired_builders)
    unit_count = _get(ct, "get_unit_count", desired_builders + 1)
    builder_cost = _cost(ct, "get_builder_bot_cost", GameConstants.BUILDER_BOT_BASE_COST)
    if unit_count < desired_builders + 1 and resources >= builder_cost + budget.liquidity and not turn.acted:
        positions = _spawn_positions(ct)
        if positions:
            start = state.spawn_cursor % len(positions); ordered = positions[start:] + positions[:start]
            for position in ordered:
                builder_id = turn.spawn(position)
                if builder_id is not None:
                    state.spawn_cursor = (start + 1) % len(positions); state.spawned_ids.append(int(builder_id))
                    owner_index = next((candidate for candidate in range(3) if candidate not in state.claim_owners), None)
                    if owner_index is not None:
                        state.claim_owners[owner_index] = int(builder_id); generation = round_no & 63; state.pending_assignments.update({owner_index: (int(builder_id), generation)}) if write_assignment(ct, owner_index, int(builder_id), generation) else None
                    break

    if not state.claim_initialized and len(state.claim_owners) >= 3: state.claim_initialized = True

    current_ammo = _get(ct, "get_global_ammo", 0); target_ammo = desired_ammo(ct, emergency_buffer=0); deficit = max(0, target_ammo - current_ammo); current_resources = _get(ct, "get_global_resources", 0); current_budget = compute_budget(ct, route_projects=0)
    if round_no < 850 and deficit and state.phase != Phase.OPENING:
        amount = min(deficit, max(0, current_resources - current_budget.construction - current_budget.defense - current_budget.liquidity))
        if amount and not turn.acted:
            turn.convert_ammo(amount)
    return state
