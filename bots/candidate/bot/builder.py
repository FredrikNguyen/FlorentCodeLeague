from __future__ import annotations

from dataclasses import dataclass, field

from fcode import Direction, EntityType, Environment, GameConstants, Position

from .actions import CARDINALS, TurnActions, cpu_is_safe
from .comms import PROJECT_COUNT, Slot, assignment_is_fresh, decode_alert, decode_global_strategy, epoch_distance, read_assignment, read_project, read_shared_threat, write_project
from .core import compute_budget
from .defense import assess_threat, choose_defensive_build, choose_turret_type
from .economy import MAX_HEALTHY_ROUTES, claim_should_release, estimate_payback_round, estimate_route_cost, expansion_allowed, next_harvester_state, rank_ore_projects, score_ore
from .feature_flags import ENABLE_DEFENSIVE_BUILDING, ENABLE_FORWARD_GUNNERS, ENABLE_LAUNCHERS, ENABLE_PHASE_STRATEGY, ENABLE_RAIDS, ENABLE_REDUNDANCY, ENABLE_SECONDARY_EXPANSION
from .logistics import find_broken_link, plan_core_outward_route, teardown_allowed, verify_route
from .navigation import Navigator
from .offense import choose_attack_stance, choose_forward_turret_site, choose_forward_turret_type, choose_offensive_target, choose_raid_action, enemy_target_from_observation, publish_verified_enemy_core, target_is_enemy_building, try_builder_attack
from .policy import assign_role, choose_work_intent, late_game_policy
from .types import BuilderState, EnemyTarget, OffenseState, ProjectState, Role, RoutePlan, StrategyPhase, ThreatKind, WorkIntent
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
    redundancy_branch: tuple[Position, ...] = (); redundancy_index: int = -1; redundancy_join: Position | None = None; project_count: int = 0; project_pending: bool = False; route_replans: int = 0; repair_attempts: int = 0; route_failure_reason: str | None = None
    offense_state: OffenseState = OffenseState.IDLE; offense_target: EnemyTarget | None = None; offense_epoch: int = 0; last_offense_progress_round: int = 0; paid_attacks: int = 0; retreat_reason: str | None = None
    work_intent: WorkIntent = WorkIntent.DISCOVER_ORE; intent_round: int = -1
    explored_tiles: set[Position] = field(default_factory=set); frontier_target: Position | None = None
    patrol_target: Position | None = None; patrol_cursor: int = 0; patrol_repair_target: Position | None = None


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
    return [(index, assignment, read_project(ct, index)) for index in range(PROJECT_COUNT) if (assignment := read_assignment(ct, index)) is not None]


def _active_project_count(ct: object, state: BuilderStateData | None = None) -> int:
    active = sum(1 for index in range(PROJECT_COUNT) if (project := read_project(ct, index)) is not None and project.state not in (ProjectState.IDLE, ProjectState.FAILED)); local = int(state is not None and bool(state.project_count or state.route_search is not None or state.route_index >= 0 or state.redundancy_branch)); return min(MAX_HEALTHY_ROUTES, max(active, local))


def _reserve_project(ct: object, state: BuilderStateData, *, wait_visible: bool = False) -> bool:
    if state.claim_slot is None: return False
    round_no = _round(ct); project = read_project(ct, state.claim_slot)
    if state.project_pending:
        visible = project is not None and project.epoch == (state.claim_epoch & 63) and project.state not in (ProjectState.IDLE, ProjectState.FAILED)
        state.project_pending = not visible; return visible
    if project is not None and project.state not in (ProjectState.IDLE, ProjectState.FAILED): state.project_count = max(1, state.project_count); return True
    if _active_project_count(ct, state) >= MAX_HEALTHY_ROUTES: return False
    if not write_project(ct, state.claim_slot, state.ore_target, round_no & 63, ProjectState.CLAIMED, int(ct.get_map_width()), int(ct.get_map_height()), writer=state.claim_slot): return False
    state.project_count, state.project_pending, state.claim_epoch = 1, True, round_no & 63
    return False


def _ore_is_valid(ct: object, world: WorldMemory, position: Position | None) -> bool: return position is not None and 0 <= position.x < world.width and 0 <= position.y < world.height and (position in world.ore_positions or ct.get_tile_env(position) == Environment.ORE_TITANIUM)


def _reset_route_search(state: BuilderStateData) -> None:
    state.route_search = None; state.route = None; state.route_index = -1; state.repair_index = None; state.last_final_storage = None; state.redundancy_branch = (); state.redundancy_index = -1; state.redundancy_join = None; state.repair_attempts = 0


def _project_status(state: BuilderStateData) -> ProjectState:
    return ProjectState.IDLE if state.project_count <= 0 and state.ore_target is None and state.route is None and state.route_search is None and not state.redundancy_branch else ProjectState.MAINTAIN if state.last_delivery_round is not None or state.state == BuilderState.MAINTAIN else ProjectState.DELIVERING if state.state == BuilderState.DELIVER else ProjectState.VERIFYING if state.state == BuilderState.VERIFY or state.route is not None and state.route_index < 0 else ProjectState.BUILDING if state.route is not None else ProjectState.PLANNING if state.route_search is not None else ProjectState.CLAIMED


def _set_project(ct: object, state: BuilderStateData, status: ProjectState, round_no: int) -> None:
    if state.claim_slot is not None: write_project(ct, state.claim_slot, state.ore_target, round_no & 63, status, int(ct.get_map_width()), int(ct.get_map_height()), writer=state.claim_slot)


def _fail_route(ct: object, state: BuilderStateData, reason: str, round_no: int, *, replan: bool = False) -> None:
    state.route_failure_reason, state.route_replans = reason, state.route_replans + 1; status = ProjectState.PLANNING if replan and state.route_replans < 3 else ProjectState.FAILED; _reset_route_search(state); state.project_count = 0 if status == ProjectState.FAILED else state.project_count; _set_project(ct, state, status, round_no)


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
        publish_verified_enemy_core(ct, world.enemy_core)
    except Exception: pass


def _can_spend(ct: object, cost: int, *, preserve_defense: bool = False, projected_output: float | None = None, allow_late_completion: bool = False, emergency: bool = False, near_term_core_kill: bool = False, state: BuilderStateData | None = None, new_project: bool = False) -> bool: return _can_spend_with_policy(ct, cost, preserve_defense=preserve_defense, projected_output=projected_output, allow_late_completion=allow_late_completion, emergency=emergency, near_term_core_kill=near_term_core_kill, state=state, new_project=new_project)


def _can_spend_with_policy(ct: object, cost: int, *, preserve_defense: bool = False, projected_output: float | None = None, allow_late_completion: bool = False, emergency: bool = False, near_term_core_kill: bool = False, state: BuilderStateData | None = None, new_project: bool = False) -> bool:
    try:
        round_no, resources = _round(ct), int(ct.get_global_resources()); active_projects = _active_project_count(ct, state); own_project = int(state is not None and bool(state.project_count or state.route_search is not None or state.route_index >= 0 or state.redundancy_branch)); budget = compute_budget(ct, route_projects=max(0, active_projects - own_project) + int(new_project))
    except Exception:
        return False
    cost = max(0, int(cost))
    if cost <= 0 or new_project and state is not None and state.claim_slot is not None and active_projects >= MAX_HEALTHY_ROUTES or round_no >= 850 and not (allow_late_completion or emergency or near_term_core_kill) or projected_output is not None and float(projected_output) <= 0: return False
    protected = budget.construction + budget.ammo + budget.liquidity + (0 if emergency else budget.defense)
    if resources < cost + protected: return False
    if emergency or near_term_core_kill:
        return not new_project or state is None or state.claim_slot is None or _reserve_project(ct, state, wait_visible=True)
    if estimate_payback_round(cost, output_per_round=2.5, start_round=round_no, horizon=1000) is None: return False
    return not new_project or state is None or state.claim_slot is None or _reserve_project(ct, state, wait_visible=True)


def _claim(ct: object, state: BuilderStateData, world: WorldMemory, round_no: int):
    claims = _read_claims(ct, world.width, world.height)
    own = next(((index, assignment, project) for index, assignment, project in claims if assignment.owner_id == _id(ct)), None)
    if own is None:
        if state.claim_slot is not None: claim_should_release(False, 0, 31, True); state.claim_slot, state.ore_target = None, None; _reset_route_search(state)
        return None
    state.claim_slot, assignment, project = own
    if not ENABLE_SECONDARY_EXPANSION and state.claim_slot != 0: state.ore_target = None; return None
    target = project.position if project is not None else None; heartbeat = project.epoch if project is not None and project.state != ProjectState.IDLE else assignment.generation; age = epoch_distance(round_no & 63, heartbeat); valid_ore = target is None or _ore_is_valid(ct, world, target)
    # A delayed assignment may expose a CLAIMED project before Core has an
    # ore target to publish. It is a reservation, not yet a productive route
    # owner, so keep this Builder eligible for discovery.
    if project is not None and project.state not in (ProjectState.IDLE, ProjectState.FAILED) and project.position is not None:
        state.project_count = max(1, state.project_count); state.project_pending = False
    failed = project is not None and project.state == ProjectState.FAILED
    assignment_live = assignment_is_fresh(assignment, round_no & 63) or (project is not None and project.state not in (ProjectState.IDLE, ProjectState.FAILED) and age <= 31)
    if not assignment_live or claim_should_release(valid_ore, age, 31, False) or failed:
        state.claim_slot, state.ore_target = None, None; _reset_route_search(state); return None
    lower_owner = next((index for index, other_assignment, other_project in claims if index < state.claim_slot and other_project is not None and other_project.position == target and (assignment_is_fresh(other_assignment, round_no & 63) or other_project.state not in (ProjectState.IDLE, ProjectState.FAILED))), None) if target is not None else None
    if lower_owner is not None:
        target = None
        state.ore_target = None
        state.project_count, state.project_pending = 0, False
    if target is not None and lower_owner is None: state.ore_target = target; _publish_owner_state(ct, state, world, round_no); return target
    claimed = {other_project.position for index, other_assignment, other_project in claims if index != state.claim_slot and other_project is not None and other_project.position is not None and assignment_is_fresh(other_assignment, round_no & 63)}
    candidates = [position for position in world.known_ore() if position not in claimed]
    if not candidates:
        try:
            candidates = [tile for tile in ct.get_nearby_tiles() if tile not in claimed and ct.get_tile_env(tile) == Environment.ORE_TITANIUM]
        except Exception: candidates = []
    if not candidates:
        if state.claim_slot is not None:
            write_project(ct, state.claim_slot, None, round_no & 63, ProjectState.IDLE, world.width, world.height, writer=state.claim_slot)
        return None
    origin = _pos(ct)
    try:
        ranked = rank_ore_projects(candidates, origin=origin, claimed=claimed, round_no=round_no, conveyor_cost=int(ct.get_conveyor_cost()), harvester_cost=int(ct.get_harvester_cost()), scale_percent=int(ct.get_scale_percent()), min_margin=0)
    except Exception:
        ranked = ()
    if ranked:
        candidates = [estimate.position for estimate in ranked]
    else:
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


def _friendly(ct: object, entity_id: int | None) -> bool:
    if entity_id is None: return False
    try: return ct.get_team(entity_id) == ct.get_team()
    except Exception: return False


def _visible_route(state: BuilderStateData, ct: object, route: RoutePlan):
    def get(position: Position):
        _, entity_type, direction = _visible(ct, position)
        if entity_type is None:
            try: return state.built_links.get(position) if not ct.is_in_vision(position) else (entity_type, direction)
            except Exception: return state.built_links.get(position)
        return entity_type, direction

    return get


def _route_health(ct: object, state: BuilderStateData, route: RoutePlan, round_no: int) -> tuple[bool, bool]:
    previous_round = state.last_resource_round; state.last_resource_round = round_no; state.last_resource_total = None
    final_id: int | None = None; final = route.cells[-1] if route.cells else None
    if final is not None:
        entity_id, entity_type, _ = _visible(ct, final)
        if entity_type in (EntityType.CONVEYOR, EntityType.SPLITTER) and _friendly(ct, entity_id):
            try: final_id = ct.get_stored_resource_id(entity_id)
            except Exception:
                try: final_id = int(ct.get_stored_resource(entity_id)) if ct.get_stored_resource(entity_id) is not None else None
                except Exception: final_id = None
    final_stored = final_id is not None; storage_delivery = state.last_final_storage is True and not final_stored; state.last_final_storage = final_stored
    elapsed_rounds = 0 if previous_round is None else max(0, round_no - previous_round)
    return storage_delivery, bool(final_stored and elapsed_rounds > 0 and not storage_delivery)


def _observe_route(ct: object, state: BuilderStateData, round_no: int) -> bool:
    if state.route is None: return False
    delivered, blocked_output = _route_health(ct, state, state.route, round_no)
    if delivered: state.last_delivery_round = round_no; state.backlog_rounds = 0; state.repair_attempts = 0; state.state = BuilderState.MAINTAIN; _set_project(ct, state, ProjectState.MAINTAIN, round_no); return True
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
    if adjacent and direction == Direction.CENTRE: state.blocked_steps += 1; return False
    if direction != Direction.CENTRE and not (not adjacent and state.ore_target is None and current.add(direction) in world.ore_positions) and actions.move(direction): state.blocked_steps = 0; return True
    state.blocked_steps += 1
    if state.blocked_steps >= 3:
        state.navigator.invalidate()
        for offset in range(4):
            direction = CARDINALS[(state.cursor + offset) % 4]
            if adjacent and current.add(direction) == goal or not adjacent and state.ore_target is None and current.add(direction) in world.ore_positions:
                continue
            if actions.move(direction): state.cursor = (state.cursor + offset + 1) % 4; state.blocked_steps = 3; return True
    state.cursor = (state.cursor + 1) % 4; return False


def _expansion_ok(projected: int, harvester: int, route: int, budget: object, resources: int, *, concurrent_projects: int = 0) -> bool: return expansion_allowed(projected_output=projected, harvester_cost=harvester, route_cost=route, current_harvester_cost=harvester, construction_reserve=budget.construction, defense_reserve=budget.defense, ammo_reserve=budget.ammo, liquidity_reserve=budget.liquidity, available_resources=resources, concurrent_projects=concurrent_projects, max_projects=MAX_HEALTHY_ROUTES)


def _route(ct: object, state: BuilderStateData, ore: Position, round_no: int) -> RoutePlan | None:
    world = state.world
    if world is None or world.own_core is None or not cpu_is_safe(ct) or (not ENABLE_SECONDARY_EXPANSION and state.claim_slot not in (None, 0)): return state.route
    if state.route is not None and state.route.ore == ore and state.blocked_steps < 3: return state.route
    if round_no >= 850 and state.route is None and state.route_search is None: return state.route
    if state.navigator is not None: state.navigator.invalidate()
    try:
        conveyor_cost, harvester_cost, available_resources = max(0, int(ct.get_conveyor_cost())), max(0, int(ct.get_harvester_cost())), max(0, int(ct.get_global_resources()))
    except Exception: return state.route
    distance = abs(ore.x - world.own_core.x) + abs(ore.y - world.own_core.y); route_cost = estimate_route_cost(max(1, distance), conveyor_cost); active_projects = _active_project_count(ct, state); owns_route_reservation = state.project_count > 0; other_projects = max(0, active_projects - int(owns_route_reservation)); budget = compute_budget(ct, route_projects=active_projects if owns_route_reservation else active_projects + 1); projected_output = max(0, int((1000 - round_no) * 2.5))
    if estimate_payback_round(harvester_cost + route_cost, output_per_round=2.5, start_round=round_no, horizon=1000) is None: state.route_failure_reason = "payback"; _set_project(ct, state, ProjectState.FAILED, round_no); state.route_search = None; return state.route
    if not _expansion_ok(projected_output, harvester_cost, route_cost, budget, available_resources, concurrent_projects=other_projects) or (not owns_route_reservation and not _reserve_project(ct, state)): state.route_search = None; return state.route
    if state.route_search is None: _set_project(ct, state, ProjectState.PLANNING, round_no)
    search = state.route_search if state.route_search is not None else {}
    def route_blocked(position: Position) -> bool:
        if world.is_route_planning_blocked(position): return True
        try: builder_id = ct.get_tile_builder_bot_id(position)
        except Exception: builder_id = None
        if builder_id is not None: return not _friendly(ct, builder_id)
        entity_id, _, _ = _visible(ct, position)
        return entity_id is not None and not _friendly(ct, entity_id)
    planned = plan_core_outward_route(ore, world.core_footprint or {world.own_core}, world.width, world.height, route_blocked, created_round=round_no, cpu_check=ct.get_cpu_time_elapsed, obstacle_epoch=world.layout_epoch, search_state=search)
    if planned is not None:
        exact_route_cost = estimate_route_cost(len(planned.cells), conveyor_cost)
        if estimate_payback_round(harvester_cost + exact_route_cost, output_per_round=2.5, start_round=round_no, horizon=1000) is None or not _expansion_ok(projected_output, harvester_cost, exact_route_cost, budget, available_resources, concurrent_projects=other_projects): _set_project(ct, state, ProjectState.FAILED, round_no); state.project_count, state.project_pending = 0, False; state.route_search = None; return state.route
        state.route, state.route_index, state.repair_index, state.blocked_steps, state.route_search, state.route_failure_reason = planned, len(planned.cells) - 1, None, 0, None, None; state.built_links.clear(); _set_project(ct, state, ProjectState.BUILDING, round_no)
    elif not search.get("complete"): state.route_search = search
    else: _set_project(ct, state, ProjectState.FAILED, round_no); state.project_count, state.project_pending = 0, False; state.route_search = None
    return planned


def _build_route(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    route = state.route
    if route is None or state.route_index < 0: return False
    index, target, expected = state.route_index, route.cells[state.route_index], route.directions[state.route_index]
    try: builder_id = ct.get_tile_builder_bot_id(target)
    except Exception: builder_id = None
    if builder_id is not None and builder_id != _id(ct):
        if _friendly(ct, builder_id):
            state.route_failure_reason = "transient_builder_occupancy"; state.blocked_steps += 1
            if state.blocked_steps >= 3:
                _fail_route(ct, state, "transient_builder_occupancy", _round(ct), replan=True); state.blocked_steps = 0
            return False
        state.route_replans += 1; state.route_failure_reason = "occupied_enemy"; _reset_route_search(state); _set_project(ct, state, ProjectState.FAILED if state.route_replans >= 3 else ProjectState.PLANNING, _round(ct)); return False
    entity_id, entity_type, direction = _visible(ct, target); friendly = _friendly(ct, entity_id)
    if entity_type == EntityType.CONVEYOR and direction == expected and friendly:
        state.built_links[target], state.route_index, state.blocked_steps = (entity_type, direction), index - 1, 0; state.state = BuilderState.VERIFY if index == 0 else BuilderState.ROUTE; _set_project(ct, state, ProjectState.VERIFYING if index == 0 else ProjectState.BUILDING, _round(ct)); return True
    if entity_id is not None and not friendly:
        state.route_replans += 1; state.route_failure_reason = "occupied_enemy"; _reset_route_search(state); _set_project(ct, state, ProjectState.FAILED if state.route_replans >= 3 else ProjectState.PLANNING, _round(ct)); return False
    if state.world is not None and state.world.is_route_planning_blocked(target):
        state.route_replans += 1; state.route_failure_reason = "permanent_obstacle"; _reset_route_search(state); _set_project(ct, state, ProjectState.FAILED if state.route_replans >= 3 else ProjectState.PLANNING, _round(ct)); return False
    if entity_id is not None:
        if entity_type != EntityType.CONVEYOR: _fail_route(ct, state, "occupied_friendly", _round(ct), replan=True); return False
        if _pos(ct).distance_squared(target) != 1: return _move(ct, state, target, actions, adjacent=True)
        if actions.destroy(target): state.repair_attempts += 1; state.blocked_steps = 0; return True
        state.blocked_steps += 1; return False
    if _pos(ct).distance_squared(target) == 1:
        try:
            if not _can_spend(ct, int(ct.get_conveyor_cost()), projected_output=2.5, allow_late_completion=route.created_round < 850, state=state): return False
        except Exception: return False
        building_id = actions.build_conveyor(target, expected)
        if building_id is not None:
            state.built_links[target], state.route_index, state.state, state.blocked_steps, state.route_failure_reason = (EntityType.CONVEYOR, expected), index - 1, BuilderState.VERIFY if index == 0 else BuilderState.ROUTE, 0, None; _set_project(ct, state, ProjectState.VERIFYING if index == 0 else ProjectState.BUILDING, _round(ct)); return True
        state.blocked_steps += 1
        if state.blocked_steps >= 3: state.route_failure_reason = "build_denied"; state.route_replans += 1; _reset_route_search(state); _set_project(ct, state, ProjectState.FAILED, _round(ct))
        return False
    return _move(ct, state, target, actions, adjacent=True)


def _verified(state: BuilderStateData, ct: object) -> bool:
    if state.route is None or not verify_route(state.route, _visible_route(state, ct, state.route)): return False
    for cell in state.route.cells:
        entity_id, entity_type, _ = _visible(ct, cell)
        if entity_id is None and cell in state.built_links: continue
        if entity_type != EntityType.CONVEYOR or not _friendly(ct, entity_id): return False
    return True


def _harvester(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    if state.route is None or state.ore_target is None or not _verified(state, ct): return False
    round_no = _round(ct)
    harvester_id, entity_type, _ = _visible(ct, state.ore_target)
    if entity_type == EntityType.HARVESTER and _friendly(ct, harvester_id):
        state.delivery_started_round = state.delivery_started_round if state.delivery_started_round is not None else round_no
        if not _observe_route(ct, state, round_no) and state.last_delivery_round is None: state.state = BuilderState.DELIVER
        return True
    if _pos(ct).distance_squared(state.ore_target) != 1: state.state = BuilderState.APPROACH_BUILD_TILE; return _move(ct, state, state.ore_target, actions, adjacent=True)
    try: harvester_cost = int(ct.get_harvester_cost())
    except Exception: return False
    state.state = BuilderState.BUILD
    if not _can_spend(ct, harvester_cost, projected_output=2.5, allow_late_completion=round_no >= 850, state=state): return False
    if actions.build_harvester(state.ore_target) is not None: _set_project(ct, state, ProjectState.DELIVERING, round_no); state.project_count, state.project_pending, state.delivery_started_round, state.last_resource_total, state.last_resource_round, state.state = 1, False, round_no, None, None, BuilderState.DELIVER; state.repair_attempts = 0; return True
    state.repair_attempts += 1
    if state.repair_attempts >= 3: state.route_failure_reason = "harvester_build_denied"; _set_project(ct, state, ProjectState.FAILED, round_no)
    return False


def _repair(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    route = state.route
    if route is None: return False
    round_no = _round(ct)
    delivered = _observe_route(ct, state, round_no)
    if delivered: return True
    reference_round = state.last_delivery_round if state.last_delivery_round is not None else state.delivery_started_round; timeout_due = reference_round is not None and round_no - reference_round >= 12
    broken = find_broken_link(route, _visible_route(state, ct, route), current_round=None, last_delivery_round=state.last_delivery_round, route_start_round=state.delivery_started_round, blocked_output=False)
    if broken is None:
        if timeout_due:
            state.repair_attempts += 1
            if state.repair_attempts >= 3: _fail_route(ct, state, "delivery_timeout", round_no); return True
        if state.last_delivery_round is not None or state.state == BuilderState.MAINTAIN: state.state = BuilderState.MAINTAIN
        return False
    state.repair_index, target, expected = broken, route.cells[broken], route.directions[broken]
    entity_id, entity_type, direction = _visible(ct, target)
    friendly = _friendly(ct, entity_id)
    if entity_id is not None and not friendly: _fail_route(ct, state, "repair_occupied_enemy", round_no, replan=True); return True
    if entity_type is not None and (entity_type != EntityType.CONVEYOR or direction != expected):
        if _pos(ct).distance_squared(target) == 1:
            if friendly and teardown_allowed(verified_misdirected=True) and actions.destroy(target): state.repair_attempts += 1; _set_project(ct, state, ProjectState.BUILDING, round_no); return True
            state.repair_attempts += 1; return False
        return _move(ct, state, target, actions, adjacent=True)
    if _pos(ct).distance_squared(target) == 1:
        try:
            if not _can_spend(ct, int(ct.get_conveyor_cost()), projected_output=2.5, allow_late_completion=True, state=state): return False
        except Exception: return False
        if actions.build_conveyor(target, expected) is not None: state.built_links[target], state.repair_index, state.state = (EntityType.CONVEYOR, expected), None, BuilderState.DELIVER; state.delivery_started_round, state.backlog_rounds, state.repair_attempts = round_no, 0, 0; _set_project(ct, state, ProjectState.BUILDING, round_no); return True
        state.repair_attempts += 1
        if state.repair_attempts >= 3: _fail_route(ct, state, "repair_build_denied", round_no)
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


def _defend(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    if not cpu_is_safe(ct): return False
    try:
        current = _pos(ct); positions = tuple(position for position in (current.add(direction) for direction in CARDINALS) if ct.is_tile_empty(position)); threat = next(iter(state.world.threat_list(_round(ct))), None) if state.world else None
        if threat is None: return False
        own_core = state.world.own_core if state.world else None
        if threat.score < 7 and (own_core is None or own_core.distance_squared(threat.position) > 16): return False
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
    reserved = set(world.core_footprint) | _core_exit_tiles(world) | (set(route.cells) if route else set()); choices = tuple(position for position in positions if position not in reserved)
    if not choices: return False
    threat = next(iter(world.threat_list(round_no)), None)
    critical = _fresh_critical_threat(ct, state, round_no) is not None
    if ENABLE_DEFENSIVE_BUILDING and critical and state.role == Role.DEFENDER and threat is not None and threat.position.distance_squared(current) <= 4:
        try:
            barrier_cost = int(ct.get_barrier_cost())
        except Exception: return False
        escape_tiles = _legal_escape_tiles(ct, current)
        if len(escape_tiles) <= 1: return False
        barrier_target = min(choices, key=lambda position: (position.y, position.x))
        if _can_spend(ct, barrier_cost, preserve_defense=True, emergency=round_no >= 850, projected_output=threat.score, state=state, new_project=True): return actions.build_barrier(barrier_target) is not None
    if ENABLE_LAUNCHERS and state.role == Role.SIEGE and round_no < 850 and _fresh_verified_rally(ct, state, world, round_no):
        try:
            launcher_cost = int(ct.get_launcher_cost())
        except Exception: return False
        if _can_spend(ct, launcher_cost, projected_output=2.5, state=state, new_project=True): return actions.build_launcher(min(choices, key=lambda position: (position.y, position.x))) is not None
    if ENABLE_FORWARD_GUNNERS and _strategy_allows_offense(ct) and state.role in (Role.RAIDER, Role.SIEGE) and world.enemy_core is not None and round_no < 850:
        target = enemy_target_from_observation(world.enemy_core, EntityType.CORE, current_round=round_no, confidence=100)
        lanes: dict[tuple[Position, Direction], int] = {}
        for position in choices:
            for direction in CARDINALS:
                try:
                    lanes[position, direction] = sum(bool(ct.can_fire_from(position, direction, EntityType.GUNNER, tile)) for tile in tuple(ct.get_attackable_tiles_from(position, direction, EntityType.GUNNER))[:16])
                except Exception:
                    lanes[position, direction] = 0
        try:
            resources = int(ct.get_global_resources()); gunner_cost = int(ct.get_gunner_cost()); ammo_reserve = 4
        except Exception:
            resources, gunner_cost, ammo_reserve = 0, 0, 0
        site = choose_forward_turret_site(choices, target=target, firing_lanes=lanes, home_reserve=resources, construction_cost=gunner_cost, ammo_reserve=ammo_reserve)
        if site is not None and _can_spend(ct, gunner_cost, preserve_defense=True, projected_output=site[2], state=state, new_project=True):
            position, direction, _ = site
            turret_type = choose_forward_turret_type(lane_length=lanes.get((position, direction), 0))
            built = actions.build_sentinel(position, direction) if turret_type == EntityType.SENTINEL else actions.build_gunner(position, direction)
            if built is not None:
                state.offense_state = OffenseState.BUILDING_FORWARD_TURRET
                return True
    return False


def _raid(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    if _round(ct) >= 850 or not _strategy_allows_offense(ct): return False
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
    if not target_is_enemy_building(ct, position): return False
    attacked = actions.fire(position)
    if attacked:
        state.offense_state = OffenseState.SABOTAGING_LOGISTICS
        state.last_offense_progress_round, state.paid_attacks = _round(ct), state.paid_attacks + 1
    return attacked


def _offense_step(ct: object, state: BuilderStateData, actions: TurnActions, round_no: int) -> bool:
    if not ENABLE_RAIDS or not _strategy_allows_offense(ct) or state.role not in (Role.RAIDER, Role.SIEGE) or round_no >= 850:
        return False
    try:
        own_team = ct.get_team()
        observations = []
        for entity_id in tuple(ct.get_nearby_buildings())[:64]:
            if ct.get_team(entity_id) == own_team:
                continue
            entity_type = ct.get_entity_type(entity_id)
            if entity_type == EntityType.BUILDER_BOT:
                continue
            position = ct.get_position(entity_id)
            hp = int(ct.get_hp(entity_id)) if hasattr(ct, "get_hp") else None
            observations.append(enemy_target_from_observation(position, entity_type, current_round=round_no, hp=hp, confidence=80, source_id=int(entity_id)))
    except Exception:
        return False
    target = choose_offensive_target(tuple(observations), current_round=round_no, direct_core_window=True, crippled_economy=False)
    if target is None:
        state.offense_state = OffenseState.SCOUTING
        return False
    state.offense_target = target
    stance = choose_attack_stance(_pos(ct), target.position)
    if stance is None:
        return False
    if _pos(ct).distance_squared(target.position) == 1:
        if _can_spend(ct, GameConstants.BUILDER_BOT_ATTACK_COST, projected_output=max(1, target.confidence), state=state) and try_builder_attack(ct, target, free_attack_titanium=max(0, int(ct.get_global_resources())), attack_cost=GameConstants.BUILDER_BOT_ATTACK_COST):
            state.offense_state = OffenseState.SABOTAGING_LOGISTICS
            state.last_offense_progress_round, state.paid_attacks = round_no, state.paid_attacks + 1
            return True
        return False
    state.offense_state = OffenseState.APPROACHING_OBJECTIVE
    return _move(ct, state, stance, actions, adjacent=False)


def _record_exploration(ct: object, state: BuilderStateData, world: WorldMemory) -> None:
    """Keep a bounded per-Builder map of tiles that have actually been seen."""
    try:
        visible = tuple(ct.get_nearby_tiles())[: max(1, min(world.width * world.height, 4096))]
    except Exception:
        visible = ()
    for position in visible:
        if 0 <= position.x < world.width and 0 <= position.y < world.height:
            state.explored_tiles.add(position)
    current = _pos(ct)
    if 0 <= current.x < world.width and 0 <= current.y < world.height:
        state.explored_tiles.add(current)


def _exploration_complete(state: BuilderStateData, world: WorldMemory) -> bool:
    return len(state.explored_tiles) >= max(1, world.width * world.height)


def _frontier_candidates(ct: object, state: BuilderStateData, world: WorldMemory) -> tuple[Position, ...]:
    """Return deterministic visible frontier tiles before selecting unknown tiles."""
    current = _pos(ct)
    visible_frontier: list[Position] = []
    try:
        visible = tuple(ct.get_nearby_tiles())[: max(1, min(world.width * world.height, 4096))]
    except Exception:
        visible = ()
    for position in visible:
        if position in world.static_walls or not (0 <= position.x < world.width and 0 <= position.y < world.height):
            continue
        try:
            if not ct.is_tile_passable(position):
                continue
        except Exception:
            continue
        unknown_neighbour = any(
            0 <= neighbour.x < world.width
            and 0 <= neighbour.y < world.height
            and neighbour not in state.explored_tiles
            for direction in CARDINALS
            for neighbour in (position.add(direction),)
        )
        if unknown_neighbour:
            visible_frontier.append(position)
    if visible_frontier:
        return tuple(sorted(set(visible_frontier), key=lambda position: (current.distance_squared(position), position.y, position.x)))
    # Never path to an unseen tile as if it were empty.  If the visible ring
    # has no explicit frontier, move to its farthest known passable tile so a
    # later vision update can expose the next ring.
    known_passable: list[Position] = []
    for position in visible:
        if position in world.static_walls:
            continue
        try:
            if ct.is_tile_passable(position):
                known_passable.append(position)
        except Exception:
            continue
    return tuple(sorted(set(known_passable), key=lambda position: (-current.distance_squared(position), position.y, position.x)))[:32]


def _discover_frontier(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    world = state.world
    if world is None:
        return False
    current = _pos(ct)
    for _ in range(2):
        if state.frontier_target is None or state.frontier_target == current or state.frontier_target in state.explored_tiles:
            candidates = _frontier_candidates(ct, state, world)
            state.frontier_target = candidates[0] if candidates else None
        target = state.frontier_target
        if target is None:
            return False
        moved = _move(ct, state, target, actions)
        if moved:
            return True
        if state.blocked_steps < 3:
            return False
        # A blocked frontier is discarded immediately so the same turn can
        # select the next deterministic frontier instead of corner-wandering.
        state.frontier_target = None
        state.blocked_steps = 0
    return False


def _friendly_logistics(ct: object) -> tuple[tuple[int, Position, EntityType, Direction | None], ...]:
    try:
        own_team = ct.get_team()
        entities = tuple(ct.get_nearby_buildings())[:96]
    except Exception:
        return ()
    result: list[tuple[int, Position, EntityType, Direction | None]] = []
    for entity_id in sorted(entities):
        try:
            entity_type = ct.get_entity_type(entity_id)
            if entity_type not in (EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.HARVESTER) or ct.get_team(entity_id) != own_team:
                continue
            direction = None
            if entity_type in (EntityType.CONVEYOR, EntityType.SPLITTER):
                try:
                    direction = ct.get_direction(entity_id)
                except Exception:
                    direction = None
            result.append((int(entity_id), ct.get_position(entity_id), entity_type, direction))
        except Exception:
            continue
    return tuple(result)


def _visible_patrol_gap(ct: object, state: BuilderStateData) -> tuple[Position, Direction] | None:
    world = state.world
    if world is None:
        return None
    for _, position, entity_type, direction in _friendly_logistics(ct):
        if entity_type not in (EntityType.CONVEYOR, EntityType.SPLITTER) or direction not in CARDINALS:
            continue
        gap = position.add(direction)
        continuation = gap.add(direction)
        if not (0 <= gap.x < world.width and 0 <= gap.y < world.height):
            continue
        if world.is_route_planning_blocked(gap) or gap in world.ore_positions:
            continue
        try:
            if not ct.is_tile_empty(gap) or ct.get_tile_building_id(continuation) is None:
                continue
            next_id = ct.get_tile_building_id(continuation)
            if next_id is None or not _friendly(ct, next_id) or ct.get_entity_type(next_id) not in (EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.HARVESTER):
                continue
        except Exception:
            continue
        return gap, direction
    return None


def _patrol_logistics(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    """Patrol the visible network and fill only an evidenced one-cell gap."""
    gap = _visible_patrol_gap(ct, state)
    if gap is not None:
        target, direction = gap
        state.patrol_repair_target = target
        if _pos(ct).distance_squared(target) != 1:
            return _move(ct, state, target, actions, adjacent=True)
        try:
            cost = int(ct.get_conveyor_cost())
        except Exception:
            return False
        if not _can_spend(ct, cost, projected_output=1, allow_late_completion=True, state=None):
            return False
        built = actions.build_conveyor(target, direction)
        if built is not None:
            state.patrol_repair_target = None
            state.blocked_steps = 0
            return True
        return False
    state.patrol_repair_target = None
    logistics = _friendly_logistics(ct)
    if logistics:
        positions = tuple(item[1] for item in logistics)
        if state.patrol_target is None or state.patrol_target not in positions or _pos(ct).distance_squared(state.patrol_target) <= 1:
            state.patrol_target = positions[state.patrol_cursor % len(positions)]
            state.patrol_cursor = (state.patrol_cursor + 1) % len(positions)
        return _move(ct, state, state.patrol_target, actions, adjacent=True)
    if state.world is None:
        return False
    staging = state.world.own_core or Position(state.world.width // 2, state.world.height // 2)
    return _move(ct, state, staging, actions, adjacent=True)


def _fresh_critical_threat(ct: object, state: BuilderStateData, round_no: int) -> object | None:
    world = state.world
    if world is None:
        return None
    core = world.own_core or _pos(ct)
    route_cells = set(state.route.cells) if state.route is not None else set()
    logistics_cells = tuple(item[1] for item in _friendly_logistics(ct))
    for threat in world.threat_list(round_no):
        age = max(0, round_no - threat.seen_round)
        near_core = core.distance_squared(threat.position) <= 16
        near_route = (bool(route_cells) and min((cell.distance_squared(threat.position) for cell in route_cells), default=999) <= 4) or min((cell.distance_squared(threat.position) for cell in logistics_cells), default=999) <= 4
        assessed = assess_threat(
            position=threat.position,
            enemy_builder_distance=max(0, int(core.distance_squared(threat.position) ** 0.5)),
            firing_line=threat.kind == ThreatKind.FIRING_LINE,
            sabotage=threat.kind == ThreatKind.SABOTAGE,
            current_round=round_no,
            entity_type=threat.entity_type,
        )
        effective = assessed if assessed is not None and assessed.score > threat.score else threat
        if age <= 3 and effective.score >= 7 and (near_core or near_route):
            return effective
    try:
        shared = read_shared_threat(ct, current_round=round_no)
    except Exception:
        shared = None
    if shared is not None and shared.severity >= 12 and (core.distance_squared(shared.position) <= 16 or shared.target_asset in route_cells):
        return ThreatKind.CORE_DAMAGE
    return None


def _route_repair_due(ct: object, state: BuilderStateData, round_no: int) -> bool:
    if state.repair_index is not None or state.patrol_repair_target is not None:
        return True
    route = state.route
    if route is None or state.route_index >= 0:
        return False
    try:
        return find_broken_link(route, _visible_route(state, ct, route), current_round=None, last_delivery_round=state.last_delivery_round, route_start_round=state.delivery_started_round, blocked_output=state.backlog_rounds >= 3) is not None
    except Exception:
        return False


def _resolve_work_intent(ct: object, state: BuilderStateData, world: WorldMemory, round_no: int, target: Position | None, strategy_phase: StrategyPhase) -> WorkIntent:
    # A delayed/idle claim is not a productive route reservation yet.  Keep
    # that Builder scouting so the project can discover ore on a later write.
    route_owner = bool(target is not None or state.project_count or state.route is not None or state.route_search is not None or state.ore_target is not None)
    maintaining_routes = sum(
        project is not None and project.state == ProjectState.MAINTAIN
        for index in range(PROJECT_COUNT)
        for project in (read_project(ct, index),)
    )
    # Route owners keep their economic reservation during an alert; free
    # Builders are the first responders.  This preserves the route-claim
    # invariant while still giving a critical event an immediate worker.
    critical = not route_owner and (strategy_phase == StrategyPhase.DEFENSE_ALERT or _fresh_critical_threat(ct, state, round_no) is not None)
    attack = not route_owner and strategy_phase in (StrategyPhase.OFFENSIVE_PRESSURE, StrategyPhase.CORE_SIEGE)
    preparation = not route_owner and strategy_phase == StrategyPhase.ATTACK_PREPARATION
    intent = choose_work_intent(
        critical_threat=critical,
        route_repair_due=_route_repair_due(ct, state, round_no),
        route_owner=route_owner,
        attack_preparation=preparation,
        attack=attack,
        exploration_complete=_exploration_complete(state, world) and maintaining_routes >= MAX_HEALTHY_ROUTES,
    )
    state.work_intent, state.intent_round = intent, round_no
    return intent


def _scout(ct: object, state: BuilderStateData, actions: TurnActions) -> bool:
    return _discover_frontier(ct, state, actions)


def _apply_strategy_role(ct: object, state: BuilderStateData) -> StrategyPhase:
    if not ENABLE_PHASE_STRATEGY:
        return StrategyPhase.BOOTSTRAP_ECON
    try:
        decoded = decode_global_strategy(int(ct.read_store(int(Slot.STRATEGY))))
    except Exception:
        return StrategyPhase.BOOTSTRAP_ECON
    if decoded is None:
        return StrategyPhase.BOOTSTRAP_ECON
    strategy_phase, _, _ = decoded
    # An owned project always wins over a convenience role.  Once a Builder is
    # free, the Core's single global phase is authoritative: preparation
    # scouts, pressure raiders, and a verified siege window gets siege units.
    if state.claim_slot is None and state.route is None and state.route_search is None and state.ore_target is None:
        if strategy_phase == StrategyPhase.CORE_SIEGE:
            state.role = Role.SIEGE
        elif strategy_phase == StrategyPhase.OFFENSIVE_PRESSURE:
            state.role = Role.RAIDER
        elif strategy_phase == StrategyPhase.ATTACK_PREPARATION:
            state.role = Role.SCOUT
        elif strategy_phase == StrategyPhase.DEFENSE_ALERT:
            state.role = Role.DEFENDER
        elif strategy_phase == StrategyPhase.RECOVERY:
            state.role = Role.REPAIR
    if strategy_phase in (StrategyPhase.DEFENSE_ALERT, StrategyPhase.RECOVERY):
        state.offense_state = OffenseState.RETREATING if state.offense_target is not None else state.offense_state
    return strategy_phase


def _strategy_allows_offense(ct: object) -> bool:
    if not ENABLE_PHASE_STRATEGY:
        return True
    try:
        decoded = decode_global_strategy(int(ct.read_store(int(Slot.STRATEGY))))
    except Exception:
        return False
    return decoded is not None and decoded[0] in (StrategyPhase.OFFENSIVE_PRESSURE, StrategyPhase.CORE_SIEGE)


def run_builder(ct: object, state: BuilderStateData | None = None) -> BuilderStateData:
    state = state or BuilderStateData()
    world, round_no = _world(ct, state), _round(ct)
    _record_exploration(ct, state, world)
    if state.role == Role.SCOUT and state.last_position is None: state.role = assign_role(_id(ct))
    _read_rally(ct, state)
    if state.rally_target is not None and not _fresh_verified_rally(ct, state, world, round_no): state.rally_target, state.rally_expires_epoch = None, 0
    target = _claim(ct, state, world, round_no)
    strategy_phase = _apply_strategy_role(ct, state)
    _publish_rally(ct, state, world, round_no)
    try:
        resources = int(ct.get_global_resources()); harvester_count = sum(1 for entity_id in tuple(ct.get_nearby_buildings())[:64] if ct.get_entity_type(entity_id) == EntityType.HARVESTER)
    except Exception: resources, harvester_count = 0, 0
    priorities = late_game_policy(round_no, delivery_due=state.state in (BuilderState.DELIVER, BuilderState.VERIFY), route_repair_due=state.repair_index is not None or state.backlog_rounds >= 3, harvester_payback_positive=target is not None, stored_titanium=resources, collected_titanium=state.last_delivery_round or 0, harvester_count=harvester_count)
    actions = TurnActions(ct)
    intent = _resolve_work_intent(ct, state, world, round_no, target, strategy_phase)
    if intent == WorkIntent.CRITICAL_DEFENSE:
        if _support_build(ct, state, actions, round_no) or _defend(ct, state, actions):
            state.last_position = _pos(ct)
            return state
        _discover_frontier(ct, state, actions)
        state.last_position = _pos(ct)
        return state
    route_owner = intent in (WorkIntent.ROUTE_OWNER, WorkIntent.REPAIR_ROUTE) and bool(target is not None or state.project_count or state.route is not None or state.route_search is not None or state.ore_target is not None)
    if route_owner:
        if state.route is not None and state.blocked_steps >= 3: _reset_route_search(state)
        if state.route is None and target is not None:
            if round_no < 850 or state.route_search is not None:
                planned = _route(ct, state, target, round_no)
                if planned is not None: state.state = BuilderState.ROUTE
        if state.route is not None and state.route_index >= 0:
            state.state = BuilderState.ROUTE; _build_route(ct, state, actions)
        elif state.route is not None:
            if _repair(ct, state, actions): state.last_position = _pos(ct); return state
            _harvester(ct, state, actions)
        elif target is not None and state.route_search is not None:
            # Incremental search may take several turns.  Keep the owner
            # moving toward a legal tile adjacent to its ore while search
            # continues, rather than consuming turns without a responsibility.
            state.state = BuilderState.APPROACH_BUILD_TILE
            _move(ct, state, target, actions, adjacent=True)
        state.last_position = _pos(ct); return state
    if state.route is not None and state.route_index < 0:
        if _repair(ct, state, actions): state.last_position = _pos(ct); return state
        if state.state in (BuilderState.DELIVER, BuilderState.VERIFY) and _harvester(ct, state, actions): state.last_position = _pos(ct); return state
    if intent == WorkIntent.REPAIR_ROUTE:
        _patrol_logistics(ct, state, actions)
    elif intent == WorkIntent.ATTACK:
        if _support_build(ct, state, actions, round_no):
            state.last_position = _pos(ct)
            return state
        if ENABLE_RAIDS and "no_paid_attack" not in priorities and _raid(ct, state, actions):
            state.last_position = _pos(ct)
            return state
        if ENABLE_RAIDS and _offense_step(ct, state, actions, round_no):
            state.last_position = _pos(ct)
            return state
        _discover_frontier(ct, state, actions)
    elif intent in (WorkIntent.DISCOVER_ORE, WorkIntent.ATTACK_PREPARATION):
        _discover_frontier(ct, state, actions)
    else:
        _patrol_logistics(ct, state, actions)
    state.last_position = _pos(ct)
    return state
