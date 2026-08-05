
from __future__ import annotations

from fcode import Direction, EntityType, Position

from .actions import TurnActions, cpu_is_safe
from .comms import Slot, decode_alert, epoch_distance
from .offense import score_ally_insertion, score_enemy_ejection, score_sabotage_target


CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


def _entity_at(ct: object, target: Position) -> tuple[int | None, EntityType | None]:
    entity_id = None
    try:
        entity_id = ct.get_tile_building_id(target)
    except Exception: pass
    if entity_id is None:
        try:
            entity_id = ct.get_tile_builder_bot_id(target)
        except Exception: pass
    if entity_id is None:
        return None, None
    try: return entity_id, ct.get_entity_type(entity_id)
    except Exception: return entity_id, None


def choose_fire_target(ct: object, targets: list[Position] | tuple[Position, ...] | None = None) -> Position | None:
    if not cpu_is_safe(ct): return None
    if targets is None:
        try:
            targets = tuple(ct.get_attackable_tiles())
        except Exception: return None
    ranked: list[tuple[int, Position]] = []
    for target in tuple(targets)[:64]:
        try:
            legal = bool(ct.can_fire(target))
        except Exception: legal = False
        if not legal: continue
        _, entity_type = _entity_at(ct, target)
        if entity_type is None: continue
        priority = {
            EntityType.CORE: 500,
            EntityType.HARVESTER: 420,
            EntityType.SPLITTER: 320,
            EntityType.CONVEYOR: 220,
            EntityType.BUILDER_BOT: 180,
            EntityType.SENTINEL: 160,
            EntityType.GUNNER: 150,
            EntityType.LAUNCHER: 140,
            EntityType.BARRIER: 80,
        }.get(entity_type, 0)
        priority += score_sabotage_target(entity_type, distance=0) if entity_type in (
            EntityType.HARVESTER,
            EntityType.SPLITTER,
            EntityType.CONVEYOR,
        ) else 0
        if priority > 0: ranked.append((priority, target))
    if not ranked: return None
    return max(ranked, key=lambda item: (item[0], -item[1].y, -item[1].x))[1]


def choose_gunner_rotation(ct: object) -> Direction | None:
    if not cpu_is_safe(ct): return None
    try:
        position = ct.get_position()
    except Exception: return None
    choices: list[tuple[int, Direction]] = []
    for direction in CARDINALS:
        try:
            tiles = tuple(ct.get_attackable_tiles_from(position, direction, EntityType.GUNNER))[:32]
        except Exception: continue
        count = 0
        for target in tiles:
            try:
                if ct.can_fire_from(position, direction, EntityType.GUNNER, target):
                    count += 1
            except Exception: continue
        choices.append((count, direction))
    if not choices: return None
    return max(choices, key=lambda item: (item[0], -CARDINALS.index(item[1])))[1]


def _default_destinations(ct: object, origin: Position) -> tuple[Position, ...]:
    try:
        width = int(ct.get_map_width())
        height = int(ct.get_map_height())
    except Exception: return ()
    destinations: list[Position] = []
    seen: set[Position] = set()
    for radius in range(1, 6):
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy > 26 or (dx == 0 and dy == 0): continue
                position = Position(origin.x + dx, origin.y + dy)
                if position in seen or not (0 <= position.x < width and 0 <= position.y < height): continue
                seen.add(position)
                destinations.append(position)
                if len(destinations) >= 32:
                    return tuple(destinations)
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
    if not cpu_is_safe(ct): return None
    try:
        origin = ct.get_position()
    except Exception: return None
    if pickup_tiles is None:
        pickup_tiles = tuple(
            Position(origin.x + dx, origin.y + dy)
            for dy in (-1, 0, 1)
            for dx in (-1, 0, 1)
            if dx or dy
        )
    pickup_tiles = tuple(pickup_tiles)[:8]
    if destinations is None:
        destinations = _default_destinations(ct, origin)
    destinations = tuple(destinations)[:32]
    try:
        own_team = ct.get_team()
    except Exception: own_team = None
    best: tuple[int, Position, Position] | None = None
    for pickup in pickup_tiles:
        if not cpu_is_safe(ct):
            return (best[1], best[2], best[0]) if best and best[0] > 0 else None
        try:
            builder_id = ct.get_tile_builder_bot_id(pickup)
            builder_team = ct.get_team(builder_id) if builder_id is not None else None
        except Exception: builder_id, builder_team = None, None
        if builder_id is None: continue
        for destination in destinations:
            if not cpu_is_safe(ct):
                return (best[1], best[2], best[0]) if best and best[0] > 0 else None
            try:
                if not ct.can_launch(pickup, destination): continue
            except Exception: continue
            if own_team is not None and builder_team == own_team:
                if enemy_target is None: continue
                score = score_ally_insertion(pickup.distance_squared(enemy_target), destination.distance_squared(enemy_target))
            elif own_core is not None and (enemy_target is not None or logistics):
                score = score_enemy_ejection(destination, own_core=own_core, logistics=logistics, enemy_target=enemy_target)
            else:
                continue
            candidate_key = (score, -pickup.y, -pickup.x, -destination.y, -destination.x)
            best_key = None if best is None else (best[0], -best[1].y, -best[1].x, -best[2].y, -best[2].x)
            if best is None or candidate_key > best_key: best = (score, pickup, destination)
    if best is None or best[0] <= 0: return None
    return best[1], best[2], best[0]


def run_gunner(ct: object) -> None:
    actions = TurnActions(ct)
    target = choose_fire_target(ct)
    if target is not None and actions.fire(target): return
    direction = choose_gunner_rotation(ct)
    if direction is not None: actions.rotate(direction)


def run_sentinel(ct: object) -> None:
    actions = TurnActions(ct)
    target = choose_fire_target(ct)
    if target is not None: actions.fire(target)


def _observed_enemy_target(ct: object, target: Position) -> bool:
    try:
        own_team = ct.get_team()
        entity_ids = tuple(ct.get_nearby_entities())[:64]
    except Exception:
        try:
            own_team = ct.get_team()
            entity_ids = tuple(ct.get_nearby_buildings())[:64] + tuple(ct.get_nearby_units())[:64]
        except Exception: return False
    for entity_id in entity_ids:
        if not cpu_is_safe(ct): return False
        try:
            if ct.get_team(entity_id) != own_team and ct.get_position(entity_id) == target: return True
        except Exception: continue
    return False


def _fresh_rally(ct: object) -> Position | None:
    try:
        width, height = int(ct.get_map_width()), int(ct.get_map_height())
        decoded = decode_alert(ct.read_store(int(Slot.RALLY)), width, height)
        round_no = int(ct.get_current_round()) & 63
    except Exception: return None
    if decoded is None: return None
    position, expires_epoch = decoded
    if position is None or epoch_distance(expires_epoch, round_no) > 8: return None
    return position if _observed_enemy_target(ct, position) else None


def _own_core(ct: object) -> Position | None:
    try:
        own_team = ct.get_team()
        positions = []
        for entity_id in tuple(ct.get_nearby_buildings())[:64]:
            if not cpu_is_safe(ct): break
            if ct.get_entity_type(entity_id) == EntityType.CORE and ct.get_team(entity_id) == own_team: positions.append(ct.get_position(entity_id))
    except Exception: return None
    return min(positions, key=lambda position: (position.y, position.x)) if positions else None


def run_launcher(ct: object) -> None:
    rally = _fresh_rally(ct)
    own_core = _own_core(ct)
    logistics: list[Position] = []
    if own_core is not None:
        try:
            own_team = ct.get_team()
            for entity_id in tuple(ct.get_nearby_buildings())[:32]:
                if not cpu_is_safe(ct): break
                if ct.get_team(entity_id) != own_team: continue
                if ct.get_entity_type(entity_id) in (EntityType.CONVEYOR, EntityType.SPLITTER): logistics.append(ct.get_position(entity_id))
        except Exception: logistics = []
    choice = choose_launch(ct, enemy_target=rally, own_core=own_core, logistics=tuple(logistics))
    if choice is None: return
    pickup, destination, _ = choice
    TurnActions(ct).launch(pickup, destination)
