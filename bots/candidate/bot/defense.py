
from __future__ import annotations

from fcode import Direction, EntityType, Position

from .types import Threat, ThreatKind


def assess_threat(
    *,
    position: Position = Position(0, 0),
    enemy_builder_distance: int = 999,
    firing_line: bool = False,
    sabotage: bool = False,
    core_hp_delta: int = 0,
    alert_age: int = 0,
    current_round: int = 0,
    entity_type: EntityType | None = None,
) -> Threat | None:
    scores = [
        max(0, 12 - max(0, int(enemy_builder_distance))),
        5 if firing_line else 0,
        4 if sabotage else 0,
        max(0, -int(core_hp_delta) // 2),
        max(0, 3 - int(alert_age) // 4),
    ]
    score = sum(scores)
    if score <= 0:
        return None
    kind = (
        ThreatKind.BUILDER_RUSH
        if enemy_builder_distance < 8
        else ThreatKind.FIRING_LINE
        if firing_line
        else ThreatKind.SABOTAGE
        if sabotage
        else ThreatKind.CORE_DAMAGE
    )
    return Threat(position, kind, score, int(current_round), int(current_round) + 3, entity_type)


def score_defense_placement(
    position: Position,
    turret_type: EntityType,
    *,
    threat: Threat | None = None,
    attackable_count: int = 0,
    reserved_core_exits: set[Position] | frozenset[Position] = frozenset(),
    route_cells: set[Position] | frozenset[Position] = frozenset(),
    escape_tiles: set[Position] | frozenset[Position] = frozenset(),
) -> int:
    if position in reserved_core_exits or position in route_cells or position in escape_tiles:
        return -10_000
    score = max(0, int(attackable_count)) * 3
    if turret_type == EntityType.SENTINEL:
        score += 4
    elif turret_type == EntityType.GUNNER:
        score += 2
    if threat is not None:
        score += threat.score
        score -= position.distance_squared(threat.position)
    return score


def choose_turret_type(
    *,
    lane_length: int = 0,
    wall_crossing: bool = False,
    durable_anchor: bool = False,
    changing_corridor: bool = False,
    threat_score: int = 0,
) -> EntityType:
    if wall_crossing or durable_anchor or int(lane_length) >= 6:
        return EntityType.SENTINEL
    if changing_corridor or threat_score > 0:
        return EntityType.GUNNER
    return EntityType.GUNNER if int(lane_length) < 6 else EntityType.SENTINEL


def choose_defensive_build(
    positions: list[Position] | tuple[Position, ...],
    *,
    threat: Threat | None = None,
    lane_length: int = 0,
    wall_crossing: bool = False,
    durable_anchor: bool = False,
    changing_corridor: bool = True,
    reserved_core_exits: set[Position] | frozenset[Position] = frozenset(),
    route_cells: set[Position] | frozenset[Position] = frozenset(),
    escape_tiles: set[Position] | frozenset[Position] = frozenset(),
    attackable: dict[tuple[Position, Direction], int] | None = None,
) -> tuple[Position, EntityType, Direction, int] | None:
    turret_type = choose_turret_type(
        lane_length=lane_length,
        wall_crossing=wall_crossing,
        durable_anchor=durable_anchor,
        changing_corridor=changing_corridor,
        threat_score=threat.score if threat else 0,
    )
    candidates: list[tuple[int, Position, Direction]] = []
    for position in sorted(positions, key=lambda pos: (pos.y, pos.x)):
        for direction in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            count = 0 if attackable is None else int(attackable.get((position, direction), 0))
            score = score_defense_placement(
                position,
                turret_type,
                threat=threat,
                attackable_count=count,
                reserved_core_exits=reserved_core_exits,
                route_cells=route_cells,
                escape_tiles=escape_tiles,
            )
            if score > -10_000:
                candidates.append((score, position, direction))
    if not candidates:
        return None
    score, position, direction = max(candidates, key=lambda item: (item[0], -item[1].y, -item[1].x, item[2].value))
    return position, turret_type, direction, score

