
from __future__ import annotations

from fcode import Position

from .types import BuilderState, Opening, OpeningDescriptor, Phase, Role


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
