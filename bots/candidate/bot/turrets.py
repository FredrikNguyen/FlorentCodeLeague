from __future__ import annotations

from fcode import Direction, EntityType, Position

from .actions import FACING_DIRECTIONS, TurnActions, cpu_is_safe
from .comms import Slot, decode_rally
from .offense import score_ally_insertion, score_enemy_ejection


def _entity_at(ct: object, target: Position) -> tuple[int | None, EntityType | None]:
    entity_id = None
    try:
        entity_id = ct.get_tile_building_id(target)
    except Exception:
        pass
    if entity_id is None:
        try:
            entity_id = ct.get_tile_builder_bot_id(target)
        except Exception:
            pass
    if entity_id is None:
        return None, None
    try:
        return entity_id, ct.get_entity_type(entity_id)
    except Exception:
        return entity_id, None


def _target_score(ct: object, target: Position) -> int:
    entity_id, entity_type = _entity_at(ct, target)
    if entity_type is None or entity_id is None:
        return 0
    # Hypothetical firing helpers are geometric. Explicitly exclude allied
    # entities so a Gunner never pays to rotate toward its own logistics.
    try:
        if ct.get_team(entity_id) == ct.get_team():
            return 0
    except Exception:
        return 0
    # A legal Core shot is always best because it directly advances the win
    # condition. Otherwise kill mobile enemy Builders, then dismantle economy.
    score = {
        EntityType.CORE: 2000,
        EntityType.BUILDER_BOT: 950,
        EntityType.HARVESTER: 850,
        EntityType.SPLITTER: 760,
        EntityType.CONVEYOR: 680,
        EntityType.SENTINEL: 620,
        EntityType.GUNNER: 600,
        EntityType.LAUNCHER: 560,
        EntityType.BARRIER: 300,
    }.get(entity_type, 0)
    if entity_id is not None:
        try:
            hp = max(1, int(ct.get_hp(entity_id)))
            score += max(0, 80 - hp)
        except Exception:
            pass
        if entity_type in (EntityType.CONVEYOR, EntityType.SPLITTER):
            try:
                score += 120 if ct.get_stored_resource(entity_id) is not None else 0
            except Exception:
                pass
    return score


def choose_fire_target(
    ct: object,
    targets: list[Position] | tuple[Position, ...] | None = None,
) -> Position | None:
    if not cpu_is_safe(ct):
        return None
    if targets is None:
        try:
            targets = tuple(ct.get_attackable_tiles())[:64]
        except Exception:
            return None
    best: tuple[int, Position] | None = None
    for target in tuple(targets)[:64]:
        try:
            if not ct.can_fire(target):
                continue
        except Exception:
            continue
        score = _target_score(ct, target)
        candidate = (score, target)
        if score > 0 and (
            best is None
            or (candidate[0], -target.y, -target.x) > (best[0], -best[1].y, -best[1].x)
        ):
            best = candidate
    return best[1] if best else None


def _direction_score(ct: object, position: Position, direction: Direction) -> int:
    try:
        tiles = tuple(ct.get_attackable_tiles_from(position, direction, EntityType.GUNNER))[:32]
    except Exception:
        return 0
    score = 0
    for target in tiles:
        if not cpu_is_safe(ct):
            break
        try:
            if ct.can_fire_from(position, direction, EntityType.GUNNER, target):
                score = max(score, _target_score(ct, target))
        except Exception:
            continue
    return score


def choose_gunner_rotation(ct: object) -> Direction | None:
    if not cpu_is_safe(ct):
        return None
    try:
        position = ct.get_position()
        current_direction = ct.get_direction()
        resources = int(ct.get_global_resources())
    except Exception:
        return None
    current_score = _direction_score(ct, position, current_direction)
    best_score = current_score
    best_direction = current_direction
    for direction in FACING_DIRECTIONS:
        score = _direction_score(ct, position, direction)
        if score > best_score:
            best_score = score
            best_direction = direction
    # Rotation costs 10 Ti. Never rotate on a zero/tied view and retain a modest
    # liquidity reserve for route repair and paid Builder actions.
    if best_direction == current_direction or best_score <= current_score or best_score <= 0:
        return None
    if resources < 50:
        return None
    return best_direction


def _default_destinations(ct: object, origin: Position) -> tuple[Position, ...]:
    try:
        width = int(ct.get_map_width())
        height = int(ct.get_map_height())
    except Exception:
        return ()
    # The old radius-by-radius early return filled the 24-candidate budget with
    # tiles at distance one or two, wasting most of the Launcher's r^2=26 throw.
    # Enumerate the full legal disk and consider long throws first.
    destinations = [
        Position(origin.x + dx, origin.y + dy)
        for dy in range(-5, 6)
        for dx in range(-5, 6)
        if 0 < dx * dx + dy * dy <= 26
        and 0 <= origin.x + dx < width
        and 0 <= origin.y + dy < height
    ]
    destinations.sort(
        key=lambda position: (-origin.distance_squared(position), position.y, position.x)
    )
    return tuple(destinations)


def choose_launch(
    ct: object,
    pickup_tiles: list[Position] | tuple[Position, ...] | None = None,
    destinations: list[Position] | tuple[Position, ...] | None = None,
    *,
    enemy_target: Position | None = None,
    own_core: Position | None = None,
    logistics: tuple[Position, ...] = (),
) -> tuple[Position, Position, int] | None:
    if not cpu_is_safe(ct):
        return None
    try:
        origin = ct.get_position()
        own_team = ct.get_team()
    except Exception:
        return None
    if pickup_tiles is None:
        pickup_tiles = tuple(
            Position(origin.x + dx, origin.y + dy)
            for dy in (-1, 0, 1)
            for dx in (-1, 0, 1)
            if dx or dy
        )
    if destinations is None:
        destinations = _default_destinations(ct, origin)
    best: tuple[int, Position, Position] | None = None
    for pickup in tuple(pickup_tiles)[:8]:
        if not cpu_is_safe(ct):
            break
        try:
            builder_id = ct.get_tile_builder_bot_id(pickup)
            builder_team = ct.get_team(builder_id) if builder_id is not None else None
        except Exception:
            builder_id = builder_team = None
        if builder_id is None:
            continue
        for destination in tuple(destinations)[:64]:
            if not cpu_is_safe(ct):
                break
            try:
                if not ct.can_launch(pickup, destination):
                    continue
            except Exception:
                continue
            if builder_team == own_team and enemy_target is not None:
                score = score_ally_insertion(
                    pickup.distance_squared(enemy_target),
                    destination.distance_squared(enemy_target),
                )
            elif builder_team != own_team:
                if own_core is not None:
                    score = score_enemy_ejection(
                        destination,
                        own_core=own_core,
                        logistics=logistics,
                        enemy_target=enemy_target,
                    )
                else:
                    # Forward Launchers often cannot see the home Core. They
                    # should still clear an adjacent hostile body-blocker: throw
                    # it as far from the Launcher and shared assault rally as the
                    # legal destination set permits.
                    score = 4 * origin.distance_squared(destination)
                    if enemy_target is not None:
                        score += destination.distance_squared(enemy_target)
                        score -= pickup.distance_squared(enemy_target)
            else:
                continue
            if best is None or (score, -pickup.y, -pickup.x, -destination.y, -destination.x) > (
                best[0],
                -best[1].y,
                -best[1].x,
                -best[2].y,
                -best[2].x,
            ):
                best = (score, pickup, destination)
    if best is None or best[0] <= 0:
        return None
    return best[1], best[2], best[0]


def run_gunner(ct: object) -> None:
    actions = TurnActions(ct)
    target = choose_fire_target(ct)
    if target is not None and actions.fire(target):
        return
    direction = choose_gunner_rotation(ct)
    if direction is not None:
        actions.rotate(direction)


def run_sentinel(ct: object) -> None:
    actions = TurnActions(ct)
    target = choose_fire_target(ct)
    if target is not None:
        actions.fire(target)


def _fresh_rally(ct: object) -> Position | None:
    try:
        decoded = decode_rally(
            ct.read_store(int(Slot.RALLY)),
            int(ct.get_map_width()),
            int(ct.get_map_height()),
        )
        round_no = int(ct.get_current_round()) & 63
    except Exception:
        return None
    if decoded is None:
        return None
    position, expires, priority = decoded
    forward = (int(expires) - round_no) & 63
    horizon = 30 if int(priority) >= 15 else 8
    return position if position is not None and forward <= horizon else None


def _own_core(ct: object) -> Position | None:
    try:
        own_team = ct.get_team()
        positions = [
            ct.get_position(entity_id)
            for entity_id in tuple(ct.get_nearby_buildings())[:64]
            if ct.get_entity_type(entity_id) == EntityType.CORE
            and ct.get_team(entity_id) == own_team
        ]
    except Exception:
        return None
    return min(positions, key=lambda position: (position.y, position.x)) if positions else None


def run_launcher(ct: object) -> None:
    rally = _fresh_rally(ct)
    own_core = _own_core(ct)
    logistics: list[Position] = []
    if own_core is not None:
        try:
            own_team = ct.get_team()
            for entity_id in tuple(ct.get_nearby_buildings())[:32]:
                if ct.get_team(entity_id) == own_team and ct.get_entity_type(entity_id) in (
                    EntityType.CONVEYOR,
                    EntityType.SPLITTER,
                ):
                    logistics.append(ct.get_position(entity_id))
        except Exception:
            logistics = []
    choice = choose_launch(
        ct,
        enemy_target=rally,
        own_core=own_core,
        logistics=tuple(logistics),
    )
    if choice is not None:
        TurnActions(ct).launch(choice[0], choice[1])
