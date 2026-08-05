from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fcode import Direction, EntityType, Position


class Role(str, Enum):
    ECONOMY = "economy"; REPAIR = "repair"; DEFENDER = "defender"; SCOUT = "scout"; RAIDER = "raider"; SIEGE = "siege"; IDLE = "idle"


class Phase(str, Enum):
    OPENING = "opening"; ECONOMY = "economy"; DEFENSE = "defense"; OFFENSE = "offense"; ENDGAME = "endgame"


class Opening(str, Enum):
    COMPACT_PRESSURE = "compact_pressure"; BALANCED_ECONOMY = "balanced_economy"; WIDE_EXPANSION = "wide_expansion"; CHOKEPOINT_CONTROL = "chokepoint_control"; ANTI_RUSH = "anti_rush"


class BuilderState(str, Enum):
    DISCOVER = "discover"; CLAIM = "claim"; APPROACH_BUILD_TILE = "approach_build_tile"; ROUTE = "route"; BUILD = "build"; VERIFY = "verify"; DELIVER = "deliver"; MAINTAIN = "maintain"


class ThreatKind(str, Enum):
    BUILDER_RUSH = "builder_rush"; FIRING_LINE = "firing_line"; SABOTAGE = "sabotage"; CORE_DAMAGE = "core_damage"; ECONOMY_RUSH = "economy_rush"; UNKNOWN = "unknown"


class RouteStatus(str, Enum):
    PLANNED = "planned"; BUILDING = "building"; VERIFIED = "verified"; BROKEN = "broken"; DELIVERING = "delivering"; MAINTAIN = "maintain"; STALE = "stale"


class ProjectState(str, Enum):
    IDLE = "idle"; CLAIMED = "claimed"; PLANNING = "planning"; BUILDING = "building"; VERIFYING = "verifying"; DELIVERING = "delivering"; MAINTAIN = "maintain"; FAILED = "failed"


@dataclass(frozen=True, slots=True)
class Assignment:
    owner_id: int; generation: int


@dataclass(frozen=True, slots=True)
class Project:
    position: Position | None; epoch: int; state: ProjectState


@dataclass(frozen=True, slots=True)
class Threat:
    position: Position; kind: ThreatKind = ThreatKind.UNKNOWN; score: int = 0; seen_round: int = 0; expires_round: int = 0; entity_type: EntityType | None = None


@dataclass(frozen=True, slots=True)
class Budget:
    construction: int = 0; defense: int = 0; ammo: int = 0; expansion: int = 0; liquidity: int = 0

    @property
    def reserved(self) -> int:
        return sum(max(0, value) for value in (self.construction, self.defense, self.ammo, self.liquidity))


@dataclass(frozen=True, slots=True)
class RoutePlan:
    ore: Position; cells: tuple[Position, ...] = (); directions: tuple[Direction, ...] = (); core_footprint: tuple[Position, ...] = (); status: RouteStatus = RouteStatus.PLANNED; created_round: int = 0; expected_output: int = 0

    @property
    def first_receiver(self) -> Position | None:
        return self.cells[0] if self.cells else None

    @property
    def final_conveyor(self) -> Position | None:
        return self.cells[-1] if self.cells else None


@dataclass(frozen=True, slots=True)
class OpeningDescriptor:
    width: int = 0; height: int = 0; area: int = 0; nearby_ore_count: int = 0; nearest_ore_distance: int = 999; wall_density: float = 0.0; low_degree_passable_tiles: int = 0; route_exposure: float = 0.0; estimated_enemy_distance: int = 999
