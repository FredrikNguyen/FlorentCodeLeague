from __future__ import annotations

from dataclasses import dataclass
from fcode import EntityType, Environment, Position, Team
from .types import Threat, ThreatKind

PASSABLE_BUILDINGS = frozenset({EntityType.CONVEYOR, EntityType.SPLITTER})


@dataclass(frozen=True, slots=True)
class DynamicObservation:
    entity_type: EntityType; team: Team | None; seen_round: int; blocks: bool


class WorldMemory:
    __slots__ = ("width", "height", "static_walls", "ore_positions", "dynamic", "own_core", "enemy_core", "core_footprint", "threats", "navigation_epoch", "layout_epoch", "goal", "goal_invalidated", "last_round")

    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = max(0, int(width)), max(0, int(height)); self.static_walls=set(); self.ore_positions=set(); self.dynamic={}; self.own_core=None; self.enemy_core=None; self.core_footprint=set(); self.threats={}; self.navigation_epoch=0; self.layout_epoch=0; self.goal=None; self.goal_invalidated=False; self.last_round=0

    def _in_bounds(self, pos: Position) -> bool: return 0 <= pos.x < self.width and 0 <= pos.y < self.height
    def _core_cells(self, anchor: Position) -> set[Position]: return {cell for cell in (anchor, Position(anchor.x+1, anchor.y), Position(anchor.x, anchor.y+1), Position(anchor.x+1, anchor.y+1)) if self._in_bounds(cell)}
    @property
    def obstacle_epoch(self) -> int: return self.navigation_epoch

    def _set_dynamic(self, pos: Position, observation: DynamicObservation) -> None:
        old = self.dynamic.get(pos); self.dynamic[pos] = observation
        self.navigation_epoch += int((old is not None and old.blocks) != observation.blocks); self.layout_epoch += int((old is not None and old.entity_type != EntityType.BUILDER_BOT and old.entity_type not in PASSABLE_BUILDINGS) != (observation.entity_type != EntityType.BUILDER_BOT and observation.entity_type not in PASSABLE_BUILDINGS)); self.goal_invalidated = self.goal_invalidated or (self.goal == pos and observation.blocks)

    def _remove_dynamic(self, pos: Position) -> None:
        old = self.dynamic.pop(pos, None)
        self.navigation_epoch += int(old is not None and old.blocks); self.layout_epoch += int(old is not None and old.entity_type != EntityType.BUILDER_BOT and old.entity_type not in PASSABLE_BUILDINGS); self.goal_invalidated = self.goal_invalidated or (old is not None and self.goal == pos)

    def observe(self, ct: object, round_no: int | None = None) -> None:
        try: current = int(ct.get_current_round() if round_no is None else round_no)
        except Exception: current = self.last_round
        self.last_round = current
        try: tiles = tuple(ct.get_nearby_tiles())
        except Exception: tiles = ()
        try: own_team, own_id = ct.get_team(), int(ct.get_id())
        except Exception: own_team, own_id = None, None
        for pos in tiles:
            if not self._in_bounds(pos): continue
            try: environment = ct.get_tile_env(pos)
            except Exception: continue
            if environment == Environment.WALL:
                if pos not in self.static_walls: self.static_walls.add(pos); self.navigation_epoch += 1; self.layout_epoch += 1
                continue
            if environment == Environment.ORE_TITANIUM: self.ore_positions.add(pos)
            try: building_id, builder_id = ct.get_tile_building_id(pos), ct.get_tile_builder_bot_id(pos)
            except Exception: building_id, builder_id = None, None
            entity_id = builder_id if builder_id is not None else building_id
            if entity_id is None or entity_id == own_id: self._remove_dynamic(pos); continue
            try: entity_type = ct.get_entity_type(entity_id); team = ct.get_team(entity_id)
            except Exception: continue
            self._set_dynamic(pos, DynamicObservation(entity_type, team, current, entity_type not in PASSABLE_BUILDINGS))
            if entity_type == EntityType.CORE:
                if team == own_team:
                    before = set(self.core_footprint); self.own_core = min((self.own_core, pos), key=lambda p: (p.y, p.x)) if self.own_core else pos; self.core_footprint.update(self._core_cells(self.own_core))
                    if before != self.core_footprint: self.navigation_epoch += 1; self.layout_epoch += 1
                elif team is not None: self.enemy_core = pos
            elif team is not None and own_team is not None and team != own_team:
                kind = ThreatKind.BUILDER_RUSH if entity_type == EntityType.BUILDER_BOT else ThreatKind.SABOTAGE; self.threats[pos] = Threat(pos, kind, 4 if entity_type == EntityType.BUILDER_BOT else 2, current, current + 3, entity_type)
        self.expire_dynamic(current)
        self.threats = {pos: threat for pos, threat in self.threats.items() if threat.expires_round > current}

    def expire_dynamic(self, current_round: int | None = None) -> None:
        current = self.last_round if current_round is None else int(current_round)
        for pos, observation in tuple(self.dynamic.items()):
            if current - observation.seen_round >= 3: self._remove_dynamic(pos)

    def is_navigation_blocked(self, pos: Position) -> bool:
        observation = self.dynamic.get(pos); return not self._in_bounds(pos) or pos in self.static_walls or pos in self.core_footprint or bool(observation and observation.blocks)

    def is_route_planning_blocked(self, pos: Position) -> bool:
        observation = self.dynamic.get(pos); return not self._in_bounds(pos) or pos in self.static_walls or pos in self.core_footprint or bool(observation and observation.entity_type != EntityType.BUILDER_BOT and observation.entity_type not in PASSABLE_BUILDINGS)

    def classify(self, pos: Position) -> EntityType | Environment | None:
        observation = self.dynamic.get(pos); return Environment.WALL if pos in self.static_walls else observation.entity_type if observation else None
    def is_blocked(self, pos: Position) -> bool: return self.is_navigation_blocked(pos)
    def is_passable(self, pos: Position) -> bool: return not self.is_navigation_blocked(pos)
    def set_goal(self, goal: Position | None) -> None: self.goal, self.goal_invalidated = goal, False
    def consume_goal_invalidation(self) -> bool: result = self.goal_invalidated; self.goal_invalidated = False; return result

    def invalidate_after_throw(self, position: Position | None = None) -> None:
        old = self.dynamic.pop(position, None) if position is not None else None; self.navigation_epoch += 1 + int(old is not None and old.blocks); self.layout_epoch += int(old is not None and old.entity_type != EntityType.BUILDER_BOT and old.entity_type not in PASSABLE_BUILDINGS); self.goal_invalidated = True

    def known_ore(self) -> tuple[Position, ...]: return tuple(sorted(self.ore_positions, key=lambda pos: (pos.y, pos.x)))
    def threat_list(self, current_round: int | None = None) -> tuple[Threat, ...]:
        current = self.last_round if current_round is None else current_round
        return tuple(sorted((threat for threat in self.threats.values() if threat.expires_round > current), key=lambda threat: (-threat.score, threat.position.y, threat.position.x)))
