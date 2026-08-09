from __future__ import annotations

from dataclasses import dataclass

from fcode import EntityType, Environment, Position, Team

from .types import Threat, ThreatKind

PASSABLE_BUILDINGS = frozenset({EntityType.CONVEYOR, EntityType.SPLITTER})
TRANSIENT_TYPES = frozenset({EntityType.BUILDER_BOT})


@dataclass(frozen=True, slots=True)
class DynamicObservation:
    entity_type: EntityType
    team: Team | None
    seen_round: int
    blocks: bool


class WorldMemory:
    """Per-unit bounded world memory with separate dynamic/static epochs."""

    __slots__ = (
        "width",
        "height",
        "static_walls",
        "seen_tiles",
        "ore_positions",
        "dynamic",
        "own_core",
        "enemy_core",
        "core_footprint",
        "threats",
        "navigation_epoch",
        "layout_epoch",
        "goal",
        "goal_invalidated",
        "last_round",
    )

    def __init__(self, width: int, height: int) -> None:
        self.width = max(0, int(width))
        self.height = max(0, int(height))
        self.static_walls: set[Position] = set()
        self.seen_tiles: set[Position] = set()
        self.ore_positions: set[Position] = set()
        self.dynamic: dict[Position, DynamicObservation] = {}
        self.own_core: Position | None = None
        self.enemy_core: Position | None = None
        self.core_footprint: set[Position] = set()
        self.threats: dict[Position, Threat] = {}
        self.navigation_epoch = 0
        self.layout_epoch = 0
        self.goal: Position | None = None
        self.goal_invalidated = False
        self.last_round = 0

    @property
    def obstacle_epoch(self) -> int:
        """Compatibility alias used by movement code."""
        return self.navigation_epoch

    def _in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def _core_cells(self, anchor: Position) -> set[Position]:
        return {
            cell
            for cell in (
                anchor,
                Position(anchor.x + 1, anchor.y),
                Position(anchor.x, anchor.y + 1),
                Position(anchor.x + 1, anchor.y + 1),
            )
            if self._in_bounds(cell)
        }

    @staticmethod
    def _permanent(observation: DynamicObservation | None) -> bool:
        return observation is not None and observation.entity_type not in TRANSIENT_TYPES

    def _set_dynamic(self, pos: Position, observation: DynamicObservation) -> None:
        old = self.dynamic.get(pos)
        self.dynamic[pos] = observation
        # ``seen_round`` is only freshness metadata. Comparing the complete
        # dataclass here used to increment the navigation epoch every round for
        # every unchanged visible entity, invalidating all active Builder paths
        # and forcing needless BFS replans. Only occupancy semantics affect paths.
        old_signature = (old.entity_type, old.team, old.blocks) if old is not None else None
        new_signature = (observation.entity_type, observation.team, observation.blocks)
        if old_signature != new_signature:
            self.navigation_epoch += 1
        if self._permanent(old) != self._permanent(observation) or (
            self._permanent(old)
            and old is not None
            and (old.entity_type, old.team) != (observation.entity_type, observation.team)
        ):
            self.layout_epoch += 1
        if self.goal == pos and observation.blocks:
            self.goal_invalidated = True

    def _remove_dynamic(self, pos: Position) -> None:
        old = self.dynamic.pop(pos, None)
        if old is None:
            return
        self.navigation_epoch += 1
        if self._permanent(old):
            self.layout_epoch += 1
        if self.goal == pos:
            self.goal_invalidated = True

    def observe(self, ct: object, round_no: int | None = None) -> None:
        try:
            current = int(ct.get_current_round() if round_no is None else round_no)
        except Exception:
            current = self.last_round
        self.last_round = current
        try:
            tiles = tuple(ct.get_nearby_tiles())[:256]
        except Exception:
            tiles = ()
        try:
            own_team = ct.get_team()
        except Exception:
            own_team = None
        try:
            own_id = int(ct.get_id())
        except Exception:
            own_id = None

        for pos in tiles:
            if not self._in_bounds(pos):
                continue
            self.seen_tiles.add(pos)
            try:
                environment = ct.get_tile_env(pos)
            except Exception:
                continue
            if environment == Environment.WALL:
                if pos not in self.static_walls:
                    self.static_walls.add(pos)
                    self.navigation_epoch += 1
                    self.layout_epoch += 1
                continue
            if environment == Environment.ORE_TITANIUM:
                self.ore_positions.add(pos)
            try:
                building_id = ct.get_tile_building_id(pos)
                builder_id = ct.get_tile_builder_bot_id(pos)
            except Exception:
                building_id = builder_id = None
            entity_id = building_id if building_id is not None else builder_id
            if entity_id is None or entity_id == own_id:
                self._remove_dynamic(pos)
                # A tile we can currently see is authoritative. Do not keep a
                # ghost infiltrator/turret alarm at a position proven empty or
                # occupied only by ourselves. Stale threat coordinates were
                # pulling responders back toward already-cleared ground.
                self.threats.pop(pos, None)
                continue
            try:
                entity_type = ct.get_entity_type(entity_id)
            except Exception:
                continue
            try:
                team = ct.get_team(entity_id)
            except Exception:
                team = None
            blocks = entity_type not in PASSABLE_BUILDINGS
            self._set_dynamic(pos, DynamicObservation(entity_type, team, current, blocks))
            if entity_type == EntityType.CORE:
                try:
                    anchor = ct.get_position(entity_id)
                except Exception:
                    anchor = pos
                if team == own_team:
                    if anchor != self.own_core:
                        self.own_core = anchor
                        self.core_footprint = self._core_cells(anchor)
                        self.layout_epoch += 1
                elif team is not None:
                    self.enemy_core = anchor
            elif team is not None and own_team is not None and team != own_team:
                if entity_type == EntityType.BUILDER_BOT:
                    kind, base = ThreatKind.BUILDER_RUSH, 12
                elif entity_type == EntityType.GUNNER:
                    kind, base = ThreatKind.GUNNER_FIRE, 14
                elif entity_type == EntityType.SENTINEL:
                    kind, base = ThreatKind.SENTINEL_FIRE, 15
                elif entity_type == EntityType.LAUNCHER:
                    kind, base = ThreatKind.SABOTAGE, 11
                else:
                    kind, base = ThreatKind.SABOTAGE, 5
                # Mobile Builders get a short last-known lifetime; stationary
                # weapons remain actionable longer when they slip just outside
                # vision. A newly observed contact refreshes this every round.
                ttl = 4 if entity_type == EntityType.BUILDER_BOT else (10 if entity_type in (EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER) else 6)
                self.threats[pos] = Threat(
                    pos, kind, base, current, current + ttl, entity_type,
                )
        self.expire_dynamic(current)
        for pos in tuple(self.threats):
            if self.threats[pos].expires_round <= current:
                self.threats.pop(pos, None)

    def expire_dynamic(self, current_round: int | None = None) -> None:
        current = self.last_round if current_round is None else int(current_round)
        for pos, observation in tuple(self.dynamic.items()):
            ttl = 2 if observation.entity_type == EntityType.BUILDER_BOT else 8
            if current - observation.seen_round >= ttl:
                self._remove_dynamic(pos)

    def classify(self, pos: Position) -> EntityType | Environment | None:
        if pos in self.static_walls:
            return Environment.WALL
        observation = self.dynamic.get(pos)
        return observation.entity_type if observation else None

    def is_navigation_blocked(self, pos: Position) -> bool:
        if not self._in_bounds(pos) or pos in self.static_walls or pos in self.core_footprint:
            return True
        observation = self.dynamic.get(pos)
        return bool(observation.blocks) if observation else False

    def is_route_blocked(self, pos: Position) -> bool:
        """Block permanent layout only; ignore temporary Builder traffic.

        Friendly/enemy conveyors and splitters remain passable route cells and are
        verified/reused/replaced by construction logic.
        """
        if not self._in_bounds(pos) or pos in self.static_walls or pos in self.core_footprint:
            return True
        observation = self.dynamic.get(pos)
        if observation is None or observation.entity_type == EntityType.BUILDER_BOT:
            return False
        return observation.entity_type not in PASSABLE_BUILDINGS

    def is_blocked(self, pos: Position) -> bool:
        return self.is_navigation_blocked(pos)

    def is_passable(self, pos: Position) -> bool:
        return not self.is_navigation_blocked(pos)

    def set_goal(self, goal: Position | None) -> None:
        self.goal = goal
        self.goal_invalidated = False

    def consume_goal_invalidation(self) -> bool:
        result = self.goal_invalidated
        self.goal_invalidated = False
        return result

    def known_ore(self) -> tuple[Position, ...]:
        return tuple(sorted(self.ore_positions, key=lambda pos: (pos.y, pos.x)))

    def threat_list(self, current_round: int | None = None) -> tuple[Threat, ...]:
        current = self.last_round if current_round is None else int(current_round)
        return tuple(
            sorted(
                (threat for threat in self.threats.values() if threat.expires_round > current),
                key=lambda threat: (-threat.score, threat.position.y, threat.position.x),
            )
        )
