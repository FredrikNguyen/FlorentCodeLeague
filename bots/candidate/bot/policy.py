
from __future__ import annotations

from fcode import Position

from .types import BuilderState, DefenseMode, EconomySnapshot, Opening, OpeningDescriptor, Phase, Role, StrategyPhase, WorkIntent


PERSISTENT_DEFENDERS_SMALL = 2
PERSISTENT_DEFENDERS_LARGE = 3
MIN_MAINTENANCE_WORKERS = 1
ECONOMY_READY_STABLE_ROUNDS = 8
ENDGAME_START = 850
ATTACK_PREPARATION_RESERVE = 80
REQUIRED_HEALTHY_ROUTES = 4
MIN_FREE_BUILDERS_FOR_OFFENSE = 2


def choose_work_intent(
    *,
    critical_threat: bool = False,
    route_repair_due: bool = False,
    route_owner: bool = False,
    attack_preparation: bool = False,
    attack: bool = False,
    exploration_complete: bool = False,
) -> WorkIntent:
    """Resolve one deterministic productive responsibility for a Builder."""
    if critical_threat:
        return WorkIntent.CRITICAL_DEFENSE
    if route_repair_due:
        return WorkIntent.REPAIR_ROUTE
    if route_owner:
        return WorkIntent.ROUTE_OWNER
    if attack:
        return WorkIntent.ATTACK
    if attack_preparation:
        return WorkIntent.ATTACK_PREPARATION
    return WorkIntent.PATROL_LOGISTICS if exploration_complete else WorkIntent.DISCOVER_ORE


def assign_role(entity_id: int, phase: Phase = Phase.OPENING, opening: Opening | None = None) -> Role:
    value = abs(int(entity_id)) % 8
    if phase == Phase.ENDGAME:
        return Role.RAIDER if value % 2 else Role.REPAIR
    if opening == Opening.ANTI_RUSH and value in (0, 1, 2):
        return Role.DEFENDER if value == 2 else Role.ECONOMY
    return {
        0: Role.ECONOMY,
        1: Role.ECONOMY,
        2: Role.REPAIR,
        3: Role.DEFENDER,
        4: Role.SCOUT,
        5: Role.RAIDER,
        6: Role.SIEGE,
        7: Role.REPAIR,
    }[value]


def describe_opening(
    width: int,
    height: int,
    nearby_ore_count: int = 0,
    nearest_ore_distance: int = 999,
    wall_density: float = 0.0,
    low_degree_passable_tiles: int = 0,
    route_exposure: float = 0.0,
    estimated_enemy_distance: int = 999,
) -> OpeningDescriptor:
    width = max(0, int(width))
    height = max(0, int(height))
    return OpeningDescriptor(
        width=width,
        height=height,
        area=width * height,
        nearby_ore_count=max(0, int(nearby_ore_count)),
        nearest_ore_distance=max(0, int(nearest_ore_distance)),
        wall_density=max(0.0, min(1.0, float(wall_density))),
        low_degree_passable_tiles=max(0, int(low_degree_passable_tiles)),
        route_exposure=max(0.0, min(1.0, float(route_exposure))),
        estimated_enemy_distance=max(0, int(estimated_enemy_distance)),
    )


def choose_opening(descriptor: OpeningDescriptor) -> Opening:
    compact = descriptor.area <= 196
    near_enemy = descriptor.estimated_enemy_distance <= max(5, min(descriptor.width, descriptor.height) // 2)
    chokepoint = descriptor.wall_density >= 0.28 or descriptor.low_degree_passable_tiles >= max(
        4, descriptor.area // 18
    )
    wide = descriptor.area >= 500 or descriptor.width >= 25 or descriptor.height >= 25
    if near_enemy:
        return Opening.ANTI_RUSH
    if chokepoint:
        return Opening.CHOKEPOINT_CONTROL
    if compact:
        return Opening.COMPACT_PRESSURE
    if wide:
        return Opening.WIDE_EXPANSION
    return Opening.BALANCED_ECONOMY


def choose_phase(
    round_no: int,
    *,
    opening: Opening = Opening.BALANCED_ECONOMY,
    threat_score: int = 0,
    verified_enemy_core: bool = False,
    economy_ready: bool = False,
) -> Phase:
    round_no = int(round_no)
    if round_no >= 850:
        return Phase.ENDGAME
    if threat_score >= 5:
        return Phase.DEFENSE
    if verified_enemy_core and economy_ready and round_no >= 250:
        return Phase.OFFENSE
    if round_no < 80 or opening == Opening.ANTI_RUSH and round_no < 120:
        return Phase.OPENING
    return Phase.ECONOMY


def late_game_policy(
    round_no: int,
    *,
    verified_near_term_core_kill: bool = False,
    delivery_due: bool = False,
    route_repair_due: bool = False,
    harvester_payback_positive: bool = False,
    stored_titanium: int = 0,
    collected_titanium: int = 0,
    harvester_count: int = 0,
) -> tuple[str, ...]:
    if int(round_no) < 850:
        return ("delivery", "repair", "harvester", "defense", "combat", "stored_titanium")
    if verified_near_term_core_kill:
        return ("core_kill", "defense", "delivery", "repair", "stored_titanium")
    priorities: list[str] = []
    if delivery_due:
        priorities.append("delivery")
    if route_repair_due:
        priorities.append("repair")
    if harvester_payback_positive:
        priorities.append("harvester")
    priorities.extend(("defense", "collected_titanium", "harvester_count", "stored_titanium"))
    priorities.extend(("no_ammo_conversion", "no_paid_attack"))
    return tuple(dict.fromkeys(priorities))


def state_for_role(role: Role, route_ready: bool = False) -> BuilderState:
    if role == Role.ECONOMY:
        return BuilderState.ROUTE if route_ready else BuilderState.DISCOVER
    if role == Role.REPAIR:
        return BuilderState.MAINTAIN
    return BuilderState.DISCOVER


def nearest_position(origin: Position, positions: tuple[Position, ...] | list[Position]) -> Position | None:
    if not positions:
        return None
    return min(positions, key=lambda pos: (origin.distance_squared(pos), pos.y, pos.x))


def required_route_count(*, reachable_ore_count: int = 0, exploration_complete: bool = False, max_routes: int = REQUIRED_HEALTHY_ROUTES) -> int:
    """Require all four routes unless exhaustive exploration proves fewer exist."""
    limit = max(1, int(max_routes))
    if not exploration_complete:
        return limit
    return max(1, min(limit, max(0, int(reachable_ore_count))))


def economy_ready_for_attack(snapshot: EconomySnapshot, *, required_routes: int = REQUIRED_HEALTHY_ROUTES, stable_rounds: int = ECONOMY_READY_STABLE_ROUNDS) -> bool:
    return bool(snapshot.maintaining_routes >= max(1, int(required_routes)) and snapshot.broken_routes == 0 and snapshot.free_titanium >= ATTACK_PREPARATION_RESERVE and int(stable_rounds) >= ECONOMY_READY_STABLE_ROUNDS)


def choose_strategy_phase(
    snapshot: EconomySnapshot,
    *,
    defense_mode: DefenseMode = DefenseMode.CLEAR,
    enemy_core_fresh: bool = False,
    attack_roles_assigned: bool = False,
    free_builders: int | None = None,
    required_routes: int = REQUIRED_HEALTHY_ROUTES,
    direct_core_window: bool = False,
    stable_rounds: int = 0,
    endgame_start: int = ENDGAME_START,
) -> StrategyPhase:
    if defense_mode == DefenseMode.CRITICAL:
        return StrategyPhase.DEFENSE_ALERT
    if snapshot.round >= int(endgame_start):
        return StrategyPhase.ENDGAME
    if snapshot.maintaining_routes <= 0:
        return StrategyPhase.FIRST_ROUTE_RUSH if snapshot.active_projects else StrategyPhase.BOOTSTRAP_ECON
    if snapshot.broken_routes > 0 or snapshot.failed_projects > 0 and snapshot.maintaining_routes <= 1:
        return StrategyPhase.RECOVERY
    economy_gate = economy_ready_for_attack(snapshot, required_routes=required_routes, stable_rounds=stable_rounds)
    if defense_mode == DefenseMode.ACTIVE and economy_gate:
        return StrategyPhase.DEFENSE_ALERT
    if not economy_gate:
        return StrategyPhase.ECONOMY_EXPANSION
    if free_builders is not None and int(free_builders) <= 0:
        return StrategyPhase.ECONOMY_EXPANSION
    if not enemy_core_fresh:
        return StrategyPhase.ATTACK_PREPARATION
    if free_builders is not None and int(free_builders) < MIN_FREE_BUILDERS_FOR_OFFENSE:
        return StrategyPhase.ATTACK_PREPARATION
    if free_builders is None and not attack_roles_assigned:
        return StrategyPhase.ATTACK_PREPARATION
    if direct_core_window:
        return StrategyPhase.CORE_SIEGE
    return StrategyPhase.OFFENSIVE_PRESSURE


def choose_effective_phase(global_phase: StrategyPhase, defense_mode: DefenseMode) -> StrategyPhase:
    return StrategyPhase.DEFENSE_ALERT if defense_mode in (DefenseMode.ACTIVE, DefenseMode.CRITICAL) else global_phase


def persistent_defender_count(*, map_area: int = 0, recent_threat: bool = False) -> int:
    return PERSISTENT_DEFENDERS_LARGE if int(map_area) >= 500 or recent_threat else PERSISTENT_DEFENDERS_SMALL


def allocate_roles(
    builder_ids: tuple[int, ...] | list[int],
    *,
    phase: StrategyPhase,
    defenders: int = PERSISTENT_DEFENDERS_SMALL,
    maintenance_workers: int = MIN_MAINTENANCE_WORKERS,
    scouts: int = 1,
) -> dict[int, Role]:
    """Stable deterministic role allocation; project owners are applied by Core first."""
    ids = tuple(sorted(set(int(entity_id) for entity_id in builder_ids)))
    result: dict[int, Role] = {}
    if phase in (StrategyPhase.BOOTSTRAP_ECON, StrategyPhase.FIRST_ROUTE_RUSH, StrategyPhase.ECONOMY_EXPANSION, StrategyPhase.RECOVERY):
        for index, entity_id in enumerate(ids):
            result[entity_id] = Role.ECONOMY if index < max(1, len(ids) - max(0, int(scouts))) else Role.SCOUT
        return result
    defender_ids = ids[: max(0, min(len(ids), int(defenders)))]
    for entity_id in defender_ids:
        result[entity_id] = Role.DEFENDER
    remaining = [entity_id for entity_id in ids if entity_id not in defender_ids]
    for entity_id in remaining[: max(0, int(maintenance_workers))]:
        result[entity_id] = Role.REPAIR
    remaining = [entity_id for entity_id in remaining if entity_id not in result]
    for entity_id in remaining[: max(0, int(scouts))]:
        result[entity_id] = Role.SCOUT
    for entity_id in remaining:
        result[entity_id] = Role.SIEGE if phase == StrategyPhase.CORE_SIEGE else Role.RAIDER
    return result
