
from __future__ import annotations

from dataclasses import dataclass, field

from fcode import Direction, EntityType, Position

from .actions import cpu_is_safe
from .comms import read_shared_threat, write_shared_threat
from .types import DefenseMode, Threat, ThreatKind, ThreatReport


DEFENSE_WATCH_THRESHOLD = 1
DEFENSE_ACTIVE_THRESHOLD = 7
DEFENSE_CRITICAL_THRESHOLD = 12
DEFENSE_STANDDOWN_DELAY = 8
PERSISTENT_DEFENDERS_SMALL = 2
PERSISTENT_DEFENDERS_LARGE = 3


@dataclass(slots=True)
class DefenseState:
    mode: DefenseMode = DefenseMode.CLEAR
    threat: ThreatReport | None = None
    local_reports: tuple[ThreatReport, ...] = ()
    defenders: tuple[int, ...] = ()
    last_threat_round: int = -1
    last_mode_round: int = 0
    previous_core_hp: int | None = None
    leader_id: int | None = None
    prior_roles: dict[int, str] = field(default_factory=dict)


def _safe_int(ct: object, method: str, default: int = 0, entity_id: int | None = None) -> int:
    try:
        getter = getattr(ct, method)
        return int(getter() if entity_id is None else getter(entity_id))
    except Exception:
        return default


def _entities(ct: object) -> tuple[int, ...]:
    try:
        return tuple(ct.get_nearby_entities())[:96]
    except Exception:
        try:
            return tuple(ct.get_nearby_buildings())[:64] + tuple(ct.get_nearby_units())[:32]
        except Exception:
            return ()


def _own_core_position(ct: object) -> Position | None:
    try:
        own_team = ct.get_team()
        positions = tuple(
            ct.get_position(entity_id)
            for entity_id in _entities(ct)
            if ct.get_entity_type(entity_id) == EntityType.CORE and ct.get_team(entity_id) == own_team
        )
    except Exception:
        return None
    return min(positions, key=lambda pos: (pos.y, pos.x)) if positions else None


def _own_core_id(ct: object) -> int | None:
    try:
        own_team = ct.get_team()
        ids = tuple(entity_id for entity_id in _entities(ct) if ct.get_entity_type(entity_id) == EntityType.CORE and ct.get_team(entity_id) == own_team)
    except Exception:
        return None
    return min(ids) if ids else None


def _kind_for_entity(entity_type: EntityType) -> ThreatKind:
    return {
        EntityType.BUILDER_BOT: ThreatKind.ENEMY_BUILDER,
        EntityType.GUNNER: ThreatKind.ENEMY_GUNNER,
        EntityType.SENTINEL: ThreatKind.ENEMY_SENTINEL,
        EntityType.LAUNCHER: ThreatKind.ENEMY_LAUNCHER,
        EntityType.HARVESTER: ThreatKind.HARVESTER_UNDER_ATTACK,
        EntityType.CONVEYOR: ThreatKind.ROUTE_UNDER_ATTACK,
        EntityType.SPLITTER: ThreatKind.ROUTE_UNDER_ATTACK,
    }.get(entity_type, ThreatKind.UNKNOWN)


def _type_weight(entity_type: EntityType) -> int:
    return {
        EntityType.BUILDER_BOT: 5,
        EntityType.GUNNER: 7,
        EntityType.SENTINEL: 8,
        EntityType.LAUNCHER: 7,
        EntityType.HARVESTER: 4,
        EntityType.CONVEYOR: 4,
        EntityType.SPLITTER: 5,
    }.get(entity_type, 1)


def observe_local_threats(ct: object, *, current_round: int | None = None) -> tuple[ThreatReport, ...]:
    """Return bounded, deterministic observations from the unit's current vision."""
    if not cpu_is_safe(ct, 7000):
        return ()
    round_no = _safe_int(ct, "get_current_round", 0) if current_round is None else int(current_round)
    try:
        own_team = ct.get_team()
        core = _own_core_position(ct) or ct.get_position()
    except Exception:
        return ()
    reports: list[ThreatReport] = []
    for entity_id in sorted(_entities(ct)):
        try:
            if ct.get_team(entity_id) == own_team:
                continue
            entity_type = ct.get_entity_type(entity_id)
            position = ct.get_position(entity_id)
        except Exception:
            continue
        distance = core.distance_squared(position)
        proximity = max(0, 8 - int(distance ** 0.5))
        severity = _type_weight(entity_type) + proximity
        if distance <= 1:
            severity += 4
        kind = _kind_for_entity(entity_type)
        if entity_type in (EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER) and distance <= 16:
            severity += 2
        reports.append(ThreatReport(kind, position, core, severity, round_no, round_no, round_no + 3, int(entity_id)))
    reports.sort(key=lambda report: (-report.severity, report.position.y, report.position.x, report.reporter_id))
    return tuple(reports[:8])


def merge_threat_reports(local: tuple[ThreatReport, ...], shared: ThreatReport | None) -> ThreatReport | None:
    reports = list(local)
    if shared is not None:
        reports.append(shared)
    if not reports:
        return None
    return max(reports, key=lambda report: (int(report.severity), -report.position.y, -report.position.x, -report.reporter_id))


def choose_defense_mode(
    threat: ThreatReport | None,
    *,
    previous: DefenseMode = DefenseMode.CLEAR,
    current_round: int = 0,
    last_threat_round: int = -1,
) -> DefenseMode:
    if threat is not None:
        if threat.severity >= DEFENSE_CRITICAL_THRESHOLD:
            return DefenseMode.CRITICAL
        if threat.severity >= DEFENSE_ACTIVE_THRESHOLD:
            return DefenseMode.ACTIVE
        return DefenseMode.WATCH
    if previous in (DefenseMode.ACTIVE, DefenseMode.CRITICAL, DefenseMode.RECOVERY) and last_threat_round >= 0 and int(current_round) - last_threat_round <= DEFENSE_STANDDOWN_DELAY:
        return DefenseMode.RECOVERY
    return DefenseMode.CLEAR


def required_defender_count(mode: DefenseMode, severity: int = 0, *, map_area: int = 0) -> int:
    if mode == DefenseMode.CRITICAL:
        return 3 if int(severity) >= 16 else 2
    if mode == DefenseMode.ACTIVE:
        return 2
    if mode == DefenseMode.WATCH:
        return 1
    if mode == DefenseMode.RECOVERY:
        return 1
    return PERSISTENT_DEFENDERS_LARGE if int(map_area) >= 500 and mode != DefenseMode.CLEAR else 0


def choose_defenders(
    candidates: tuple[tuple[int, Position, int, bool], ...] | list[tuple[int, Position, int, bool]],
    required: int,
    *,
    threat_position: Position | None = None,
    critical_route_owners: frozenset[int] = frozenset(),
) -> tuple[int, ...]:
    if required <= 0:
        return ()
    target = threat_position or Position(0, 0)
    ranked = sorted(
        candidates,
        key=lambda item: (
            item[1].distance_squared(target)
            + (100 if item[0] in critical_route_owners else 0)
            + (100 if item[3] else 0),
            -int(item[2]),
            item[0],
        ),
    )
    return tuple(item[0] for item in ranked[: max(0, int(required))])


def update_defense_overlay(ct: object, state: DefenseState | None = None) -> DefenseState:
    state = state or DefenseState()
    round_no = _safe_int(ct, "get_current_round")
    local = observe_local_threats(ct, current_round=round_no)
    shared = read_shared_threat(ct, current_round=round_no)
    try:
        core_id = _own_core_id(ct)
        core_hp = _safe_int(ct, "get_hp", 0, core_id)
        if state.previous_core_hp is not None and core_hp < state.previous_core_hp:
            core = _own_core_position(ct) or Position(0, 0)
            local = local + (ThreatReport(ThreatKind.CORE_UNDER_FIRE, core, core, DEFENSE_CRITICAL_THRESHOLD, round_no, round_no, round_no + 3, _safe_int(ct, "get_id")),)
        state.previous_core_hp = core_hp
    except Exception:
        pass
    authoritative = merge_threat_reports(local, shared)
    mode = choose_defense_mode(authoritative, previous=state.mode, current_round=round_no, last_threat_round=state.last_threat_round)
    if authoritative is not None:
        state.last_threat_round = round_no
    state.local_reports, state.threat, state.mode = local, authoritative, mode
    state.last_mode_round = round_no
    # Lowest visible friendly Builder ID is the sole shared-threat writer.
    try:
        own_team = ct.get_team()
        builders = tuple(sorted(entity_id for entity_id in _entities(ct) if ct.get_entity_type(entity_id) == EntityType.BUILDER_BOT and ct.get_team(entity_id) == own_team))
        state.leader_id = builders[0] if builders else None
        if authoritative is not None and state.leader_id == _safe_int(ct, "get_id"):
            write_shared_threat(ct, authoritative)
    except Exception:
        pass
    return state


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
