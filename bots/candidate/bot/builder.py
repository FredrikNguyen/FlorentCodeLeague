from __future__ import annotations

from dataclasses import dataclass, field

from fcode import Direction, EntityType, Environment, GameConstants, Position

from .actions import CARDINALS, TurnActions, cpu_is_safe
from .comms import Slot, assignment_is_fresh, decode_alert, epoch_distance, read_assignment, read_project, write_project
from .core import compute_budget
from .defense import assess_threat, choose_defensive_build, choose_turret_type
from .economy import claim_should_release, estimate_payback_round, estimate_route_cost, expansion_allowed, next_harvester_state, score_ore
from .logistics import find_broken_link, plan_core_outward_route, splitter_redundancy_justified, teardown_allowed, verify_route
from .navigation import Navigator, bounded_bfs
from .offense import choose_raid_action, choose_rally
from .policy import assign_role, late_game_policy, nearest_position
from .types import BuilderState, ProjectState, Role, RoutePlan, ThreatKind
from .world import WorldMemory


@dataclass(slots=True)
class BuilderStateData:
    role: Role = Role.SCOUT; state: BuilderState = BuilderState.DISCOVER; world: WorldMemory | None = None; navigator: Navigator | None = None
    ore_target: Position | None = None; route: RoutePlan | None = None; route_index: int = -1; repair_index: int | None = None
    claim_slot: int | None = None; claim_epoch: int = 0; claim_started_round: int = 0; last_delivery_round: int | None = None
    last_position: Position | None = None; blocked_steps: int = 0; cursor: int = 0
    built_links: dict[Position, tuple[EntityType, Direction]] = field(default_factory=dict)
    route_search: dict[str, object] | None = None; last_resource_total: int | None = None; last_resource_round: int | None = None; delivery_started_round: int | None = None
    backlog_rounds: int = 0; rally_target: Position | None = None; rally_expires_epoch: int = 0; last_final_storage: bool | None = None
    redundancy_branch: tuple[Position, ...] = (); redundancy_index: int = -1; redundancy_join: Position | None = None; project_count: int = 0; project_pending: bool = False


def _id(ct: object) -> int:
    try: return int(ct.get_id())
    except Exception: return 0


def _round(ct: object) -> int:
    try: return int(ct.get_current_round())
    except Exception: return 0


def _pos(ct: object) -> Position:
    try: return ct.get_position()
    except Exception: return Position(0, 0)


def _read_claims(ct: object, width: int, height: int):
    return [(index, assignment, read_project(ct, index)) for index in range(3) if (assignment := read_assignment(ct, index)) is not None]


def _active_project_count(ct: object, state: BuilderStateData | None = None) -> int:
    active = sum(1 for index in range(3) if (project := read_project(ct, index)) is not None and project.state not in (ProjectState.IDLE, ProjectState.FAILED)); local = int(state is not None and bool(state.project_count or state.route_search is not None or state.route_index >= 0 or state.redundancy_branch)); return min(3, max(active, local))


def _reserve_project(ct: object, state: BuilderStateData, *, wait_visible: bool = False) -> bool:
    if state.claim_slot is None: return False
    round_no = _round(ct); project = read_project(ct, state.claim_slot)
    if state.project_pending:
        visible = project is not None and project.epoch == (state.claim_epoch & 63) and project.state not in (ProjectState.IDLE, ProjectState.FAILED)
        state.project_pending = not visible; return visible
    if project is not None and project.state not in (ProjectState.IDLE, ProjectState.FAILED): state.project_count = max(1, state.project_count); return True
    if _active_project_count(ct, state) >= 3: return False
    if not write_project(ct, state.claim_slot, state.ore_target, round_no & 63, ProjectState.CLAIMED, int(ct.get_map_width()), int(ct.get_map_height()), writer=state.claim_slot): return False
    state.project_count, state.project_pending, state.claim_epoch = 1, True, round_no & 63
    return False


def _ore_is_valid(ct: object, world: WorldMemory, position: Position | None) -> bool: return position is not None and 0 <= position.x < world.width and 0 <= position.y < world.height and (position in world.ore_positions or ct.get_tile_env(position) == Environment.ORE_TITANIUM)


def _reset_route_search(state: BuilderStateData) -> None:
    state.route_search = None; state.route = None; state.route_index = -1; state.repair_index = None; state.last_final_storage = None; state.redundancy_branch = (); state.redundancy_index = -1; state.redundancy_join = None


def _project_status(state: BuilderStateData) -> ProjectState:
    return ProjectState.IDLE if state.project_count <= 0 and state.ore_target is None and state.route is None and state.route_search is None and not state.redundancy_branch else ProjectState.PLANNING if state.route_search is not None and state.route is None else ProjectState.BUILDING if state.route is not None and state.route_index >= 0 else ProjectState.VERIFYING if state.state == BuilderState.VERIFY else ProjectState.DELIVERING if state.state == BuilderState.DELIVER else ProjectState.MAINTAIN if state.state == BuilderState.MAINTAIN else ProjectState.CLAIMED


def _set_project(ct: object, state: BuilderStateData, status: ProjectState, round_no: int) -> None:
    if state.claim_slot is not None: write_project(ct, state.claim_slot, state.ore_target, round_no & 63, status, int(ct.get_map_width()), int(ct.get_map_height()), writer=state.claim_slot)


def _publish_owner_state(ct: object, state: BuilderStateData, world: WorldMemory, round_no: int) -> None:
    if state.claim_slot is None or round_no % 8 != 0: return
    write_project(ct, state.claim_slot, state.ore_target, round_no & 63, _project_status(state), world.width, world.height, writer=state.claim_slot)


def _read_rally(ct: object, state: BuilderStateData) -> None:
    try:
        decoded = decode_alert(ct.read_store(int(Slot.RALLY)), int(ct.get_map_width()), int(ct.get_map_height()))
        round_no = int(ct.get_current_round()) & 63
    except Exception: state.rally_target, state.rally_expires_epoch = None, 0; return
    if decoded is None: state.rally_target, state.rally_expires_epoch = None, 0; return
    position, expires_epoch = decoded
    state.rally_target = position if position is not None and epoch_distance(expires_epoch, round_no) <= 8 else None; state.rally_expires_epoch = expires_epoch if state.rally_target is not None else 0


def _fresh_verified_rally(ct: object, state: BuilderStateData, world: WorldMemory, round_no: int) -> bool:
    target, observation = state.rally_target, world.dynamic.get(state.rally_target) if state.rally_target is not None else None
    if target is None or epoch_distance(state.rally_expires_epoch, round_no & 63) > 8 or observation is None or round_no - observation.seen_round >= 3: return False
    try: return observation.team is None or observation.team != ct.get_team()
    except Exception: return False


def _publish_rally(ct: object, state: BuilderStateData, world: WorldMemory, round_no: int) -> None:
    if state.claim_slot != 0 or world.enemy_core is None or round_no % 4 != 0: return
    observation = world.dynamic.get(world.enemy_core)
    if observation is None or round_no - observation.seen_round >= 3: return
    try:
        rally = choose_rally(_pos(ct), verified_target=world.enemy_core, target_age=0); expires = (round_no + 8) & 63; ct.write_store(int(Slot.RALLY), encode_alert(rally, world.width, expires)); state.rally_target, state.rally_expires_epoch = rally, expires
    except Exception: pass


def _can_spend(ct: object, cost: int, *, preserve_defense: bool = False, projected_output: float | None = None, allow_late_completion: bool = False, emergency: bool = False, near_term_core_kill: bool = False, state: BuilderStateData | None = None, new_project: bool = False) -> bool: return _can_spend_with_policy(ct, cost, preserve_defense=preserve_defense, projected_output=projected_output, allow_late_completion=allow_late_completion, emergency=emergency, near_term_core_kill=near_term_core_kill, state=state, new_project=new_project)


def _can_spend_with_policy(ct: object, cost: int, *, preserve_defense: bool = False, projected_output: float | None = None, allow_late_completion: bool = False, emergency: bool = False, near_term_core_kill: bool = False, state: BuilderStateData | None = None, new_project: bool = False) -> bool:
    try:
        round_no, resources = _round(ct), int(ct.get_global_resources()); active_projects = _active_project_count(ct, state); own_project = int(state is not None and bool(state.project_count or state.route_search is not None or state.route_index >= 0 or state.redundancy_branch)); budget = compute_budget(ct, route_projects=max(0, active_projects - own_project) + int(new_project))
    except Exception:
        return False
    cost = max(0, int(cost))
    if cost <= 0 or new_project and active_projects >= 3 or round_no >= 850 and not (allow_late_completion or emergency or near_term_core_kill) or projected_output is not None and float(projected_output) <= 0: return False
    protected = budget.construction + budget.ammo + budget.liquidity + (0 if emergency else budget.defense)
    if resources < cost + protected: return False
    if emergency or near_term_core_kill: return not new_project or (state is not None and _reserve_project(ct, state, wait_visible=True))
    if estimate_payback_round(cost, output_per_round=2.5, start_round=round_no, horizon=1000) is None: return False
    return not new_project or (state is not None and _reserve_project(ct, state, wait_visible=True))


def _claim(ct: object, state: BuilderStateData, world: WorldMemory, round_no: int):
    claims = _read_claims(ct, world.width, world.height)
    own = next(((index, assignment, project) for index, assignment, project in claims if assignment.owner_id == _id(ct)), None)
    if own is None:
        if state.claim_slot is not None: claim_should_release(False, 0, 31, True); state.claim_slot, state.ore_target = None, None; _reset_route_search(state)
        return None
    state.claim_slot, assignment, project = own; target = project.position if project is not None else None; heartbeat = project.epoch if project is not None and project.state != ProjectState.IDLE else assignment.generation; age = epoch_distance(round_no & 63, heartbeat); valid_ore = target is None or _ore_is_valid(ct, world, target)
    failed = project is not None and project.state == ProjectState.FAILED
    if not assignment_is_fresh(assignment, round_no & 63) or claim_should_release(valid_ore, age, 31, False) or failed:
        state.claim_slot, state.ore_target = None, None; _reset_route_search(state); return None
    if target is not None: state.ore_target = target; _publish_owner_state(ct, state, world, round_no); return target
    claimed = {project.position for _, assignment, project in claims if project is not None and project.position is not None and assignment_is_fresh(assignment, round_no & 63)}
    candidates = [position for position in world.known_ore() if position not in claimed]
    if not candidates:
        try:
            candidates = [tile for tile in ct.get_nearby_tiles() if tile not in claimed and ct.get_tile_env(tile) == Environment.ORE_TITANIUM]
        except Exception: candidates = []
    if not candidates: return None
    origin = _pos(ct)
    candidates.sort(key=lambda position: (-score_ore(position, origin=origin, expected_output_horizon=max(0, 1000 - round_no) * 2), position.y, position.x))
    target = candidates[min(state.claim_slot, len(candidates) - 1)]
    state.ore_target = target; state.claim_epoch, state.claim_started_round = round_no & 63, round_no
    write_project(ct, state.claim_slot, target, round_no & 63, ProjectState.CLAIMED, world.width, world.height, writer=state.claim_slot)
    return target


def _visible(ct: object, position: Position):
    try:
        entity_id = ct.get_tile_building_id(position)
    except Exception: return None, None, None
    if entity_id is None: return None, None, None
    try: entity_type = ct.get_entity_type(entity_id)
    except Exception: entity_type = None
    try: direction = ct.get_direction(entity_id)
    except Exception: direction = None
    return entity_id, entity_type, direction


def _visible_route(state: BuilderStateData, ct: object, route: RoutePlan):
    def get(position: Position):
        _, entity_type, direction = _visible(ct, position)
        if entity_type is None:
            try: return state.built_links.get(position) if not ct.is_in_vision(position) else (entity_type, direction)
            except Exception: return state.built_links.get(position)
        return entity_type, direction

    return get


def _route_health(ct: object, state: BuilderStateData, route: RoutePlan, round_no: int) -> tuple[bool, bool]:
    try:
        resources = int(ct.get_global_resources())
    except Exception: resources = state.last_resource_total if state.last_resource_total is not None else 0
    previous_resources, previous_round = state.last_resource_total, state.last_resource_round; state.last_resource_total, state.last_resource_round = resources, round_no
    elapsed_rounds = 0 if previous_round is None else max(0, round_no - previous_round)
    passive_output = (0 if previous_round is None else max(0, round_no // GameConstants.PASSIVE_TITANIUM_INTERVAL - previous_round // GameConstants.PASSIVE_TITANIUM_INTERVAL)) * GameConstants.PASSIVE_TITANIUM_AMOUNT
    resource_gain = previous_resources is not None and resources > previous_resources and resources - previous_resources > passive_output
    final_storage: bool | None = None; positions = tuple(dict.fromkeys(route.cells[:2] + route.cells[-2:]))
    for position in positions:
        _, entity_type, _ = _visible(ct, position)
        if entity_type not in (EntityType.CONVEYOR, EntityType.SPLITTER): continue
        try: stored = ct.get_stored_resource(_visible(ct, position)[0]) is not None
        except Exception: continue
        if position == route.cells[-1]: final_storage = stored
    final_stored = bool(final_storage); storage_delivery = state.last_final_storage is True and final_storage is False; state.last_final_storage = final_storage
    output_blocked = final_storage is not None and final_stored and not resource_gain and not storage_delivery and elapsed_rounds > 0
    return storage_delivery, output_blocked


def _observe_route(ct: object, state: BuilderStateData, round_no: int) -> bool:
    if state.route is None: return False
    delivered, blocked_output = _route_health(ct, state, state.route, round_no)
    if delivered: state.last_delivery_round = round_no; state.backlog_rounds = 0; state.state = BuilderState.MAINTAIN; return True
    state.backlog_rounds = state.backlog_rounds + 1 if blocked_output else 0
    return False


def _world(ct: object, state: BuilderStateData) -> WorldMemory:
    width, height = int(ct.get_map_width()), int(ct.get_map_height()); fresh = state.world is None or (state.world.width, state.world.height) != (width, height); state.world = WorldMemory(width, height) if fresh else state.world; state.navigator = Navigator(width, height, state.world.is_navigation_blocked, cpu=ct.get_cpu_time_elapsed) if fresh else state.navigator; state.world.observe(ct); state.world.expire_dynamic(_round(ct)); return state.world


def _move(ct: object, state: BuilderStateData, goal: Position, actions: TurnActions, *, adjacent: bool = False) -> bool:
    world = state.world
    if world is None: return False
    if state.navigator is None: state.navigator = Navigator(world.width, world.height, world.is_navigation_blocked, cpu=ct.get_cpu_time_elapsed)
    current = _pos(ct)
    direction = state.navigator.next_direction_to_adjacent(current, goal, world.navigation_epoch, can_step=ct.can_move) if adjacent else state.navigator.next_direction_to_tile(current, goal, world.navigation_epoch, can_step=ct.can_move)
    if direction != Direction.CENTRE and actions.move(direction): state.blocked_steps = 0; return True
    state.blocked_steps += 1
    if state.blocked_steps >= 3:
        state.navigator.invalidate()
        for offset in range(4):
            direction = CARDINALS[(state.cursor + offset) % 4]
            if adjacent and current.add(direction) == goal:
                continue
            if actions.move(direction): state.cursor = (state.cursor + offset + 1) % 4; state.blocked_steps = 3; return True
    state.cursor = (state.cursor + 1) % 4; return False


def _expansion_ok(projected: int, harvester: int, route: int, budget: object, resources: int, *, concurrent_projects: int = 0) -> bool: return expansion_allowed(projected_output=projected, harvester_cost=harvester, route_cost=route, current_harvester_cost=harvester, construction_reserve=budget.construction, defense_reserve=budget.defense, ammo_reserve=budget.ammo, liquidity_reserve=budget.liquidity, available_resources=resources, concurrent_projects=concurrent_projects, max_projects=3)


def _route(ct: object, state: BuilderStateData, ore: Position, round_no: int) -> RoutePlan | None:
    world = state.world
    if world is None or world.own_core is None or not cpu_is_safe(ct): return state.route
    if state.route is not None and state.route.ore == ore and state.blocked_steps < 3: return state.route
    if round_no >= 850 and state.route is None and state.route_search is None: return state.route
    if state.navigator is not None: state.navigator.invalidate()
    try:
        conveyor_cost, harvester_cost, available_resources = max(0, int(ct.get_conveyor_cost())), max(0, int(ct.get_harvester_cost())), max(0, int(ct.get_global_resources()))
    except Exception: return state.route
    distance = abs(ore.x - world.own_core.x) + abs(ore.y - world.own_core.y); route_cost = estimate_route_cost(max(1, distance), conveyor_cost); active_projects = _active_project_count(ct, state); owns_route_reservation = state.project_count > 0; other_projects = max(0, active_projects - int(owns_route_reservation)); budget = compute_budget(ct, route_projects=active_projects if owns_route_reservation else active_projects + 1); projected_output = max(0, int((1000 - round_no) * 2.5))
    if estimate_payback_round(harvester_cost + route_cost, output_per_round=2.5, start_round=round_no, horizon=1000) is None: state.route_search = None; return state.route
    if not _expansion_ok(projected_output, harvester_cost, route_cost, budget, available_resources, concurrent_projects=other_projects) or (not owns_route_reservation and not _reserve_project(ct, state)): state.route_search = None; return state.route
    search = state.route_search if state.route_search is not None else {}
    planned = plan_core_outward_route(ore, world.core_footprint or {world.own_core}, world.width, world.height, world.is_route_planning_blocked, created_round=round_no, cpu_check=ct.get_cpu_time_elapsed, obstacle_epoch=world.layout_epoch, search_state=search)
    if planned is not None:
        exact_route_cost = estimate_route_cost(len(planned.cells), conveyor_cost)
        if estimate_payback_round(harvester_cost + exact_route_cost, output_per_round=2.5, start_round=round_no, horizon=1000) is None or not _expansion_ok(projected_output, harvester_cost, exact_route_cost, budget, available_resources, concurrent_projects=other_projects): _set_project(ct, state, ProjectState.FAILED, round_no); state.project_count, state.project_pending = 0, False; state.route_search = None; return state.route
        state.route, state.route_index, state.repair_index, state.blocked_steps, state.route_search = planned, len(planned.cells) - 1, None, 0, None; state.built_links.clear()
    elif not search.get("complete"): state.route_search = search
    else: _set_project(ct, state, ProjectState.FAILED, round_no); state.project_count, state.project_pending = 0, False; state.route_search = None
    return planned


def _build_route(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    route = state.route
    if route is None or state.route_index < 0: return False
    index, target, expected = state.route_index, route.cells[state.route_index], route.directions[state.route_index]
    if state.world is not None and state.world.is_route_planning_blocked(target): state.blocked_steps = 3; return False
    _, entity_type, direction = _visible(ct, target)
    if entity_type == EntityType.CONVEYOR and direction == expected: state.built_links[target], state.route_index = (entity_type, direction), index - 1; return True
    if _pos(ct).distance_squared(target) == 1:
        try:
            if not _can_spend(ct, int(ct.get_conveyor_cost()), projected_output=2.5, allow_late_completion=route.created_round < 850, state=state): return False
        except Exception: return False
        building_id = actions.build_conveyor(target, expected)
        if building_id is not None: state.built_links[target], state.route_index, state.state = (EntityType.CONVEYOR, expected), index - 1, BuilderState.VERIFY; return True
        return False
    return _move(ct, state, target, actions, adjacent=True)


def _verified(state: BuilderStateData, ct: object) -> bool: return state.route is not None and verify_route(state.route, _visible_route(state, ct, state.route))


def _harvester(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    if state.route is None or state.ore_target is None or not _verified(state, ct): return False
    round_no = _round(ct)
    _, entity_type, _ = _visible(ct, state.ore_target)
    if entity_type == EntityType.HARVESTER:
        state.delivery_started_round = state.delivery_started_round if state.delivery_started_round is not None else round_no
        if not _observe_route(ct, state, round_no) and state.last_delivery_round is None: state.state = BuilderState.DELIVER
        return True
    if _pos(ct).distance_squared(state.ore_target) != 1: return _move(ct, state, state.ore_target, actions, adjacent=True)
    try: harvester_cost = int(ct.get_harvester_cost())
    except Exception: return False
    if not _can_spend(ct, harvester_cost, projected_output=2.5, allow_late_completion=round_no >= 850, state=state): return False
    if actions.build_harvester(state.ore_target) is not None: _set_project(ct, state, ProjectState.DELIVERING, round_no); state.project_count, state.project_pending, state.delivery_started_round, state.last_resource_total, state.last_resource_round, state.state = 1, False, round_no, None, None, BuilderState.DELIVER; return True
    return False


def _repair(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    route = state.route
    if route is None: return False
    round_no = _round(ct)
    backlog_due = state.backlog_rounds >= 3; delivered = _observe_route(ct, state, round_no); backlog_due = backlog_due and not delivered
    reference_round = state.last_delivery_round if state.last_delivery_round is not None else state.delivery_started_round; timeout_due = reference_round is not None and round_no - reference_round >= 12
    broken = find_broken_link(route, _visible_route(state, ct, route), current_round=round_no, last_delivery_round=state.last_delivery_round, route_start_round=state.delivery_started_round, blocked_output=backlog_due or state.backlog_rounds >= 3)
    if broken is None:
        if state.last_delivery_round is not None or state.state == BuilderState.MAINTAIN: state.state = BuilderState.MAINTAIN
        return False
    state.repair_index, target, expected = broken, route.cells[broken], route.directions[broken]
    entity_id, entity_type, direction = _visible(ct, target)
    try: friendly = entity_id is not None and ct.get_team(entity_id) == ct.get_team()
    except Exception: friendly = False
    if entity_type is not None and (entity_type != EntityType.CONVEYOR or direction != expected):
        if _pos(ct).distance_squared(target) == 1: return actions.destroy(target) if friendly and teardown_allowed(verified_misdirected=True) else False
        return _move(ct, state, target, actions, adjacent=True)
    if (backlog_due or timeout_due) and entity_type == EntityType.CONVEYOR and direction == expected:
        if _pos(ct).distance_squared(target) == 1: return actions.destroy(target) if friendly and teardown_allowed(verified_obsolete=True) else False
        return _move(ct, state, target, actions, adjacent=True)
    if _pos(ct).distance_squared(target) == 1:
        try:
            if not _can_spend(ct, int(ct.get_conveyor_cost()), projected_output=2.5, allow_late_completion=True, state=state): return False
        except Exception: return False
        if actions.build_conveyor(target, expected) is not None: state.built_links[target], state.repair_index, state.state = (EntityType.CONVEYOR, expected), None, BuilderState.DELIVER; state.delivery_started_round, state.backlog_rounds = round_no, 0; return True
        return False
    return _move(ct, state, target, actions, adjacent=True)


def _core_exit_tiles(world: WorldMemory) -> frozenset[Position]:
    footprint = set(world.core_footprint); exits: set[Position] = set()
    for cell in sorted(footprint, key=lambda pos: (pos.y, pos.x)):
        for direction in CARDINALS:
            position = cell.add(direction)
            if 0 <= position.x < world.width and 0 <= position.y < world.height and position not in footprint: exits.add(position)
    return frozenset(exits)


def _legal_escape_tiles(ct: object, current: Position) -> frozenset[Position]:
    escapes: set[Position] = set()
    for direction in CARDINALS:
        try:
            escapes.update((current.add(direction),) if ct.can_move(direction) else ())
        except Exception: continue
    return frozenset(escapes)


def _exposed_route_join(world: WorldMemory, route: RoutePlan, threat: object | None) -> Position | None:
    route_cells = set(route.cells)
    for cell in route.cells:
        if threat is not None:
            try:
                if cell.distance_squared(threat.position) <= 4: return cell
            except Exception: pass
        for direction in CARDINALS:
            neighbour = cell.add(direction)
            if neighbour in world.static_walls or ((neighbour.x == 0 or neighbour.y == 0 or neighbour.x == world.width - 1 or neighbour.y == world.height - 1) and neighbour not in route_cells):
                return cell
    return None


def _bounded_disjoint_branch(ct: object, world: WorldMemory, route: RoutePlan, start: Position, join: Position) -> tuple[Position, ...]:
    route_cells = set(route.cells); blocked = set(world.core_footprint) | set(world.static_walls) | (route_cells - {join}); blocked.update(position for position in world.dynamic if world.is_blocked(position) and position != join)
    try:
        branch = bounded_bfs(start, join, world.width, world.height, blocked, max_expansions=world.width * world.height, cpu_check=ct.get_cpu_time_elapsed)
    except Exception: return ()
    if len(branch) < 2 or len(branch) - 1 > 12 or branch[-1] != join: return ()
    return tuple(branch) if set(branch[:-1]).isdisjoint(route_cells) else ()


def _build_redundancy_branch(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    branch = state.redundancy_branch
    if not branch or state.redundancy_index < 0: return False
    join_index = len(branch) - 1
    if state.redundancy_index + 1 >= join_index: state.redundancy_branch = (); state.redundancy_index = -1; state.redundancy_join = None; return False
    index = state.redundancy_index
    current_target = branch[index + 1]
    expected = branch[index].cardinal_direction_to(current_target)
    if expected == Direction.CENTRE: state.redundancy_branch = (); state.redundancy_index = -1; state.redundancy_join = None; return False
    _, entity_type, direction = _visible(ct, current_target)
    if entity_type == EntityType.CONVEYOR and direction == expected: state.redundancy_index += 1; return True
    if _pos(ct).distance_squared(current_target) != 1: return _move(ct, state, current_target, actions, adjacent=True)
    try: conveyor_cost = int(ct.get_conveyor_cost())
    except Exception: return False
    if not _can_spend(ct, conveyor_cost, projected_output=2.5, allow_late_completion=True, state=state): return False
    if actions.build_conveyor(current_target, expected) is None: return False
    state.built_links[current_target] = (EntityType.CONVEYOR, expected); state.redundancy_index += 1
    if state.redundancy_index + 1 >= join_index: state.redundancy_branch = (); state.redundancy_index = -1; state.redundancy_join = None
    return True


def _defend(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    if not cpu_is_safe(ct): return False
    try:
        current = _pos(ct); positions = tuple(position for position in (current.add(direction) for direction in CARDINALS) if ct.is_tile_empty(position)); threat = next(iter(state.world.threat_list(_round(ct))), None) if state.world else None
        if threat is None: return False
        assessed = assess_threat(position=threat.position, enemy_builder_distance=max(0, int(current.distance_squared(threat.position) ** 0.5)), firing_line=threat.kind == ThreatKind.FIRING_LINE, sabotage=threat.kind == ThreatKind.SABOTAGE, current_round=_round(ct), entity_type=threat.entity_type)
        if assessed is not None: threat = assessed
        attackable_by_type: dict[EntityType, dict[tuple[Position, Direction], int]] = {EntityType.GUNNER: {}, EntityType.SENTINEL: {}}; wall_crossing = False
        for turret_type in (EntityType.GUNNER, EntityType.SENTINEL):
            for position in positions:
                for direction in CARDINALS:
                    if not cpu_is_safe(ct): return False
                    try: tiles = tuple(ct.get_attackable_tiles_from(position, direction, turret_type))[:32]
                    except Exception: tiles = ()
                    legal = 0
                    for target in tiles:
                        try:
                            legal += bool(ct.can_fire_from(position, direction, turret_type, target)); wall_crossing = wall_crossing or ct.get_tile_env(target) == Environment.WALL
                        except Exception: pass
                    attackable_by_type[turret_type][position, direction] = legal
    except Exception: return False
    lane_length = max((max(values.values(), default=0) for values in attackable_by_type.values()), default=0)
    if lane_length <= 0: return False
    turret_type = choose_turret_type(lane_length=lane_length, wall_crossing=wall_crossing, durable_anchor=bool(state.route and len(state.route.cells) >= 8), changing_corridor=not wall_crossing, threat_score=threat.score)
    if max(attackable_by_type[turret_type].values(), default=0) <= 0:
        available = tuple(candidate for candidate in (EntityType.SENTINEL, EntityType.GUNNER) if max(attackable_by_type[candidate].values(), default=0) > 0)
        if not available: return False
        turret_type = max(available, key=lambda candidate: (max(attackable_by_type[candidate].values(), default=0), int(candidate == EntityType.SENTINEL)))
    world = state.world
    escape_tiles = _legal_escape_tiles(ct, current)
    if len(escape_tiles) > 1: escape_tiles = frozenset()
    choice = choose_defensive_build(positions, threat=threat, lane_length=lane_length, wall_crossing=wall_crossing if turret_type == EntityType.SENTINEL else False, changing_corridor=turret_type == EntityType.GUNNER, durable_anchor=(bool(state.route and len(state.route.cells) >= 8) if turret_type == EntityType.SENTINEL else False), reserved_core_exits=_core_exit_tiles(world) if world else frozenset(), route_cells=set(state.route.cells) if state.route else frozenset(), escape_tiles=escape_tiles, attackable=attackable_by_type[turret_type])
    if choice is None: return False
    position, entity_type, direction, _ = choice
    if entity_type != turret_type or attackable_by_type[entity_type].get((position, direction), 0) <= 0: return False
    try:
        cost = ct.get_sentinel_cost() if entity_type == EntityType.SENTINEL else ct.get_gunner_cost()
    except Exception: return False
    immediate_loss = threat.position.distance_squared(current) <= 4 and _round(ct) >= 850
    if not _can_spend(ct, cost, preserve_defense=True, emergency=immediate_loss, projected_output=threat.score, state=state, new_project=True): return False
    return (actions.build_sentinel(position, direction) if entity_type == EntityType.SENTINEL else actions.build_gunner(position, direction)) is not None


def _support_build(ct: object, state: BuilderStateData, actions: TurnActions, round_no: int) -> bool:
    world, route = state.world, state.route
    if world is None or not cpu_is_safe(ct): return False
    try:
        current = _pos(ct); positions = tuple(position for position in (current.add(direction) for direction in CARDINALS) if ct.is_tile_empty(position))
    except Exception: return False
    if _build_redundancy_branch(ct, state, actions): return True
    reserved = set(world.core_footprint) | _core_exit_tiles(world) | (set(route.cells) if route else set()); choices = tuple(position for position in positions if position not in reserved)
    if not choices: return False
    threat = next(iter(world.threat_list(round_no)), None)
    if state.role == Role.REPAIR and route is not None and state.route_index < 0 and _verified(state, ct):
        try:
            splitter_cost, conveyor_cost = int(ct.get_splitter_cost()), int(ct.get_conveyor_cost())
        except Exception: return False
        mature, join = state.last_delivery_round is not None or state.state == BuilderState.MAINTAIN, _exposed_route_join(world, route, threat)
        if mature and join is not None:
            for target in sorted(choices, key=lambda position: (position.y, position.x)):
                if not cpu_is_safe(ct): break
                branch = _bounded_disjoint_branch(ct, world, route, target, join)
                if not branch: continue
                branch_length = len(branch) - 1; branch_cost = branch_length * max(0, conveyor_cost); avoided_output = max(0.0, (1000 - round_no) * max(1, route.expected_output) * 0.25)
                justified = splitter_redundancy_justified(0.75 if threat is not None else 0.5, avoided_output, splitter_cost, branch_cost, float(branch_length), mature_route=True, exposed_segment=True, disjoint_branch=set(branch[:-1]).isdisjoint(set(route.cells)) and branch[-1] == join, branch_length=branch_length)
                if not justified or not _can_spend(ct, splitter_cost, projected_output=avoided_output, state=state, new_project=True): continue
                direction = branch[0].cardinal_direction_to(branch[1])
                if direction == Direction.CENTRE: continue
                if actions.build_splitter(target, direction) is not None: state.redundancy_branch, state.redundancy_index, state.redundancy_join = branch, 0, join; return True
    if state.role == Role.DEFENDER and threat is not None and threat.position.distance_squared(current) <= 4:
        try:
            barrier_cost = int(ct.get_barrier_cost())
        except Exception: return False
        escape_tiles = _legal_escape_tiles(ct, current)
        if len(escape_tiles) <= 1: return False
        barrier_target = min(choices, key=lambda position: (position.y, position.x))
        if _can_spend(ct, barrier_cost, preserve_defense=True, emergency=round_no >= 850, projected_output=threat.score, state=state, new_project=True): return actions.build_barrier(barrier_target) is not None
    if state.role == Role.SIEGE and round_no < 850 and _fresh_verified_rally(ct, state, world, round_no):
        try:
            launcher_cost = int(ct.get_launcher_cost())
        except Exception: return False
        if _can_spend(ct, launcher_cost, projected_output=2.5, state=state, new_project=True): return actions.build_launcher(min(choices, key=lambda position: (position.y, position.x))) is not None
    return False


def _raid(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    if _round(ct) >= 850: return False
    try:
        own_team, current, targets = ct.get_team(), _pos(ct), []
        for entity_id in tuple(ct.get_nearby_buildings())[:32]:
            if ct.get_team(entity_id) == own_team: continue
            position, entity_type = ct.get_position(entity_id), ct.get_entity_type(entity_id)
            if current.distance_squared(position) == 1: targets.append((position, entity_type, bool(ct.get_stored_resource(entity_id)), 0))
    except Exception: return False
    if not targets: return False
    try:
        budget, resources = compute_budget(ct, route_projects=1), int(ct.get_global_resources())
    except Exception: return False
    economy_reserve = budget.construction + budget.defense + budget.ammo + budget.liquidity
    choice = choose_raid_action(tuple(targets), resources=resources, economy_reserve=economy_reserve, attack_cost=GameConstants.BUILDER_BOT_ATTACK_COST)
    if choice is None: return False
    position, score = choice
    if not _can_spend(ct, GameConstants.BUILDER_BOT_ATTACK_COST, projected_output=score, state=state): return False
    return actions.fire(position)


def _scout(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    if (world := state.world) is None: return False
    target = world.enemy_core or nearest_position(_pos(ct), world.known_ore())
    if target is None: target = (Position(0, 0), Position(max(0, world.width - 1), 0), Position(0, max(0, world.height - 1)))[state.cursor % 3]
    return _move(ct, state, target, actions)


def run_builder(ct: object, state: BuilderStateData | None = None) -> BuilderStateData:
    state = state or BuilderStateData()
    world, round_no = _world(ct, state), _round(ct)
    if state.role == Role.SCOUT and state.last_position is None: state.role = assign_role(_id(ct))
    _read_rally(ct, state)
    if state.rally_target is not None and not _fresh_verified_rally(ct, state, world, round_no): state.rally_target, state.rally_expires_epoch = None, 0
    target = _claim(ct, state, world, round_no)
    _publish_rally(ct, state, world, round_no)
    try:
        resources = int(ct.get_global_resources()); harvester_count = sum(1 for entity_id in tuple(ct.get_nearby_buildings())[:64] if ct.get_entity_type(entity_id) == EntityType.HARVESTER)
    except Exception: resources, harvester_count = 0, 0
    priorities = late_game_policy(round_no, delivery_due=state.state in (BuilderState.DELIVER, BuilderState.VERIFY), route_repair_due=state.repair_index is not None or state.backlog_rounds >= 3, harvester_payback_positive=target is not None, stored_titanium=resources, collected_titanium=state.last_delivery_round or 0, harvester_count=harvester_count)
    actions = TurnActions(ct)
    if target is not None:
        if state.route is not None and state.blocked_steps >= 3: _reset_route_search(state)
        if state.route is None:
            if round_no < 850 or state.route_search is not None: state.state = next_harvester_state(state.state); _route(ct, state, target, round_no)
        if state.route is not None and state.route_index >= 0:
            state.state = BuilderState.ROUTE; _build_route(ct, state, actions)
        elif state.route is not None:
            if _repair(ct, state, actions): state.last_position = _pos(ct); return state
            _harvester(ct, state, actions)
        state.last_position = _pos(ct); return state
    if state.route is not None and state.route_index < 0:
        if _repair(ct, state, actions): state.last_position = _pos(ct); return state
        if state.state in (BuilderState.DELIVER, BuilderState.VERIFY) and _harvester(ct, state, actions): state.last_position = _pos(ct); return state
    if state.role == Role.DEFENDER and round_no >= 240 and (round_no < 850 or "defense" in priorities):
        threats = world.threat_list(round_no); close_threat = bool(threats and threats[0].position.distance_squared(_pos(ct)) <= 4)
        if close_threat and _support_build(ct, state, actions, round_no): state.last_position = _pos(ct); return state
        if _defend(ct, state, actions): state.last_position = _pos(ct); return state
    if _support_build(ct, state, actions, round_no): state.last_position = _pos(ct); return state
    if state.role in (Role.RAIDER, Role.SIEGE) and "no_paid_attack" not in priorities and _raid(ct, state, actions): state.last_position = _pos(ct); return state
    _scout(ct, state, actions); state.last_position = _pos(ct); return state
