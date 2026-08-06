
from __future__ import annotations

from dataclasses import dataclass, field

from fcode import Direction, EntityType, Position

from .comms import Slot, decode_alert, encode_alert, epoch_distance
from .types import AttackObjective, EnemyTarget, OffenseState


ATTACK_NO_PROGRESS_ROUNDS = 20
OFFENSE_REGROUP_ROUNDS = 12
MIN_ATTACKERS_TO_PRESS = 2
FORWARD_TURRET_MIN_SCORE = 1


@dataclass(slots=True)
class OffenseStateData:
    state: OffenseState = OffenseState.IDLE
    target: EnemyTarget | None = None
    objective: AttackObjective | None = None
    rally: Position | None = None
    objective_epoch: int = 0
    last_progress_round: int = 0
    paid_attacks: int = 0
    damage_observed: int = 0
    retreat_reason: str | None = None
    cooldown_until: int = 0


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


def enemy_target_from_observation(
    position: Position,
    entity_type: EntityType,
    *,
    current_round: int = 0,
    hp: int | None = None,
    confidence: int = 0,
    source_id: int = 0,
) -> EnemyTarget:
    return EnemyTarget(position, entity_type, int(current_round), hp, max(0, min(100, int(confidence))), int(source_id))


def target_stale(target: EnemyTarget, current_round: int, *, ttl: int = 24) -> bool:
    return int(current_round) - int(target.last_seen_round) > max(0, int(ttl))


def score_offensive_target(
    target: EnemyTarget,
    *,
    current_round: int | None = None,
    loaded: bool = False,
    connectivity_cut: int = 0,
    approach_cost: int = 0,
    turret_exposure: int = 0,
    direct_core_window: bool = False,
) -> int:
    base = {
        EntityType.CONVEYOR: 30,
        EntityType.SPLITTER: 55,
        EntityType.HARVESTER: 50,
        EntityType.BARRIER: 35,
        EntityType.GUNNER: 44,
        EntityType.SENTINEL: 48,
        EntityType.LAUNCHER: 46,
        EntityType.CORE: 30,
    }.get(target.entity_type, 0)
    if loaded and target.entity_type == EntityType.CONVEYOR:
        base += 24
    base += max(0, int(connectivity_cut)) * 10 + max(0, int(target.confidence)) // 10
    if direct_core_window and target.entity_type == EntityType.CORE:
        base += 500
    base -= max(0, int(approach_cost)) + max(0, int(turret_exposure))
    return base if current_round is None or not target_stale(target, current_round) else -10_000


def choose_offensive_target(
    targets: list[EnemyTarget] | tuple[EnemyTarget, ...],
    *,
    current_round: int = 0,
    direct_core_window: bool = False,
    crippled_economy: bool = False,
) -> EnemyTarget | None:
    ranked: list[tuple[int, EnemyTarget]] = []
    for target in tuple(targets)[:96]:
        if target_stale(target, current_round):
            continue
        loaded = target.entity_type == EntityType.CONVEYOR and target.confidence >= 70
        cut = 3 if target.entity_type == EntityType.SPLITTER else 2 if target.entity_type == EntityType.CONVEYOR else 0
        score = score_offensive_target(target, current_round=current_round, loaded=loaded, connectivity_cut=cut, direct_core_window=direct_core_window and crippled_economy)
        if score > 0:
            ranked.append((score, target))
    if not ranked:
        return None
    return max(ranked, key=lambda item: (item[0], -item[1].position.y, -item[1].position.x, -item[1].source_id))[1]


def target_is_enemy_building(ct: object, target: EnemyTarget | Position) -> bool:
    position = target.position if isinstance(target, EnemyTarget) else target
    try:
        entity_id = ct.get_tile_building_id(position)
        return entity_id is not None and ct.get_team(entity_id) != ct.get_team() and ct.get_entity_type(entity_id) != EntityType.BUILDER_BOT
    except Exception:
        return False


def try_builder_attack(ct: object, target: EnemyTarget | Position, *, free_attack_titanium: int, attack_cost: int = 2) -> bool:
    position = target.position if isinstance(target, EnemyTarget) else target
    if int(free_attack_titanium) < int(attack_cost) or not target_is_enemy_building(ct, position):
        return False
    try:
        if ct.get_position().distance_squared(position) != 1 or not ct.can_fire(position):
            return False
        ct.fire(position)
    except Exception:
        return False
    return True


def choose_attack_stance(
    origin: Position,
    target: Position,
    *,
    candidates: list[Position] | tuple[Position, ...] = (),
    turret_exposure: dict[Position, int] | None = None,
    congestion: dict[Position, int] | None = None,
) -> Position | None:
    available = tuple(candidates) or tuple(target.add(direction) for direction in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST))
    legal = tuple(position for position in available if position.distance_squared(target) == 1)
    if not legal:
        return None
    turret_exposure = turret_exposure or {}
    congestion = congestion or {}
    return min(legal, key=lambda position: (origin.distance_squared(position) + turret_exposure.get(position, 0) * 4 + congestion.get(position, 0) * 2, position.y, position.x))


def choose_forward_turret_site(
    positions: list[Position] | tuple[Position, ...],
    *,
    target: EnemyTarget,
    firing_lanes: dict[tuple[Position, Direction], int] | None = None,
    home_reserve: int = 0,
    construction_cost: int = 0,
    ammo_reserve: int = 0,
) -> tuple[Position, Direction, int] | None:
    if int(home_reserve) < int(construction_cost) + int(ammo_reserve):
        return None
    firing_lanes = firing_lanes or {}
    candidates = []
    for position in sorted(positions, key=lambda pos: (pos.y, pos.x)):
        for direction in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            lane = int(firing_lanes.get((position, direction), 0))
            score = lane * 20 - min(20, position.distance_squared(target.position))
            if score >= FORWARD_TURRET_MIN_SCORE:
                candidates.append((score, position, direction))
    if not candidates:
        return None
    score, position, direction = max(candidates, key=lambda item: (item[0], -item[1].y, -item[1].x, -(Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST).index(item[2])))
    return position, direction, score


def choose_forward_turret_type(*, lane_length: int, wall_crossing: bool = False) -> EntityType:
    return EntityType.SENTINEL if wall_crossing or int(lane_length) >= 6 else EntityType.GUNNER


def should_retreat(
    *,
    current_round: int,
    last_progress_round: int,
    target_fresh: bool,
    attackers_remaining: int,
    minimum_attackers: int = MIN_ATTACKERS_TO_PRESS,
    home_threat_critical: bool = False,
    budget_exhausted: bool = False,
) -> bool:
    return bool(home_threat_critical or budget_exhausted or not target_fresh or attackers_remaining < int(minimum_attackers) or int(current_round) - int(last_progress_round) >= ATTACK_NO_PROGRESS_ROUNDS)


def publish_verified_enemy_core(ct: object, target: Position, *, confidence: int = 100) -> bool:
    try:
        own_team = ct.get_team()
        entity_id = ct.get_tile_building_id(target)
        if entity_id is None or ct.get_team(entity_id) == own_team or ct.get_entity_type(entity_id) != EntityType.CORE:
            return False
        width, height = int(ct.get_map_width()), int(ct.get_map_height())
        ct.write_store(int(Slot.ENEMY_CORE), encode_alert(target, width, (int(ct.get_current_round()) + max(1, confidence // 10)) & 63))
    except Exception:
        return False
    return True


def read_verified_enemy_core(ct: object, *, max_age: int = 24) -> Position | None:
    try:
        decoded = decode_alert(ct.read_store(int(Slot.ENEMY_CORE)), int(ct.get_map_width()), int(ct.get_map_height()))
        now = int(ct.get_current_round()) & 63
    except Exception:
        return None
    if decoded is None:
        return None
    position, expiry = decoded
    return position if position is not None and epoch_distance(expiry, now) <= int(max_age) else None


def update_attack_objective(
    state: OffenseStateData,
    targets: list[EnemyTarget] | tuple[EnemyTarget, ...],
    *,
    current_round: int,
    direct_core_window: bool = False,
    crippled_economy: bool = False,
) -> OffenseStateData:
    target = choose_offensive_target(targets, current_round=current_round, direct_core_window=direct_core_window, crippled_economy=crippled_economy)
    state.target = target
    state.objective = None if target is None else AttackObjective(target, OffenseState.APPROACHING_OBJECTIVE, state.objective_epoch, score_offensive_target(target, current_round=current_round, direct_core_window=direct_core_window, crippled_economy=crippled_economy))
    state.state = OffenseState.SCOUTING if target is None else (OffenseState.PRESSURING_CORE if target.entity_type == EntityType.CORE else OffenseState.SABOTAGING_LOGISTICS)
    return state


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
