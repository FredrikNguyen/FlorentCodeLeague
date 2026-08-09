
from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable, Mapping

from fcode import Direction, EntityType, Position

from .navigation import CARDINALS
from .types import RoutePlan, RouteStatus


def _footprint(core: Position | Iterable[Position]) -> tuple[Position, ...]:
    if isinstance(core, Position): return (core, Position(core.x + 1, core.y), Position(core.x, core.y + 1), Position(core.x + 1, core.y + 1))
    return tuple(core)


def _inside(pos: Position, width: int, height: int) -> bool:
    return 0 <= pos.x < width and 0 <= pos.y < height


def _direction_between(start: Position, end: Position) -> Direction:
    for direction in CARDINALS:
        if start.add(direction) == end: return direction
    return Direction.CENTRE


def directions_for_route(
    cells: Iterable[Position], core_footprint: Position | Iterable[Position]
) -> tuple[Direction, ...]:
    ordered = tuple(cells)
    footprint = set(_footprint(core_footprint))
    if not ordered: return ()
    directions: list[Direction] = []
    for index, cell in enumerate(ordered):
        if index + 1 < len(ordered): direction = _direction_between(cell, ordered[index + 1])
        else: direction = next((candidate for candidate in CARDINALS if cell.add(candidate) in footprint), Direction.CENTRE)
        if direction == Direction.CENTRE: return ()
        directions.append(direction)
    return tuple(directions)


def plan_core_outward_route(
    ore: Position,
    core_footprint: Position | Iterable[Position],
    width: int,
    height: int,
    blocked: Callable[[Position], bool] | set[Position] | frozenset[Position] | None = None,
    *,
    created_round: int = 0,
    cpu_check: Callable[[], int | bool] | None = None,
    obstacle_epoch: int = 0,
    search_state: dict[str, object] | None = None,
    stats: dict[str, int] | None = None,
    reuse_direction: Callable[[Position], Direction | None] | None = None,
) -> RoutePlan | None:
    """Plan an ore-to-Core Conveyor route.

    With ``reuse_direction`` unset this preserves the original bounded BFS.
    When supplied, route length remains the primary objective and the planner
    maximizes already-correct friendly Conveyor reuse among equal-length paths.
    A known Conveyor pointing the wrong way is skipped instead of planning
    through it and discovering the conflict only at build time.

    Reuse is implemented as a deterministic BFS tie-break, not a weighted
    search.  Route length therefore remains shortest-path bounded and CPU cost
    stays close to the original planner under the 10 ms per-unit ladder limit.
    """
    footprint = tuple(sorted((cell for cell in _footprint(core_footprint) if _inside(cell, width, height)), key=lambda pos: (pos.y, pos.x)))
    if not footprint or not _inside(ore, width, height): return None
    blocked_set = set(footprint)

    def is_blocked(pos: Position) -> bool:
        if pos in blocked_set: return True
        if blocked is None: return False
        return pos in blocked if not callable(blocked) else bool(blocked(pos))

    def ordered_adjacent(seeds: Iterable[Position]) -> tuple[Position, ...]:
        seen: set[Position] = set()
        ordered: list[Position] = []
        for seed in seeds:
            for direction in CARDINALS:
                position = seed.add(direction)
                if position in seen or not _inside(position, width, height) or is_blocked(position): continue
                seen.add(position); ordered.append(position)
        return tuple(ordered)

    starts = ordered_adjacent((ore,))
    exits = ordered_adjacent(footprint)
    state = search_state if search_state is not None else {}
    mode = 'reuse' if reuse_direction is not None else 'bfs'
    signature = (ore, footprint, int(width), int(height), int(obstacle_epoch), mode)

    def planning_is_safe() -> bool:
        if cpu_check is None: return True
        try:
            value = cpu_check()
            return value if isinstance(value, bool) else int(value) < 7000
        except Exception: return True

    if stats is not None:
        stats['expansions'] = stats['stopped_cpu'] = stats['complete'] = 0
        stats['reused_links'] = 0

    if reuse_direction is not None:
        if state.get('signature') != signature:
            footprint_set = set(footprint)
            reusable_exits: list[Position] = []
            ordinary_exits: list[Position] = []
            for position in exits:
                known = reuse_direction(position)
                if known is not None:
                    if position.add(known) not in footprint_set:
                        # A known Conveyor at a Core exit flowing the wrong way
                        # cannot be part of this route without destructive churn.
                        continue
                    reusable_exits.append(position)
                else:
                    ordinary_exits.append(position)
            ordered_exits = tuple(reusable_exits + ordinary_exits)
            state.clear(); state.update({
                'signature': signature,
                'queue': deque(ordered_exits),
                'parents': {position: None for position in ordered_exits},
                'starts': frozenset(starts),
                'blocked': is_blocked,
                'reuse_direction': reuse_direction,
                'complete': False,
                'created_round': int(created_round),
                'expansions': 0,
            })
        if state.get('complete'):
            return None

        queue = state['queue']
        parents = state['parents']
        starts_set = state['starts']
        blocked_fn = state['blocked']
        reuse_fn = state['reuse_direction']
        expansions = int(state.get('expansions', 0))
        while queue and expansions < width * height:
            if cpu_check is not None and not planning_is_safe():
                state['expansions'] = expansions
                if stats is not None: stats['stopped_cpu'] = 1
                return None
            current = queue.popleft()
            expansions += 1
            if stats is not None: stats['expansions'] = int(stats.get('expansions', 0)) + 1
            if current in starts_set:
                cells_reversed = [current]
                while parents[cells_reversed[-1]] is not None:
                    cells_reversed.append(parents[cells_reversed[-1]])
                cells = tuple(cells_reversed)
                directions = directions_for_route(cells, footprint)
                if directions:
                    state['complete'] = True
                    state['expansions'] = expansions
                    if stats is not None:
                        stats['complete'] = 1
                        stats['reused_links'] = sum(
                            reuse_fn(cell) == direction
                            for cell, direction in zip(cells, directions)
                        )
                    return RoutePlan(
                        ore=ore,
                        cells=cells,
                        directions=directions,
                        core_footprint=footprint,
                        status=RouteStatus.PLANNED,
                        created_round=int(state.get('created_round', created_round)),
                        expected_output=10,
                    )

            # Normal BFS still determines distance.  Among cells discovered at
            # the same distance, enqueue already-correct friendly Conveyors first.
            # This is much cheaper than heap/Dijkstra while giving later routes a
            # strong tendency to collapse onto existing trunks.
            reused: list[Position] = []
            fresh: list[Position] = []
            for direction in CARDINALS:
                neighbour = current.add(direction)
                if not _inside(neighbour, width, height) or neighbour in parents or blocked_fn(neighbour):
                    continue
                known = reuse_fn(neighbour)
                if known is not None:
                    if neighbour.add(known) != current:
                        continue
                    reused.append(neighbour)
                else:
                    fresh.append(neighbour)
            for neighbour in reused + fresh:
                parents[neighbour] = current
                queue.append(neighbour)
        state['complete'] = True
        state['expansions'] = expansions
        if stats is not None: stats['complete'] = 1
        return None

    if state.get('signature') != signature:
        state.clear(); state.update({'signature': signature, 'queue': deque(exits), 'parents': {position: None for position in exits}, 'starts': frozenset(starts), 'blocked': is_blocked, 'complete': False, 'created_round': int(created_round)})
    if state.get('complete'):
        return None

    queue = state['queue']
    parents = state['parents']
    starts_set = state['starts']
    blocked_fn = state['blocked']
    expansions = int(state.get('expansions', 0))
    while queue and expansions < width * height:
        if cpu_check is not None and not planning_is_safe():
            state['expansions'] = expansions
            if stats is not None: stats['stopped_cpu'] = 1
            return None
        current = queue.popleft()
        expansions += 1
        if stats is not None: stats['expansions'] = int(stats.get('expansions', 0)) + 1
        if current in starts_set:
            cells_reversed = [current]
            while parents[cells_reversed[-1]] is not None: cells_reversed.append(parents[cells_reversed[-1]])
            cells = tuple(cells_reversed)
            directions = directions_for_route(cells, footprint)
            if directions:
                state['complete'] = True
                state['expansions'] = expansions
                if stats is not None:
                    stats['complete'] = 1
                return RoutePlan(
                    ore=ore,
                    cells=cells,
                    directions=directions,
                    core_footprint=footprint,
                    status=RouteStatus.PLANNED,
                    created_round=int(state.get('created_round', created_round)),
                    expected_output=10,
                )
        for direction in CARDINALS:
            neighbour = current.add(direction)
            if not _inside(neighbour, width, height) or neighbour in parents or blocked_fn(neighbour):
                continue
            parents[neighbour] = current
            queue.append(neighbour)
    state['complete'] = True
    state['expansions'] = expansions
    if stats is not None:
        stats['complete'] = 1
    return None


def _visible_at(
    visible: Mapping[Position, object] | Callable[[Position], object], pos: Position
) -> object | None:
    try:
        return visible(pos) if callable(visible) else visible.get(pos)
    except Exception:
        return None


def _entity_and_direction(value: object) -> tuple[EntityType | None, Direction | None]:
    if isinstance(value, tuple) and len(value) >= 2:
        entity, direction = value[0], value[1]
        return entity if isinstance(entity, EntityType) else None, direction if isinstance(direction, Direction) else None
    if isinstance(value, EntityType):
        return value, None
    return None, None


def verify_route(
    route: RoutePlan | Iterable[Position],
    visible: Mapping[Position, object] | Callable[[Position], object],
    core_footprint: Position | Iterable[Position] | None = None,
) -> bool:
    if isinstance(route, RoutePlan):
        cells = route.cells
        directions = route.directions
        footprint = set(route.core_footprint)
    else:
        cells = tuple(route)
        footprint = set(_footprint(core_footprint)) if core_footprint is not None else set()
        directions = directions_for_route(cells, footprint) if footprint else ()
    if not cells or len(cells) != len(directions):
        return False
    for cell, expected_direction, in zip(cells, directions):
        entity, direction = _entity_and_direction(_visible_at(visible, cell))
        if entity != EntityType.CONVEYOR or direction != expected_direction:
            return False
    if footprint and cells[-1].add(directions[-1]) not in footprint:
        return False
    return True


def find_broken_link(
    route: RoutePlan,
    visible: Mapping[Position, object] | Callable[[Position], object],
    *,
    current_round: int | None = None,
    last_delivery_round: int | None = None,
    route_start_round: int | None = None,
    delivery_timeout: int = 12,
    blocked_output: bool = False,
) -> int | None:
    for index, cell in enumerate(route.cells):
        value = _visible_at(visible, cell)
        entity, direction = _entity_and_direction(value)
        if entity != EntityType.CONVEYOR or direction != route.directions[index]:
            return index
    if blocked_output:
        return max(0, len(route.cells) - 1)
    reference_round = last_delivery_round if last_delivery_round is not None else route_start_round
    if current_round is not None and reference_round is not None and int(current_round) - int(reference_round) >= max(1, int(delivery_timeout)):
        return 0
    return None


def repair_priority(
    broken_index: int | None,
    route_length: int,
    *,
    backlog: int = 0,
    non_delivery_rounds: int = 0,
) -> int:
    if broken_index is None and backlog <= 0 and non_delivery_rounds <= 0:
        return 0
    proximity = max(0, int(route_length) - max(0, int(broken_index or 0)))
    return 10 + max(0, int(backlog)) + max(0, int(non_delivery_rounds)) + proximity


def splitter_redundancy_justified(
    probability_of_cut: float,
    remaining_expected_route_output: float,
    splitter_cost: int,
    branch_cost: int,
    estimated_latency_penalty: float,
    *,
    mature_route: bool,
    exposed_segment: bool,
    disjoint_branch: bool,
    branch_length: int,
    max_branch_length: int = 12,
) -> bool:
    if not (mature_route and exposed_segment and disjoint_branch):
        return False
    if int(branch_length) <= 0 or int(branch_length) > int(max_branch_length):
        return False
    avoided = max(0.0, float(probability_of_cut)) * max(0.0, float(remaining_expected_route_output))
    cost = max(0, int(splitter_cost)) + max(0, int(branch_cost)) + max(
        0.0, float(estimated_latency_penalty)
    )
    return avoided > cost


def teardown_allowed(
    *,
    verified_obsolete: bool = False,
    verified_misdirected: bool = False,
    friendly: bool = True,
) -> bool:
    return bool(friendly and (verified_obsolete or verified_misdirected))
