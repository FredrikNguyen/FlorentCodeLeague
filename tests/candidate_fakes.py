from __future__ import annotations

from dataclasses import dataclass

from fcode import Direction, EntityType, Environment, Position, ResourceType, Team


@dataclass
class FakeEntity:
    entity_type: EntityType
    position: Position
    team: Team
    direction: Direction | None = None
    hp: int = 40
    max_hp: int = 40
    stored: bool = False


class FakeController:
    """Deterministic Controller double covering the candidate API surface."""

    def __init__(
        self,
        entity_type: EntityType = EntityType.BUILDER_BOT,
        *,
        width: int = 10,
        height: int = 10,
        position: Position = Position(1, 1),
        team: Team = Team.A,
        terrain: dict[Position, Environment] | None = None,
    ) -> None:
        self.width, self.height = width, height
        self.round = 0
        self.resources = 500
        self.ammo = 0
        self.cpu = 0
        self.terrain = dict(terrain or {})
        self.calls: list[tuple[object, ...]] = []
        self.denied: set[str] = set()
        self.entities: dict[int, FakeEntity] = {
            1: FakeEntity(entity_type, position, team, Direction.EAST)
        }
        self.self_id = 1
        self.next_id = 10
        self.store = [0] * 16
        self.pending: dict[int, int] = {}
        self.cooldown = 0
        self.move_cooldown = 0
        self.fail_run = False

    def _self(self) -> FakeEntity:
        return self.entities[self.self_id]

    def _allowed(self, name: str) -> bool:
        return name not in self.denied

    def _adjacent(self, position: Position) -> bool:
        current = self._self().position
        return abs(current.x - position.x) + abs(current.y - position.y) == 1

    def _in_bounds(self, position: Position) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def get_team(self, entity_id: int | None = None) -> Team:
        return self.entities[self.self_id if entity_id is None else entity_id].team

    def get_position(self, entity_id: int | None = None) -> Position:
        return self.entities[self.self_id if entity_id is None else entity_id].position

    def get_id(self) -> int:
        return self.self_id

    def get_action_cooldown(self) -> int:
        return self.cooldown

    def get_move_cooldown(self) -> int:
        return self.move_cooldown

    def can_act(self) -> bool:
        return self.cooldown == 0 and self._allowed("act")

    def get_vision_radius_sq(self, entity_id: int | None = None) -> int:
        return 1000

    def get_hp(self, entity_id: int | None = None) -> int:
        return self.entities[self.self_id if entity_id is None else entity_id].hp

    def get_max_hp(self, entity_id: int | None = None) -> int:
        return self.entities[self.self_id if entity_id is None else entity_id].max_hp

    def get_entity_type(self, entity_id: int | None = None) -> EntityType:
        return self.entities[self.self_id if entity_id is None else entity_id].entity_type

    def get_direction(self, entity_id: int | None = None) -> Direction:
        direction = self.entities[self.self_id if entity_id is None else entity_id].direction
        if direction is None:
            raise ValueError("no direction")
        return direction

    def get_stored_resource(self, entity_id: int | None = None) -> ResourceType | None:
        entity = self.entities[self.self_id if entity_id is None else entity_id]
        return ResourceType.TITANIUM if entity.stored else None

    def get_stored_resource_id(self, entity_id: int | None = None) -> int | None:
        return 1 if self.get_stored_resource(entity_id) else None

    def get_tile_env(self, position: Position) -> Environment:
        return self.terrain.get(position, Environment.EMPTY)

    def get_tile_building_id(self, position: Position) -> int | None:
        for entity_id, entity in self.entities.items():
            if entity.position == position and entity.entity_type != EntityType.BUILDER_BOT:
                return entity_id
        return None

    def get_tile_builder_bot_id(self, position: Position) -> int | None:
        for entity_id, entity in self.entities.items():
            if entity.position == position and entity.entity_type == EntityType.BUILDER_BOT:
                return entity_id
        return None

    def is_tile_empty(self, position: Position) -> bool:
        return self._in_bounds(position) and self.get_tile_env(position) != Environment.WALL and self.get_tile_building_id(position) is None and self.get_tile_builder_bot_id(position) is None

    def is_tile_passable(self, position: Position) -> bool:
        if not self._in_bounds(position) or self.get_tile_env(position) == Environment.WALL:
            return False
        building = self.get_tile_building_id(position)
        return self.get_tile_builder_bot_id(position) is None and (
            building is None or self.get_entity_type(building) in (EntityType.CONVEYOR, EntityType.SPLITTER)
        )

    def is_in_vision(self, position: Position) -> bool:
        return self._in_bounds(position)

    def get_nearby_tiles(self, dist_sq: int | None = None) -> list[Position]:
        positions = [Position(x, y) for y in range(self.height) for x in range(self.width)]
        if dist_sq is None:
            return positions
        origin = self.get_position()
        return [position for position in positions if origin.distance_squared(position) <= dist_sq]

    def get_nearby_entities(self, dist_sq: int | None = None) -> list[int]:
        return self._nearby_ids(dist_sq, include_buildings=True, include_units=True)

    def get_nearby_buildings(self, dist_sq: int | None = None) -> list[int]:
        return self._nearby_ids(dist_sq, include_buildings=True, include_units=False)

    def get_nearby_units(self, dist_sq: int | None = None) -> list[int]:
        return self._nearby_ids(dist_sq, include_buildings=False, include_units=True)

    def _nearby_ids(self, dist_sq: int | None, *, include_buildings: bool, include_units: bool) -> list[int]:
        origin = self.get_position()
        result = []
        buildings = {EntityType.CORE, EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER, EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.HARVESTER, EntityType.BARRIER}
        for entity_id, entity in self.entities.items():
            is_building = entity.entity_type in buildings
            if (is_building and not include_buildings) or (not is_building and not include_units):
                continue
            if dist_sq is None or origin.distance_squared(entity.position) <= dist_sq:
                result.append(entity_id)
        return result

    def get_map_width(self) -> int:
        return self.width

    def get_map_height(self) -> int:
        return self.height

    def get_current_round(self) -> int:
        return self.round

    def get_global_resources(self) -> int:
        return self.resources

    def get_global_ammo(self) -> int:
        return self.ammo

    def can_convert_ammo(self, amount: int) -> bool:
        return self._allowed("convert") and amount > 0 and amount <= self.resources

    def convert_ammo(self, amount: int) -> None:
        self.calls.append(("convert_ammo", amount))
        self.resources -= amount
        self.ammo += amount

    def get_scale_percent(self) -> float:
        return 100.0

    def get_cpu_time_elapsed(self) -> int:
        return self.cpu

    def get_conveyor_cost(self) -> int:
        return 3

    def get_splitter_cost(self) -> int:
        return 6

    def get_harvester_cost(self) -> int:
        return 20

    def get_barrier_cost(self) -> int:
        return 3

    def get_gunner_cost(self) -> int:
        return 20

    def get_sentinel_cost(self) -> int:
        return 30

    def get_launcher_cost(self) -> int:
        return 20

    def get_builder_bot_cost(self) -> int:
        return 30

    def get_unit_count(self) -> int:
        return sum(1 for entity in self.entities.values() if entity.entity_type != EntityType.HARVESTER)

    def can_move(self, direction: Direction) -> bool:
        target = self.get_position().add(direction)
        return self._allowed("move") and direction.is_cardinal() and self.move_cooldown == 0 and self.is_tile_passable(target)

    def move(self, direction: Direction) -> None:
        self.calls.append(("move", direction))
        if not self.can_move(direction):
            raise ValueError("illegal move")
        self._self().position = self._self().position.add(direction)
        self.move_cooldown = 1

    def _can_build(self, entity_type: EntityType, position: Position, direction: Direction | None = None) -> bool:
        return self._allowed("build") and self.can_act() and self._adjacent(position) and self.is_tile_empty(position) and (direction is None or direction.is_cardinal())

    def _build(self, entity_type: EntityType, position: Position, direction: Direction | None = None) -> int:
        if not self._can_build(entity_type, position, direction):
            raise ValueError("illegal build")
        entity_id = self.next_id
        self.next_id += 1
        self.entities[entity_id] = FakeEntity(entity_type, position, self.get_team(), direction, 30, 30)
        self.calls.append(("build", entity_type, position, direction))
        self.resources -= 1
        self.cooldown = 1
        return entity_id

    def can_build_conveyor(self, position: Position, direction: Direction) -> bool:
        return self._can_build(EntityType.CONVEYOR, position, direction)

    def can_build_splitter(self, position: Position, direction: Direction) -> bool:
        return self._can_build(EntityType.SPLITTER, position, direction)

    def can_build_harvester(self, position: Position) -> bool:
        return self._can_build(EntityType.HARVESTER, position) and self.get_tile_env(position) == Environment.ORE_TITANIUM

    def can_build_barrier(self, position: Position) -> bool:
        return self._can_build(EntityType.BARRIER, position)

    def can_build_gunner(self, position: Position, direction: Direction) -> bool:
        return self._can_build(EntityType.GUNNER, position, direction)

    def can_build_sentinel(self, position: Position, direction: Direction) -> bool:
        return self._can_build(EntityType.SENTINEL, position, direction)

    def can_build_launcher(self, position: Position) -> bool:
        return self._can_build(EntityType.LAUNCHER, position)

    def build_conveyor(self, position: Position, direction: Direction) -> int:
        return self._build(EntityType.CONVEYOR, position, direction)

    def build_splitter(self, position: Position, direction: Direction) -> int:
        return self._build(EntityType.SPLITTER, position, direction)

    def build_harvester(self, position: Position) -> int:
        return self._build(EntityType.HARVESTER, position)

    def build_barrier(self, position: Position) -> int:
        return self._build(EntityType.BARRIER, position)

    def build_gunner(self, position: Position, direction: Direction) -> int:
        return self._build(EntityType.GUNNER, position, direction)

    def build_sentinel(self, position: Position, direction: Direction) -> int:
        return self._build(EntityType.SENTINEL, position, direction)

    def build_launcher(self, position: Position) -> int:
        return self._build(EntityType.LAUNCHER, position)

    def can_build(self, entity_type: EntityType, position: Position, extra=None) -> bool:
        if entity_type == EntityType.CONVEYOR:
            return self.can_build_conveyor(position, extra)
        if entity_type == EntityType.SPLITTER:
            return self.can_build_splitter(position, extra)
        if entity_type == EntityType.HARVESTER:
            return self.can_build_harvester(position)
        if entity_type == EntityType.BARRIER:
            return self.can_build_barrier(position)
        if entity_type == EntityType.GUNNER:
            return self.can_build_gunner(position, extra)
        if entity_type == EntityType.SENTINEL:
            return self.can_build_sentinel(position, extra)
        return self.can_build_launcher(position)

    def build(self, entity_type: EntityType, position: Position, extra=None) -> int:
        if not self.can_build(entity_type, position, extra):
            raise ValueError("illegal build")
        return self._build(entity_type, position, extra if isinstance(extra, Direction) else None)

    def can_heal(self, position: Position) -> bool:
        return self._allowed("heal") and self.can_act() and self._adjacent(position)

    def heal(self, position: Position) -> None:
        if not self.can_heal(position):
            raise ValueError("illegal heal")
        self.calls.append(("heal", position))

    def can_destroy(self, position: Position) -> bool:
        return self._allowed("destroy") and self._adjacent(position) and self.get_tile_building_id(position) is not None

    def destroy(self, position: Position) -> None:
        if not self.can_destroy(position):
            raise ValueError("illegal destroy")
        entity_id = self.get_tile_building_id(position)
        self.entities.pop(entity_id, None)
        self.calls.append(("destroy", position))

    def can_fire(self, target: Position) -> bool:
        return self._allowed("fire") and self.can_act() and self._adjacent(target)

    def fire(self, target: Position) -> None:
        if not self.can_fire(target):
            raise ValueError("illegal fire")
        self.calls.append(("fire", target))

    def can_rotate(self, direction: Direction) -> bool:
        return self._allowed("rotate") and self.can_act() and direction.is_cardinal()

    def rotate(self, direction: Direction) -> None:
        if not self.can_rotate(direction):
            raise ValueError("illegal rotate")
        self._self().direction = direction
        self.calls.append(("rotate", direction))

    def get_gunner_target(self) -> Position | None:
        return None

    def get_attackable_tiles(self) -> list[Position]:
        return self.get_nearby_tiles()

    def get_attackable_tiles_from(self, position: Position, direction: Direction, turret_type: EntityType) -> list[Position]:
        return [position.add(direction)]

    def can_fire_from(self, position: Position, direction: Direction, turret_type: EntityType, target: Position) -> bool:
        return position.add(direction) == target

    def can_launch(self, bot_pos: Position, target: Position) -> bool:
        return self._allowed("launch") and self.can_act() and self.get_tile_builder_bot_id(bot_pos) is not None

    def launch(self, bot_pos: Position, target: Position) -> None:
        if not self.can_launch(bot_pos, target):
            raise ValueError("illegal launch")
        builder_id = self.get_tile_builder_bot_id(bot_pos)
        self.entities[builder_id].position = target
        self.calls.append(("launch", bot_pos, target))

    def spawn_builder(self, position: Position) -> int:
        if not self.can_spawn(position):
            raise ValueError("illegal spawn")
        entity_id = self.next_id
        self.next_id += 1
        self.entities[entity_id] = FakeEntity(EntityType.BUILDER_BOT, position, self.get_team())
        self.calls.append(("spawn_builder", position))
        self.cooldown = 1
        return entity_id

    def can_spawn(self, position: Position) -> bool:
        return self._allowed("spawn") and self.can_act() and self._in_bounds(position) and self.is_tile_empty(position)

    def write_store(self, index: int, value: int) -> None:
        self.pending[index] = value & 0xFFFFFFFF
        self.calls.append(("write_store", index, value & 0xFFFFFFFF))

    def read_store(self, index: int) -> int:
        return self.store[index]

    def draw_indicator_dot(self, position: Position, r: int, g: int, b: int) -> None:
        self.calls.append(("dot", position, r, g, b))

    def draw_indicator_line(self, *args) -> None:
        self.calls.append(("line",) + args)

    def advance(self) -> None:
        self.store.update(self.pending) if hasattr(self.store, "update") else None
        for index, value in self.pending.items():
            self.store[index] = value
        self.pending.clear()
        self.round += 1
        self.cooldown = 0
        self.move_cooldown = 0

