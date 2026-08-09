from __future__ import annotations

from dataclasses import dataclass, field

from fcode import Direction, EntityType, Environment, Position

from .actions import CARDINALS, FACING_DIRECTIONS, TurnActions, cpu_is_safe
from .comms import (
    Slot,
    claim_is_fresh,
    claim_slot,
    decode_budget,
    decode_defense_alert,
    decode_epoch_pulse,
    decode_rally,
    decode_scenario,
    decode_strategy,
    decode_team_status,
    encode_defense_alert,
    encode_rally,
    epoch_distance,
    pack_claim,
    unpack_claim,
)
from .core import compute_budget
from .economy import estimate_payback_round, estimate_route_cost, score_ore
from .logistics import plan_core_outward_route
from .navigation import Navigator
from .offense import score_sabotage_target
from .policy import assign_role
from .types import BuilderState, Opening, Phase, Role, RoutePlan, Scenario, ThreatKind
from .world import WorldMemory


# Rules with no dynamic Controller getter. All scalable construction costs are
# queried from the Controller at the point of use.
BUILDER_ATTACK_COST = 2
BASE_CONVEYOR_COST = 3
BASE_HARVESTER_COST = 20
BASE_LAUNCHER_COST = 20
BASE_GUNNER_COST = 20
BASE_SENTINEL_COST = 30
BASE_BARRIER_COST = 3

PROJECT_STATUS_SLOTS = (
    Slot.PRIMARY_ORE,
    Slot.LOGISTICS,
    Slot.THREAT,
    Slot.ENEMY_CORE,
)


@dataclass(slots=True)
class BuilderStateData:
    role: Role = Role.SCOUT
    phase: Phase = Phase.OPENING
    opening: Opening = Opening.BALANCED_ECONOMY
    scenario: Scenario = Scenario.STANDARD
    team_route_target: int = 0
    team_route_capacity: int = 0
    team_maintaining_routes: int = 0
    team_active_projects: int = 0
    team_defense_severity: int = 0
    team_attack_priority: int = 0
    team_route_progress_age: int = 0
    team_core_congestion: int = 0
    economy_established: bool = False
    priority_owner_ids: tuple[int, ...] = ()
    priority_owner_round: int = -1
    state: BuilderState = BuilderState.DISCOVER
    world: WorldMemory | None = None
    navigator: Navigator | None = None
    ore_target: Position | None = None
    route: RoutePlan | None = None
    route_index: int = -1
    repair_index: int | None = None
    claim_slot: int | None = None
    claim_epoch: int = 0
    claim_started_round: int = 0
    last_delivery_round: int | None = None
    delivery_started_round: int | None = None
    last_position: Position | None = None
    blocked_steps: int = 0
    cursor: int = 0
    built_links: dict[Position, tuple[EntityType, Direction]] = field(default_factory=dict)
    # Per-Builder memory of friendly Conveyor directions observed from other
    # routes.  This lets later pipelines prefer an already-correct shared trunk
    # without pretending the team has omniscient map state. Entries expire so a
    # destroyed off-screen line cannot bias planning forever.
    known_trunk_links: dict[Position, tuple[Direction, int]] = field(default_factory=dict)
    trunk_epoch: int = 0
    route_shared_links: set[Position] = field(default_factory=set)
    route_search: dict[str, object] | None = None
    route_blocked: set[Position] = field(default_factory=set)
    route_plan_failures: int = 0
    last_route_plan_failure: int = -999
    rejected_ore_until: dict[Position, int] = field(default_factory=dict)
    last_final_storage: bool | None = None
    last_rally_write: int = -999
    rally_target: Position | None = None
    rally_expires_epoch: int = 0
    rally_priority: int = 0
    last_defense_alert: int = -999
    defense_target: Position | None = None
    defense_expires_epoch: int = 0
    defense_severity: int = 0
    defense_kind: ThreatKind = ThreatKind.UNKNOWN
    last_forward_turret: int = -999
    last_forward_launcher: int = -999
    last_defensive_turret: int = -999
    last_defensive_barrier: int = -999
    bootstrap_defense_built: bool = False
    last_forward_outpost: int = -999
    last_project_status: int = -1
    last_project_write: int = -999
    patrol_index: int = -1
    patrol_direction: int = 1
    last_full_verify_round: int | None = None
    last_harvester_seen_round: int | None = None
    next_patrol_round: int = 0
    move_history: list[Position] = field(default_factory=list)
    stuck_goal: Position | None = None
    stuck_adjacent: bool = False
    stuck_since_round: int = -1
    best_goal_distance: int = 1 << 30
    last_goal_progress_round: int = -1
    last_blocker_position: Position | None = None
    last_blocker_id: int | None = None
    last_blocker_turret: int = -999
    temporary_route_blocked: dict[Position, int] = field(default_factory=dict)
    route_avoid_epoch: int = 0
    explore_cursor: int = 0
    explored_waypoints: set[Position] = field(default_factory=set)
    last_ore_offer_round: int = -999
    last_productive_round: int = -1
    idle_turns: int = 0
    nonprogress_turns: int = 0
    last_seen_tile_count: int = 0
    build_fail_position: Position | None = None
    build_fail_count: int = 0
    last_build_fail_round: int = -999
    last_real_route_progress_round: int = -1
    layout_invalidations: int = 0
    hypothesis_shift: int = 0
    last_hypothesis_shift_round: int = -999
    # Decentralized post-bootstrap expansion. Primary Store projects remain the
    # authoritative resilient routes; one survey caste may add an extra short
    # profitable route without consuming another Store slot.
    satellite_mode: bool = False
    satellite_started_round: int = -999
    satellite_completed_round: int = -999
    satellite_cooldown_until: int = 0
    satellite_completed_ores: set[Position] = field(default_factory=set)
    # Enemy-economy capture memory. Sabotage is not complete when a Harvester is
    # destroyed: a claimless mobile Builder should convert that exposed ore into
    # our next route, then resume pressure from the newly advanced frontier.
    capture_target: Position | None = None
    capture_until_round: int = -1
    capture_started_round: int = -999
    # Primary-route ownership is a construction lease, not a permanent job. Once
    # the complete Conveyor chain + Harvester has been verified, the claim remains
    # reserved for accounting/repair but the Builder rejoins the mobile workforce.
    # Lease expiry or a real route threat recalls it for another verification pass.
    flex_primary_owner: bool = False
    # Compressed free-worker rank after active economy owners are removed.
    # This lets support behavior distinguish the first home defender from a
    # second large-map frontier defender without depending on raw entity IDs.
    role_key: int = 1
    # Free-worker roles must not flap whenever a primary owner briefly switches
    # between construction and passive handoff.  A short lease stabilizes the
    # mission; real defense and active route ownership still pre-empt instantly.
    role_lock_until: int = 0
    # Friendly right-of-way may intentionally move us backwards.  Remember the
    # vacated tile briefly so the normal mission does not undo that yield next turn.
    traffic_yield_origin: Position | None = None
    traffic_yield_until: int = -1
    anti_reverse_position: Position | None = None
    anti_reverse_until: int = -1
    # Mission-level thrash is different from path-level oscillation: two higher
    # layers may alternate goals and make A->B->A look legal to the navigator.
    # Track rapid goal switches so free workers can refuse the immediate reversal.
    last_goal_switch_round: int = -999
    rapid_goal_switches: int = 0
    # Survey target hysteresis keeps one exploration leg coherent instead of
    # recomputing a different waypoint after every buffered macro-state change.
    scout_target: Position | None = None
    scout_target_until: int = -1
    counterbattery_cursor: int = 0
    last_hp: int | None = None


def _id(ct: object) -> int:
    try:
        return int(ct.get_id())
    except Exception:
        return 0


def _round(ct: object) -> int:
    try:
        return int(ct.get_current_round())
    except Exception:
        return 0


def _pos(ct: object) -> Position:
    try:
        return ct.get_position()
    except Exception:
        return Position(0, 0)


def _refresh_trunk_memory(ct: object, state: BuilderStateData) -> None:
    """Remember recently *observed* friendly Conveyor directions.

    Sensing remains local.  This is only per-unit memory of infrastructure the
    Builder has actually seen; it is not a global map shortcut.  Ninety-six
    rounds is long enough for a scout/owner to exploit a trunk it just crossed,
    while bounded expiry prevents a destroyed unseen line from biasing plans
    forever.
    """
    world = state.world
    if world is None:
        return
    round_no = _round(ct)
    changed = False
    for position, (_direction, seen_round) in tuple(state.known_trunk_links.items()):
        if round_no - int(seen_round) > 96:
            state.known_trunk_links.pop(position, None)
            changed = True
    try:
        own_team = ct.get_team()
    except Exception:
        own_team = None
    for position, observation in tuple(world.dynamic.items()):
        if observation.seen_round != round_no or observation.entity_type != EntityType.CONVEYOR:
            continue
        if own_team is not None and observation.team != own_team:
            continue
        try:
            entity_id = ct.get_tile_building_id(position)
            if entity_id is None:
                continue
            direction = ct.get_direction(entity_id)
        except Exception:
            continue
        if direction not in CARDINALS:
            continue
        previous = state.known_trunk_links.get(position)
        current = (direction, round_no)
        if previous is None or previous[0] != direction:
            changed = True
        state.known_trunk_links[position] = current
    if changed:
        state.trunk_epoch = (state.trunk_epoch + 1) & 0xFFFF


def _known_trunk_direction(
    state: BuilderStateData,
    position: Position,
    round_no: int,
) -> Direction | None:
    built = state.built_links.get(position)
    if built is not None and built[0] == EntityType.CONVEYOR:
        return built[1]
    remembered = state.known_trunk_links.get(position)
    if remembered is None:
        return None
    direction, seen_round = remembered
    if int(round_no) - int(seen_round) > 96:
        return None
    return direction


def _core_distance(world: WorldMemory, position: Position) -> int:
    core_cells = world.core_footprint or ({world.own_core} if world.own_core is not None else set())
    if not core_cells:
        return 999
    return min(abs(position.x - cell.x) + abs(position.y - cell.y) for cell in core_cells)


def _rough_new_links_via_trunk(
    state: BuilderStateData,
    ore: Position,
    round_no: int,
) -> int:
    """Conservative lower estimate of new links if a seen trunk can be joined.

    Only remembered links whose facing makes net progress toward the Core are
    used for the rough admission estimate.  The exact route planner still has to
    find a legal full path, so this can only make planning less prematurely
    pessimistic; it never authorizes construction by itself.
    """
    world = state.world
    if world is None:
        return 999
    direct = max(1, _core_distance(world, ore) - 1)
    best = direct
    candidates = list(state.known_trunk_links.items())
    for position, (direction, seen_round) in candidates:
        if int(round_no) - int(seen_round) > 96:
            continue
        before = _core_distance(world, position)
        after = _core_distance(world, position.add(direction))
        if after >= before:
            continue
        join_new = max(1, abs(ore.x - position.x) + abs(ore.y - position.y) - 1)
        best = min(best, join_new)
    return best


def _route_reuse_cells(
    state: BuilderStateData,
    route: RoutePlan,
    round_no: int,
) -> set[Position]:
    return {
        cell
        for cell, expected in zip(route.cells, route.directions)
        if _known_trunk_direction(state, cell, round_no) == expected
    }


def _read_claims(ct: object, width: int, height: int):
    result = []
    for index, slot in enumerate((Slot.CLAIM_0, Slot.CLAIM_1, Slot.CLAIM_2, Slot.CLAIM_3)):
        try:
            claim = unpack_claim(ct.read_store(int(slot)), width, height)
        except Exception:
            claim = None
        if claim is not None:
            result.append((index, claim))
    return result


def _world(ct: object, state: BuilderStateData) -> WorldMemory:
    width = int(ct.get_map_width())
    height = int(ct.get_map_height())
    fresh = state.world is None or (state.world.width, state.world.height) != (width, height)
    if fresh:
        state.world = WorldMemory(width, height)
        state.navigator = Navigator(
            width,
            height,
            state.world.is_navigation_blocked,
            cpu=ct.get_cpu_time_elapsed,
        )
    state.world.observe(ct)
    state.world.expire_dynamic(_round(ct))
    return state.world


def _read_strategy(ct: object, state: BuilderStateData) -> None:
    try:
        raw = int(ct.read_store(int(Slot.STRATEGY)))
        decoded = decode_strategy(raw)
        scenario = decode_scenario(raw)
        team = decode_team_status(raw)
    except Exception:
        decoded = None
        scenario = Scenario.STANDARD
        team = decode_team_status(0)
    if decoded is not None:
        state.phase, state.opening = decoded
        state.scenario = scenario
    state.team_route_target = team.route_target
    state.team_route_capacity = team.route_capacity
    state.team_maintaining_routes = team.maintaining_routes
    if team.maintaining_routes > 0:
        state.economy_established = True
    state.team_active_projects = team.active_projects
    state.team_defense_severity = team.defense_severity
    state.team_attack_priority = team.attack_priority
    try:
        pulse = decode_epoch_pulse(int(ct.read_store(int(Slot.EPOCH))))
    except Exception:
        pulse = decode_epoch_pulse(0)
    state.team_route_progress_age = pulse.route_progress_age
    state.team_core_congestion = pulse.core_congestion


def _free_worker_rank(ct: object, state: BuilderStateData) -> int:
    """Return this Builder's rank after removing only *active* route owners.

    A verified passive pipeline no longer consumes a permanent workforce slot. Its
    owner remains the Store writer for that route, but is ranked with ordinary
    mobile workers until the maintenance lease expires.
    """
    role_key = _id(ct)
    owner_ids = _priority_owner_ids(ct, state)
    if state.flex_primary_owner:
        owner_ids = tuple(owner_id for owner_id in owner_ids if owner_id != role_key)
    return max(1, role_key - sum(1 for owner_id in owner_ids if owner_id < role_key))


def _refresh_role(ct: object, state: BuilderStateData, route_owner: bool) -> None:
    world = state.world
    area = world.width * world.height if world is not None else 0
    large = area >= 500
    compact = 0 < area <= 196
    role_key = _id(ct) if route_owner else _free_worker_rank(ct, state)
    state.role_key = max(1, int(role_key))
    desired = assign_role(
        state.role_key,
        state.phase,
        state.opening,
        route_owner=route_owner,
        large_map=large,
        compact_map=compact,
        scenario=state.scenario,
    )
    # Before the first producer exists there is nothing useful to repair or guard.
    if not route_owner and state.team_maintaining_routes <= 0:
        desired = Role.SCOUT

    round_no = _round(ct)
    emergency = state.phase == Phase.DEFENSE or state.scenario == Scenario.CONTESTED
    if route_owner or emergency:
        state.role = desired
        state.role_lock_until = round_no
        return

    # Rank changes caused by route handoff used to reshuffle the entire free
    # workforce every few rounds. Keep a useful mobile specialization for a short
    # lease, then accept the newly computed role. This is deliberately bounded so
    # OFFENSE/ENDGAME can still reshape the army quickly.
    mobile_roles = {Role.REPAIR, Role.SCOUT, Role.SABOTEUR, Role.RAIDER, Role.SIEGE}
    if (
        desired != state.role
        and round_no < state.role_lock_until
        and state.role in mobile_roles
        and desired in mobile_roles
    ):
        return
    if desired != state.role:
        state.role = desired
        state.role_lock_until = round_no + (8 if state.phase in (Phase.OFFENSE, Phase.ENDGAME) else 12)
        # A newly accepted specialization must not inherit the previous role's
        # waypoint (e.g. a rear Scout target after becoming the Saboteur). That
        # stale target was another source of apparently conflicted backtracking.
        state.scout_target = None
        state.scout_target_until = -1
        if state.navigator is not None:
            state.navigator.invalidate()
    else:
        state.role = desired


def _minimum_primary_routes(state: BuilderStateData) -> int:
    """Primary economy never shrinks because the map is small or close-contact."""
    del state
    return 4


def _project_status_for_claim(
    ct: object,
    index: int,
    claim: object,
    round_no: int,
) -> int:
    """Read one fresh project heartbeat, validating it against claim ownership."""
    try:
        raw = int(ct.read_store(int(PROJECT_STATUS_SLOTS[index])))
    except Exception:
        return 0
    owner = raw >> 8
    epoch = (raw >> 2) & 63
    status = raw & 3
    if owner != int(claim.owner_id) or epoch_distance(round_no & 63, epoch) > 12:
        return 0
    return status


def _priority_owner_ids(ct: object, state: BuilderStateData) -> tuple[int, ...]:
    """Return Builders that still have an active primary-economy job.

    Status 2 is a verified passive pipeline. Keeping those owners in this set was
    the core workforce bug: every completed Harvester permanently removed one
    Builder from scouting/defense/offense even though the infrastructure runs by
    itself. Healthy owners are now excluded until their local maintenance lease
    expires and they republish a non-maintaining status.
    """
    world = state.world
    if world is None:
        return ()
    round_no = _round(ct)
    if state.priority_owner_round == round_no:
        return state.priority_owner_ids
    minimum_routes = state.team_route_target or _minimum_primary_routes(state)
    owner_slots: list[tuple[int, int]] = []
    for index, claim in _read_claims(ct, world.width, world.height):
        if not claim_is_fresh(claim, round_no & 63):
            continue
        if index >= minimum_routes and claim.position is None:
            continue
        status = _project_status_for_claim(ct, index, claim, round_no)
        if status == 2:
            continue
        owner_slots.append((claim.owner_id, index))
    owner_slots.sort()
    state.priority_owner_ids = tuple(owner_id for owner_id, _index in owner_slots)
    state.priority_owner_round = round_no
    return state.priority_owner_ids


def _route_owner_status(ct: object, state: BuilderStateData, builder_id: int) -> tuple[int | None, int]:
    """Return (claim-slot, project-status) for a current primary claim writer.

    This intentionally searches all fresh claims, not only active construction
    owners, because a handed-off status-2 owner is still the route's authoritative
    Store writer and may need to be recalled for maintenance.
    """
    world = state.world
    if world is None:
        return None, 0
    round_no = _round(ct)
    for index, claim in _read_claims(ct, world.width, world.height):
        if claim.owner_id != int(builder_id) or not claim_is_fresh(claim, round_no & 63):
            continue
        return index, _project_status_for_claim(ct, index, claim, round_no)
    return None, 0


def _builder_role_snapshot(
    ct: object,
    state: BuilderStateData,
    builder_id: int,
) -> tuple[Role, bool]:
    """Infer another friendly Builder's macro role from shared Store state.

    Roles are deterministic once current route owners are known, so a unit can
    reason about right-of-way without another Store write or private memory.
    This is deliberately a macro inference: a satellite worker may temporarily
    be busier than its inferred Scout role, but primary construction/defense
    priorities remain correct and ties still fall back to stable IDs.
    """
    world = state.world
    if world is None:
        return Role.SCOUT, False
    active_owner_ids = _priority_owner_ids(ct, state)
    route_owner = int(builder_id) in active_owner_ids
    if route_owner:
        return Role.ECONOMY, True
    rank = max(1, int(builder_id) - sum(1 for owner_id in active_owner_ids if owner_id < int(builder_id)))
    area = world.width * world.height
    role = assign_role(
        rank,
        state.phase,
        state.opening,
        route_owner=False,
        large_map=area >= 500,
        compact_map=area <= 196,
        scenario=state.scenario,
    )
    if state.team_maintaining_routes <= 0:
        role = Role.SCOUT
    return role, False


def _mission_priority_for_builder(
    ct: object,
    state: BuilderStateData,
    builder_id: int,
    *,
    route_sensitive: bool = False,
) -> int:
    """Shared-state right-of-way priority for friendly traffic.

    This is not combat target priority. It answers only which Builder should
    keep a scarce corridor/stance when two friendly missions collide.
    """
    role, route_owner = _builder_role_snapshot(ct, state, builder_id)
    route_pressure = (
        state.team_active_projects > state.team_maintaining_routes
        or state.team_maintaining_routes < (state.team_route_target or _minimum_primary_routes(state))
        or (
            state.team_route_progress_age >= 20
            and state.team_active_projects > 0
        )
    )
    if route_owner:
        slot_index, project_status = _route_owner_status(ct, state, builder_id)
        # Give scarce corridor time to the owner that can create income *now*,
        # not to every economy owner merely because some route somewhere is busy.
        # A producer-ready line is most urgent; active construction follows. A
        # healthy maintenance owner deliberately yields to an emergency defender
        # or repair worker instead of blocking the whole team.
        if project_status == 3:
            priority = 120
        elif project_status == 1:
            priority = 114
        elif project_status == 0 and route_pressure:
            priority = 86
        else:
            priority = 76
        if slot_index is not None:
            priority -= min(6, 2 * int(slot_index))
    elif role == Role.DEFENDER:
        priority = 104 if state.team_defense_severity >= 8 else 72
    elif role == Role.REPAIR:
        priority = 96 if route_pressure or state.team_defense_severity >= 6 else 68
    elif role == Role.SABOTEUR:
        priority = 84 if state.team_attack_priority >= 9 else 56
    elif role == Role.SIEGE:
        priority = 90 if state.team_attack_priority >= 13 else 62
    elif role == Role.RAIDER:
        priority = 86 if state.team_attack_priority >= 11 else 58
    else:
        priority = 44
    if int(builder_id) == _id(ct) and route_sensitive:
        priority += 12
    return priority


def _maintaining_route_count(ct: object, round_no: int) -> int:
    count = 0
    for slot in (Slot.PRIMARY_ORE, Slot.LOGISTICS, Slot.THREAT, Slot.ENEMY_CORE):
        try:
            value = int(ct.read_store(int(slot)))
        except Exception:
            continue
        epoch = (value >> 2) & 63
        status = value & 3
        if status == 2 and epoch_distance(round_no & 63, epoch) <= 12:
            count += 1
    return count


def _maintaining_claims(
    ct: object,
    state: BuilderStateData,
    round_no: int | None = None,
) -> tuple[tuple[int, object], ...]:
    """Return fresh Store claims whose owners report a healthy live pipeline."""
    world = state.world
    if world is None:
        return ()
    now = _round(ct) if round_no is None else int(round_no)
    claims = dict(_read_claims(ct, world.width, world.height))
    healthy: list[tuple[int, object]] = []
    for index, slot in enumerate(PROJECT_STATUS_SLOTS):
        claim = claims.get(index)
        if claim is None or claim.position is None or not claim_is_fresh(claim, now & 63):
            continue
        try:
            value = int(ct.read_store(int(slot)))
        except Exception:
            continue
        owner = value >> 8
        epoch = (value >> 2) & 63
        status = value & 3
        if (
            owner == claim.owner_id
            and status == 2
            and epoch_distance(now & 63, epoch) <= 12
        ):
            healthy.append((index, claim))
    return tuple(healthy)


def _frontier_claim_position(ct: object, state: BuilderStateData) -> Position | None:
    """Return the outermost maintained producer endpoint known through Store."""
    world = state.world
    if world is None or world.own_core is None:
        return None
    healthy = _maintaining_claims(ct, state)
    if not healthy:
        return None
    origin = world.own_core
    return max(
        (claim.position for _index, claim in healthy if claim.position is not None),
        key=lambda pos: (
            abs(pos.x - origin.x) + abs(pos.y - origin.y),
            pos.distance_squared(origin),
            pos.y,
            pos.x,
        ),
        default=None,
    )


def _frontier_push_target(
    ct: object,
    state: BuilderStateData,
    *,
    advance: int = 7,
) -> Position | None:
    """Project a control point beyond our outermost healthy economic line.

    The game has no explicit territory object; our durable territory is the space
    around producing infrastructure that we can see, repair, and reinforce.  This
    target makes mobile workers stage through that line and keep moving outward
    instead of repeatedly launching every mission from the Core.
    """
    world = state.world
    if world is None or world.own_core is None:
        return None
    frontier = _frontier_claim_position(ct, state)
    if frontier is None:
        return None
    origin = world.own_core
    distance = abs(frontier.x - origin.x) + abs(frontier.y - origin.y)
    minimum = max(5, min(world.width, world.height) // 3)
    if distance < minimum:
        return None

    dx = frontier.x - origin.x
    dy = frontier.y - origin.y
    sx = 0 if dx == 0 else (1 if dx > 0 else -1)
    sy = 0 if dy == 0 else (1 if dy > 0 else -1)
    if sx == 0 and sy == 0:
        return None
    # Dominant-axis advance keeps the target reachable through cardinal paths; a
    # small deterministic lateral offset spreads multiple raiders/scouts.
    step = max(4, min(10, int(advance)))
    if abs(dx) >= abs(dy):
        tx = frontier.x + sx * step
        lateral = ((abs(_id(ct)) % 3) - 1) * 2
        ty = frontier.y + lateral
    else:
        ty = frontier.y + sy * step
        lateral = ((abs(_id(ct)) % 3) - 1) * 2
        tx = frontier.x + lateral
    target = Position(
        max(0, min(world.width - 1, tx)),
        max(0, min(world.height - 1, ty)),
    )
    if target == frontier or world.is_navigation_blocked(target):
        # Fall back to the uncluttered map-edge point in the same outward
        # direction. Unknown terrain is intentionally allowed; the worker is a
        # scout/pressure unit whose job is to reveal it.
        target = Position(
            world.width - 1 if sx > 0 else (0 if sx < 0 else frontier.x),
            world.height - 1 if sy > 0 else (0 if sy < 0 else frontier.y),
        )
    return target



def _shared_enemy_core_target(state: BuilderStateData) -> Position | None:
    """Best locally usable enemy-Core coordinate.

    A Builder remembers a Core it personally observed in ``WorldMemory``.  The
    shared priority-15 rally propagates the same coordinate to the rest of the
    team.  Treat either as authoritative enough for strategic depth decisions;
    unlike a Harvester rally, a Core rally is the terminal objective.
    """
    world = state.world
    if world is not None and world.enemy_core is not None:
        return world.enemy_core
    if state.rally_target is not None and state.rally_priority >= 15:
        return state.rally_target
    return None


def _enemy_core_exclusion_zone(state: BuilderStateData, position: Position) -> bool:
    """True when an ore tile is better treated as assault space than economy.

    Building a long, fragile conveyor/Harvester line inside the enemy Core's
    immediate operating area converts positional advantage into an asset that is
    hard to defend.  Once we are this deep, mobile Builders and combat buildings
    are the valuable use of the foothold instead.
    """
    world = state.world
    core = _shared_enemy_core_target(state)
    if world is None or core is None:
        return False
    distance = abs(position.x - core.x) + abs(position.y - core.y)
    # Compact maps need a smaller absolute bubble; large maps can afford a wider
    # no-Harvester assault zone because reinforcement travel is more expensive.
    short_side = max(1, min(world.width, world.height))
    radius = max(4, min(8, short_side // 3 + 2))
    return distance <= radius


def _capture_is_supportable(ct: object, state: BuilderStateData, target: Position) -> bool:
    """Whether a sabotaged ore tile should become economy rather than a beachhead.

    Core-adjacent ore is always reserved for assault.  Deeper enemy-side ore may
    still be captured when our maintained frontier or a recently observed
    friendly conveyor trunk is close enough to make the route a real extension
    of controlled territory instead of an isolated donation to the opponent.
    """
    world = state.world
    if world is None or world.own_core is None:
        return True
    if _enemy_core_exclusion_zone(state, target):
        return False

    enemy_core = _shared_enemy_core_target(state)
    if enemy_core is None:
        return True
    own_distance = abs(target.x - world.own_core.x) + abs(target.y - world.own_core.y)
    enemy_distance = abs(target.x - enemy_core.x) + abs(target.y - enemy_core.y)
    # If the tile is not clearly on their side, ordinary economic scoring is
    # sufficient. The dangerous case is a deep incursion unsupported by our net.
    if enemy_distance + 4 >= own_distance:
        return True

    round_no = _round(ct)
    trunk_supported = any(
        round_no - int(seen_round) <= 96
        and abs(position.x - target.x) + abs(position.y - target.y) <= 5
        for position, (_direction, seen_round) in state.known_trunk_links.items()
    )
    if trunk_supported:
        return True

    frontier = _frontier_claim_position(ct, state)
    if frontier is None:
        return False
    frontier_gap = abs(frontier.x - target.x) + abs(frontier.y - target.y)
    support_radius = max(6, min(10, min(world.width, world.height) // 3 + 3))
    return frontier_gap <= support_radius


def _assault_engineer(state: BuilderStateData) -> bool:
    """Allow several first-wave attackers to build a real Core-kill foothold.

    v0042 depended on exactly one SIEGE role reaching the right tile.  Once the
    enemy Core is confirmed, the first few attack ordinals may also act as siege
    engineers.  This remains bounded, so the team does not turn every Raider into
    an expensive turret spammer.
    """
    if state.role == Role.SIEGE:
        return True
    if state.role != Role.RAIDER or state.team_attack_priority < 15:
        return False
    world = state.world
    area = world.width * world.height if world is not None else 324
    limit = 2 if area <= 196 else (3 if area < 500 else 4)
    return _attack_worker_ordinal(state) <= limit

def _primary_owner_can_flex(
    state: BuilderStateData,
    target: Position | None,
    round_no: int,
) -> bool:
    """Release a verified primary owner until its maintenance lease expires.

    The Store claim and local route blueprint remain intact. This makes handoff
    reversible: passive infrastructure keeps earning with no babysitter, while a
    stale verification automatically turns the same Builder back into an active
    route owner for one service pass. Defense overlays can recall it sooner when
    an actual threat is observed near its route.
    """
    return bool(
        state.claim_slot is not None
        and target is not None
        and state.route is not None
        and _route_health_fresh(state, int(round_no))
        and state.scenario != Scenario.ECONOMY_RESCUE
    )


def _active_primary_job(state: BuilderStateData) -> bool:
    return state.claim_slot is not None and not state.flex_primary_owner


def _free_mobile_worker(state: BuilderStateData) -> bool:
    return not _active_primary_job(state) and not state.satellite_mode


def _compact_map(state: BuilderStateData) -> bool:
    world = state.world
    return bool(world is not None and world.width * world.height <= 196)


def _offense_active(state: BuilderStateData) -> bool:
    return (
        state.phase in (Phase.OFFENSE, Phase.ENDGAME)
        and state.scenario not in (Scenario.ECONOMY_RESCUE, Scenario.CONTESTED)
    )


def _pressure_active(state: BuilderStateData) -> bool:
    """Allow a small mobile raid once the minimum economy is saturated."""
    return _offense_active(state) or (
        state.phase == Phase.ECONOMY
        and state.scenario == Scenario.EXPANSION
        and state.role == Role.RAIDER
)


def _read_rally(ct: object, state: BuilderStateData) -> None:
    try:
        decoded = decode_rally(
            ct.read_store(int(Slot.RALLY)),
            int(ct.get_map_width()),
            int(ct.get_map_height()),
        )
    except Exception:
        decoded = None
    if decoded is None:
        state.rally_target = None
        state.rally_expires_epoch = 0
        state.rally_priority = 0
        return
    position, expires, priority = decoded
    forward = (int(expires) - (_round(ct) & 63)) & 63
    horizon = 30 if int(priority) >= 15 else 8
    if position is None or forward > horizon:
        state.rally_target = None
        state.rally_expires_epoch = 0
        state.rally_priority = 0
        return
    state.rally_target = position
    state.rally_expires_epoch = int(expires)
    state.rally_priority = int(priority)


def _read_defense_alert(ct: object, state: BuilderStateData) -> None:
    try:
        decoded = decode_defense_alert(
            ct.read_store(int(Slot.DEFENSE_ALERT)),
            int(ct.get_map_width()),
            int(ct.get_map_height()),
        )
    except Exception:
        decoded = None
    if decoded is None:
        state.defense_target = None
        state.defense_expires_epoch = 0
        state.defense_severity = 0
        state.defense_kind = ThreatKind.UNKNOWN
        return
    position, expires, severity, kind = decoded
    forward = (int(expires) - (_round(ct) & 63)) & 63
    if position is None or forward > 12:
        state.defense_target = None
        state.defense_expires_epoch = 0
        state.defense_severity = 0
        state.defense_kind = ThreatKind.UNKNOWN
        return
    state.defense_target = position
    state.defense_expires_epoch = int(expires)
    state.defense_severity = max(1, int(severity))
    state.defense_kind = kind


def _publish_rally(
    ct: object,
    state: BuilderStateData,
    target: Position,
    *,
    priority: int = 1,
) -> None:
    round_no = _round(ct)
    priority = max(0, min(15, int(priority)))
    if round_no - state.last_rally_write < 3 and priority <= state.rally_priority:
        return
    # Never replace a fresh Core/Harvester objective with a lower-value local
    # conveyor.  The store is buffered, so this comparison uses the shared
    # previous-round plan and remains deterministic for every unit this turn.
    if state.rally_target is not None and state.rally_priority > priority:
        return
    try:
        expires = (round_no + (30 if priority >= 15 else 8)) & 63
        ct.write_store(
            int(Slot.RALLY),
            encode_rally(
                target,
                int(ct.get_map_width()),
                expires,
                priority,
            ),
        )
        state.rally_target = target
        state.rally_expires_epoch = expires
        state.rally_priority = priority
        state.last_rally_write = round_no
    except Exception:
        pass


def _publish_defense_alert(
    ct: object,
    state: BuilderStateData,
    target: Position,
    *,
    severity: int = 8,
    kind: ThreatKind = ThreatKind.UNKNOWN,
) -> None:
    round_no = _round(ct)
    if round_no - state.last_defense_alert < 2 and severity < 14:
        return
    # Multiple units can report in one buffered round. Never replace a stronger
    # still-fresh alarm with a weaker logistics sighting.
    try:
        current = decode_defense_alert(
            ct.read_store(int(Slot.DEFENSE_ALERT)),
            int(ct.get_map_width()),
            int(ct.get_map_height()),
        )
    except Exception:
        current = None
    if current is not None:
        _pos0, expires0, severity0, _kind0 = current
        forward = (int(expires0) - (round_no & 63)) & 63
        if forward <= 12 and int(severity0) > int(severity):
            return
    try:
        ct.write_store(
            int(Slot.DEFENSE_ALERT),
            encode_defense_alert(
                target,
                int(ct.get_map_width()),
                (round_no + 12) & 63,
                severity,
                kind,
            ),
        )
        state.last_defense_alert = round_no
    except Exception:
        pass


def _visible_firing_source(
    ct: object,
    victim: Position,
) -> tuple[Position | None, ThreatKind]:
    """Identify a visible turret whose current firing geometry can hit victim."""
    candidates: list[tuple[int, Position, ThreatKind]] = []
    for entity_id, entity_type, position in _enemy_entities(ct, buildings_only=True):
        if entity_type not in (EntityType.GUNNER, EntityType.SENTINEL):
            continue
        try:
            facing = ct.get_direction(entity_id)
            if not ct.can_fire_from(position, facing, entity_type, victim):
                continue
        except Exception:
            continue
        kind = ThreatKind.SENTINEL_FIRE if entity_type == EntityType.SENTINEL else ThreatKind.GUNNER_FIRE
        # Prefer the long-range Sentinel when both lines overlap; it is the more
        # dangerous source and barriers cannot stop its shot.
        priority = 2 if entity_type == EntityType.SENTINEL else 1
        candidates.append((priority, position, kind))
    if not candidates:
        return None, ThreatKind.UNKNOWN
    _priority, position, kind = max(candidates, key=lambda item: (item[0], -victim.distance_squared(item[1])))
    return position, kind


def _damage_kind(delta: int, *, core: bool = False) -> ThreatKind:
    delta = max(0, int(delta))
    if core and delta in (2, 4, 6):
        return ThreatKind.BUILDER_RUSH
    if delta in (18, 36):
        return ThreatKind.SENTINEL_FIRE
    if delta in (7, 14, 21, 28):
        return ThreatKind.GUNNER_FIRE
    if delta >= 15:
        return ThreatKind.SENTINEL_FIRE
    if delta >= 6:
        return ThreatKind.GUNNER_FIRE
    return ThreatKind.FIRING_LINE


def _publish_damage_alarm_if_needed(ct: object, state: BuilderStateData) -> None:
    """Turn unexplained damage near owned territory into a shared alarm.

    Vision is local and Sentinels can shoot through walls from farther than a
    Builder can necessarily see. A Builder that takes damage while standing near
    home or a maintained route is therefore a valuable sensor even if no hostile
    entity is currently visible. Deep offensive workers deliberately do *not*
    recall the team merely because they were shot in enemy territory.
    """
    try:
        hp = int(ct.get_hp())
    except Exception:
        return
    previous = state.last_hp
    state.last_hp = hp
    if previous is None or hp >= previous:
        return
    damage_delta = max(1, int(previous) - hp)
    world = state.world
    if world is None:
        return
    current = _pos(ct)
    near_home = bool(
        world.own_core is not None and current.distance_squared(world.own_core) <= 49
    )
    near_owned_route = False
    if state.route is not None:
        near_owned_route = min(
            (current.distance_squared(cell) for cell in state.route.cells),
            default=999,
        ) <= 20
    # Every mobile worker is a sensor for the *team* network. A claimless Scout or
    # Saboteur taking a ranged hit beside somebody else's Harvester must publish
    # it just as reliably as the owner/repairer.
    if not near_owned_route:
        near_owned_route = _team_economy_near(
            ct, state, current, harvester_radius_sq=36, trunk_radius_sq=12
        )
    if not (near_home or near_owned_route):
        return
    source, source_kind = _visible_firing_source(ct, current)
    inferred_kind = source_kind if source is not None else _damage_kind(damage_delta)
    _publish_defense_alert(
        ct,
        state,
        source or current,
        severity=15 if near_home or inferred_kind == ThreatKind.SENTINEL_FIRE else 13,
        kind=inferred_kind,
    )



def _publish_project_status(ct: object, state: BuilderStateData) -> None:
    if state.claim_slot is None:
        return
    if _route_health_fresh(state, _round(ct)):
        status = 2
    elif (
        state.route is not None
        and state.route_index < 0
        and state.ore_target is not None
        and all(
            state.built_links.get(cell) == (EntityType.CONVEYOR, direction)
            for cell, direction in zip(state.route.cells, state.route.directions)
        )
    ):
        # The expensive transport line is complete and the only missing piece is
        # the producer.  The Core uses this state to stop optional Builder
        # purchases until the Harvester can be afforded.
        entity_id, entity_type, _ = _visible(ct, state.ore_target)
        if entity_type == EntityType.HARVESTER and _is_friendly(ct, entity_id):
            status = 2
        else:
            try:
                ore_visible = bool(ct.is_in_vision(state.ore_target))
            except Exception:
                ore_visible = False
            # Do not report "producer missing" from stale off-screen memory while
            # the owner is halfway through a verification patrol.
            status = 3 if ore_visible else 1
    elif state.route is not None or state.route_search is not None or state.ore_target is not None:
        # A heartbeat is not progress. On maze maps a pioneer can otherwise hold
        # the opening forever while replanning the same impossible corridor.
        stalled_for = _round(ct) - max(state.last_real_route_progress_round, state.claim_started_round)
        status = 0 if stalled_for >= 36 and state.route_index >= 0 else 1
    else:
        status = 0
    round_no = _round(ct)
    if status == state.last_project_status and round_no - state.last_project_write < 4:
        return
    slot = (Slot.PRIMARY_ORE, Slot.LOGISTICS, Slot.THREAT, Slot.ENEMY_CORE)[state.claim_slot]
    try:
        ct.write_store(int(slot), (_id(ct) << 8) | ((round_no & 63) << 2) | status)
        state.last_project_status = status
        state.last_project_write = round_no
    except Exception:
        pass

def _visible(ct: object, position: Position):
    try:
        entity_id = ct.get_tile_building_id(position)
    except Exception:
        return None, None, None
    if entity_id is None:
        return None, None, None
    try:
        entity_type = ct.get_entity_type(entity_id)
    except Exception:
        entity_type = None
    try:
        direction = ct.get_direction(entity_id)
    except Exception:
        direction = None
    return entity_id, entity_type, direction


def _is_friendly(ct: object, entity_id: int | None) -> bool:
    if entity_id is None:
        return False
    try:
        return ct.get_team(entity_id) == ct.get_team()
    except Exception:
        return False


def _claim(ct: object, state: BuilderStateData, world: WorldMemory, round_no: int):
    claims = _read_claims(ct, world.width, world.height)
    own = next(((index, claim) for index, claim in claims if claim.owner_id == _id(ct)), None)
    if own is None:
        if state.claim_slot is not None:
            _reset_route(state, keep_target=False)
        state.claim_slot = None
        return None
    index, claim = own
    state.claim_slot = index
    if not claim_is_fresh(claim, round_no & 63) and epoch_distance(round_no & 63, claim.epoch) > 40:
        return None
    if claim.position is not None:
        duplicates = [
            (other_index, other)
            for other_index, other in claims
            if other.position == claim.position
        ]
        winner = min(duplicates, key=lambda item: (item[0], item[1].owner_id)) if duplicates else (index, claim)
        if winner[0] != index or winner[1].owner_id != _id(ct):
            # Store writes are delayed by one round, so two owners can discover
            # and claim the same ore simultaneously. Lowest claim slot wins; the
            # loser releases the duplicate and resumes its own exploration shard.
            _reset_route(state, keep_target=False)
            try:
                ct.write_store(
                    int(claim_slot(index)),
                    pack_claim(None, world.width, round_no, _id(ct), world.height),
                )
            except Exception:
                pass
            return None
        # A scout may hand this owner an ore coordinate that the owner has not
        # personally seen. Sensing methods are local, so treating an off-screen
        # lookup failure as "not ore" silently discarded every useful handoff.
        # Accept unseen claims provisionally and verify them once the tile enters
        # vision; reject only a visible tile that is definitively not ore.
        try:
            visible = bool(ct.is_in_vision(claim.position))
        except Exception:
            visible = claim.position in world.ore_positions
        if not visible:
            valid = True
        else:
            try:
                valid = ct.get_tile_env(claim.position) == Environment.ORE_TITANIUM
            except Exception:
                valid = claim.position in world.ore_positions
        if valid:
            if state.ore_target is not None and state.ore_target != claim.position:
                _reset_route(state, keep_target=False)
            state.ore_target = claim.position
            if round_no % 4 == 0:
                try:
                    ct.write_store(
                        int(claim_slot(index)),
                        pack_claim(claim.position, world.width, round_no, _id(ct), world.height),
                    )
                except Exception:
                    pass
            return claim.position
        _reset_route(state, keep_target=False)
        return None

    # Later primary owners wait briefly for the survey network to populate their
    # empty Store claim. Without this handoff window a newly spawned owner sees
    # only Core-local ore and immediately locks itself to another local deposit,
    # defeating the frontier scoring below. Store writes are visible next round,
    # so two rounds is enough for a Scout offer without materially delaying a map
    # that has no outer discovery yet.
    if index >= 1 and _any_route_maintaining(ct, round_no):
        claim_age = epoch_distance(round_no & 63, claim.epoch)
        if claim_age <= 2:
            return None

    for rejected, until in tuple(state.rejected_ore_until.items()):
        if until <= round_no:
            state.rejected_ore_until.pop(rejected, None)
    claimed = {
        other.position
        for _, other in claims
        if other.position is not None and other.owner_id != _id(ct)
    }
    candidates = [
        position
        for position in world.known_ore()
        if position not in claimed and position not in state.rejected_ore_until
    ]
    if not candidates:
        try:
            candidates = [
                tile
                for tile in tuple(ct.get_nearby_tiles())[:128]
                if tile not in claimed
                and tile not in state.rejected_ore_until
                and ct.get_tile_env(tile) == Environment.ORE_TITANIUM
            ]
        except Exception:
            candidates = []
    # Optional Store-backed routes (beyond the map's minimum resilient target)
    # are economic opportunities, not obligations. Required primary routes keep
    # the permissive bootstrap behavior; optional routes include estimated travel
    # and build time so long frontier lines are allowed early but rejected when
    # they are too late to repay.
    optional_scores: dict[Position, float] = {}
    if candidates and index >= 1 and _any_route_maintaining(ct, round_no):
        try:
            conveyor_cost = max(0, int(ct.get_conveyor_cost()))
            harvester_cost = max(0, int(ct.get_harvester_cost()))
        except Exception:
            conveyor_cost = BASE_CONVEYOR_COST
            harvester_cost = BASE_HARVESTER_COST
        core_cells = world.core_footprint or ({world.own_core} if world.own_core is not None else set())
        frontier = _frontier_claim_position(ct, state)
        frontier_distance = 0
        if frontier is not None and core_cells:
            frontier_distance = min(
                abs(frontier.x - cell.x) + abs(frontier.y - cell.y)
                for cell in core_cells
            )
        profitable: list[Position] = []
        for position in candidates:
            if core_cells:
                distance = min(
                    abs(position.x - cell.x) + abs(position.y - cell.y)
                    for cell in core_cells
                )
            else:
                distance = abs(position.x - _pos(ct).x) + abs(position.y - _pos(ct).y)
            rough_new_links = min(
                max(1, distance - 1),
                _rough_new_links_via_trunk(state, position, round_no),
            )
            estimated = harvester_cost + estimate_route_cost(rough_new_links, conveyor_cost)
            # Reused trunk cells still take travel/verification time but require
            # no build action.  New cells therefore dominate construction delay.
            build_delay = max(6, max(1, distance - 1) + rough_new_links + 6)
            production_start = round_no + build_delay
            payback = estimate_payback_round(
                estimated,
                output_per_round=2.5,
                start_round=production_start,
                horizon=970,
            )
            if payback is None:
                continue
            remaining_output = max(0.0, (1000 - production_start) * 2.5)
            frontier_gain = max(0, distance - frontier_distance)
            frontier_weight = 3 if index == 1 else (6 if index == 2 else 8)
            optional_scores[position] = (
                remaining_output
                - estimated
                - 0.5 * distance
                + min(140, frontier_gain * frontier_weight)
                + (_secure_ore_bias(world, world.own_core or _pos(ct), position) if index <= 2 else 0)
            )
            profitable.append(position)
        candidates = profitable

    if not candidates:
        if round_no % 4 == 0:
            try:
                ct.write_store(
                    int(claim_slot(index)),
                    pack_claim(None, world.width, round_no, _id(ct), world.height),
                )
            except Exception:
                pass
        return None
    origin = world.own_core or _pos(ct)
    if optional_scores:
        candidates.sort(
            key=lambda position: (
                -optional_scores.get(position, float("-inf")),
                position.y,
                position.x,
            )
        )
    else:
        candidates.sort(
            key=lambda position: (
                -score_ore(
                    position,
                    origin=origin,
                    expected_output_horizon=max(0, 1000 - round_no) * 2,
                ),
                position.y,
                position.x,
            )
        )
    # During the first buffered assignment round every owner sees the same empty
    # claim snapshot. If all of them choose candidates[0], they collide on one
    # ore and lose another round resolving duplicates. Shard the initial known
    # list by claim slot; once any real claim exists, take the best remaining ore.
    if not claimed:
        if index >= len(candidates):
            if round_no % 4 == 0:
                try:
                    ct.write_store(
                        int(claim_slot(index)),
                        pack_claim(None, world.width, round_no, _id(ct), world.height),
                    )
                except Exception:
                    pass
            return None
        target = candidates[index]
    else:
        target = candidates[0]
    state.ore_target = target
    state.claim_epoch = round_no & 63
    state.claim_started_round = round_no
    try:
        ct.write_store(
            int(claim_slot(index)),
            pack_claim(target, world.width, round_no, _id(ct), world.height),
        )
    except Exception:
        pass
    return target



def _offer_discovered_ore(
    ct: object,
    state: BuilderStateData,
    world: WorldMemory,
    round_no: int,
) -> bool:
    """Let free surveyors hand ore coordinates to waiting route owners.

    A write does not consume the Builder action, so the scout continues moving
    in the same turn. Duplicate reports are harmless: claim arbitration keeps the
    lowest slot and releases the others on the following round.
    """
    if round_no - state.last_ore_offer_round < 3:
        return False
    claims = [
        (index, claim)
        for index, claim in _read_claims(ct, world.width, world.height)
        if claim_is_fresh(claim, round_no & 63)
    ]
    waiting = [
        (index, claim)
        for index, claim in claims
        if claim.position is None and index != state.claim_slot
    ]
    if not waiting:
        return False
    claimed = {claim.position for _index, claim in claims if claim.position is not None}
    bootstrap = not _any_route_maintaining(ct, round_no)
    try:
        conveyor_cost = max(0, int(ct.get_conveyor_cost()))
        harvester_cost = max(0, int(ct.get_harvester_cost()))
    except Exception:
        conveyor_cost = BASE_CONVEYOR_COST
        harvester_cost = BASE_HARVESTER_COST
    core_cells = world.core_footprint or ({world.own_core} if world.own_core is not None else set())
    candidates: list[Position] = []
    for position in world.known_ore():
        if position in claimed or position in state.rejected_ore_until:
            continue
        try:
            building_id = ct.get_tile_building_id(position)
            if building_id is not None:
                continue
        except Exception:
            # Unknown/off-screen ore from this scout's own memory is still a
            # valid report; the owner will verify it on arrival.
            pass
        if core_cells:
            distance = min(
                abs(position.x - cell.x) + abs(position.y - cell.y)
                for cell in core_cells
            )
            rough_new_links = min(
                max(1, distance - 1),
                _rough_new_links_via_trunk(state, position, round_no),
            )
            estimated_cost = harvester_cost + estimate_route_cost(rough_new_links, conveyor_cost)
            if not bootstrap and estimate_payback_round(
                estimated_cost,
                output_per_round=2.5,
                start_round=round_no,
                horizon=1000,
            ) is None:
                continue
        candidates.append(position)
    if not candidates:
        return False
    origin = world.own_core or _pos(ct)
    # Use the one-round buffered store to fill distinct waiting channels in
    # parallel. Select the waiting slot first because later slots intentionally
    # value frontier gain more strongly than the first-income route.
    ordered_waiting = sorted(waiting, key=lambda item: item[0])
    rank = abs(_id(ct)) % len(ordered_waiting)
    index, claim = ordered_waiting[rank]
    if bootstrap or index == 0:
        candidates.sort(
            key=lambda position: (
                -score_ore(
                    position,
                    origin=origin,
                    expected_output_horizon=max(0, 1000 - round_no) * 2,
                ),
                position.y,
                position.x,
            )
        )
    else:
        frontier = _frontier_claim_position(ct, state)
        frontier_distance = 0
        if frontier is not None and core_cells:
            frontier_distance = min(
                abs(frontier.x - cell.x) + abs(frontier.y - cell.y)
                for cell in core_cells
            )
        frontier_weight = 3 if index == 1 else (6 if index == 2 else 8)

        def offer_score(position: Position) -> float:
            if core_cells:
                distance = min(
                    abs(position.x - cell.x) + abs(position.y - cell.y)
                    for cell in core_cells
                )
            else:
                distance = abs(position.x - origin.x) + abs(position.y - origin.y)
            rough_new_links = min(
                max(1, distance - 1),
                _rough_new_links_via_trunk(state, position, round_no),
            )
            estimated = harvester_cost + estimate_route_cost(rough_new_links, conveyor_cost)
            build_delay = max(6, max(1, distance - 1) + rough_new_links + 6)
            remaining_output = max(0.0, (1000 - (round_no + build_delay)) * 2.5)
            frontier_gain = max(0, distance - frontier_distance)
            return (
                remaining_output
                - estimated
                - 0.5 * distance
                + min(140, frontier_gain * frontier_weight)
                + (_secure_ore_bias(world, origin, position) if index <= 2 else 0)
            )

        candidates.sort(
            key=lambda position: (-offer_score(position), position.y, position.x)
        )
    target = candidates[min(rank, len(candidates) - 1)]
    try:
        ct.write_store(
            int(claim_slot(index)),
            pack_claim(target, world.width, round_no, claim.owner_id, world.height),
        )
    except Exception:
        return False
    state.last_ore_offer_round = round_no
    return True


def _any_route_maintaining(ct: object, round_no: int) -> bool:
    """Return whether a route owner recently confirmed a live producer chain."""
    for slot in (Slot.PRIMARY_ORE, Slot.LOGISTICS, Slot.THREAT, Slot.ENEMY_CORE):
        try:
            value = int(ct.read_store(int(slot)))
        except Exception:
            continue
        epoch = (value >> 2) & 63
        status = value & 3
        if status == 2 and epoch_distance(round_no & 63, epoch) <= 12:
            return True
    return False


def _route_can_start_construction(
    ct: object,
    state: BuilderStateData,
    round_no: int,
) -> bool:
    """Finish useful pipelines instead of fragmenting titanium across trunks.

    The first producer is serialized because its immediate 10-Ti output is the
    fastest way to fund everything else.  Once income exists, at most the next
    two primary channels are released in parallel.  A producer-ready lower route
    always blocks new Conveyor spending until its Harvester is purchased.
    """
    if state.route is None or state.claim_slot is None:
        return True

    maintaining = 0
    producer_ready = 0
    stalled_lower = False
    own_slot = int(state.claim_slot)
    for index, slot in enumerate((Slot.PRIMARY_ORE, Slot.LOGISTICS, Slot.THREAT, Slot.ENEMY_CORE)):
        try:
            value = int(ct.read_store(int(slot)))
        except Exception:
            continue
        epoch = (value >> 2) & 63
        if epoch_distance(round_no & 63, epoch) > 12:
            continue
        status = value & 3
        if status == 2:
            maintaining += 1
        elif status == 3:
            producer_ready += 1
        elif status == 0 and index < own_slot:
            stalled_lower = True

    if producer_ready > 0:
        return False
    if own_slot == 0:
        return True

    # A *funded* second pioneer is useful on resource-rich openings.  The old
    # policy released every short route at once; strict serialization then swung
    # too far the other way and gave up early Harvester ticks on rich maps. Keep
    # the concurrency cap at two and require enough bank for two producers, this
    # route's links, a conservative pioneer segment, and a liquidity floor.
    if maintaining == 0 and own_slot == 1:
        try:
            resources = max(0, int(ct.get_global_resources()))
            harvester = max(0, int(ct.get_harvester_cost()))
            conveyor = max(0, int(ct.get_conveyor_cost()))
        except Exception:
            resources = 0
            harvester = BASE_HARVESTER_COST
            conveyor = BASE_CONVEYOR_COST
        funded_parallel = (
            2 * harvester
            + (len(state.route.cells) + 6) * conveyor
            + 30
        )
        if resources >= funded_parallel:
            return True

    # Normal bounded release: one pioneer before income, then two unfinished
    # projects may follow each completed producer.  This is geometry-agnostic and
    # avoids the old "short route => everybody spends now" compact-map failure.
    if maintaining > 0:
        normal_limit = min(3, maintaining + 1)
        if own_slot <= normal_limit:
            return True

    # Never let one impossible pioneer freeze the whole match.  The fallback is
    # deliberately much slower than normal release so it acts only as recovery.
    if state.scenario == Scenario.ECONOMY_RESCUE or stalled_lower:
        fallback_round = (0, 72, 150, 230)[max(0, min(3, own_slot))]
        return round_no >= fallback_round
    return False

def _spend_allowed(
    ct: object,
    cost: int,
    *,
    route_completion: bool = False,
    producer_purchase: bool = False,
    emergency: bool = False,
    paid_attack: bool = False,
    endgame_commit: bool = False,
) -> bool:
    try:
        resources = int(ct.get_global_resources())
        round_no = _round(ct)
    except Exception:
        return False
    try:
        raw_budget = int(ct.read_store(int(Slot.BUDGET)))
        budget = decode_budget(raw_budget) if raw_budget > 0 else None
    except Exception:
        budget = None
    if budget is None:
        try:
            decoded = decode_strategy(int(ct.read_store(int(Slot.STRATEGY))))
            phase = decoded[0] if decoded is not None else Phase.ECONOMY
        except Exception:
            phase = Phase.ECONOMY
        budget = compute_budget(ct, phase=phase)
    cost = max(0, int(cost))
    if cost <= 0:
        return False
    if paid_attack and round_no >= 975 and not endgame_commit:
        return False
    reserve = budget.liquidity
    if route_completion:
        try:
            harvester_cost = max(0, int(ct.get_harvester_cost()))
        except Exception:
            harvester_cost = BASE_HARVESTER_COST
        if producer_purchase:
            # Once the line is ready, buying the producer is the highest-value
            # economic action. Keep only a small emergency floor instead of a
            # fully scaled future Builder purchase.
            reserve = min(20, max(5, cost // 5))
        else:
            # Conveyor construction must preserve the producer that makes the
            # line useful, but it must not preserve an increasingly expensive
            # Builder as well.
            reserve = min(reserve, max(20, harvester_cost))
    else:
        reserve += budget.construction
    if not emergency:
        reserve += budget.defense
    return resources >= cost + reserve


def _bootstrap_defense_build_allowed(state: BuilderStateData) -> bool:
    """Avoid redundant pre-income structures on close-contact geometries."""
    if state.team_maintaining_routes > 0 or state.economy_established:
        return True
    world = state.world
    close_specialized = bool(
        world is not None
        and min(world.width, world.height) <= 20
        and state.opening != Opening.BALANCED_ECONOMY
    )
    if not close_specialized:
        return True
    return bool(
        state.role == Role.DEFENDER
        and state.role_key == 1
        and not state.bootstrap_defense_built
    )


def _bootstrap_owner_builder_interrupt_allowed(
    state: BuilderStateData,
    *,
    local: bool,
    distance_squared: int,
) -> bool:
    """Keep first-income owners on route unless an intruder reaches them.

    Free workers receive the same shared Builder-rush alert and remain available
    to respond.  Pulling every active owner toward a merely nearby roaming
    Builder can freeze all valid Conveyor plans indefinitely.  Once this team has
    established income, or the intruder is in immediate personal contact, the
    normal defense policy resumes.
    """
    world = state.world
    close_specialized = bool(
        world is not None
        and min(world.width, world.height) <= 20
        and state.opening != Opening.BALANCED_ECONOMY
    )
    if (
        not close_specialized
        or state.claim_slot is None
        or not _active_primary_job(state)
        or state.team_maintaining_routes > 0
        or state.economy_established
    ):
        return True
    return bool(local and max(0, int(distance_squared)) <= 2)


def _reset_route(state: BuilderStateData, *, keep_target: bool = True) -> None:
    state.route_search = None
    state.route = None
    state.route_index = -1
    state.route_shared_links.clear()
    state.repair_index = None
    if not keep_target:
        state.built_links.clear()
    state.last_final_storage = None
    state.delivery_started_round = None
    state.last_delivery_round = None
    state.last_full_verify_round = None
    state.last_harvester_seen_round = None
    state.patrol_index = -1
    state.patrol_direction = 1
    state.next_patrol_round = 0
    state.blocked_steps = 0
    state.stuck_goal = None
    state.stuck_since_round = -1
    state.best_goal_distance = 1 << 30
    state.last_goal_progress_round = -1
    state.last_blocker_position = None
    state.last_blocker_id = None
    state.build_fail_position = None
    state.build_fail_count = 0
    state.last_build_fail_round = -999
    if not keep_target:
        state.ore_target = None
        state.route_blocked.clear()
        if state.temporary_route_blocked:
            state.temporary_route_blocked.clear()
            state.route_avoid_epoch += 1
        state.route_plan_failures = 0
        state.last_route_plan_failure = -999
        state.layout_invalidations = 0
        state.last_real_route_progress_round = -1


def _clear_build_failure(state: BuilderStateData) -> None:
    state.build_fail_position = None
    state.build_fail_count = 0
    state.last_build_fail_round = -999


def _record_build_failure(
    state: BuilderStateData,
    target: Position,
    round_no: int,
    *,
    threshold: int = 2,
) -> bool:
    if state.build_fail_position != target or round_no - state.last_build_fail_round > 2:
        state.build_fail_position = target
        state.build_fail_count = 1
    else:
        state.build_fail_count += 1
    state.last_build_fail_round = round_no
    return state.build_fail_count >= max(1, int(threshold))


def _normalize_route_state(state: BuilderStateData) -> None:
    """Repair stale local indices before route logic dereferences them."""
    route = state.route
    if route is None:
        state.route_index = -1
        state.repair_index = None
        state.patrol_index = -1
        return
    if not route.cells or len(route.cells) != len(route.directions):
        _reset_route(state)
        return
    last = len(route.cells) - 1
    if state.route_index > last:
        state.route_index = last
    if state.repair_index is not None and not 0 <= state.repair_index <= last:
        state.repair_index = None
    if state.patrol_index > last:
        state.patrol_index = -1


def _release_ore_claim(
    ct: object,
    state: BuilderStateData,
    round_no: int,
) -> None:
    slot = state.claim_slot
    rejected = state.ore_target
    _reset_route(state, keep_target=False)
    if rejected is not None:
        state.rejected_ore_until[rejected] = round_no + 80
    if slot is None:
        return
    try:
        ct.write_store(
            int(claim_slot(slot)),
            pack_claim(
                None,
                int(ct.get_map_width()),
                round_no,
                _id(ct),
                int(ct.get_map_height()),
            ),
        )
    except Exception:
        pass


def _register_route_plan_failure(
    ct: object,
    state: BuilderStateData,
    round_no: int,
    *,
    definitive: bool,
) -> None:
    if not definitive:
        return
    if round_no - state.last_route_plan_failure > 6:
        state.route_plan_failures = 0
    state.route_plan_failures += 1
    state.last_route_plan_failure = round_no
    if state.route_plan_failures >= 4:
        _release_ore_claim(ct, state, round_no)


def _builder_at(ct: object, position: Position) -> tuple[int | None, bool | None]:
    try:
        builder_id = ct.get_tile_builder_bot_id(position)
    except Exception:
        return None, None
    if builder_id is None:
        return None, None
    try:
        return int(builder_id), ct.get_team(builder_id) == ct.get_team()
    except Exception:
        return int(builder_id), None


def _record_move(state: BuilderStateData, position: Position) -> None:
    state.move_history.append(position)
    if len(state.move_history) > 8:
        del state.move_history[:-8]


def _prune_temporary_route_blocks(state: BuilderStateData, round_no: int) -> None:
    expired = [position for position, until in state.temporary_route_blocked.items() if until <= round_no]
    if expired:
        for position in expired:
            state.temporary_route_blocked.pop(position, None)
        state.route_avoid_epoch += 1


def _temporarily_avoid_route_cell(
    state: BuilderStateData,
    position: Position,
    round_no: int,
    *,
    duration: int,
) -> None:
    until = round_no + max(2, int(duration))
    if until > state.temporary_route_blocked.get(position, -1):
        state.temporary_route_blocked[position] = until
        state.route_avoid_epoch += 1


def _escape_step(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
    goal: Position,
    *,
    blocker: Position | None = None,
    adjacent: bool = False,
) -> bool:
    """Take a deterministic passing-bay/backtrack step after a deadlock.

    The score prefers locally open, recently unvisited tiles and moves away from
    the blocker without completely abandoning the strategic goal. Engine
    ``can_move`` remains authoritative for transient occupancy.
    """
    world = state.world
    if world is None:
        return False
    current = _pos(ct)
    recent = set(state.move_history[-4:])
    candidates: list[tuple[int, Direction, Position]] = []
    rotation = (_id(ct) + state.cursor) % 4
    for offset in range(4):
        direction = CARDINALS[(rotation + offset) % 4]
        candidate = current.add(direction)
        if adjacent and candidate == goal:
            continue
        try:
            if not ct.can_move(direction):
                continue
        except Exception:
            continue
        freedom = 0
        for neighbour_direction in CARDINALS:
            neighbour = candidate.add(neighbour_direction)
            if not world.is_navigation_blocked(neighbour):
                freedom += 1
        goal_distance = candidate.distance_squared(goal)
        blocker_distance = candidate.distance_squared(blocker) if blocker is not None else 0
        revisit_score = -80 if candidate in recent else 12
        score = 18 * freedom + revisit_score + 3 * blocker_distance - goal_distance
        # Stable tie-breaking still differs between units, preventing a whole
        # group from choosing the same side of a congestion point.
        score -= offset
        candidates.append((score, direction, candidate))
    for _score, direction, candidate in sorted(candidates, key=lambda item: -item[0]):
        if actions.move(direction):
            state.blocked_steps = 0
            state.cursor = (state.cursor + 1) % 4
            distance = candidate.distance_squared(goal)
            if distance < state.best_goal_distance:
                state.best_goal_distance = distance
                state.last_goal_progress_round = _round(ct)
            if state.navigator is not None:
                state.navigator.invalidate()
            _record_move(state, candidate)
            return True
    return False


def _yield_to_urgent_neighbor(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """Vacate a shared lane when an adjacent friendly mission is more urgent.

    Only free workers do this proactively. Route owners and committed satellite
    builders keep their construction stance; defenders/repairers with equal or
    greater mission priority also hold. The move is local and deterministic, so
    it does not require same-round Store writes or reservations.
    """
    if not _free_mobile_worker(state):
        return False
    world = state.world
    if world is None:
        return False
    current = _pos(ct)
    own_priority = _mission_priority_for_builder(ct, state, _id(ct))
    urgent: list[tuple[int, int, Position]] = []
    for direction in CARDINALS:
        position = current.add(direction)
        builder_id, friendly = _builder_at(ct, position)
        if builder_id is None or friendly is not True:
            continue
        priority = _mission_priority_for_builder(ct, state, builder_id)
        if priority > own_priority:
            urgent.append((priority, builder_id, position))
    if not urgent:
        return False
    _priority, _builder_id_value, blocker = max(
        urgent, key=lambda item: (item[0], -item[1], -item[2].y, -item[2].x)
    )

    recent = set(state.move_history[-3:])
    candidates: list[tuple[int, int, Direction, Position]] = []
    for offset, direction in enumerate(CARDINALS):
        candidate = current.add(direction)
        try:
            if not ct.can_move(direction):
                continue
        except Exception:
            continue
        if world.is_navigation_blocked(candidate):
            continue
        freedom = sum(
            not world.is_navigation_blocked(candidate.add(other))
            for other in CARDINALS
        )
        score = 18 * freedom + 7 * candidate.distance_squared(blocker)
        if candidate in recent:
            score -= 35
        if world.own_core is not None and candidate in world.core_footprint:
            score -= 200
        candidates.append((score, -offset, direction, candidate))
    if not candidates:
        return False
    _score, _tie, direction, candidate = max(candidates)
    if actions.move(direction):
        state.cursor = (state.cursor + 1) % 8
        state.traffic_yield_origin = current
        state.traffic_yield_until = _round(ct) + 3
        if state.navigator is not None:
            state.navigator.invalidate()
        _record_move(state, candidate)
        return True
    return False


def _corridor_chain_yield(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
    *,
    scan_depth: int = 7,
) -> bool:
    """Propagate right-of-way through a short one-tile friendly convoy.

    Same-round Store reservations cannot work because Store writes are delayed.
    Instead a low-priority free worker in a static two-neighbour corridor scans a
    few cells along both corridor directions. If a more urgent friendly mission
    is queued on one side, it moves one cell *away* from that pressure. The
    frontmost worker in a chain moves first; following workers clear on subsequent
    rounds, producing a deterministic convoy instead of a permanent face-off.
    """
    if not _free_mobile_worker(state):
        return False
    world = state.world
    if world is None:
        return False
    current = _pos(ct)
    open_dirs = [
        direction for direction in CARDINALS
        if not world.is_navigation_blocked(current.add(direction))
    ]
    # Passing bays/open rooms already have local escape choices; reserve this
    # stronger behavior for actual corridor/dead-end geometry.
    if len(open_dirs) != 2:
        return False
    first, second = open_dirs

    own_priority = _mission_priority_for_builder(ct, state, _id(ct))

    def scan(direction: Direction) -> int:
        position = current
        previous = current
        step_direction = direction
        for _step in range(max(1, int(scan_depth))):
            next_position = position.add(step_direction)
            if not (0 <= next_position.x < world.width and 0 <= next_position.y < world.height):
                break
            if world.is_navigation_blocked(next_position):
                break
            previous, position = position, next_position
            builder_id, friendly = _builder_at(ct, position)
            if builder_id is not None and friendly is True:
                priority = _mission_priority_for_builder(ct, state, builder_id)
                if priority > own_priority:
                    return priority
            # Follow a unique corridor continuation, including bends. Stop at a
            # junction/passing bay because normal local yielding has room there.
            continuations: list[Position] = []
            for next_direction in CARDINALS:
                candidate = position.add(next_direction)
                if candidate == previous or world.is_navigation_blocked(candidate):
                    continue
                continuations.append(candidate)
            if len(continuations) != 1:
                break
            step_direction = position.cardinal_direction_to(continuations[0])
            if step_direction == Direction.CENTRE:
                break
        return -1

    p_first = scan(first)
    p_second = scan(second)
    if p_first > own_priority or p_second > own_priority:
        if p_first == p_second:
            return False
        # Urgent pressure on one side => clear toward the other side.
        escape = second if p_first > p_second else first
    else:
        # Very long friendly queues can exceed local vision, so not every member
        # can see the urgent owner/defender at the tail. During global route
        # pressure or a serious Core alarm, low-priority mobile workers adopt a
        # shared traffic direction: away from home. The front of a jam clears
        # first, then the convoy drains one cell per round without Store tile
        # reservations or omniscient positions.
        role, _route_owner = _builder_role_snapshot(ct, state, _id(ct))
        route_pressure = (
            state.team_active_projects > state.team_maintaining_routes
            or state.team_maintaining_routes < (state.team_route_target or _minimum_primary_routes(state))
        )
        friendly_adjacent = any(
            _builder_at(ct, current.add(direction))[1] is True for direction in open_dirs
        )
        if not friendly_adjacent or not (route_pressure or state.team_defense_severity >= 8):
            return False
        if role not in (Role.SCOUT, Role.SABOTEUR, Role.RAIDER, Role.SIEGE):
            return False
        if role == Role.SIEGE and state.team_attack_priority >= 13:
            return False
        if world.own_core is None:
            return False
        first_distance = current.add(first).distance_squared(world.own_core)
        second_distance = current.add(second).distance_squared(world.own_core)
        if first_distance == second_distance:
            return False
        escape = first if first_distance > second_distance else second
    try:
        if not ct.can_move(escape):
            return False
    except Exception:
        return False
    candidate = current.add(escape)
    if actions.move(escape):
        state.cursor = (state.cursor + 1) % 8
        state.traffic_yield_origin = current
        state.traffic_yield_until = _round(ct) + 3
        if state.navigator is not None:
            state.navigator.invalidate()
        _record_move(state, candidate)
        return True
    return False


def _resolve_builder_blocker(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
    blocker_position: Position,
    goal: Position,
    *,
    adjacent: bool = False,
    route_sensitive: bool = False,
) -> bool:
    blocker_id, friendly = _builder_at(ct, blocker_position)
    if blocker_id is None:
        return False
    round_no = _round(ct)
    state.last_blocker_position = blocker_position
    state.last_blocker_id = blocker_id

    if route_sensitive and state.blocked_steps >= 2:
        _temporarily_avoid_route_cell(
            state,
            blocker_position,
            round_no,
            duration=8 if friendly else 16,
        )

    if friendly is False:
        # Builders cannot shoot other Builders directly. The legal way to kill a
        # hostile body-blocker is to establish a Gunner/Sentinel firing solution;
        # otherwise route around it while the temporary avoidance is active.
        if (
            _offense_active(state)
            and state.role == Role.SIEGE
            and round_no - state.last_blocker_turret >= 24
        ):
            if _build_turret_against(ct, state, actions, blocker_position, forward=True):
                state.last_blocker_turret = round_no
                return True
        return _escape_step(
            ct,
            state,
            actions,
            goal,
            blocker=blocker_position,
            adjacent=adjacent,
        )

    # Friendly traffic uses mission-aware deterministic right-of-way. A route
    # owner completing first income, a live defender responding to a Core alert,
    # or a repair worker servicing a broken line should not yield merely because
    # its numeric ID is larger than an idle Scout. Equal-priority missions retain
    # the old stable-ID tie-break; repeated deadlock still forces bounded escape.
    own_priority = _mission_priority_for_builder(
        ct, state, _id(ct), route_sensitive=route_sensitive
    )
    blocker_priority = _mission_priority_for_builder(ct, state, blocker_id)
    should_yield = friendly is True and (
        own_priority < blocker_priority
        or (own_priority == blocker_priority and _id(ct) > blocker_id)
        or state.blocked_steps >= 4
    )
    if should_yield:
        origin = _pos(ct)
        yielded = _escape_step(
            ct,
            state,
            actions,
            goal,
            blocker=blocker_position,
            adjacent=adjacent,
        )
        if yielded:
            state.traffic_yield_origin = origin
            state.traffic_yield_until = round_no + 3
        return yielded
    return False


def _move(
    ct: object,
    state: BuilderStateData,
    goal: Position,
    actions: TurnActions,
    *,
    adjacent: bool = False,
    route_sensitive: bool = False,
) -> bool:
    world = state.world
    if world is None:
        return False
    if state.navigator is None:
        state.navigator = Navigator(
            world.width,
            world.height,
            world.is_navigation_blocked,
            cpu=ct.get_cpu_time_elapsed,
        )
    start = _pos(ct)
    round_no = _round(ct)
    same_goal = state.stuck_goal == goal and state.stuck_adjacent == adjacent
    goal_changed = state.stuck_goal is not None and not same_goal
    if not same_goal:
        if goal_changed:
            if round_no - state.last_goal_switch_round <= 4:
                state.rapid_goal_switches = min(6, state.rapid_goal_switches + 1)
            else:
                state.rapid_goal_switches = 1
            state.last_goal_switch_round = round_no
        elif round_no - state.last_goal_switch_round > 6:
            state.rapid_goal_switches = 0
        state.stuck_goal = goal
        state.stuck_adjacent = adjacent
        state.stuck_since_round = round_no
        state.best_goal_distance = start.distance_squared(goal)
        state.last_goal_progress_round = round_no
        state.blocked_steps = 0
    elif round_no - state.last_goal_switch_round > 6:
        state.rapid_goal_switches = 0
    if not state.move_history or state.move_history[-1] != start:
        _record_move(state, start)
    start_distance = start.distance_squared(goal)
    if start_distance < state.best_goal_distance:
        state.best_goal_distance = start_distance
        state.last_goal_progress_round = round_no

    preferred_direct = start.cardinal_direction_to(goal)
    direct_position = start.add(preferred_direct) if preferred_direct != Direction.CENTRE else None
    if direct_position is not None:
        direct_id, direct_friendly = _builder_at(ct, direct_position)
        if direct_id is not None:
            state.blocked_steps += 1
            if _resolve_builder_blocker(
                ct,
                state,
                actions,
                direct_position,
                goal,
                adjacent=adjacent,
                route_sensitive=route_sensitive,
            ):
                return True
            # The lower-ID Builder has right-of-way. Waiting briefly lets the
            # higher-ID blocker yield instead of making both bots reverse in
            # lockstep down a one-tile corridor.
            alternate_legal = False
            for alternate in CARDINALS:
                if alternate == preferred_direct:
                    continue
                try:
                    if ct.can_move(alternate):
                        alternate_legal = True
                        break
                except Exception:
                    continue
            if (
                direct_friendly is True
                and _id(ct) < direct_id
                and state.blocked_steps < 3
                and not alternate_legal
            ):
                return False

    if adjacent:
        direction = state.navigator.next_direction_to_adjacent(
            start,
            goal,
            world.layout_epoch,
            can_step=ct.can_move,
        )
    else:
        direction = state.navigator.next_direction(
            start,
            goal,
            world.layout_epoch,
            can_step=ct.can_move,
        )

    if direction != Direction.CENTRE:
        candidate = start.add(direction)
        # A deliberate friendly-traffic yield is useful only if we do not reverse
        # it on the very next turn. Hold the passing bay for two rounds unless an
        # economy construction step or a severe defense interrupt needs the tile.
        undoing_yield = bool(
            not route_sensitive
            and round_no < state.traffic_yield_until
            and state.traffic_yield_origin is not None
            and candidate == state.traffic_yield_origin
            and state.team_defense_severity < 12
        )
        anti_reverse = bool(
            round_no < state.anti_reverse_until
            and state.anti_reverse_position is not None
            and candidate == state.anti_reverse_position
            and not route_sensitive
        )
        # Repeated A-B-A-B motion toward the same goal is a pathing failure, not
        # progress. Force a different local branch before taking the old step.
        oscillating = (
            same_goal
            and len(state.move_history) >= 2
            and state.move_history[-1] == start
            and state.move_history[-2] == candidate
        )
        mission_thrashing = (
            goal_changed
            and state.rapid_goal_switches >= 2
            and len(state.move_history) >= 2
            and state.move_history[-1] == start
            and state.move_history[-2] == candidate
            and not route_sensitive
            and state.team_defense_severity < 12
        )
        if undoing_yield or anti_reverse:
            state.navigator.invalidate()
            return False
        if not oscillating and not mission_thrashing and actions.move(direction):
            state.blocked_steps = 0
            distance = candidate.distance_squared(goal)
            if distance < state.best_goal_distance:
                state.best_goal_distance = distance
                state.last_goal_progress_round = round_no
            _record_move(state, candidate)
            return True
        if oscillating or mission_thrashing:
            state.blocked_steps += 1
            state.anti_reverse_position = candidate
            state.anti_reverse_until = round_no + 4
            state.navigator.invalidate()
            if _escape_step(ct, state, actions, goal, adjacent=adjacent):
                return True

    if adjacent and start.distance_squared(goal) == 1:
        state.blocked_steps = 0
        return False

    state.blocked_steps += 1
    # Inspect the body-blocker most relevant to this goal. The direct greedy tile
    # is checked first, followed by any adjacent Builder that is closer to the
    # objective than our current position.
    preferred = start.cardinal_direction_to(goal)
    direct = start.add(preferred) if preferred != Direction.CENTRE else None
    blocker_positions = []
    for cardinal in CARDINALS:
        position = start.add(cardinal)
        blocker_id, _friendly = _builder_at(ct, position)
        if blocker_id is None:
            continue
        priority = 0 if position == direct else 1
        blocker_positions.append((priority, position.distance_squared(goal), position))
    for _priority, _distance, blocker_position in sorted(
        blocker_positions, key=lambda item: (item[0], item[1], item[2].y, item[2].x)
    ):
        if _resolve_builder_blocker(
            ct,
            state,
            actions,
            blocker_position,
            goal,
            adjacent=adjacent,
            route_sensitive=route_sensitive,
        ):
            return True

    no_progress = round_no - state.last_goal_progress_round >= 6
    if state.blocked_steps >= 2 or no_progress:
        state.navigator.invalidate()
        if _escape_step(ct, state, actions, goal, adjacent=adjacent):
            return True
    state.cursor = (state.cursor + 1) % 4
    return False


def _plan_route(ct: object, state: BuilderStateData, ore: Position, round_no: int) -> bool:
    world = state.world
    if world is None or world.own_core is None or not cpu_is_safe(ct):
        return False
    if state.route is not None and state.route.ore == ore:
        return True
    try:
        conveyor_cost = max(0, int(ct.get_conveyor_cost()))
        harvester_cost = max(0, int(ct.get_harvester_cost()))
    except Exception:
        return False
    distance = min(
        abs(ore.x - cell.x) + abs(ore.y - cell.y)
        for cell in (world.core_footprint or {world.own_core})
    )
    rough_new_links = (
        max(1, distance - 1)
        if state.satellite_mode
        else min(
            max(1, distance - 1),
            _rough_new_links_via_trunk(state, ore, round_no),
        )
    )
    estimated_cost = harvester_cost + estimate_route_cost(rough_new_links, conveyor_cost)
    # Before the first live Harvester, even a long route is preferable to an
    # indefinitely idle team. Cost-based payback filtering is useful only after
    # the economy has a working baseline.
    rescue_override = (
        not _any_route_maintaining(ct, round_no) and round_no < 700
    ) or (state.scenario == Scenario.ECONOMY_RESCUE and round_no < 760)
    if (
        estimate_payback_round(
            estimated_cost,
            output_per_round=2.5,
            start_round=round_no,
            horizon=1000,
        ) is None
        and not rescue_override
        and not state.satellite_mode
    ):
        _register_route_plan_failure(ct, state, round_no, definitive=True)
        return False
    # Planning is free. The previous version refused even to compute a path when
    # the global balance was below a Builder-sized reserve, leaving assigned
    # owners wandering near the Core with no actionable route state.
    _prune_temporary_route_blocks(state, round_no)
    search = state.route_search if state.route_search is not None else {}

    def route_blocked(position: Position) -> bool:
        # After repeated layout invalidations, stop gambling on unseen maze cells.
        # The Builder's world memory accumulates every observed tile, so moving
        # toward the ore gradually reveals a real corridor that can be planned
        # without laying another orphan trunk.
        if (
            state.layout_invalidations >= 2
            and position not in world.seen_tiles
            and position != ore
        ):
            return True
        if state.satellite_mode and _known_trunk_direction(state, position, round_no) is not None:
            # Four Harvesters already saturate a one-stack/round shared trunk on
            # average (10 Ti every four rounds each). Route five+ therefore
            # establishes an independent receiving lane instead of piling more
            # producers onto an already mature backbone.
            return True
        return (
            position in state.route_blocked
            or position in state.temporary_route_blocked
            or world.is_route_blocked(position)
        )

    reuse_trunk = not state.satellite_mode
    planned = plan_core_outward_route(
        ore,
        world.core_footprint or {world.own_core},
        world.width,
        world.height,
        route_blocked,
        created_round=round_no,
        cpu_check=ct.get_cpu_time_elapsed,
        obstacle_epoch=(world.layout_epoch << 20) ^ (state.route_avoid_epoch << 12) ^ (state.trunk_epoch if reuse_trunk else 0),
        search_state=search,
        reuse_direction=(
            (lambda position: _known_trunk_direction(state, position, round_no))
            if reuse_trunk
            else None
        ),
    )
    if planned is not None:
        reused_cells = (
            _route_reuse_cells(state, planned, round_no) if reuse_trunk else set()
        )
        new_link_count = max(0, len(planned.cells) - len(reused_cells))
        exact_cost = harvester_cost + estimate_route_cost(new_link_count, conveyor_cost)
        if (
            estimate_payback_round(
                exact_cost,
                output_per_round=2.5,
                start_round=round_no,
                horizon=1000,
            ) is None
            and not rescue_override
        ):
            state.route_search = None
            _register_route_plan_failure(ct, state, round_no, definitive=True)
            return False
        state.route_plan_failures = 0
        state.last_route_plan_failure = -999
        state.route = planned
        state.route_shared_links = reused_cells
        state.route_index = len(planned.cells) - 1
        state.route_search = None
        state.state = BuilderState.ROUTE
        if state.navigator is not None:
            state.navigator.invalidate()
        return True
    if not search.get("complete"):
        state.route_search = search
    else:
        state.route_search = None
        if state.layout_invalidations >= 2:
            # Corridor-survey mode: keep the claim while the owner physically
            # reveals a connected path. Abandon only after a long bounded window.
            if round_no - state.claim_started_round >= 180:
                _release_ore_claim(ct, state, round_no)
        else:
            _register_route_plan_failure(ct, state, round_no, definitive=True)
    return False


def _invalidate_route_layout(state: BuilderStateData, target: Position) -> None:
    state.route_blocked.add(target)
    state.layout_invalidations += 1
    _reset_route(state)


def _build_route(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    route = state.route
    if route is None or state.route_index < 0:
        return False

    # Reused/shared trunk links require no action. Consume all consecutive valid
    # links in this turn so a route does not spend one idle round per conveyor.
    while state.route_index >= 0 and cpu_is_safe(ct):
        index = state.route_index
        target = route.cells[index]
        expected = route.directions[index]
        entity_id, entity_type, direction = _visible(ct, target)
        blocker_id, _blocker_friendly = _builder_at(ct, target)
        if blocker_id is not None:
            state.blocked_steps += 1
            if _resolve_builder_blocker(
                ct,
                state,
                actions,
                target,
                target,
                adjacent=True,
                route_sensitive=True,
            ):
                return True
            if target in state.temporary_route_blocked:
                _reset_route(state)
            return False
        if (
            entity_type == EntityType.CONVEYOR
            and direction == expected
            and _is_friendly(ct, entity_id)
        ):
            _clear_build_failure(state)
            state.built_links[target] = (entity_type, direction)
            state.route_shared_links.add(target)
            state.known_trunk_links[target] = (direction, _round(ct))
            state.route_index -= 1
            state.last_real_route_progress_round = _round(ct)
            continue
        if entity_type is not None:
            # Never destroy an unknown shared route. Replan around incompatible
            # or enemy infrastructure instead of causing multi-route churn.
            # If this is a Conveyor this owner previously built, it is an
            # orphan from an earlier plan. Before the first producer, repair it
            # in-place instead of permanently fencing off our own corridor.
            friendly = _is_friendly(ct, entity_id)
            if friendly and entity_type == EntityType.CONVEYOR and target in state.built_links:
                if _pos(ct).distance_squared(target) == 1 and actions.destroy(target):
                    state.built_links.pop(target, None)
                    state.last_real_route_progress_round = _round(ct)
                    return True
            _invalidate_route_layout(state, target)
            return False
        # Newly revealed terrain can invalidate a route planned through unknown
        # space. A visible wall or non-empty non-building cell must trigger a
        # replan rather than an infinite sequence of failed can_build calls.
        try:
            visible = bool(ct.is_in_vision(target))
        except Exception:
            visible = False
        if visible:
            try:
                impossible_terrain = ct.get_tile_env(target) == Environment.WALL
            except Exception:
                impossible_terrain = False
            if impossible_terrain:
                _invalidate_route_layout(state, target)
                return False
        if _pos(ct).distance_squared(target) != 1:
            return _move(
                ct,
                state,
                target,
                actions,
                adjacent=True,
                route_sensitive=True,
            )
        try:
            cost = int(ct.get_conveyor_cost())
        except Exception:
            return False
        if not _spend_allowed(ct, cost, route_completion=True):
            return False
        if actions.build_conveyor(target, expected) is None:
            # If the action is ready, the tile is adjacent/visible, and the team
            # can afford it, repeated failure means this cell is structurally
            # unusable under the current layout. Replan around it.
            try:
                actionable = bool(ct.can_act())
            except Exception:
                actionable = True
            if actionable and _record_build_failure(state, target, _round(ct)):
                _invalidate_route_layout(state, target)
            return False
        _clear_build_failure(state)
        state.built_links[target] = (EntityType.CONVEYOR, expected)
        state.route_shared_links.discard(target)
        state.known_trunk_links[target] = (expected, _round(ct))
        state.route_index -= 1
        state.last_real_route_progress_round = _round(ct)
        state.state = BuilderState.VERIFY
        return True
    return False


def _verified(state: BuilderStateData, ct: object) -> bool:
    route = state.route
    if route is None or not route.cells or len(route.cells) != len(route.directions):
        return False
    for cell, expected in zip(route.cells, route.directions):
        entity_id, entity_type, direction = _visible(ct, cell)
        if entity_type is None:
            try:
                visible = bool(ct.is_in_vision(cell))
            except Exception:
                visible = False
            if not visible and state.built_links.get(cell) == (EntityType.CONVEYOR, expected):
                continue
            return False
        if (
            entity_type != EntityType.CONVEYOR
            or direction != expected
            or not _is_friendly(ct, entity_id)
        ):
            return False
    return route.cells[-1].add(route.directions[-1]) in set(route.core_footprint)


def _route_health_timeout(state: BuilderStateData) -> int:
    """Length of a passive route's maintenance lease.

    Healthy Harvesters and Conveyors require no Builder action. Quiet routes are
    therefore re-inspected only occasionally; contested routes get a much shorter
    lease. Real locally observed threats still pre-empt this timer immediately.
    """
    length = len(state.route.cells) if state.route is not None else 0
    if state.scenario == Scenario.CONTESTED or state.team_defense_severity >= 12:
        return max(20, min(40, length + 16))
    # Passive lines do not need babysitters, but 96--180 rounds is long enough for
    # one enemy Builder to cut a remote producer and disappear before anybody
    # notices. Revisit on a moderate lease while shared repair/scout workers cover
    # the network between full owner inspections.
    return max(40, min(80, 2 * length + 32))


def _team_economy_near(
    ct: object,
    state: BuilderStateData,
    position: Position,
    *,
    harvester_radius_sq: int = 36,
    trunk_radius_sq: int = 12,
) -> bool:
    """Whether a hostile position threatens any known team economy, not just ours."""
    for _index, claim in _maintaining_claims(ct, state, _round(ct)):
        if claim.position is not None and position.distance_squared(claim.position) <= harvester_radius_sq:
            return True
    for trunk_position, (_direction, seen_round) in state.known_trunk_links.items():
        if _round(ct) - int(seen_round) <= 96 and position.distance_squared(trunk_position) <= trunk_radius_sq:
            return True
    return False


def _nearest_team_economy_anchor(
    ct: object,
    state: BuilderStateData,
    position: Position,
) -> Position | None:
    candidates = [
        claim.position
        for _index, claim in _maintaining_claims(ct, state, _round(ct))
        if claim.position is not None
    ]
    if not candidates:
        return None
    return min(candidates, key=lambda pos: (position.distance_squared(pos), pos.y, pos.x))


def _counterbattery_probe(
    ct: object,
    state: BuilderStateData,
    damage_site: Position,
    kind: ThreatKind,
) -> Position | None:
    """Probe all legal turret firing rays for an unseen ranged source.

    Gunner/Sentinel facing may be cardinal *or diagonal*.  Search the eight
    straight rays whose squared ranges match the actual turret envelopes instead
    of assuming a four-direction cross around the victim.
    """
    world = state.world
    if world is None or kind not in (ThreatKind.GUNNER_FIRE, ThreatKind.SENTINEL_FIRE, ThreatKind.FIRING_LINE):
        return None
    range_sq = 32 if kind == ThreatKind.SENTINEL_FIRE else (13 if kind == ThreatKind.GUNNER_FIRE else 32)
    min_step = 2
    directions = tuple(FACING_DIRECTIONS)
    if not directions:
        directions = tuple(CARDINALS)
    rotation = (max(1, state.role_key) - 1 + state.counterbattery_cursor) % len(directions)
    ordered_dirs = tuple(directions[(rotation + i) % len(directions)] for i in range(len(directions)))
    candidates: list[tuple[int, int, int, Position]] = []
    current = _pos(ct)
    for dir_rank, direction in enumerate(ordered_dirs):
        probe = damage_site
        step = 0
        while True:
            step += 1
            probe = probe.add(direction)
            if damage_site.distance_squared(probe) > range_sq:
                break
            if step < min_step:
                continue
            if not (0 <= probe.x < world.width and 0 <= probe.y < world.height):
                break
            # Static walls disprove a Gunner source beyond the wall on that ray,
            # but Sentinel fire pierces obstacles so keep probing past them.
            if probe in world.static_walls and kind == ThreatKind.GUNNER_FIRE:
                break
            observation = world.dynamic.get(probe)
            if observation is not None and observation.entity_type in (EntityType.GUNNER, EntityType.SENTINEL):
                return probe
            # Already-seen empty cells are disproven source hypotheses.
            if probe in world.seen_tiles and observation is None:
                continue
            candidates.append((dir_rank, current.distance_squared(probe), -step, probe))
    if not candidates:
        state.counterbattery_cursor = (state.counterbattery_cursor + 1) % len(directions)
        return None
    candidates.sort(key=lambda item: (item[0], item[1], item[2], item[3].y, item[3].x))
    return candidates[0][3]

def _route_health_fresh(state: BuilderStateData, round_no: int) -> bool:
    if (
        state.route is None
        or state.last_full_verify_round is None
        or state.last_harvester_seen_round is None
    ):
        return False
    timeout = _route_health_timeout(state)
    return (
        round_no - state.last_full_verify_round <= timeout
        and round_no - state.last_harvester_seen_round <= timeout
    )


def _observe_final_delivery(ct: object, state: BuilderStateData, round_no: int) -> None:
    route = state.route
    if route is None or route.final_conveyor is None:
        return
    final_id, final_type, _ = _visible(ct, route.final_conveyor)
    stored: bool | None = None
    if final_id is not None and final_type in (EntityType.CONVEYOR, EntityType.SPLITTER):
        try:
            stored = ct.get_stored_resource(final_id) is not None
        except Exception:
            stored = None
    if state.last_final_storage is True and stored is False:
        state.last_delivery_round = round_no
    state.last_final_storage = stored


def _ensure_harvester(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    route = state.route
    ore = state.ore_target
    if route is None or ore is None:
        return False
    round_no = _round(ct)
    entity_id, entity_type, _ = _visible(ct, ore)
    try:
        ore_visible = bool(ct.is_in_vision(ore))
    except Exception:
        ore_visible = False
    if ore_visible:
        try:
            is_ore = ct.get_tile_env(ore) == Environment.ORE_TITANIUM
        except Exception:
            is_ore = ore in (state.world.ore_positions if state.world is not None else set())
        if not is_ore:
            _release_ore_claim(ct, state, round_no)
            return False
    if entity_type == EntityType.HARVESTER and _is_friendly(ct, entity_id):
        state.last_harvester_seen_round = round_no
        if state.delivery_started_round is None:
            state.delivery_started_round = round_no
        if state.state != BuilderState.MAINTAIN:
            state.state = BuilderState.DELIVER
        return False
    if entity_type is not None:
        state.state = BuilderState.VERIFY
        current = _pos(ct)
        if current.distance_squared(ore) != 1:
            return _move(ct, state, ore, actions, adjacent=True, route_sensitive=True)
        if _is_friendly(ct, entity_id):
            return actions.destroy(ore)
        try:
            attack_cost = BUILDER_ATTACK_COST
        except Exception:
            attack_cost = 2
        if _spend_allowed(ct, attack_cost, emergency=True, paid_attack=True):
            return actions.fire(ore)
        return False
    blocker_id, _blocker_friendly = _builder_at(ct, ore)
    if blocker_id is not None:
        state.blocked_steps += 1
        return _resolve_builder_blocker(
            ct,
            state,
            actions,
            ore,
            ore,
            adjacent=True,
            route_sensitive=True,
        )
    # Do not construct a producer on top of an unverified or broken chain.  We
    # may still observe/defend an existing Harvester above so patrols can repair
    # the route instead of getting stuck at the ore endpoint.
    if not _verified(state, ct):
        return False
    if _pos(ct).distance_squared(ore) != 1:
        return _move(ct, state, ore, actions, adjacent=True, route_sensitive=True)
    try:
        cost = int(ct.get_harvester_cost())
    except Exception:
        return False
    if not _spend_allowed(
        ct,
        cost,
        route_completion=True,
        producer_purchase=True,
    ):
        return False
    if actions.build_harvester(ore) is None:
        try:
            actionable = bool(ct.can_act())
        except Exception:
            actionable = True
        if actionable and _record_build_failure(state, ore, round_no, threshold=3):
            # The ore may be permanently inaccessible from the chosen side or a
            # stale claim. Replan once, then release it if the failure persists.
            if state.route is not None:
                _reset_route(state)
            else:
                _release_ore_claim(ct, state, round_no)
        return False
    _clear_build_failure(state)
    state.delivery_started_round = round_no
    state.last_harvester_seen_round = round_no
    state.state = BuilderState.DELIVER
    return True


def _repair_route_cell(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
    index: int,
) -> bool:
    route = state.route
    if route is None or not 0 <= index < len(route.cells):
        return False
    target = route.cells[index]
    expected = route.directions[index]
    entity_id, entity_type, direction = _visible(ct, target)
    blocker_id, _blocker_friendly = _builder_at(ct, target)
    if blocker_id is not None:
        state.blocked_steps += 1
        if _resolve_builder_blocker(
            ct,
            state,
            actions,
            target,
            target,
            adjacent=True,
            route_sensitive=True,
        ):
            return True
        if target in state.temporary_route_blocked:
            _reset_route(state)
        return False
    if (
        entity_type == EntityType.CONVEYOR
        and direction == expected
        and _is_friendly(ct, entity_id)
    ):
        state.built_links[target] = (entity_type, direction)
        return False

    state.repair_index = index
    current = _pos(ct)
    if entity_type is not None:
        friendly = False
        try:
            friendly = entity_id is not None and ct.get_team(entity_id) == ct.get_team()
        except Exception:
            pass
        if friendly and target in state.built_links:
            if current.distance_squared(target) != 1:
                return _move(ct, state, target, actions, adjacent=True, route_sensitive=True)
            if actions.destroy(target):
                state.built_links.pop(target, None)
                try:
                    cost = int(ct.get_conveyor_cost())
                except Exception:
                    return True
                if (
                    _spend_allowed(ct, cost, route_completion=True)
                    and actions.build_conveyor(target, expected) is not None
                ):
                    state.built_links[target] = (EntityType.CONVEYOR, expected)
                    state.repair_index = None
                    state.delivery_started_round = _round(ct)
                return True
        state.route_blocked.add(target)
        _reset_route(state)
        return False

    if current.distance_squared(target) != 1:
        return _move(ct, state, target, actions, adjacent=True, route_sensitive=True)
    try:
        cost = int(ct.get_conveyor_cost())
    except Exception:
        return False
    if (
        _spend_allowed(ct, cost, route_completion=True)
        and actions.build_conveyor(target, expected) is not None
    ):
        state.built_links[target] = (EntityType.CONVEYOR, expected)
        state.repair_index = None
        state.delivery_started_round = _round(ct)
        state.last_full_verify_round = None
        return True
    return False


def _begin_route_patrol(ct: object, state: BuilderStateData) -> None:
    route = state.route
    if route is None or not route.cells:
        state.patrol_index = -1
        return
    current = _pos(ct)
    ore_end = route.cells[0]
    core_end = route.cells[-1]
    if current.distance_squared(ore_end) <= current.distance_squared(core_end):
        state.patrol_direction = 1
        state.patrol_index = 0
    else:
        state.patrol_direction = -1
        state.patrol_index = len(route.cells) - 1
    state.state = BuilderState.VERIFY


def _finish_route_patrol(state: BuilderStateData, round_no: int) -> None:
    route = state.route
    if route is None:
        return
    # A full chain sweep is only operational evidence if the Harvester was also
    # observed during this sweep or very shortly before it.
    harvest_fresh = (
        state.last_harvester_seen_round is not None
        and round_no - state.last_harvester_seen_round <= max(12, len(route.cells) + 6)
    )
    if harvest_fresh:
        state.last_full_verify_round = round_no
        state.state = BuilderState.MAINTAIN
        # Completion is a handoff. The owner becomes mobile on the next turn and
        # returns only when this lease expires (or a real route threat pre-empts
        # it through the defense overlay).
        state.next_patrol_round = round_no + _route_health_timeout(state)
    else:
        state.state = BuilderState.DELIVER
        state.next_patrol_round = round_no
    state.patrol_index = -1
    state.patrol_direction *= -1
    state.repair_index = None


def _patrol_route(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    route = state.route
    if route is None or not route.cells:
        return False
    round_no = _round(ct)
    if state.patrol_index < 0 or state.patrol_index >= len(route.cells):
        _begin_route_patrol(ct, state)
    if state.patrol_index < 0:
        return False

    # If this sweep starts at the ore end, verify the producer before walking the
    # chain. A core-to-ore sweep performs the same check when it reaches index 0.
    if state.patrol_direction > 0 and state.patrol_index == 0:
        if _ensure_harvester(ct, state, actions):
            return True
        if state.last_harvester_seen_round != round_no:
            return _move(ct, state, route.ore, actions, adjacent=True, route_sensitive=True)

    inspected = 0
    while 0 <= state.patrol_index < len(route.cells) and inspected < len(route.cells):
        if not cpu_is_safe(ct):
            return False
        index = state.patrol_index
        target = route.cells[index]
        try:
            visible = bool(ct.is_in_vision(target))
        except Exception:
            visible = False
        if not visible:
            return _move(ct, state, target, actions, route_sensitive=True)
        entity_id, entity_type, direction = _visible(ct, target)
        expected = route.directions[index]
        if (
            entity_type != EntityType.CONVEYOR
            or direction != expected
            or not _is_friendly(ct, entity_id)
        ):
            state.last_full_verify_round = None
            return _repair_route_cell(ct, state, actions, index)
        state.built_links[target] = (EntityType.CONVEYOR, expected)
        if index == len(route.cells) - 1:
            _observe_final_delivery(ct, state, round_no)
        state.patrol_index += state.patrol_direction
        inspected += 1

    if not (0 <= state.patrol_index < len(route.cells)):
        if state.patrol_direction < 0:
            if _ensure_harvester(ct, state, actions):
                return True
            if state.last_harvester_seen_round != round_no:
                return _move(ct, state, route.ore, actions, adjacent=True, route_sensitive=True)
        _finish_route_patrol(state, round_no)
        return False

    return _move(ct, state, route.cells[state.patrol_index], actions, route_sensitive=True)


def _enemy_entities(ct: object, *, buildings_only: bool = False):
    try:
        own_team = ct.get_team()
        ids = tuple(ct.get_nearby_buildings())[:64]
        if not buildings_only:
            ids += tuple(ct.get_nearby_units())[:32]
    except Exception:
        return ()
    result = []
    seen = set()
    for entity_id in ids:
        if entity_id in seen or not cpu_is_safe(ct):
            continue
        seen.add(entity_id)
        try:
            if ct.get_team(entity_id) == own_team:
                continue
            result.append(
                (
                    entity_id,
                    ct.get_entity_type(entity_id),
                    ct.get_position(entity_id),
                )
            )
        except Exception:
            continue
    return tuple(result)


def _heal_adjacent(ct: object, actions: TurnActions) -> bool:
    current = _pos(ct)
    for direction in CARDINALS:
        target = current.add(direction)
        try:
            if ct.can_heal(target):
                return actions.heal(target)
        except Exception:
            continue
    return False


def _facing_toward(origin: Position, target: Position) -> Direction:
    dx = 0 if target.x == origin.x else (1 if target.x > origin.x else -1)
    dy = 0 if target.y == origin.y else (1 if target.y > origin.y else -1)
    return {
        (0, -1): Direction.NORTH,
        (1, -1): Direction.NORTHEAST,
        (1, 0): Direction.EAST,
        (1, 1): Direction.SOUTHEAST,
        (0, 1): Direction.SOUTH,
        (-1, 1): Direction.SOUTHWEST,
        (-1, 0): Direction.WEST,
        (-1, -1): Direction.NORTHWEST,
    }.get((dx, dy), Direction.NORTH)


def _friendly_combat_nearby(ct: object, position: Position, radius_sq: int = 20) -> bool:
    try:
        own_team = ct.get_team()
        ids = tuple(ct.get_nearby_buildings())[:64]
    except Exception:
        return False
    for entity_id in ids:
        try:
            if ct.get_team(entity_id) != own_team:
                continue
            if ct.get_entity_type(entity_id) not in (
                EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER
            ):
                continue
            if position.distance_squared(ct.get_position(entity_id)) <= radius_sq:
                return True
        except Exception:
            continue
    return False


def _build_defensive_turret(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
    threat_position: Position,
    *,
    threat_kind: ThreatKind = ThreatKind.UNKNOWN,
) -> bool:
    if not _bootstrap_defense_build_allowed(state):
        return False
    world = state.world
    round_no = _round(ct)
    route_emergency = bool(
        (
            state.claim_slot is not None
            and state.route is not None
            and min((threat_position.distance_squared(cell) for cell in state.route.cells), default=999) <= 16
        )
        or _team_economy_near(ct, state, threat_position)
    )
    if state.role not in (Role.DEFENDER, Role.REPAIR) and not route_emergency:
        return False
    compact_emergency = bool(
        _compact_map(state)
        and round_no < 260
        and world is not None
        and world.own_core is not None
        and min(
            (threat_position.distance_squared(cell) for cell in world.core_footprint),
            default=threat_position.distance_squared(world.own_core),
        ) <= 36
    )
    # Do not wait for the next buffered strategy update when an enemy is already
    # inside a compact base. The dedicated home screen may create one immediate
    # firing position while economy owners continue their routes.
    if (
        state.phase != Phase.DEFENSE
        and state.scenario != Scenario.CONTESTED
        and not compact_emergency
        and not route_emergency
    ):
        return False
    if round_no - state.last_defensive_turret < 56:
        return False
    current = _pos(ct)
    if _friendly_combat_nearby(ct, threat_position, 32):
        return False
    building_id, _building_type, _ = _visible(ct, threat_position)
    blocker_id, blocker_friendly = _builder_at(ct, threat_position)
    enemy_builder = blocker_id is not None and blocker_friendly is False
    if building_id is not None and _is_friendly(ct, building_id):
        return False
    if threat_kind == ThreatKind.SENTINEL_FIRE:
        preferred = (EntityType.SENTINEL, EntityType.GUNNER)
    elif threat_kind in (ThreatKind.GUNNER_FIRE, ThreatKind.BUILDER_RUSH):
        preferred = (EntityType.GUNNER, EntityType.SENTINEL)
    else:
        preferred = (
            (EntityType.GUNNER, EntityType.SENTINEL)
            if enemy_builder or current.distance_squared(threat_position) <= 13
            else (EntityType.SENTINEL, EntityType.GUNNER)
        )
    route_cells = set(state.route.cells) if state.route is not None else set()
    route_cells.update(state.known_trunk_links)
    route_cells.update(
        claim.position
        for _index, claim in _maintaining_claims(ct, state, round_no)
        if claim.position is not None
    )
    candidates = []
    for direction in CARDINALS:
        position = current.add(direction)
        if position in route_cells or (world is not None and position in world.core_footprint):
            continue
        try:
            if ct.is_tile_empty(position):
                candidates.append(position)
        except Exception:
            continue
    for position in sorted(candidates, key=lambda pos: (pos.distance_squared(threat_position), pos.y, pos.x)):
        for turret_type in preferred:
            for facing in FACING_DIRECTIONS:
                try:
                    if not ct.can_fire_from(position, facing, turret_type, threat_position):
                        continue
                    cost = int(
                        ct.get_gunner_cost()
                        if turret_type == EntityType.GUNNER
                        else ct.get_sentinel_cost()
                    )
                except Exception:
                    continue
                # Even an immediate defensive placement must leave the rolling
                # Harvester+Conveyor expansion seed intact. ``emergency`` skips a
                # second defensive reserve, not the economic reserve.
                if not _spend_allowed(ct, cost, emergency=True):
                    continue
                built = (
                    actions.build_gunner(position, facing)
                    if turret_type == EntityType.GUNNER
                    else actions.build_sentinel(position, facing)
                )
                if built is not None:
                    state.last_defensive_turret = round_no
                    if state.team_maintaining_routes <= 0:
                        state.bootstrap_defense_built = True
                    return True
    return False


def _build_intruder_launcher(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
    threat_position: Position,
) -> bool:
    """Cheap no-ammo answer to a lone Builder already inside our economy."""
    if not _bootstrap_defense_build_allowed(state):
        return False
    round_no = _round(ct)
    if round_no - state.last_defensive_turret < 36:
        return False
    blocker_id, blocker_friendly = _builder_at(ct, threat_position)
    if blocker_id is None or blocker_friendly is not False:
        return False
    if not _team_economy_near(ct, state, threat_position) and not (
        state.world is not None
        and state.world.own_core is not None
        and threat_position.distance_squared(state.world.own_core) <= 36
    ):
        return False
    current = _pos(ct)
    try:
        cost = max(0, int(ct.get_launcher_cost()))
    except Exception:
        cost = BASE_LAUNCHER_COST
    if not _spend_allowed(ct, cost, emergency=True):
        return False
    world = state.world
    candidates: list[Position] = []
    for direction in CARDINALS:
        position = current.add(direction)
        if position.distance_squared(threat_position) > 2:
            continue
        if world is not None and (position in world.core_footprint or position in state.known_trunk_links):
            continue
        try:
            if ct.is_tile_empty(position) and ct.can_build_launcher(position):
                candidates.append(position)
        except Exception:
            continue
    for position in sorted(candidates, key=lambda pos: (pos.distance_squared(threat_position), pos.y, pos.x)):
        if actions.build_launcher(position) is not None:
            state.last_defensive_turret = round_no
            if state.team_maintaining_routes <= 0:
                state.bootstrap_defense_built = True
            return True
    return False


def _on_straight_ray_between(source: Position, target: Position, point: Position) -> bool:
    """Return whether point lies strictly between source/target on an 8-way ray."""
    dx = target.x - source.x
    dy = target.y - source.y
    if dx == 0 and dy == 0:
        return False
    if not (dx == 0 or dy == 0 or abs(dx) == abs(dy)):
        return False
    sx = 0 if dx == 0 else (1 if dx > 0 else -1)
    sy = 0 if dy == 0 else (1 if dy > 0 else -1)
    px = point.x - source.x
    py = point.y - source.y
    if px == 0 and py == 0:
        return False
    if sx == 0:
        if px != 0 or (1 if py > 0 else -1) != sy:
            return False
        point_step = abs(py)
    elif sy == 0:
        if py != 0 or (1 if px > 0 else -1) != sx:
            return False
        point_step = abs(px)
    else:
        if abs(px) != abs(py):
            return False
        if (1 if px > 0 else -1) != sx or (1 if py > 0 else -1) != sy:
            return False
        point_step = abs(px)
    target_step = max(abs(dx), abs(dy))
    return 0 < point_step < target_step


def _build_reactive_barrier(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
    threat_position: Position,
    *,
    core_near: bool,
    route_near: bool,
    severity: int,
    threat_kind: ThreatKind = ThreatKind.UNKNOWN,
) -> bool:
    """Cheaply close a real attacked chokepoint without walling off expansion.

    Barriers cost only 3 Ti base and block movement/LOS, but every one still raises
    scale and a badly placed barrier can trap our own logistics. We therefore use
    them only reactively, on a locally narrow tile *between* a responder and the
    hostile, never on ore, Core exits, route cells, or remembered conveyor trunk.
    """
    if not _bootstrap_defense_build_allowed(state):
        return False
    world = state.world
    if world is None or severity < 11 or not (core_near or route_near):
        return False
    # Sentinel fire explicitly ignores walls/units, so a Barrier is not a ranged
    # countermeasure there. Save the titanium and send counter-battery instead.
    if threat_kind == ThreatKind.SENTINEL_FIRE:
        return False
    round_no = _round(ct)
    if round_no - state.last_defensive_barrier < 28:
        return False
    current = _pos(ct)
    protected = world.own_core
    if route_near:
        team_anchor = _nearest_team_economy_anchor(ct, state, threat_position)
        if team_anchor is not None:
            protected = team_anchor
        elif state.route is not None and state.route.cells:
            protected = min(
                state.route.cells,
                key=lambda pos: pos.distance_squared(threat_position),
            )
    if protected is None:
        return False
    reserved = set(world.core_footprint)
    if state.route is not None:
        reserved.update(state.route.cells)
        if state.ore_target is not None:
            reserved.add(state.ore_target)
    reserved.update(state.known_trunk_links)
    candidates: list[tuple[int, int, Position]] = []
    current_threat = abs(current.x - threat_position.x) + abs(current.y - threat_position.y)
    current_home = abs(current.x - protected.x) + abs(current.y - protected.y)
    for direction in CARDINALS:
        candidate = current.add(direction)
        if candidate in reserved or not (0 <= candidate.x < world.width and 0 <= candidate.y < world.height):
            continue
        if candidate in world.static_walls:
            continue
        try:
            if ct.get_tile_env(candidate) == Environment.ORE_TITANIUM:
                continue
            if not ct.is_tile_empty(candidate):
                continue
            if not ct.can_build_barrier(candidate):
                continue
        except Exception:
            continue
        threat_distance = abs(candidate.x - threat_position.x) + abs(candidate.y - threat_position.y)
        protected_distance = abs(candidate.x - protected.x) + abs(candidate.y - protected.y)
        if threat_kind == ThreatKind.GUNNER_FIRE:
            # A Gunner ray may be cardinal or diagonal. A Barrier is useful only
            # if it lies strictly on the actual one-tile firing ray.
            if not _on_straight_ray_between(threat_position, protected, candidate):
                continue
        # Build outward from the responder: the wall must be closer to the hostile
        # and no closer to the asset we are protecting.
        if threat_distance >= current_threat or protected_distance < current_home:
            continue
        degree = 0
        for step in CARDINALS:
            neighbour = candidate.add(step)
            if not (0 <= neighbour.x < world.width and 0 <= neighbour.y < world.height):
                continue
            if neighbour in world.static_walls:
                continue
            if neighbour in reserved:
                degree += 1
                continue
            try:
                if ct.is_tile_passable(neighbour):
                    degree += 1
            except Exception:
                if not world.is_navigation_blocked(neighbour):
                    degree += 1
        if degree > 2:
            continue
        candidates.append((degree, threat_distance, candidate))
    if not candidates:
        return False
    try:
        cost = max(0, int(ct.get_barrier_cost()))
    except Exception:
        cost = BASE_BARRIER_COST
    if not _spend_allowed(ct, cost, emergency=True):
        return False
    _degree, _distance, position = min(candidates, key=lambda item: (item[0], item[1], item[2].y, item[2].x))
    if actions.build_barrier(position) is not None:
        state.last_defensive_barrier = round_no
        if state.team_maintaining_routes <= 0:
            state.bootstrap_defense_built = True
        return True
    return False


def _build_forward_outpost(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
    target: Position,
) -> bool:
    """Claim advancing space with a sparse rotatable Gunner screen.

    Direct-fire Sentinels are still created by ``_build_turret_against``. These
    outposts fill the otherwise empty march between launcher stages, deny enemy
    Builders corridors, and provide a position the following wave can repair.
    """
    if not _offense_active(state) or not _assault_engineer(state):
        return False
    round_no = _round(ct)
    if round_no - state.last_forward_outpost < 84:
        return False
    world = state.world
    if world is None or world.own_core is None:
        return False
    current = _pos(ct)
    if current.distance_squared(world.own_core) < 36:
        return False
    distance = current.distance_squared(target)
    if distance < 18 or distance > 420:
        return False
    if _friendly_combat_nearby(ct, current, 24):
        return False
    try:
        cost = int(ct.get_gunner_cost())
    except Exception:
        cost = BASE_GUNNER_COST
    if not _spend_allowed(ct, cost):
        return False
    route_cells = set(state.route.cells) if state.route is not None else set()
    candidates = []
    for direction in CARDINALS:
        position = current.add(direction)
        if position in route_cells or position in world.core_footprint:
            continue
        try:
            if ct.is_tile_empty(position):
                candidates.append(position)
        except Exception:
            continue
    for position in sorted(candidates, key=lambda pos: (pos.distance_squared(target), pos.y, pos.x)):
        facing = _facing_toward(position, target)
        if actions.build_gunner(position, facing) is not None:
            state.last_forward_outpost = round_no
            return True
    return False


def _build_turret_against(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
    enemy_position: Position,
    *,
    forward: bool,
) -> bool:
    # Gunners/Sentinels are attack assets, not opening infrastructure.  Only
    # dedicated siege engineers may create them after the economy phase.
    if not _offense_active(state) or not _assault_engineer(state):
        return False
    round_no = _round(ct)
    if forward and round_no - state.last_forward_turret < 40:
        return False
    current = _pos(ct)
    world = state.world
    route_cells = set(state.route.cells) if state.route else set()
    candidates = []
    for position in (current.add(direction) for direction in CARDINALS):
        if position in route_cells or (world is not None and position in world.core_footprint):
            continue
        try:
            if not ct.is_tile_empty(position):
                continue
        except Exception:
            continue
        candidates.append(position)
    enemy_id, enemy_type, _enemy_direction = _visible(ct, enemy_position)
    del enemy_id, _enemy_direction
    distance = current.distance_squared(enemy_position)
    specialization = abs(_id(ct)) % 3
    if enemy_type in (EntityType.CORE, EntityType.HARVESTER, EntityType.SENTINEL) or distance > 13:
        preferred_types = (EntityType.SENTINEL, EntityType.GUNNER)
    else:
        preferred_types = (EntityType.GUNNER, EntityType.SENTINEL)
    if specialization == 1:
        preferred_types = (EntityType.GUNNER, EntityType.SENTINEL)
    elif specialization == 2:
        preferred_types = (EntityType.SENTINEL, EntityType.GUNNER)

    for position in sorted(candidates, key=lambda pos: (pos.distance_squared(enemy_position), pos.y, pos.x)):
        for turret_type in preferred_types:
            for direction in FACING_DIRECTIONS:
                try:
                    useful = bool(ct.can_fire_from(position, direction, turret_type, enemy_position))
                except Exception:
                    useful = False
                if not useful:
                    continue
                try:
                    cost = int(ct.get_gunner_cost() if turret_type == EntityType.GUNNER else ct.get_sentinel_cost())
                except Exception:
                    continue
                if not _spend_allowed(ct, cost, emergency=not forward):
                    continue
                built = (
                    actions.build_gunner(position, direction)
                    if turret_type == EntityType.GUNNER
                    else actions.build_sentinel(position, direction)
                )
                if built is not None:
                    if forward:
                        state.last_forward_turret = round_no
                    return True
    return False


def _build_launcher_support(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
    enemy_position: Position,
) -> bool:
    """Build a leapfrog launcher for the assault column.

    Launchers are the only non-turret offensive support building: they throw
    nearby Builders toward the shared rally, letting siege engineers advance
    without spending every turn walking. The cooldown prevents launcher spam.
    """
    if not _offense_active(state) or not _assault_engineer(state):
        return False
    # Keep exactly one early assault engineer biased toward mobility once the
    # Core is confirmed; otherwise retain the old one-third specialization.
    # This prevents Launcher spam while guaranteeing that a real Core push has a
    # chance to create a reinforcement catapult even when IDs are unlucky.
    if state.team_attack_priority >= 15:
        if _attack_worker_ordinal(state) != 2:
            return False
    elif abs(_id(ct)) % 3 != 0:
        return False
    round_no = _round(ct)
    if round_no - state.last_forward_launcher < 72:
        return False
    current = _pos(ct)
    distance = current.distance_squared(enemy_position)
    if state.team_attack_priority >= 15:
        if distance < 8 or distance > 180:
            return False
    elif distance < 20 or distance > 360:
        return False
    try:
        cost = int(ct.get_launcher_cost())
    except Exception:
        try:
            cost = BASE_LAUNCHER_COST
        except Exception:
            return False
    if not _spend_allowed(ct, cost):
        return False
    candidates = []
    for position in (current.add(direction) for direction in CARDINALS):
        try:
            if ct.is_tile_empty(position):
                candidates.append(position)
        except Exception:
            continue
    for position in sorted(
        candidates,
        key=lambda pos: (pos.distance_squared(enemy_position), pos.y, pos.x),
    ):
        if actions.build_launcher(position) is not None:
            state.last_forward_launcher = round_no
            return True
    return False


def _defense_overlay(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    world = state.world
    if world is None:
        return False
    round_no = _round(ct)
    local_threats = world.threat_list(round_no)
    current = _pos(ct)

    threat_position: Position | None = None
    severity = 0
    kind = ThreatKind.UNKNOWN
    local = False
    entity_type = None
    if local_threats:
        combat_types = {EntityType.BUILDER_BOT, EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER}
        threat = min(
            local_threats,
            key=lambda item: (
                0 if item.entity_type in combat_types else 1,
                -item.score,
                current.distance_squared(item.position),
                item.position.y,
                item.position.x,
            ),
        )
        threat_position = threat.position
        entity_type = threat.entity_type
        local = True
        severity = {
            EntityType.SENTINEL: 15,
            EntityType.GUNNER: 15,
            EntityType.LAUNCHER: 12,
            EntityType.BUILDER_BOT: 12,
            EntityType.HARVESTER: 7,
            EntityType.CONVEYOR: 6,
            EntityType.SPLITTER: 7,
        }.get(entity_type, max(5, int(threat.score)))
        kind = threat.kind
    elif state.defense_target is not None and state.defense_severity > 0:
        threat_position = state.defense_target
        severity = state.defense_severity
        kind = state.defense_kind
    if threat_position is None:
        return False

    # Enemy logistics is an offensive/sabotage opportunity, not evidence that we
    # are being attacked. Never recall defenders merely because their Harvester or
    # Conveyor is close to our route.
    if local and entity_type in (EntityType.HARVESTER, EntityType.CONVEYOR, EntityType.SPLITTER):
        loaded = False
        try:
            for entity_id, seen_type, seen_position in _enemy_entities(ct, buildings_only=True):
                if seen_type == entity_type and seen_position == threat_position:
                    loaded = bool(
                        seen_type in (EntityType.CONVEYOR, EntityType.SPLITTER)
                        and ct.get_stored_resource(entity_id) is not None
                    )
                    break
        except Exception:
            loaded = False
        _publish_rally(
            ct, state, threat_position,
            priority=_objective_priority(entity_type, loaded=loaded),
        )
        if current.distance_squared(threat_position) == 1 and _spend_allowed(
            ct, BUILDER_ATTACK_COST, paid_attack=True
        ):
            return actions.fire(threat_position)
        return False

    core_near = min(
        (threat_position.distance_squared(pos) for pos in world.core_footprint),
        default=999,
    ) <= 20
    route_near = bool(
        (
            state.route is not None
            and min(
                (threat_position.distance_squared(pos) for pos in state.route.cells),
                default=999,
            ) <= 12
        )
        or _team_economy_near(ct, state, threat_position)
    )
    personal_near = current.distance_squared(threat_position) <= 20
    if core_near:
        severity = min(15, severity + 3)
        if entity_type == EntityType.BUILDER_BOT:
            kind = ThreatKind.BUILDER_RUSH
    if route_near:
        severity = min(15, severity + 3)
        # Asset proximity raises urgency; it must not erase a more informative
        # attacker classification. Losing GUNNER/SENTINEL here made the response
        # choose the wrong countermeasure immediately after identifying the shot.
        if kind in (ThreatKind.UNKNOWN, ThreatKind.SABOTAGE, ThreatKind.ECONOMY_RUSH):
            kind = ThreatKind.ECONOMY_RUSH

    if local:
        combat_intruder = entity_type in (
            EntityType.BUILDER_BOT,
            EntityType.GUNNER,
            EntityType.SENTINEL,
            EntityType.LAUNCHER,
        )
        defensive_relevance = core_near or route_near or (
            combat_intruder
            and personal_near
            and (
                state.role in (Role.DEFENDER, Role.REPAIR)
                or state.claim_slot is not None
            )
        )
        # An offensive scout seeing enemy logistics is a rally/sabotage signal,
        # not an alarm that should pull the home screen across the map.
        if not defensive_relevance:
            return False

    if local:
        _publish_defense_alert(
            ct,
            state,
            threat_position,
            severity=severity,
            kind=kind,
        )

    close_specialized = bool(
        world is not None
        and min(world.width, world.height) <= 20
        and state.opening != Opening.BALANCED_ECONOMY
    )
    if close_specialized and kind == ThreatKind.BUILDER_RUSH:
        if not _bootstrap_owner_builder_interrupt_allowed(
            state,
            local=local,
            distance_squared=current.distance_squared(threat_position),
        ):
            return False

    near_home = bool(
        world.own_core is not None
        and current.distance_squared(world.own_core) <= 42
    )
    # Shared alerts now dispatch actual responders.  The deterministic split
    # avoids recalling the whole army: home defender, one network repairer, the
    # attacked route owner, and anyone already in immediate danger.
    respond = (
        personal_near
        or state.role == Role.DEFENDER
        or (
            state.role == Role.REPAIR
            and (
                (core_near and near_home)
                or severity >= 11
                or (severity >= 8 and abs(_id(ct)) % 2 == 0)
            )
        )
        or (state.claim_slot is not None and route_near)
        # Compact/medium offenses may have no dedicated DEFENDER among the small
        # free workforce. The primary route owner is therefore the guaranteed
        # last-resort Core responder without recalling every economy owner.
        or (core_near and state.claim_slot == 0)
        or (
            state.role in (Role.SABOTEUR, Role.RAIDER, Role.SIEGE)
            and severity >= 14
            and current.distance_squared(threat_position) <= 64
        )
    )
    if not respond:
        return False

    # If we can already see the attacked area, remove adjacent hostile buildings
    # first. Enemy Builders themselves require a turret/Launcher response.
    for _entity_id, _entity_type, position in _enemy_entities(ct, buildings_only=True):
        if current.distance_squared(position) != 1:
            continue
        if _spend_allowed(ct, BUILDER_ATTACK_COST, emergency=True, paid_attack=True):
            return actions.fire(position)

    if local and entity_type == EntityType.BUILDER_BOT:
        if _build_intruder_launcher(ct, state, actions, threat_position):
            return True
    if local and _build_reactive_barrier(
        ct,
        state,
        actions,
        threat_position,
        core_near=core_near,
        route_near=route_near,
        severity=severity,
        threat_kind=kind,
    ):
        return True
    if local and _build_defensive_turret(ct, state, actions, threat_position, threat_kind=kind):
        return True
    if _heal_adjacent(ct, actions):
        return True

    # A remote route alarm is actionable even outside this unit's vision. First
    # reach the damaged region. If we are already there and the damage signature
    # says Gunner/Sentinel but the shooter remains unseen, split responders across
    # the four legal cardinal firing lines instead of milling on the damage tile.
    response_target = threat_position
    response_adjacent = local and (personal_near or route_near)
    if (
        not local
        and current.distance_squared(threat_position) <= 20
        and kind in (ThreatKind.GUNNER_FIRE, ThreatKind.SENTINEL_FIRE, ThreatKind.FIRING_LINE)
    ):
        probe = _counterbattery_probe(ct, state, threat_position, kind)
        if probe is not None:
            response_target = probe
            response_adjacent = True
    return _move(ct, state, response_target, actions, adjacent=response_adjacent)

def _objective_priority(entity_type: EntityType, *, loaded: bool = False) -> int:
    if entity_type == EntityType.CORE:
        return 15
    if entity_type == EntityType.HARVESTER:
        return 13
    if entity_type == EntityType.SPLITTER:
        return 12 if loaded else 10
    if entity_type == EntityType.CONVEYOR:
        return 11 if loaded else 8
    if entity_type in (EntityType.SENTINEL, EntityType.GUNNER, EntityType.LAUNCHER):
        return 9
    if entity_type == EntityType.BARRIER:
        return 5
    if entity_type == EntityType.BUILDER_BOT:
        return 7
    return 1


def _assault_approach(
    ct: object,
    state: BuilderStateData,
    target: Position,
) -> Position:
    """Spread attackers over parallel lanes before the final approach."""
    world = state.world
    if world is None or world.own_core is None:
        return target
    core = world.own_core
    dx = target.x - core.x
    dy = target.y - core.y
    if abs(dx) >= abs(dy):
        px, py = 0, 1 if dx >= 0 else -1
    else:
        px, py = -1 if dy >= 0 else 1, 0
    lane_offsets = (-4, -2, 2, 4)
    offset = lane_offsets[abs(_id(ct)) % len(lane_offsets)]
    x = max(0, min(world.width - 1, target.x + px * offset))
    y = max(0, min(world.height - 1, target.y + py * offset))
    candidate = Position(x, y)
    return target if world.is_navigation_blocked(candidate) else candidate


def _attack_worker_ordinal(state: BuilderStateData) -> int:
    """1-based ordinal among deterministic RAIDER/SIEGE free-worker ranks.

    Compute from the role cycle instead of iterating up to the raw entity ID.
    Entity IDs can keep increasing after casualties/replacements, so an O(ID)
    formation helper would eventually become a CPU hazard under the 10 ms gate.
    """
    if state.flex_primary_owner and state.role in (Role.RAIDER, Role.SIEGE):
        # Reserve flex owners for outer holding slots; they are temporary attack
        # workers and should not steal one of the four stable cardinal classes.
        return 5 + (max(1, state.role_key) % 16)

    world = state.world
    area = world.width * world.height if world is not None else 324
    compact = area <= 196
    large = area >= 500

    cycle = 1
    attack_residues: tuple[int, ...] = ()
    if state.scenario == Scenario.ECONOMY_RESCUE:
        cycle, attack_residues = 1, ()
    elif state.scenario == Scenario.EXPANSION and state.phase == Phase.ECONOMY:
        if compact:
            cycle, attack_residues = 4, (3,)
        elif large:
            cycle, attack_residues = 7, (5, 6)
        else:
            cycle, attack_residues = 5, (3, 4)
    elif state.phase == Phase.DEFENSE or state.scenario == Scenario.CONTESTED:
        cycle, attack_residues = 1, ()
    elif state.phase in (Phase.OFFENSE, Phase.ENDGAME) or state.scenario in (Scenario.SIEGE, Scenario.ENDGAME):
        if compact:
            cycle, attack_residues = 6, (2, 3, 5)
        elif large:
            cycle, attack_residues = 9, (3, 4, 6, 7, 8)
        else:
            cycle, attack_residues = 7, (2, 3, 5, 6)

    key0 = max(0, int(state.role_key) - 1)
    full_cycles, residue = divmod(key0, cycle)
    count = full_cycles * len(attack_residues)
    count += sum(1 for value in attack_residues if value <= residue)
    if state.role in (Role.RAIDER, Role.SIEGE) and residue not in attack_residues:
        # Covers temporary role overrides without an O(ID) fallback.
        count += 1
    return max(1, count)


def _assigned_attack_stance(
    ct: object,
    state: BuilderStateData,
    target: Position,
) -> Position | None:
    """Assign a deterministic attack slot without same-round reservations.

    Store writes cannot reserve tiles atomically within a round. The safe way to
    avoid a thundering herd is therefore static sharding: attacker ordinals 1–4
    own the four cardinal action cells, while later attackers own distinct outer
    holding cells. This prevents several currently distant Builders from all
    selecting the same empty stance from the same start-of-round snapshot.
    """
    world = state.world
    if world is None:
        return None
    ordinal = _attack_worker_ordinal(state)
    if ordinal <= 4:
        direction = CARDINALS[(ordinal - 1) % 4]
        position = target.add(direction)
        if (
            0 <= position.x < world.width
            and 0 <= position.y < world.height
            and not world.is_navigation_blocked(position)
        ):
            try:
                builder_id = ct.get_tile_builder_bot_id(position)
            except Exception:
                builder_id = None
            if builder_id is None or int(builder_id) == _id(ct):
                return position
        # Do not steal another attacker's cardinal class from the same stale
        # snapshot; wait on this attacker's outer slot instead.

    ring = (
        (0, -2), (2, 0), (0, 2), (-2, 0),
        (1, -2), (2, 1), (-1, 2), (-2, -1),
        (-1, -2), (2, -1), (1, 2), (-2, 1),
        (0, -3), (3, 0), (0, 3), (-3, 0),
    )
    ring_index = max(0, ordinal - 5) % len(ring)
    # Try the assigned holding slot first, then deterministic alternates only if
    # it is statically illegal/visibly occupied. Different ordinals start at
    # different offsets, so same-round collisions remain rare even on bad walls.
    for offset in range(len(ring)):
        dx, dy = ring[(ring_index + offset) % len(ring)]
        position = Position(target.x + dx, target.y + dy)
        if not (0 <= position.x < world.width and 0 <= position.y < world.height):
            continue
        if world.is_navigation_blocked(position):
            continue
        try:
            builder_id = ct.get_tile_builder_bot_id(position)
        except Exception:
            builder_id = None
        if builder_id is None or int(builder_id) == _id(ct):
            return position
    return None

def _attack_priority(
    ct: object,
    entity_id: int,
    entity_type: EntityType,
    position: Position,
    current: Position,
    role: Role = Role.RAIDER,
) -> int:
    distance = current.distance_squared(position)
    stored = False
    try:
        stored = ct.get_stored_resource(entity_id) is not None
    except Exception:
        pass
    if role == Role.SIEGE:
        base = {
            EntityType.SENTINEL: 1450,
            EntityType.GUNNER: 1380,
            EntityType.LAUNCHER: 1260,
            EntityType.CORE: 1220,
            EntityType.HARVESTER: 1120,
            EntityType.SPLITTER: 900,
            EntityType.CONVEYOR: 820,
            EntityType.BARRIER: 650,
        }.get(entity_type, 0)
    else:
        # Mobile saboteurs win by permanently deleting production first, then
        # cutting loaded trunks.  Unloaded peripheral conveyors are lower value
        # than a Harvester or turret and should not drain titanium indefinitely.
        base = {
            EntityType.HARVESTER: 1500,
            EntityType.SPLITTER: 1180,
            EntityType.CONVEYOR: 1040,
            EntityType.SENTINEL: 980,
            EntityType.GUNNER: 940,
            EntityType.LAUNCHER: 900,
            EntityType.BARRIER: 560,
            EntityType.CORE: 420,
        }.get(entity_type, 0)
    if entity_type in (EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.HARVESTER):
        base += score_sabotage_target(entity_type, distance=distance, loaded=stored)
    if entity_type == EntityType.CORE:
        try:
            hp = int(ct.get_hp(entity_id))
        except Exception:
            hp = 999
        if hp <= 20 or _round(ct) >= 930:
            base = 2000
    return base - min(200, distance)


def _core_commit_ready(
    ct: object,
    state: BuilderStateData,
    buildings: list[tuple[int, EntityType, Position]],
) -> bool:
    """Finish a won local fight instead of sabotaging forever.

    Builder chip damage is expensive, so early pressure still prioritizes income.
    Once nearby production is stripped, combat support is established, the Core
    is already wounded, or the match is sufficiently late, paid Core hits become
    a legitimate conversion of the economic lead into the primary win condition.
    """
    if not _offense_active(state):
        return False
    core = next((item for item in buildings if item[1] == EntityType.CORE), None)
    if core is None:
        return False
    core_id, _core_type, core_pos = core
    try:
        hp = int(ct.get_hp(core_id))
    except Exception:
        hp = 999
    # Once resilient income exists and the enemy Core is physically known, the
    # primary win condition outranks another sabotage lap. Siege specialists may
    # still clear weapons, but Raiders converge on Core immediately.
    if state.team_maintaining_routes >= 2 or state.team_attack_priority >= 15:
        return True
    if hp <= 240:
        return True
    if _friendly_combat_nearby(ct, core_pos, 32):
        return True

    high_value_economy = False
    for entity_id, entity_type, _position in buildings:
        if entity_type in (EntityType.HARVESTER, EntityType.SPLITTER):
            high_value_economy = True
            break
        if entity_type == EntityType.CONVEYOR:
            try:
                if ct.get_stored_resource(entity_id) is not None:
                    high_value_economy = True
                    break
            except Exception:
                pass

    world = state.world
    area = world.width * world.height if world is not None else 324
    soft_round = 440 if area <= 196 else (560 if area < 500 else 680)
    hard_round = 760 if area <= 196 else (830 if area < 500 else 880)
    round_no = _round(ct)
    return round_no >= hard_round or (round_no >= soft_round and not high_value_economy)


def _paid_attack_worthwhile(
    ct: object,
    entity_id: int,
    entity_type: EntityType,
    *,
    loaded: bool = False,
    core_commit: bool = False,
) -> bool:
    """Spend Builder attacks when they advance denial or the Core kill."""
    round_no = _round(ct)
    try:
        hp = max(1, int(ct.get_hp(entity_id)))
    except Exception:
        hp = 999
    if entity_type == EntityType.CORE:
        return bool(core_commit or hp <= 240 or round_no >= 850)
    if core_commit and entity_type in (
        EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER, EntityType.BARRIER
    ):
        return True
    if entity_type == EntityType.HARVESTER:
        return round_no <= 972 or hp <= 4
    if entity_type in (EntityType.CONVEYOR, EntityType.SPLITTER):
        # A loaded link is immediate denial. An unloaded link is still useful to
        # cut early/midgame, but not worth twenty titanium of hits at the buzzer.
        return loaded or round_no <= 900 or hp <= 4
    if entity_type in (EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER):
        return round_no <= 980 or hp <= 4
    return hp <= 8 or round_no <= 850


def _attack(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    current = _pos(ct)
    buildings = _enemy_entities(ct, buildings_only=True)
    # Core localization is itself the strategic event. Publish it immediately,
    # even if this particular Scout still chooses to finish a nearby Harvester or
    # weapon first. In v0042 a Scout could physically see the Core but keep
    # advertising only the higher local sabotage target, so the Core never saw
    # priority 15 and the team failed to transition into the assault phase.
    visible_core = next((item for item in buildings if item[1] == EntityType.CORE), None)
    if visible_core is not None:
        _publish_rally(ct, state, visible_core[2], priority=15)
    enemy_builders = tuple(
        item for item in _enemy_entities(ct) if item[1] == EntityType.BUILDER_BOT
    )
    core_commit = _core_commit_ready(ct, state, buildings)

    def scored(entity_id: int, entity_type: EntityType, position: Position) -> int:
        value = _attack_priority(ct, entity_id, entity_type, position, current, state.role)
        if core_commit and entity_type == EntityType.CORE and state.role != Role.SIEGE:
            # Raiders lock onto the primary win condition. Bounded assault
            # engineers may still spend an action on a firing foothold before
            # falling back to paid Builder chip damage.
            value = max(value, 1960)
        return value

    ranked = sorted(
        (
            (scored(entity_id, entity_type, position), entity_id, entity_type, position)
            for entity_id, entity_type, position in buildings
        ),
        key=lambda item: (-item[0], item[3].y, item[3].x),
    )
    ranked = [item for item in ranked if item[0] > 0]
    if ranked:
        _, entity_id, entity_type, target = ranked[0]
        if entity_type == EntityType.HARVESTER:
            _remember_capture_target(state, target, _round(ct))
        try:
            loaded = entity_type in (EntityType.CONVEYOR, EntityType.SPLITTER) and ct.get_stored_resource(entity_id) is not None
        except Exception:
            loaded = False
        _publish_rally(
            ct,
            state,
            target,
            priority=_objective_priority(entity_type, loaded=loaded),
        )
        if _assault_engineer(state):
            distance = current.distance_squared(target)
            # Do not pay 20--30 Ti plus global entity scaling merely to chop a
            # cheap Conveyor. Mobile Builders can sabotage ordinary logistics on
            # their own. Static support is justified for producers, defended
            # positions, loaded junctions, and the Core where it changes combat.
            support_warranted = (
                entity_type in (
                    EntityType.CORE,
                    EntityType.HARVESTER,
                    EntityType.SENTINEL,
                    EntityType.GUNNER,
                    EntityType.LAUNCHER,
                )
                or (entity_type == EntityType.SPLITTER and loaded)
                or bool(enemy_builders)
            )
            if support_warranted:
                # Once the Core is confirmed, convert penetration into a firing
                # foothold before paying Builder chip damage. One engineer tries
                # to place a legal Core-firing turret, another can establish a
                # nearby Launcher that feeds reinforcements into the breach.
                if entity_type == EntityType.CORE:
                    if distance <= 81 and _build_turret_against(
                        ct, state, actions, target, forward=True
                    ):
                        return True
                    if distance <= 180 and _build_launcher_support(ct, state, actions, target):
                        return True
                    if distance > 64 and _build_forward_outpost(ct, state, actions, target):
                        return True
                else:
                    if distance > 26 and _build_launcher_support(ct, state, actions, target):
                        return True
                    if distance > 32 and _build_forward_outpost(ct, state, actions, target):
                        return True
                    if distance <= 64 and _build_turret_against(
                        ct, state, actions, target, forward=True
                    ):
                        return True
        if current.distance_squared(target) == 1:
            try:
                cost = BUILDER_ATTACK_COST
            except Exception:
                cost = 2
            if _paid_attack_worthwhile(
                ct,
                entity_id,
                entity_type,
                loaded=loaded,
                core_commit=core_commit,
            ) and _spend_allowed(
                ct,
                cost,
                paid_attack=True,
                endgame_commit=entity_type == EntityType.CORE,
            ):
                return actions.fire(target)
        # Once the target is close/visible, occupy a deterministic attack stance
        # rather than letting every Builder choose the same shortest adjacent
        # tile. Core footprints are multi-cell, so keep the generic adjacency
        # solver there; single-cell structures use explicit stance assignment.
        if entity_type != EntityType.CORE and current.distance_squared(target) > 1:
            stance = _assigned_attack_stance(ct, state, target)
            if stance is not None and current != stance:
                return _move(ct, state, stance, actions)
        approach = _assault_approach(ct, state, target)
        if current.distance_squared(target) > 36 and approach != target:
            return _move(ct, state, approach, actions)
        return _move(ct, state, target, actions, adjacent=True)

    # Turrets handle enemy Builders. A siege Builder may create a firing point;
    # ordinary raiders continue toward the shared objective instead of trying an
    # illegal Builder-on-Builder attack.
    if enemy_builders and _assault_engineer(state):
        target = min(enemy_builders, key=lambda item: current.distance_squared(item[2]))[2]
        if _build_turret_against(ct, state, actions, target, forward=True):
            return True

    world = state.world
    target = state.rally_target or (world.enemy_core if world else None)
    if target is None and world is not None and world.own_core is not None:
        # Half of blind mobile pressure stages through the outermost healthy
        # economic line and then pushes beyond it. This converts remote pipelines
        # into real forward presence while the other half still fans across the
        # three enemy-symmetry hypotheses for localization.
        frontier_target = _frontier_push_target(ct, state, advance=9)
        if (
            frontier_target is not None
            and abs(_id(ct)) % 2 == 0
            and current.distance_squared(frontier_target) > 16
        ):
            target = frontier_target
        else:
            own = world.own_core
            hypotheses = (
                Position(max(0, world.width - 2 - own.x), max(0, world.height - 2 - own.y)),
                Position(max(0, world.width - 2 - own.x), own.y),
                Position(own.x, max(0, world.height - 2 - own.y)),
            )
            target = hypotheses[(abs(_id(ct)) + state.hypothesis_shift) % len(hypotheses)]
    if target is not None:
        if _assault_engineer(state):
            # Never build expensive combat infrastructure toward a symmetry guess.
            # Blind Siege workers are mobile scouts/escorts until a real rally or
            # enemy Core is known. This prevents Launcher/turret scale inflation on
            # the wrong side of the map while preserving immediate support once
            # contact is verified.
            verified_combat_target = bool(
                world is not None and world.enemy_core is not None
            ) or bool(state.rally_target is not None and state.rally_priority >= 9)
            if verified_combat_target:
                distance = current.distance_squared(target)
                if state.rally_priority >= 15:
                    if distance <= 81 and _build_turret_against(
                        ct, state, actions, target, forward=True
                    ):
                        return True
                    if distance <= 180 and _build_launcher_support(ct, state, actions, target):
                        return True
                    if distance > 64 and _build_forward_outpost(ct, state, actions, target):
                        return True
                else:
                    if distance > 26 and _build_launcher_support(ct, state, actions, target):
                        return True
                    if distance > 32 and _build_forward_outpost(ct, state, actions, target):
                        return True
                    if distance <= 64 and _build_turret_against(
                        ct, state, actions, target, forward=True
                    ):
                        return True
        # Use separated lanes until the final firing approach. If a stale rally
        # is already visible and empty, sweep around it instead of idling on an
        # adjacent tile forever.
        try:
            target_visible = bool(ct.is_in_vision(target))
            target_building = ct.get_tile_building_id(target)
        except Exception:
            target_visible = False
            target_building = None
        if target_visible and target_building is None and state.rally_target == target:
            state.rally_target = None
            state.rally_priority = 0
            state.hypothesis_shift = (state.hypothesis_shift + 1) % 3
            state.last_hypothesis_shift_round = _round(ct)
            world = state.world
            if world is not None:
                sweep = Position(
                    max(0, min(world.width - 1, target.x + ((abs(_id(ct)) % 3) - 1) * 3)),
                    max(0, min(world.height - 1, target.y + (((abs(_id(ct)) // 3) % 3) - 1) * 3)),
                )
                if sweep != current and not world.is_navigation_blocked(sweep):
                    return _move(ct, state, sweep, actions)
        if (
            state.rally_target is None
            and _round(ct) - state.last_goal_progress_round >= 24
            and _round(ct) - state.last_hypothesis_shift_round >= 20
        ):
            state.hypothesis_shift = (state.hypothesis_shift + 1) % 3
            state.last_hypothesis_shift_round = _round(ct)
            if state.navigator is not None:
                state.navigator.invalidate()
        approach = _assault_approach(ct, state, target)
        if current.distance_squared(target) > 36 and approach != target:
            return _move(ct, state, approach, actions)
        return _move(ct, state, target, actions, adjacent=True)
    return False



def _opportunistic_harvest(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    """Let otherwise idle workers complete a receiver-backed nearby Harvester.

    This never creates an isolated Harvester: an adjacent Core or correctly
    oriented friendly Conveyor must already be able to receive its first stack.
    """
    # A receiver-backed Harvester is excellent tempo before terminal assault,
    # but after the endgame switch mobile actions belong to finding/killing Core.
    if _round(ct) >= 850:
        return False
    current = _pos(ct)
    try:
        own_team = ct.get_team()
    except Exception:
        return False
    for ore in (current.add(direction) for direction in CARDINALS):
        try:
            if ct.get_tile_env(ore) != Environment.ORE_TITANIUM:
                continue
            if ct.get_tile_building_id(ore) is not None:
                continue
        except Exception:
            continue
        if _enemy_core_exclusion_zone(state, ore):
            continue
        receiver_ready = False
        for direction in CARDINALS:
            receiver = ore.add(direction)
            entity_id, entity_type, facing = _visible(ct, receiver)
            if entity_id is None:
                continue
            try:
                friendly = ct.get_team(entity_id) == own_team
            except Exception:
                friendly = False
            if not friendly:
                continue
            if entity_type == EntityType.CORE:
                receiver_ready = True
                break
            if entity_type == EntityType.CONVEYOR and facing is not None:
                input_side = receiver.cardinal_direction_to(ore)
                if input_side != facing:
                    receiver_ready = True
                    break
        if not receiver_ready:
            continue
        try:
            cost = int(ct.get_harvester_cost())
        except Exception:
            return False
        if _spend_allowed(
            ct,
            cost,
            route_completion=True,
            producer_purchase=True,
        ) and actions.build_harvester(ore) is not None:
            return True
    return False

def _repair_visible_friendly(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """Heal or approach the nearest damaged friendly entity in vision."""
    try:
        own_team = ct.get_team()
        own_id = int(ct.get_id())
        ids = tuple(ct.get_nearby_entities())[:64]
    except Exception:
        return False
    current = _pos(ct)
    damaged: list[tuple[int, Position]] = []
    for entity_id in ids:
        if not cpu_is_safe(ct):
            break
        try:
            if int(entity_id) == own_id or ct.get_team(entity_id) != own_team:
                continue
            hp = int(ct.get_hp(entity_id))
            max_hp = int(ct.get_max_hp(entity_id))
            if hp >= max_hp:
                continue
            position = ct.get_position(entity_id)
        except Exception:
            continue
        priority = (max_hp - hp) * 20 - current.distance_squared(position)
        damaged.append((priority, position))
    if not damaged:
        return False
    _, target = max(damaged, key=lambda item: (item[0], -item[1].y, -item[1].x))
    if current.distance_squared(target) == 1:
        return actions.heal(target)
    return _move(ct, state, target, actions, adjacent=True)


def _defender_home_work(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """Reactive home responder; never pre-build a quiet-map turret."""
    world = state.world
    if world is not None:
        _offer_discovered_ore(ct, state, world, _round(ct))
    if _repair_visible_friendly(ct, state, actions):
        return True
    if _opportunistic_harvest(ct, state, actions):
        return True
    # Actual hostile contact is handled by _defense_overlay before role work. If
    # the shared alert remains but this responder has not reached vision yet, hold
    # useful home geometry without spending titanium speculatively.
    return _guard_patrol(ct, state, actions)


def _opening_ore_sprint(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """Use a newly spawned Builder's otherwise lost buffered-claim turn.

    Core claim writes become visible next round, but a spawned Builder acts in
    the current round.  Moving toward a visible ore immediately saves a full
    opening step without committing construction before ownership is known.
    """
    round_no = _round(ct)
    if state.claim_slot is not None or round_no >= 12:
        return False
    world = state.world
    if world is None:
        return False
    ores = [
        position
        for position in world.known_ore()
        if not world.is_navigation_blocked(position)
        or position in world.ore_positions
    ]
    if not ores:
        return False
    current = _pos(ct)
    ores.sort(
        key=lambda position: (
            current.distance_squared(position), position.y, position.x
        )
    )
    # Spread simultaneous new workers over the visible deposits. When only one
    # deposit is known they still fan around its adjacent approach naturally.
    target = ores[abs(_id(ct)) % len(ores)]
    if current.distance_squared(target) <= 1:
        return False
    return _move(ct, state, target, actions, adjacent=True, route_sensitive=True)


def _resource_guard_work(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """Service the producing network, with one repairer biased to the frontier."""
    if _repair_visible_friendly(ct, state, actions):
        return True
    world = state.world
    if world is None:
        return False
    round_no = _round(ct)

    if (
        int(state.role_key) == 1
        and world.own_core is not None
        and state.team_maintaining_routes < 2
    ):
        current = _pos(ct)
        if current.distance_squared(world.own_core) > 36:
            return _move(ct, state, world.own_core, actions, adjacent=True)
        if _opportunistic_harvest(ct, state, actions):
            return True
        forward = world.enemy_core or Position(
            max(0, world.width - 2 - world.own_core.x),
            max(0, world.height - 2 - world.own_core.y),
        )
        offsets = ((-2, 0), (3, 0), (0, -2), (0, 3), (-2, -1), (3, 2), (2, -2), (-1, 3))
        candidates = []
        for dx, dy in offsets:
            target = Position(world.own_core.x + dx, world.own_core.y + dy)
            if not (0 <= target.x < world.width and 0 <= target.y < world.height):
                continue
            if world.is_navigation_blocked(target):
                continue
            candidates.append(target)
        if candidates:
            target = min(candidates, key=lambda pos: (pos.distance_squared(forward), pos.y, pos.x))
            if current != target and current.distance_squared(target) > 1:
                return _move(ct, state, target, actions)
        return False

    healthy = [
        claim
        for _index, claim in _maintaining_claims(ct, state, round_no)
        if claim.position is not None
    ]
    claims = healthy or [
        claim
        for _index, claim in _read_claims(ct, world.width, world.height)
        if claim.position is not None and claim_is_fresh(claim, round_no & 63)
    ]
    if not claims:
        if _opportunistic_harvest(ct, state, actions):
            return True
        return _guard_patrol(ct, state, actions)

    origin = world.own_core or _pos(ct)
    area = world.width * world.height
    # On medium/large maps the first even-ranked repair worker becomes the
    # frontier service unit. Other repairers rotate normally across the network.
    # This preserves home coverage through the dedicated Defender while ensuring
    # a long pipeline is not left with only its owner for maintenance.
    frontier_service = area >= 225 and state.role_key % 2 == 0 and len(claims) >= 2
    if frontier_service:
        claim = max(
            claims,
            key=lambda item: (
                abs(item.position.x - origin.x) + abs(item.position.y - origin.y),
                item.position.distance_squared(origin),
                item.position.y,
                item.position.x,
            ),
        )
    else:
        claims.sort(key=lambda claim: (claim.position.y, claim.position.x))
        # Rotate fast enough that one lone saboteur cannot spend dozens of turns
        # dismantling a remote producer completely unseen.  This is inspection,
        # not a permanent guard: the worker keeps traversing useful network space.
        claim = claims[(abs(_id(ct)) // 2 + round_no // 16) % len(claims)]

    target = claim.position
    current = _pos(ct)
    if current.distance_squared(target) > 13:
        return _move(ct, state, target, actions, adjacent=True)
    if _opportunistic_harvest(ct, state, actions):
        return True
    # A shared repairer may briefly stage around a producer while servicing it.
    offsets = ((-2, 0), (0, -2), (2, 0), (0, 2), (-1, -1), (1, 1))
    for step in range(len(offsets)):
        dx, dy = offsets[(state.cursor + step) % len(offsets)]
        patrol = Position(target.x + dx, target.y + dy)
        if not (0 <= patrol.x < world.width and 0 <= patrol.y < world.height):
            continue
        if world.is_navigation_blocked(patrol):
            continue
        state.cursor = (state.cursor + step + 1) % len(offsets)
        if patrol != current:
            return _move(ct, state, patrol, actions)
    return False



def _remember_capture_target(
    state: BuilderStateData,
    position: Position,
    round_no: int,
    *,
    horizon: int = 96,
) -> None:
    """Remember enemy production as territory to convert, not merely destroy."""
    state.capture_target = position
    state.capture_started_round = int(round_no)
    state.capture_until_round = max(state.capture_until_round, int(round_no) + max(24, int(horizon)))


def _capture_enemy_economy_work(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """Turn a sabotaged enemy Harvester tile into our next economic route.

    Only claimless Scouts/Raiders use the satellite route state. Primary owners
    keep their recovery blueprint intact. While the enemy building still exists,
    ordinary attack logic handles destruction; once the ore is exposed this job
    pre-empts roaming and begins a real Conveyor+Harvester takeover.
    """
    target = state.capture_target
    round_no = _round(ct)
    # Harvester rallies use priority 13. If the original saboteur moved on or was
    # a primary owner, a claimless follower arriving one round later can inherit
    # the takeover once it sees the now-empty ore tile.
    if target is None and state.rally_target is not None and state.rally_priority == 13:
        inherited = state.rally_target
        try:
            exposed = (
                bool(ct.is_in_vision(inherited))
                and ct.get_tile_building_id(inherited) is None
                and ct.get_tile_env(inherited) == Environment.ORE_TITANIUM
            )
        except Exception:
            exposed = False
        if exposed:
            _remember_capture_target(state, inherited, round_no, horizon=72)
            target = inherited
    if target is None or state.satellite_mode:
        return False
    if round_no > state.capture_until_round:
        state.capture_target = None
        return False
    if state.claim_slot is not None or state.role not in (Role.SCOUT, Role.RAIDER):
        return False
    world = state.world
    if world is None:
        return False
    current = _pos(ct)
    try:
        visible = bool(ct.is_in_vision(target))
    except Exception:
        visible = current.distance_squared(target) <= 16
    if not visible:
        # Return to the recently sabotaged economic tile instead of following the
        # attack column away and surrendering the resource back to the opponent.
        return _move(ct, state, target, actions, adjacent=True, route_sensitive=True)

    try:
        building_id = ct.get_tile_building_id(target)
    except Exception:
        building_id = None
    if building_id is not None:
        try:
            friendly = _is_friendly(ct, int(building_id))
        except Exception:
            friendly = False
        if friendly:
            state.capture_target = None
            return False
        # Still contested: keep sabotaging this economy rather than allowing the
        # generic rally to drag the capture worker toward some newer target.
        return _attack(ct, state, actions)
    try:
        is_ore = ct.get_tile_env(target) == Environment.ORE_TITANIUM
    except Exception:
        is_ore = target in world.ore_positions
    if not is_ore:
        state.capture_target = None
        return False

    # Deep enemy territory is not automatically economy. If this ore is inside
    # the enemy Core zone or detached from our maintained/trunk frontier, convert
    # the successful sabotage into an assault instead of funding an indefensible
    # Harvester and a long vulnerable conveyor chain.
    if not _capture_is_supportable(ct, state, target):
        state.capture_target = None
        enemy_core = _shared_enemy_core_target(state)
        if enemy_core is not None:
            _publish_rally(ct, state, enemy_core, priority=15)
            return _attack(ct, state, actions)
        return False

    claimed = {
        claim.position
        for _index, claim in _read_claims(ct, world.width, world.height)
        if claim.position is not None and claim_is_fresh(claim, round_no & 63)
    }
    if target in claimed or target in state.satellite_completed_ores:
        state.capture_target = None
        return False

    try:
        resources = max(0, int(ct.get_global_resources()))
        harvester = max(0, int(ct.get_harvester_cost()))
        conveyor = max(0, int(ct.get_conveyor_cost()))
        raw_budget = int(ct.read_store(int(Slot.BUDGET)))
        budget = decode_budget(raw_budget) if raw_budget > 0 else None
    except Exception:
        resources = 0
        harvester = BASE_HARVESTER_COST
        conveyor = BASE_CONVEYOR_COST
        budget = None
    if budget is None:
        budget = compute_budget(ct, phase=Phase.ECONOMY)
    # This takeover *is* the next economic project, so preserve liquidity and any
    # real defense envelope but do not double-reserve another full construction seed.
    capture_seed = harvester + 3 * conveyor
    reserve = max(20, budget.liquidity) + budget.defense
    if resources < capture_seed + reserve:
        # Occupy the resource while passive income replenishes the bank.
        if current.distance_squared(target) > 2:
            return _move(ct, state, target, actions, adjacent=True, route_sensitive=True)
        return True

    _reset_route(state, keep_target=False)
    state.ore_target = target
    state.claim_started_round = round_no
    state.satellite_started_round = round_no
    state.satellite_completed_round = -999
    state.satellite_mode = True
    state.state = BuilderState.CLAIM
    state.capture_target = None
    return _run_satellite_expansion(ct, state, actions)


def _visible_enemy_economy(ct: object) -> bool:
    """Return whether a nearby enemy asset is worth immediate economic pressure."""
    for _entity_id, entity_type, _position in _enemy_entities(ct, buildings_only=True):
        if entity_type in (
            EntityType.HARVESTER,
            EntityType.SPLITTER,
            EntityType.CONVEYOR,
            EntityType.GUNNER,
            EntityType.SENTINEL,
            EntityType.LAUNCHER,
            EntityType.CORE,
        ):
            return True
    return False


def _frontier_worker_ordinal(ct: object, state: BuilderStateData) -> int:
    """Return this claimless mobile worker's 1-based frontier ordinal.

    Passive primary owners are mobile for combat/scouting, but they cannot start a
    satellite route because doing so would overwrite their recovery blueprint.
    v0040 mistakenly counted those ineligible flex owners when electing pioneers,
    so after four primary routes the real claimless workers often had ordinals 4+
    and *nobody* was elected to expand. Exclude flex-owner role keys here.
    """
    if state.claim_slot is not None or state.role not in (Role.SCOUT, Role.RAIDER):
        return 0
    world = state.world
    if world is None:
        return 0
    area = world.width * world.height
    large = area >= 500
    compact = area <= 196
    round_no = _round(ct)
    active_owner_ids = _priority_owner_ids(ct, state)

    # Role keys are raw IDs compressed by active construction owners. Build the
    # corresponding key set for *passive* primary owners and skip them when
    # numbering satellite-eligible workers.
    flex_owner_keys: set[int] = set()
    for index, claim in _read_claims(ct, world.width, world.height):
        if not claim_is_fresh(claim, round_no & 63):
            continue
        if _project_status_for_claim(ct, index, claim, round_no) != 2:
            continue
        owner_id = int(claim.owner_id)
        key = owner_id - sum(1 for active_id in active_owner_ids if active_id < owner_id)
        flex_owner_keys.add(max(1, key))

    count = 0
    for key in range(1, max(1, int(state.role_key)) + 1):
        if key in flex_owner_keys:
            continue
        role = assign_role(
            key,
            state.phase,
            state.opening,
            route_owner=False,
            large_map=large,
            compact_map=compact,
            scenario=state.scenario,
        )
        if role in (Role.SCOUT, Role.RAIDER):
            count += 1
    return count


def _satellite_pioneer_count(ct: object, state: BuilderStateData) -> int:
    """How many claimless workers continuously grow the Harvester frontier.

    One lane starts as soon as the first producer is healthy and remains alive in
    every macro phase, including ENDGAME and confirmed-Core pressure. Rich teams
    add lanes from surplus. A severe defense interrupt may collapse back to one
    lane, but never to zero.
    """
    if state.world is None or state.team_maintaining_routes < 1:
        return 0
    if max(state.team_defense_severity, state.defense_severity) >= 12:
        return 1
    try:
        resources = max(0, int(ct.get_global_resources()))
        builder_cost = max(0, int(ct.get_builder_bot_cost()))
        harvester_cost = max(0, int(ct.get_harvester_cost()))
        conveyor_cost = max(0, int(ct.get_conveyor_cost()))
        raw_budget = int(ct.read_store(int(Slot.BUDGET)))
        budget = decode_budget(raw_budget) if raw_budget > 0 else None
    except Exception:
        return 1
    if budget is None:
        budget = compute_budget(ct, phase=Phase.ECONOMY)
    reserve = max(20, budget.liquidity) + budget.defense
    route_seed = harvester_cost + 8 * conveyor_cost
    spendable = max(0, resources - reserve)
    count = 1
    if state.team_maintaining_routes >= 2 and spendable >= builder_cost + 2 * route_seed + 80:
        count = 2
    if state.team_maintaining_routes >= 4 and spendable >= 2 * builder_cost + 3 * route_seed + 220:
        count = 3
    # A verified Core gets most surplus bodies, but one economic lane survives.
    if state.team_attack_priority >= 15:
        count = min(count, 1)
    return count


def _satellite_expansion_worker(ct: object, state: BuilderStateData) -> bool:
    """Elect bounded mobile workers as continuous frontier-economy pioneers."""
    if state.claim_slot is not None or state.role not in (Role.SCOUT, Role.RAIDER):
        return False
    if state.world is None:
        return False
    unfinished_primary = max(0, state.team_active_projects - state.team_maintaining_routes)
    if unfinished_primary > 1:
        return False
    ordinal = _frontier_worker_ordinal(ct, state)
    return 1 <= ordinal <= _satellite_pioneer_count(ct, state)

def _satellite_candidate(
    ct: object,
    state: BuilderStateData,
) -> Position | None:
    """Choose the next outward profitable producer using projected live income.

    Requiring the *entire* long route in cash up front was a major local-expansion
    bias. Existing Harvesters continue earning while a pioneer walks/builds, so we
    conservatively credit only 55% of that expected construction-window income.
    Positive-payback routes are preferred through the late game; very late
    expansion is admitted only when the bank has a large strategic cushion.
    """
    world = state.world
    round_no = _round(ct)
    if world is None or world.own_core is None or round_no >= 970:
        return None
    if state.satellite_cooldown_until > round_no:
        return None
    try:
        resources = max(0, int(ct.get_global_resources()))
        conveyor_cost = max(0, int(ct.get_conveyor_cost()))
        harvester_cost = max(0, int(ct.get_harvester_cost()))
        raw_budget = int(ct.read_store(int(Slot.BUDGET)))
        budget = decode_budget(raw_budget) if raw_budget > 0 else None
    except Exception:
        return None
    if budget is None:
        budget = compute_budget(ct, phase=Phase.ECONOMY)

    # This candidate *is* the expansion project, so do not reserve another full
    # construction envelope on top of it. Preserve liquidity and real defense.
    reserve = max(20, budget.liquidity) + budget.defense
    claimed = {
        claim.position
        for _index, claim in _read_claims(ct, world.width, world.height)
        if claim.position is not None and claim_is_fresh(claim, round_no & 63)
    }
    origin_cells = world.core_footprint or {world.own_core}
    frontier = _frontier_claim_position(ct, state)
    frontier_distance = 0
    if frontier is not None:
        frontier_distance = min(
            abs(frontier.x - cell.x) + abs(frontier.y - cell.y)
            for cell in origin_cells
        )

    maintaining = max(1, int(state.team_maintaining_routes or 0))
    pioneer_count = max(1, _satellite_pioneer_count(ct, state))
    pioneer_ordinal = max(1, _frontier_worker_ordinal(ct, state))
    candidates: list[tuple[bool, float, Position]] = []
    for ore in world.known_ore():
        if (
            ore in claimed
            or ore in state.rejected_ore_until
            or ore in state.satellite_completed_ores
            or _enemy_core_exclusion_zone(state, ore)
        ):
            continue
        try:
            if ct.is_in_vision(ore) and ct.get_tile_building_id(ore) is not None:
                continue
        except Exception:
            pass
        distance = min(
            abs(ore.x - cell.x) + abs(ore.y - cell.y)
            for cell in origin_cells
        )
        rough_new_links = min(
            max(1, distance - 1),
            _rough_new_links_via_trunk(state, ore, round_no),
        )
        estimated = harvester_cost + estimate_route_cost(rough_new_links, conveyor_cost)
        build_delay = max(6, 2 * rough_new_links + 6)
        # 10 Ti / 4 rounds / maintained Harvester, heavily hair-cut because combat
        # and repairs also spend the same bank. This merely removes the unrealistic
        # requirement that a 25-tile line be fully prepaid before its first step.
        income_credit = min(300, int(0.55 * maintaining * 2.5 * build_delay))
        if resources + income_credit < estimated + reserve:
            continue
        production_start = round_no + build_delay
        payback = estimate_payback_round(
            estimated,
            output_per_round=2.5,
            start_round=production_start,
            horizon=995,
        )
        # When the treasury is genuinely overflowing, a slightly sub-payback
        # producer can still be a rational map-control purchase: it adds a
        # Harvester tiebreaker, a forward observation anchor, and denies ore.
        # Require a large post-purchase cushion so this never applies to a poor
        # or merely comfortable economy.
        strategic_cushion = resources - reserve - estimated
        if payback is None and strategic_cushion < max(220, estimated):
            continue
        remaining_output = max(0.0, (1000 - production_start) * 2.5)
        net_value = remaining_output - estimated
        frontier_gain = distance - frontier_distance
        outward = frontier_gain >= 2
        # First prefer an actually outward producer, then maximize economic value.
        # The bounded frontier bonus breaks close calls without admitting bad lines.
        score = float(net_value + min(120, max(0, frontier_gain) * 6) - 0.5 * distance)
        candidates.append((outward, score, ore))
    if not candidates:
        return None
    outward_candidates = [item for item in candidates if item[0]]
    pool = outward_candidates or candidates
    pool.sort(key=lambda item: (-item[1], item[2].y, item[2].x))
    if pioneer_count > 1:
        # Multiple rich-state pioneers must not all pick the same best ore. Use a
        # deterministic coordinate shard; secondary pioneers wait rather than
        # duplicate the primary when their shard currently has no viable target.
        shard = [
            item
            for item in pool
            if ((item[2].x * 31 + item[2].y * 17) % pioneer_count) == pioneer_ordinal - 1
        ]
        if shard:
            pool = shard
        elif pioneer_ordinal > 1:
            return None
    return pool[0][2]

def _start_satellite_expansion(
    ct: object,
    state: BuilderStateData,
) -> bool:
    if not _satellite_expansion_worker(ct, state):
        return False
    target = _satellite_candidate(ct, state)
    if target is None:
        return False
    _reset_route(state, keep_target=False)
    state.ore_target = target
    state.claim_started_round = _round(ct)
    state.satellite_started_round = _round(ct)
    state.satellite_completed_round = -999
    state.satellite_mode = True
    state.state = BuilderState.CLAIM
    return True


def _run_satellite_expansion(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """Finish one real route, verify it, hand it off, then build the next."""
    if not state.satellite_mode:
        return False
    round_no = _round(ct)
    if state.ore_target is None:
        state.satellite_mode = False
        state.satellite_cooldown_until = round_no + 8
        return False
    if round_no - state.satellite_started_round > 220 and not _route_health_fresh(state, round_no):
        _reset_route(state, keep_target=False)
        state.satellite_mode = False
        state.satellite_cooldown_until = round_no + 32
        return False
    if state.route is None:
        planned = _plan_route(ct, state, state.ore_target, round_no)
        if not planned:
            if _pos(ct).distance_squared(state.ore_target) > 20:
                _move(ct, state, state.ore_target, actions, adjacent=True, route_sensitive=True)
            return True
    if state.route is not None and state.route_index >= 0:
        _build_route(ct, state, actions)
        if not actions.moved and not actions.acted and state.route_index >= 0:
            next_cell = state.route.cells[state.route_index]
            if _pos(ct).distance_squared(next_cell) != 1:
                _move(ct, state, next_cell, actions, adjacent=True, route_sensitive=True)
        return True
    if state.route is not None and not _route_health_fresh(state, round_no):
        _patrol_route(ct, state, actions)
        if _route_health_fresh(state, round_no):
            state.satellite_completed_round = round_no
        return not _route_health_fresh(state, round_no) or actions.moved or actions.acted
    if state.route is not None:
        if state.satellite_completed_round < 0:
            state.satellite_completed_round = round_no
        # A short stability window avoids abandoning a line that only happened to
        # look complete for one observation. After that, passive logistics need no
        # dedicated owner; the pioneer resumes outward discovery immediately.
        if round_no - state.satellite_completed_round >= 5:
            if state.ore_target is not None:
                state.satellite_completed_ores.add(state.ore_target)
            _reset_route(state, keep_target=False)
            state.satellite_mode = False
            state.satellite_cooldown_until = round_no + 2
            return False
        if round_no >= state.next_patrol_round and _patrol_route(ct, state, actions):
            return True
    return False


def _frontier_expansion_work(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """Continuous map-economy loop: build producer or deliberately reveal frontier."""
    if state.satellite_mode:
        return _run_satellite_expansion(ct, state, actions)
    if not _satellite_expansion_worker(ct, state):
        return False
    if _start_satellite_expansion(ct, state):
        return _run_satellite_expansion(ct, state, actions)
    # No profitable producer yet: increase real map knowledge. A blind radial
    # projection can repeatedly run into the same wall/corridor without learning
    # the side pockets that contain the next ore.
    return _scout(ct, state, actions)

def _route_guard_work(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """One-turn handoff/recall work around a freshly verified primary route."""
    route = state.route
    world = state.world
    if route is None or not route.cells or world is None:
        return False
    if _repair_visible_friendly(ct, state, actions):
        return True
    if _opportunistic_harvest(ct, state, actions):
        return True
    _offer_discovered_ore(ct, state, world, _round(ct))

    current = _pos(ct)
    anchor = route.ore
    origin = world.own_core or anchor
    leash = 12 if world.width * world.height >= 225 else 9
    if abs(current.x - anchor.x) + abs(current.y - anchor.y) > leash:
        return _move(ct, state, anchor, actions, adjacent=True)

    # Use the same coverage-complete survey stations as free Scouts, filtered to
    # this Harvester's response leash. Prefer stations that extend the economic
    # frontier away from Core.
    anchor_radius = abs(anchor.x - origin.x) + abs(anchor.y - origin.y)
    candidates = []
    for point in _exploration_waypoints(world, origin, resource_dense=True):
        if point in world.seen_tiles or world.is_navigation_blocked(point):
            continue
        if abs(point.x - anchor.x) + abs(point.y - anchor.y) > leash:
            continue
        radius = abs(point.x - origin.x) + abs(point.y - origin.y)
        if radius + 2 < anchor_radius:
            continue
        candidates.append(point)
    if candidates:
        target = min(
            candidates,
            key=lambda pos: (
                -(abs(pos.x - origin.x) + abs(pos.y - origin.y)),
                current.distance_squared(pos),
                pos.y,
                pos.x,
            ),
        )
        return _move(ct, state, target, actions)

    # No unknown station inside the leash: hold near the producer. No decorative orbit.
    if current.distance_squared(anchor) > 13:
        return _move(ct, state, anchor, actions, adjacent=True)
    return False


def _guard_patrol(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    """Hold one useful Core-side service station; never lap the base."""
    world = state.world
    if world is None or world.own_core is None:
        return False
    current = _pos(ct)
    forward = world.enemy_core or Position(
        max(0, world.width - 2 - world.own_core.x),
        max(0, world.height - 2 - world.own_core.y),
    )
    offsets = ((-2, 0), (3, 0), (0, -2), (0, 3), (-2, -1), (3, 2), (2, -2), (-1, 3))
    candidates = []
    for dx, dy in offsets:
        target = Position(world.own_core.x + dx, world.own_core.y + dy)
        if not (0 <= target.x < world.width and 0 <= target.y < world.height):
            continue
        if world.is_navigation_blocked(target):
            continue
        candidates.append(target)
    if not candidates:
        return False
    candidates.sort(key=lambda pos: (pos.distance_squared(forward), pos.y, pos.x))
    target = candidates[(max(1, int(state.role_key)) - 1) % min(len(candidates), 4)]
    if current == target or current.distance_squared(target) <= 1:
        return False
    return _move(ct, state, target, actions)



def _enemy_axis(world: WorldMemory, origin: Position) -> tuple[int, int]:
    """Approximate the enemy-facing axis even before the enemy Core is known."""
    if world.enemy_core is not None:
        dx = world.enemy_core.x - origin.x
        dy = world.enemy_core.y - origin.y
    else:
        # Competition maps are symmetric.  The reflected Core location is a much
        # better prior for "front" than blindly treating the farthest tile as front.
        dx = (world.width - 1 - origin.x) - origin.x
        dy = (world.height - 1 - origin.y) - origin.y
    if dx == 0 and dy == 0:
        dx = 1 if world.width >= world.height else 0
        dy = 0 if world.width >= world.height else 1
    return dx, dy


def _survey_sector(world: WorldMemory, origin: Position, position: Position) -> str:
    fx, fy = _enemy_axis(world, origin)
    vx, vy = position.x - origin.x, position.y - origin.y
    dot = vx * fx + vy * fy
    cross = fx * vy - fy * vx
    # On diagonal maps, a pure horizontal/vertical displacement is exactly 45°
    # from the enemy axis. Treat that tie as a flank rather than accidentally
    # folding both side corridors into the front/rear sectors.
    if abs(dot) > abs(cross):
        return "front" if dot >= 0 else "rear"
    return "right" if cross >= 0 else "left"


def _secure_ore_bias(world: WorldMemory, origin: Position, position: Position) -> int:
    """Reward cheap rear/side producers while the local economy is still forming."""
    distance = abs(position.x - origin.x) + abs(position.y - origin.y)
    if distance > 16:
        return 0
    sector = _survey_sector(world, origin, position)
    if sector == "rear":
        return 42
    if sector in ("left", "right"):
        return 24
    return -8

def _exploration_waypoints(
    world: WorldMemory,
    origin: Position,
    *,
    resource_dense: bool = False,
) -> tuple[Position, ...]:
    """Return a fast first-pass sweep plus coverage-complete resource fill.

    v0019 used an 8x8 waypoint lattice while considering a waypoint verified at
    squared distance 16.  On larger maps that leaves diagonal pockets outside
    every verification circle.  Replacing it outright with a dense lattice fixes
    the holes but slows common easy discoveries.

    The resource survey therefore keeps the original coarse 8x8 points first and
    appends a 7x5 anisotropic fill lattice afterward.  Easy ore is found with the
    same fast first pass; if that pass fails, the second pass guarantees every
    integer grid cell is within squared distance <= 13 of a verification point.
    Full siege scouts use only the coarse enemy-localization sweep.
    """
    margin = 2

    def lattice(spacing_x: int, spacing_y: int) -> set[Position]:
        xs = list(
            range(
                min(margin, max(0, world.width - 1)),
                world.width,
                max(1, int(spacing_x)),
            )
        )
        ys = list(
            range(
                min(margin, max(0, world.height - 1)),
                world.height,
                max(1, int(spacing_y)),
            )
        )
        if world.width:
            xs.append(max(0, world.width - 1 - margin))
            xs.append(world.width // 2)
        if world.height:
            ys.append(max(0, world.height - 1 - margin))
            ys.append(world.height // 2)
        return {
            Position(x, y)
            for x in xs
            for y in ys
            if 0 <= x < world.width and 0 <= y < world.height
        }

    coarse = lattice(8, 8)
    points = set(coarse)
    if resource_dense:
        if world.width >= world.height:
            fill = lattice(7, 5)
        else:
            fill = lattice(5, 7)
        points.update(fill)
    points.discard(origin)
    coarse.discard(origin)

    return tuple(
        sorted(
            points,
            key=lambda pos: (
                0 if pos in coarse else 1,
                abs(pos.x - origin.x) + abs(pos.y - origin.y),
                pos.distance_squared(origin),
                pos.y,
                pos.x,
            ),
        )
    )


def _scout(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    world = state.world
    if world is None:
        return False

    round_no = _round(ct)
    _offer_discovered_ore(ct, state, world, round_no)

    if world.enemy_core is not None:
        _publish_rally(ct, state, world.enemy_core, priority=15)
    # Before the first delivered route, every free Scout is a resource Scout.
    # Once income exists, only a bounded fraction probes enemy-side hypotheses;
    # local rushes are already handled immediately by the defense overlay.
    maintaining = _maintaining_route_count(ct, round_no)
    frontier_pioneer = _satellite_expansion_worker(ct, state)
    probe_mod = 4 if maintaining == 1 else 3
    early_probe = (
        maintaining >= 1
        and not _active_primary_job(state)
        and state.scenario != Scenario.ECONOMY_RESCUE
        and abs(_id(ct)) % probe_mod == 0
    )
    respond_to_rally = (
        not frontier_pioneer
        and (
            state.role == Role.SABOTEUR
            or (_offense_active(state) and state.role in (Role.RAIDER, Role.SIEGE, Role.SCOUT))
            or (_pressure_active(state) and state.role == Role.RAIDER)
            or (round_no >= 120 and early_probe)
        )
    )
    # A free scout that discovers enemy infrastructure immediately turns that
    # discovery into a shared rally and begins sabotage. Route owners only share
    # the sighting; they keep searching for their assigned ore until saturated.
    visible_enemy = _enemy_entities(ct, buildings_only=True)
    if visible_enemy:
        current = _pos(ct)
        ranked = sorted(
            (
                (
                    _attack_priority(ct, entity_id, entity_type, position, current, state.role),
                    entity_type,
                    position,
                )
                for entity_id, entity_type, position in visible_enemy
            ),
            key=lambda item: (-item[0], item[2].y, item[2].x),
        )
        if ranked and ranked[0][0] > 0:
            _score, entity_type, enemy_position = ranked[0]
            if entity_type == EntityType.HARVESTER:
                _remember_capture_target(state, enemy_position, round_no)
            loaded = False
            if entity_type in (EntityType.CONVEYOR, EntityType.SPLITTER):
                # Publish the same high-value signal that the assault routine
                # would use; otherwise a Scout can see a loaded trunk yet write
                # priority 8, preventing the Core from starting timely denial.
                for entity_id, seen_type, seen_position in visible_enemy:
                    if seen_type != entity_type or seen_position != enemy_position:
                        continue
                    try:
                        loaded = ct.get_stored_resource(entity_id) is not None
                    except Exception:
                        loaded = False
                    break
            local_priority = _objective_priority(entity_type, loaded=loaded)
            _publish_rally(
                ct,
                state,
                enemy_position,
                priority=local_priority,
            )
            # Local information is fresher than the one-round delayed Store, but
            # do not abandon a truly higher-priority shared objective. This fixes
            # Scouts walking past a Harvester they can see because an older
            # Conveyor rally was still alive.
            local_econ_denial = bool(
                entity_type == EntityType.HARVESTER
                and state.claim_slot is None
            )
            if (
                not _active_primary_job(state)
                and (respond_to_rally or local_econ_denial)
                and (local_econ_denial or local_priority >= state.rally_priority)
            ):
                if current.distance_squared(enemy_position) == 1:
                    try:
                        cost = BUILDER_ATTACK_COST
                    except Exception:
                        cost = 2
                    if _spend_allowed(
                        ct,
                        cost,
                        paid_attack=True,
                        endgame_commit=entity_type == EntityType.CORE,
                    ):
                        return actions.fire(enemy_position)
                return _move(ct, state, enemy_position, actions, adjacent=True)

    # Only after evaluating what is visible right now do we obey a shared rally.
    # The rally remains the team coordination mechanism; it simply no longer
    # suppresses better fresh local evidence.
    target = state.rally_target or world.enemy_core
    if target is not None and not _active_primary_job(state) and respond_to_rally:
        approach = _assault_approach(ct, state, target)
        if _pos(ct).distance_squared(target) > 36 and approach != target:
            return _move(ct, state, approach, actions)
        return _move(ct, state, target, actions, adjacent=True)

    origin = world.own_core or _pos(ct)

    # Keep one survey leg coherent. Buffered claims/roles can change every round,
    # but a Scout that has already committed to a useful side/rear station should
    # not turn around until it reaches/observes it or the leg is clearly stalled.
    if state.scout_target is not None and round_no < state.scout_target_until:
        current = _pos(ct)
        target = state.scout_target
        stalled = (
            state.stuck_goal == target
            and state.last_goal_progress_round >= 0
            and round_no - state.last_goal_progress_round >= 7
        )
        if (
            not world.is_navigation_blocked(target)
            and current.distance_squared(target) > 16
            and not stalled
        ):
            return _move(ct, state, target, actions)
        state.explored_waypoints.add(target)
        state.scout_target = None
        if state.navigator is not None:
            state.navigator.invalidate()

    # Systematic territory survey. The dense lattice is deliberately retained:
    # synthetic obstacle tests show it finds side-pocket ore more reliably than
    # a pure "always chase the nearest unknown frontier" policy. The behavior
    # change is in priority and completion: after first income, free surveyors
    # sweep their assigned stations outward first and never fall back to Core laps.
    rapid_opening = bool(
        maintaining <= 0
        and state.claim_slot is None
        and not _active_primary_job(state)
    )
    # Opening surveyors use a sparse, fast first pass. Their movement path reveals
    # intervening tiles, so immediately checking every dense lattice station is
    # slower than racing separate sectors before the opponent occupies the ore.
    waypoints = _exploration_waypoints(
        world,
        origin,
        resource_dense=not rapid_opening or round_no >= 72,
    )
    if waypoints:
        area = world.width * world.height
        shard_count = 4 if area <= 196 else (6 if area < 500 else 8)
        shard = state.claim_slot if state.claim_slot is not None else abs(_id(ct)) % shard_count
        unvisited = tuple(point for point in waypoints if point not in state.explored_waypoints)
        primary = tuple(
            point for point in waypoints[int(shard) :: shard_count]
            if point not in state.explored_waypoints
        )
        assigned = primary or unvisited

        outward_survey = bool(
            (rapid_opening or maintaining >= 1)
            and state.scenario not in (Scenario.ECONOMY_RESCUE, Scenario.CONTESTED)
            and (state.claim_slot is None or state.flex_primary_owner)
        )
        if outward_survey and assigned:
            # The old farthest-first ordering unintentionally sent almost everyone
            # toward the opponent-facing half of symmetric maps. During bootstrap,
            # deliberately cover rear + both flanks before the fourth lane takes
            # the front. Once income exists, the Saboteur owns the front while the
            # dedicated Scout keeps filling safer side/rear information.
            if maintaining <= 0:
                sector_order = ("rear", "left", "right", "front")
                desired_sector = sector_order[(max(1, state.role_key) - 1) % 4]
            elif state.role == Role.SABOTEUR:
                desired_sector = "front"
            elif state.role == Role.SCOUT:
                sector_order = ("left", "right", "rear", "front")
                desired_sector = sector_order[(max(1, state.role_key) - 1) % 4]
            else:
                desired_sector = None

            # Sector ownership must precede ID sharding. Previously a rear Scout
            # could receive a shard containing no rear waypoints and spend its
            # whole opening in the wrong half of the map.
            if desired_sector is not None:
                sector_pool = tuple(
                    point for point in unvisited
                    if _survey_sector(world, origin, point) == desired_sector
                )
                if sector_pool:
                    assigned = sector_pool

            def survey_key(pos: Position):
                radius = abs(pos.x - origin.x) + abs(pos.y - origin.y)
                sector_penalty = 0 if desired_sector is None or _survey_sector(world, origin, pos) == desired_sector else 1
                # First sweep a useful local security ring quickly, then push farther.
                local_band = 0 if maintaining <= 1 and 5 <= radius <= 13 else 1
                return (
                    sector_penalty,
                    local_band,
                    -radius if local_band else radius,
                    _pos(ct).distance_squared(pos),
                    pos.y, pos.x,
                )

            assigned = tuple(sorted(assigned, key=survey_key))

        attempts = 0
        while attempts < len(assigned):
            target = assigned[state.explore_cursor % len(assigned)]
            current = _pos(ct)
            known_blocked = world.is_navigation_blocked(target)
            visible = current.distance_squared(target) <= 16
            stalled = (
                state.stuck_goal == target
                and state.last_goal_progress_round >= 0
                and round_no - state.last_goal_progress_round >= 6
            )
            if not (known_blocked or visible or stalled):
                state.scout_target = target
                state.scout_target_until = round_no + 16
                return _move(ct, state, target, actions)
            state.explored_waypoints.add(target)
            if state.scout_target == target:
                state.scout_target = None
            state.explore_cursor = (state.explore_cursor + 1) % max(1, len(assigned))
            if state.navigator is not None:
                state.navigator.invalidate()
            attempts += 1

        remaining = tuple(
            point for point in waypoints
            if point not in state.explored_waypoints
            and not world.is_navigation_blocked(point)
            and _pos(ct).distance_squared(point) > 16
        )
        if remaining:
            # Fill actual survey holes before declaring this map region known.
            target = min(remaining, key=lambda pos: (
                _pos(ct).distance_squared(pos),
                -pos.distance_squared(origin),
                pos.y, pos.x,
            ))
            state.scout_target = target
            state.scout_target_until = round_no + 16
            return _move(ct, state, target, actions)

    # Local survey complete: stage beyond our current economic frontier/opponent
    # side. Never return to a centre/corner carousel just to keep moving.
    frontier_target = _frontier_push_target(ct, state, advance=9)
    if frontier_target is not None and _pos(ct).distance_squared(frontier_target) > 16:
        return _move(ct, state, frontier_target, actions)
    if world.enemy_core is None and world.own_core is not None:
        opposite = Position(
            max(0, world.width - 2 - world.own_core.x),
            max(0, world.height - 2 - world.own_core.y),
        )
        if _pos(ct).distance_squared(opposite) > 20:
            return _move(ct, state, opposite, actions, adjacent=True)
    return False


def _emergency_roam(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """Last-resort outward staging; never rotate through Core/corners."""
    world = state.world
    if world is None:
        return False
    frontier = _frontier_push_target(ct, state, advance=10)
    if frontier is not None and _pos(ct).distance_squared(frontier) > 9:
        return _move(ct, state, frontier, actions)
    if world.own_core is not None and world.enemy_core is None:
        opposite = Position(
            max(0, world.width - 2 - world.own_core.x),
            max(0, world.height - 2 - world.own_core.y),
        )
        if _pos(ct).distance_squared(opposite) > 20:
            return _move(ct, state, opposite, actions, adjacent=True)
    return False


def _core_congestion_clear(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """Push low-priority mobile workers out of a congested Core neighbourhood."""
    if state.team_core_congestion < 5:
        return False
    if not _free_mobile_worker(state):
        return False
    if state.role in (Role.DEFENDER, Role.REPAIR):
        return False
    world = state.world
    if world is None or world.own_core is None:
        return False
    current = _pos(ct)
    if current.distance_squared(world.own_core) > 36:
        return False
    frontier = _frontier_push_target(ct, state, advance=7)
    if frontier is not None and current.distance_squared(frontier) > 16:
        return _move(ct, state, frontier, actions)
    # Deterministic four-way egress if no economic frontier exists yet.
    edge_targets = (
        Position(world.width // 2, 1),
        Position(max(0, world.width - 2), world.height // 2),
        Position(world.width // 2, max(0, world.height - 2)),
        Position(1, world.height // 2),
    )
    target = edge_targets[(max(1, state.role_key) - 1) % len(edge_targets)]
    if target != current and not world.is_navigation_blocked(target):
        return _move(ct, state, target, actions)
    return False


def _progress_watchdog_work(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """Retask a mobile unit that has been busy without making real progress."""
    if state.nonprogress_turns < 5:
        return False
    if not _free_mobile_worker(state):
        return False
    if state.navigator is not None:
        state.navigator.invalidate()
    state.explore_cursor += 1
    state.hypothesis_shift = (state.hypothesis_shift + 1) % 3
    state.last_hypothesis_shift_round = _round(ct)

    if (
        state.team_defense_severity >= 8
        and state.defense_target is not None
        and state.role in (Role.SCOUT, Role.SABOTEUR, Role.RAIDER, Role.SIEGE, Role.REPAIR)
    ):
        return _move(ct, state, state.defense_target, actions, adjacent=True)

    route_stalled = (
        state.team_route_progress_age >= 20
        and state.team_active_projects > state.team_maintaining_routes
    )
    if route_stalled and state.team_attack_priority < 11:
        if state.role == Role.REPAIR and _resource_guard_work(ct, state, actions):
            return True
        if state.role in (Role.SCOUT, Role.SABOTEUR, Role.RAIDER, Role.SIEGE):
            return _scout(ct, state, actions)

    if state.team_attack_priority >= 11 and state.role in (Role.SCOUT, Role.SABOTEUR, Role.RAIDER, Role.SIEGE):
        return _attack(ct, state, actions)
    if state.role in (Role.SCOUT, Role.SABOTEUR, Role.RAIDER, Role.SIEGE):
        return _scout(ct, state, actions)
    return False


def _global_work_steal(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
) -> bool:
    """Use the Core-authored team snapshot to recover from a failed local job.

    The snapshot is intentionally coarse. Exact positions still come from the
    existing claim, defense-alert and rally slots/local vision. This function is
    only a fallback after the unit's preferred role did nothing, so it cannot
    steal a healthy route owner or interrupt a committed satellite pipeline.
    """
    if not _free_mobile_worker(state):
        return False

    # Severe defense is globally urgent. A free combat/scout worker that has no
    # productive local action this turn becomes temporary reinforcement.
    if (
        state.team_defense_severity >= 10
        and state.defense_target is not None
        and state.role in (Role.SCOUT, Role.SABOTEUR, Role.RAIDER, Role.SIEGE)
    ):
        return _move(ct, state, state.defense_target, actions, adjacent=True)

    route_pressure = (
        state.team_active_projects > state.team_maintaining_routes
        or state.team_maintaining_routes < (state.team_route_target or _minimum_primary_routes(state))
        or (
            state.team_route_progress_age >= 20
            and state.team_active_projects > 0
        )
    )
    if route_pressure and state.role in (Role.REPAIR, Role.SCOUT):
        if state.role == Role.REPAIR and _resource_guard_work(ct, state, actions):
            return True
        # Scouts keep verifying ore/frontier space while owners finish the actual
        # single-writer construction state machine.
        return _scout(ct, state, actions)

    if (
        state.team_attack_priority >= 11
        and state.role in (Role.SCOUT, Role.SABOTEUR, Role.RAIDER, Role.SIEGE)
    ):
        if _attack(ct, state, actions):
            return True

    # With a stable minimum economy and no urgent fight, idle mobile workers
    # should increase map information/territorial reach rather than roam locally.
    if (
        state.team_maintaining_routes >= (state.team_route_target or _minimum_primary_routes(state))
        and state.role in (Role.SCOUT, Role.SABOTEUR, Role.RAIDER, Role.SIEGE)
    ):
        return _scout(ct, state, actions)
    return False


def _finish_builder_turn(
    ct: object,
    state: BuilderStateData,
    actions: TurnActions,
    *,
    allow_roam: bool = True,
) -> BuilderStateData:
    """Guarantee a secondary useful job after a preferred action fails."""
    round_no = _round(ct)
    satellite_committed = bool(
        state.satellite_mode and not _route_health_fresh(state, round_no)
    )
    if not actions.moved and not actions.acted:
        # Healing is cheap and useful for every role.
        _heal_adjacent(ct, actions)

    if not actions.moved and not actions.acted:
        if satellite_committed:
            # Do not let a phase change steal the expansion worker halfway through
            # a paid route. Hold/approach the next build stance or producer until
            # this short line is actually healthy.
            if state.route is not None and state.route_index >= 0:
                index = min(state.route_index, len(state.route.cells) - 1)
                if index >= 0:
                    target = state.route.cells[index]
                    if _pos(ct).distance_squared(target) != 1:
                        _move(ct, state, target, actions, adjacent=True, route_sensitive=True)
            elif state.ore_target is not None and state.route is None:
                _move(ct, state, state.ore_target, actions, adjacent=True, route_sensitive=True)
        elif state.claim_slot is not None and not state.flex_primary_owner:
            if state.route is None or state.ore_target is None:
                _scout(ct, state, actions)
            elif state.route_index >= 0:
                # Stale/partially reset state must never index outside the route.
                # Clamp a valid index; otherwise invalidate construction state and
                # let the normal planner recover on the next turn.
                if not state.route.cells:
                    state.route_index = -1
                elif state.route_index >= len(state.route.cells):
                    state.route_index = len(state.route.cells) - 1
                if state.route_index >= 0:
                    target = state.route.cells[state.route_index]
                    if _pos(ct).distance_squared(target) != 1:
                        _move(ct, state, target, actions, adjacent=True, route_sensitive=True)
            elif _route_health_fresh(state, round_no):
                _route_guard_work(ct, state, actions)
        elif state.role == Role.DEFENDER:
            _defender_home_work(ct, state, actions)
        elif state.role == Role.SABOTEUR:
            if not _attack(ct, state, actions):
                _scout(ct, state, actions)
        elif _pressure_active(state) and state.role in (Role.RAIDER, Role.SIEGE):
            _attack(ct, state, actions)

    if (
        not satellite_committed
        and not actions.moved
        and not actions.acted
        and state.idle_turns >= 1
        and _yield_to_urgent_neighbor(ct, state, actions)
    ):
        pass
    elif (
        not satellite_committed
        and not actions.moved
        and not actions.acted
        and state.idle_turns >= 1
        and _global_work_steal(ct, state, actions)
    ):
        pass
    elif (
        not satellite_committed
        and not actions.moved
        and not actions.acted
        and _opportunistic_harvest(ct, state, actions)
    ):
        pass
    elif not actions.moved and not actions.acted and allow_roam and not satellite_committed:
        if not _scout(ct, state, actions):
            _emergency_roam(ct, state, actions)

    seen_count = len(state.world.seen_tiles) if state.world is not None else 0
    learned = seen_count > state.last_seen_tile_count
    goal_progress = state.last_goal_progress_round == round_no
    truly_productive = bool(actions.acted or learned or (actions.moved and goal_progress))

    if actions.moved or actions.acted:
        state.idle_turns = 0
    else:
        state.idle_turns += 1

    if truly_productive:
        state.last_productive_round = round_no
        state.nonprogress_turns = 0
    else:
        # Walking in circles no longer counts as productivity. This counter can
        # rise even while actions.move() succeeds every turn.
        state.nonprogress_turns += 1

    if state.idle_turns >= 2 and state.navigator is not None:
        state.navigator.invalidate()
    if state.idle_turns >= 4:
        state.cursor = (state.cursor + 1) % 8
        state.explore_cursor += 1
        state.idle_turns = 0
    if state.nonprogress_turns >= 8:
        if state.navigator is not None:
            state.navigator.invalidate()
        state.cursor = (state.cursor + 1) % 8
        state.explore_cursor += 1
        state.hypothesis_shift = (state.hypothesis_shift + 1) % 3
        state.nonprogress_turns = 5  # remain in watchdog mode until real progress
    state.last_seen_tile_count = seen_count
    state.last_position = _pos(ct)
    return state


def run_builder(
    ct: object,
    state: BuilderStateData | None = None,
) -> BuilderStateData:
    state = state or BuilderStateData()
    world = _world(ct, state)
    round_no = _round(ct)
    _refresh_trunk_memory(ct, state)
    _read_strategy(ct, state)
    _read_rally(ct, state)
    _read_defense_alert(ct, state)
    _publish_damage_alarm_if_needed(ct, state)
    target = _claim(ct, state, world, round_no)
    _normalize_route_state(state)
    state.flex_primary_owner = _primary_owner_can_flex(state, target, round_no)
    _refresh_role(ct, state, _active_primary_job(state))
    # Keep the healthy route heartbeat alive while its owner is mobile. The Core
    # still counts the passive pipeline, but role/right-of-way logic no longer
    # treats this Builder as permanently occupied by it.
    if state.flex_primary_owner:
        _publish_project_status(ct, state)
    actions = TurnActions(ct)

    if _defense_overlay(ct, state, actions):
        return _finish_builder_turn(ct, state, actions, allow_roam=False)

    if not _active_primary_job(state) and _opening_ore_sprint(ct, state, actions):
        return _finish_builder_turn(ct, state, actions, allow_roam=False)

    # Clear narrow friendly convoys *before* a low-priority worker commits to
    # another perfectly valid move. Waiting until the end-of-turn idle fallback
    # cannot unblock a Scout that keeps making progress in the wrong direction
    # while a first-income owner is queued behind it.
    if not _active_primary_job(state) and _corridor_chain_yield(ct, state, actions):
        return _finish_builder_turn(ct, state, actions, allow_roam=False)

    # Core-area traffic is globally visible to the Core and broadcast one round
    # later. Low-priority mobile workers proactively clear the spawn/logistics
    # neighbourhood instead of waiting until they physically block somebody.
    if not _active_primary_job(state) and _core_congestion_clear(ct, state, actions):
        return _finish_builder_turn(ct, state, actions, allow_roam=False)

    # Sabotage is only useful if we convert exposed enemy production into our own
    # territory. A claimless saboteur that recently hit a Harvester gets first
    # refusal on that ore before generic frontier work or the next rally.
    if not _active_primary_job(state) and _capture_enemy_economy_work(ct, state, actions):
        return _finish_builder_turn(ct, state, actions, allow_roam=False)

    # Blueprint invariant: the elected frontier Scout executes economy before
    # generic watchdog/combat work. Phase changes may pre-empt it for an actual
    # defense overlay above, but OFFENSE itself never steals the expansion lane.
    if state.satellite_mode or _satellite_expansion_worker(ct, state):
        if _frontier_expansion_work(ct, state, actions):
            return _finish_builder_turn(ct, state, actions, allow_roam=False)

    # A unit can move every round yet accomplish nothing. The progress watchdog
    # retasks such mobile workers before they repeat another stale loop.
    if not _active_primary_job(state) and _progress_watchdog_work(ct, state, actions):
        return _finish_builder_turn(ct, state, actions, allow_roam=False)

    if _active_primary_job(state):
        _publish_project_status(ct, state)
        if target is None:
            _scout(ct, state, actions)
            _publish_project_status(ct, state)
            return _finish_builder_turn(ct, state, actions)

        if state.route is None:
            _plan_route(ct, state, target, round_no)
        if state.route is not None and state.route_index >= 0:
            if not _route_can_start_construction(ct, state, round_no):
                # Wait at the next construction cell rather than wandering away.
                # This owner remains immediately ready when the first income line
                # comes online, while avoiding a second conveyor-cost spiral.
                next_cell = state.route.cells[state.route_index]
                if _pos(ct).distance_squared(next_cell) != 1:
                    _move(
                        ct,
                        state,
                        next_cell,
                        actions,
                        adjacent=True,
                        route_sensitive=True,
                    )
                else:
                    # Holding the exact legal build stance is productive. Do not
                    # patrol away and add two travel turns when the release gate
                    # opens; only perform free/local maintenance while waiting.
                    _heal_adjacent(ct, actions)
                    if state.world is not None:
                        _offer_discovered_ore(ct, state, state.world, round_no)
                _publish_project_status(ct, state)
                return _finish_builder_turn(ct, state, actions, allow_roam=False)
            route_action = _build_route(ct, state, actions)
            if route_action or state.route is None or state.route_index >= 0:
                _publish_project_status(ct, state)
                return _finish_builder_turn(ct, state, actions, allow_roam=False)

        if state.route is None:
            if state.ore_target is None:
                _scout(ct, state, actions)
            else:
                # Claimed ore with no valid route means we need more observations
                # along that corridor. Going home creates the replayed local loop.
                _move(
                    ct, state, state.ore_target, actions,
                    adjacent=True, route_sensitive=True,
                )
            _publish_project_status(ct, state)
            return _finish_builder_turn(ct, state, actions)

        health_fresh = _route_health_fresh(state, round_no)
        patrol_due = not health_fresh or round_no >= state.next_patrol_round
        if patrol_due:
            _patrol_route(ct, state, actions)
            health_fresh = _route_health_fresh(state, round_no)
            _publish_project_status(ct, state)
            if actions.moved or actions.acted or not health_fresh:
                return _finish_builder_turn(ct, state, actions, allow_roam=False)

        if health_fresh:
            _route_guard_work(ct, state, actions)
        _publish_project_status(ct, state)
        return _finish_builder_turn(ct, state, actions)

    if state.role == Role.DEFENDER:
        current = _pos(ct)
        # DEFENDER exists only during a fresh CONTESTED/DEFENSE interrupt. The
        # overlay above already travels to the exact shared threat while it is
        # live; after contact expires, regroup at home without speculative builds.
        if world.own_core is not None and current.distance_squared(world.own_core) > 36:
            _move(ct, state, world.own_core, actions, adjacent=True)
        else:
            _defender_home_work(ct, state, actions)
        return _finish_builder_turn(ct, state, actions, allow_roam=False)

    if state.role == Role.REPAIR:
        _resource_guard_work(ct, state, actions)

    # One persistent mobile specialist exists after first income. Unlike a generic
    # Scout it does not get elected as a satellite pioneer, so enemy logistics can
    # be shadowed/denied continuously while separate workers keep extending econ.
    if (
        not actions.moved
        and not actions.acted
        and state.role == Role.SABOTEUR
    ):
        if _visible_enemy_economy(ct) or state.rally_priority >= 9:
            _attack(ct, state, actions)
        if not actions.moved and not actions.acted:
            _scout(ct, state, actions)

    # The expansion phase is intentionally dual-track. Surveyors that actually
    # encounter enemy production do not walk past it merely because their stable
    # role is SCOUT; they publish/pressure the target while route owners and the
    # dedicated expansion worker continue growing our economy.
    if (
        not actions.moved
        and not actions.acted
        and state.scenario == Scenario.EXPANSION
        and state.phase == Phase.ECONOMY
        and state.role in (Role.SCOUT, Role.SABOTEUR)
        and _visible_enemy_economy(ct)
    ):
        _attack(ct, state, actions)

    if (
        not actions.moved
        and not actions.acted
        and _pressure_active(state)
        and state.role in (Role.RAIDER, Role.SIEGE)
    ):
        _attack(ct, state, actions)

    if not actions.moved and not actions.acted:
        _opportunistic_harvest(ct, state, actions)
    if not actions.moved and not actions.acted:
        _scout(ct, state, actions)
    return _finish_builder_turn(ct, state, actions)
