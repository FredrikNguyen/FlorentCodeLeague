
from __future__ import annotations

from fcode import EntityType, Position


def score_sabotage_target(
    entity_type: EntityType,
    *,
    loaded: bool = False,
    distance: int = 0,
    stale: bool = False,
) -> int:
    if stale:
        return -10_000
    priority = {
        EntityType.HARVESTER: 4,
        EntityType.SPLITTER: 3,
        EntityType.CONVEYOR: 2 if loaded else 1,
    }.get(entity_type, 0)
    return priority * 100 - max(0, int(distance))


def choose_rally(
    current: Position,
    *,
    verified_target: Position | None = None,
    enemy_core: Position | None = None,
    target_age: int = 0,
    max_age: int = 24,
) -> Position:
    if verified_target is not None and int(target_age) <= int(max_age):
        return verified_target
    if enemy_core is not None:
        return enemy_core
    return current


def choose_raid_action(
    targets: list[tuple[Position, EntityType, bool, int]] | tuple[tuple[Position, EntityType, bool, int], ...],
    *,
    resources: int,
    economy_reserve: int,
    attack_cost: int,
    stale_after: int = 24,
) -> tuple[Position, int] | None:
    if int(resources) - int(attack_cost) < int(economy_reserve):
        return None
    ranked = []
    for position, entity_type, loaded, age in targets:
        score = score_sabotage_target(entity_type, loaded=loaded, distance=0, stale=int(age) > stale_after)
        if score > 0:
            ranked.append((score, position))
    if not ranked:
        return None
    score, position = max(ranked, key=lambda item: (item[0], -item[1].y, -item[1].x))
    return position, score


def score_ally_insertion(
    before_distance: int,
    after_distance: int,
    *,
    threat_penalty: int = 0,
    route_penalty: int = 0,
) -> int:
    progress = int(before_distance) - int(after_distance)
    return progress - max(0, int(threat_penalty)) - max(0, int(route_penalty))


def score_enemy_ejection(
    destination: Position,
    *,
    own_core: Position,
    logistics: tuple[Position, ...] = (),
    enemy_target: Position | None = None,
) -> int:
    core_distance = destination.distance_squared(own_core)
    logistics_distance = min(
        (destination.distance_squared(position) for position in logistics),
        default=0,
    )
    target_utility = destination.distance_squared(enemy_target) if enemy_target is not None else 0
    return core_distance + logistics_distance + target_utility


def insertion_allowed(score: int) -> bool:
    return int(score) > 0

