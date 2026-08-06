from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
from fcode import Direction, EntityType, Position


class Role(str, Enum):
    ECONOMY = "economy"; REPAIR = "repair"; DEFENDER = "defender"; SCOUT = "scout"; RAIDER = "raider"; SIEGE = "siege"; IDLE = "idle"


class Phase(str, Enum):
    OPENING = "opening"; ECONOMY = "economy"; DEFENSE = "defense"; OFFENSE = "offense"; ENDGAME = "endgame"


class EconomyPhase(str, Enum):
    BOOTSTRAP = "bootstrap"
    FIRST_ROUTE_BUILDING = "first_route_building"
    FIRST_ROUTE_MAINTAINING = "first_route_maintaining"
    EXPANSION_EVALUATION = "expansion_evaluation"
    SECONDARY_ROUTE_BUILDING = "secondary_route_building"
    MULTI_ROUTE_MAINTAINING = "multi_route_maintaining"
    REPAIR_PRIORITY = "repair_priority"
    ECONOMY_SATURATED = "economy_saturated"
    ENDGAME_HOLD = "endgame_hold"


class Opening(str, Enum):
    COMPACT_PRESSURE = "compact_pressure"; BALANCED_ECONOMY = "balanced_economy"; WIDE_EXPANSION = "wide_expansion"; CHOKEPOINT_CONTROL = "chokepoint_control"; ANTI_RUSH = "anti_rush"


class BuilderState(str, Enum):
    DISCOVER = "discover"; CLAIM = "claim"; APPROACH_BUILD_TILE = "approach_build_tile"; ROUTE = "route"; BUILD = "build"; VERIFY = "verify"; DELIVER = "deliver"; MAINTAIN = "maintain"


class WorkIntent(str, Enum):
    """The bounded piece of work a Builder owns for the current turn."""

    ROUTE_OWNER = "route_owner"
    REPAIR_ROUTE = "repair_route"
    DISCOVER_ORE = "discover_ore"
    PATROL_LOGISTICS = "patrol_logistics"
    CRITICAL_DEFENSE = "critical_defense"
    ATTACK_PREPARATION = "attack_preparation"
    ATTACK = "attack"


class ThreatKind(str, Enum):
    BUILDER_RUSH = "builder_rush"
    ENEMY_BUILDER = "builder_rush"
    FIRING_LINE = "firing_line"
    ENEMY_GUNNER = "firing_line"
    ENEMY_SENTINEL = "enemy_sentinel"
    ENEMY_LAUNCHER = "enemy_launcher"
    SABOTAGE = "sabotage"
    ROUTE_UNDER_ATTACK = "route_under_attack"
    HARVESTER_UNDER_ATTACK = "harvester_under_attack"
    CORE_DAMAGE = "core_damage"
    CORE_UNDER_FIRE = "core_damage"
    ECONOMY_RUSH = "economy_rush"
    UNKNOWN = "unknown"


class DefenseMode(str, Enum):
    CLEAR = "defense_clear"
    WATCH = "defense_watch"
    ACTIVE = "defense_active"
    CRITICAL = "defense_critical"
    RECOVERY = "defense_recovery"


class OffenseState(str, Enum):
    IDLE = "offense_idle"
    SCOUTING = "scouting"
    RALLYING = "rallying"
    APPROACHING_OBJECTIVE = "approaching_objective"
    SABOTAGING_LOGISTICS = "sabotaging_logistics"
    DESTROYING_HARVESTER = "destroying_harvester"
    CLEARING_DEFENSE = "clearing_defense"
    BUILDING_FORWARD_TURRET = "building_forward_turret"
    PRESSURING_CORE = "pressuring_core"
    RETREATING = "retreating"
    REGROUPING = "regrouping"


class StrategyPhase(IntEnum):
    BOOTSTRAP_ECON = 0
    FIRST_ROUTE_RUSH = 1
    ECONOMY_EXPANSION = 2
    DEFENSE_ALERT = 3
    ATTACK_PREPARATION = 4
    OFFENSIVE_PRESSURE = 5
    CORE_SIEGE = 6
    RECOVERY = 7
    ENDGAME = 8


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
class ThreatReport:
    kind: ThreatKind
    position: Position
    target_asset: Position | None = None
    severity: int = 0
    first_seen_round: int = 0
    last_seen_round: int = 0
    expiry_round: int = 0
    reporter_id: int = 0


@dataclass(frozen=True, slots=True)
class EnemyTarget:
    position: Position
    entity_type: EntityType
    last_seen_round: int = 0
    hp: int | None = None
    confidence: int = 0
    source_id: int = 0


@dataclass(frozen=True, slots=True)
class AttackObjective:
    target: EnemyTarget
    state: OffenseState = OffenseState.IDLE
    epoch: int = 0
    score: int = 0
    requires_forward_support: bool = False


@dataclass(frozen=True, slots=True)
class Budget:
    construction: int = 0; defense: int = 0; ammo: int = 0; expansion: int = 0; liquidity: int = 0

    @property
    def reserved(self) -> int:
        return sum(max(0, value) for value in (self.construction, self.defense, self.ammo, self.liquidity))


@dataclass(frozen=True, slots=True)
class EconomySnapshot:
    round: int = 0
    titanium: int = 0
    ammo: int = 0
    scale_percent: int = 100
    live_units: int = 0
    desired_builders: int = 3
    active_projects: int = 0
    maintaining_routes: int = 0
    building_routes: int = 0
    failed_projects: int = 0
    broken_routes: int = 0
    remaining_route_cost: int = 0
    emergency_repair_reserve: int = 0
    defense_reserve: int = 0
    ammo_reserve: int = 0
    free_titanium: int = 0


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
