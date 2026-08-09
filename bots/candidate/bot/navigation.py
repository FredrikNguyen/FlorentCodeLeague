from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable

from fcode import Controller, Direction, Position

from .actions import TurnActions

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


def _inside(pos: Position, width: int, height: int) -> bool:
    return 0 <= pos.x < width and 0 <= pos.y < height


def _blocked_fn(blocked):
    if blocked is None:
        return lambda _pos: False
    if isinstance(blocked, (set, frozenset)):
        return lambda pos: pos in blocked
    return blocked


def bounded_bfs_to_any(
    start: Position,
    goals: Iterable[Position],
    width: int,
    height: int,
    blocked=None,
    *,
    max_expansions: int | None = None,
    cpu_check: Callable[[], int | bool] | None = None,
    stats: dict[str, int] | None = None,
) -> list[Position]:
    """Deterministic bounded cardinal BFS to the first shortest goal."""
    width, height = int(width), int(height)
    if stats is not None:
        stats["expansions"] = 0
        stats["stopped_cpu"] = 0
    if width <= 0 or height <= 0 or not _inside(start, width, height):
        return []
    goal_set = {goal for goal in goals if _inside(goal, width, height)}
    if not goal_set:
        return []
    is_blocked = _blocked_fn(blocked)
    try:
        if is_blocked(start):
            return []
    except Exception:
        return []
    goal_set = {goal for goal in goal_set if goal == start or not bool(is_blocked(goal))}
    if not goal_set:
        return []
    if start in goal_set:
        return [start]

    area = width * height
    limit = min(area, max(1, area if max_expansions is None else int(max_expansions)))
    start_index = start.y * width + start.x
    parents = [-2] * area
    parents[start_index] = -1
    queue = deque((start_index,))
    expansions = 0
    found_index: int | None = None

    while queue and expansions < limit:
        if cpu_check is not None:
            try:
                value = cpu_check()
                safe = value if isinstance(value, bool) else int(value) < 7000
            except Exception:
                safe = False
            if not safe:
                if stats is not None:
                    stats["stopped_cpu"] = 1
                break
        current = queue.popleft()
        expansions += 1
        x, y = current % width, current // width
        for direction in CARDINALS:
            neighbour_pos = Position(x, y).add(direction)
            if not _inside(neighbour_pos, width, height):
                continue
            neighbour = neighbour_pos.y * width + neighbour_pos.x
            if parents[neighbour] != -2:
                continue
            try:
                if is_blocked(neighbour_pos):
                    continue
            except Exception:
                continue
            parents[neighbour] = current
            if neighbour_pos in goal_set:
                found_index = neighbour
                queue.clear()
                break
            queue.append(neighbour)

    if stats is not None:
        stats["expansions"] = expansions
    if found_index is None:
        return []
    path: list[Position] = []
    cursor = found_index
    while cursor >= 0:
        path.append(Position(cursor % width, cursor // width))
        cursor = parents[cursor]
    path.reverse()
    return path


def bounded_bfs(
    start: Position,
    goal: Position,
    width: int,
    height: int,
    blocked=None,
    *,
    max_expansions: int | None = None,
    cpu_check: Callable[[], int | bool] | None = None,
    stats: dict[str, int] | None = None,
) -> list[Position]:
    return bounded_bfs_to_any(
        start,
        (goal,),
        width,
        height,
        blocked,
        max_expansions=max_expansions,
        cpu_check=cpu_check,
        stats=stats,
    )


class Navigator:
    """One reusable active path per unit.

    Unlike a cache keyed by the changing start tile, the active path advances as
    the Builder moves and is invalidated only by a goal/epoch change or a blocked
    next step.
    """

    __slots__ = (
        "width",
        "height",
        "blocked",
        "cpu",
        "active_goal",
        "active_mode",
        "active_epoch",
        "active_path",
        "active_index",
        "history",
        "fallback_cursor",
        "replans",
        "cache_hits",
    )

    def __init__(
        self,
        width: int,
        height: int,
        blocked=None,
        *,
        cpu: Callable[[], int] | None = None,
        cache_limit: int = 1,
    ) -> None:
        del cache_limit
        self.width = max(0, int(width))
        self.height = max(0, int(height))
        self.blocked = blocked
        self.cpu = cpu
        self.active_goal: Position | None = None
        self.active_mode = "tile"
        self.active_epoch = -1
        self.active_path: tuple[Position, ...] = ()
        self.active_index = 0
        self.history = deque(maxlen=6)
        self.fallback_cursor = 0
        self.replans = 0
        self.cache_hits = 0

    def _is_blocked(self, pos: Position) -> bool:
        try:
            if self.blocked is None:
                return False
            return bool(self.blocked(pos)) if callable(self.blocked) else pos in self.blocked
        except Exception:
            return True

    def _safe(self) -> bool:
        try:
            return self.cpu is None or int(self.cpu()) < 7000
        except Exception:
            return False

    def invalidate(self) -> None:
        self.active_goal = None
        self.active_epoch = -1
        self.active_path = ()
        self.active_index = 0

    def _goals(self, goal: Position, mode: str) -> tuple[Position, ...]:
        if mode == "tile":
            return (goal,) if _inside(goal, self.width, self.height) else ()
        result = []
        for direction in CARDINALS:
            candidate = goal.add(direction)
            if _inside(candidate, self.width, self.height) and not self._is_blocked(candidate):
                result.append(candidate)
        return tuple(result)

    def _align(self, start: Position) -> bool:
        if not self.active_path:
            return False
        begin = max(0, self.active_index - 1)
        for index in range(begin, len(self.active_path)):
            if self.active_path[index] == start:
                self.active_index = index
                return True
        return False

    def _legal(self, direction: Direction, can_step) -> bool:
        if direction == Direction.CENTRE:
            return False
        try:
            return can_step is None or bool(can_step(direction))
        except Exception:
            return False

    def _greedy(self, start: Position, goals: tuple[Position, ...], can_step) -> Direction:
        if not goals:
            return Direction.CENTRE
        target = min(goals, key=lambda pos: (start.distance_squared(pos), pos.y, pos.x))
        preferred = start.cardinal_direction_to(target)
        ordered = ((preferred,) if preferred != Direction.CENTRE else ()) + CARDINALS
        seen: set[Direction] = set()
        for direction in ordered:
            if direction in seen:
                continue
            seen.add(direction)
            candidate = start.add(direction)
            if not _inside(candidate, self.width, self.height) or self._is_blocked(candidate):
                continue
            if self._legal(direction, can_step):
                return direction
        return Direction.CENTRE

    def _next(
        self,
        start: Position,
        goal: Position,
        obstacle_epoch: int,
        *,
        mode: str,
        can_step: Callable[[Direction], bool] | None,
    ) -> Direction:
        goals = self._goals(goal, mode)
        if start in goals:
            self.history.clear()
            self.history.append(start)
            return Direction.CENTRE
        signature_changed = (
            self.active_goal != goal
            or self.active_mode != mode
            or self.active_epoch != int(obstacle_epoch)
        )
        reusable = not signature_changed and self._align(start)
        if reusable and self.active_index + 1 < len(self.active_path):
            next_pos = self.active_path[self.active_index + 1]
            direction = start.cardinal_direction_to(next_pos)
            if not self._is_blocked(next_pos) and self._legal(direction, can_step):
                self.cache_hits += 1
                self.active_index += 1
                self.history.append(start)
                return direction
        if self._safe():
            path = bounded_bfs_to_any(
                start,
                goals,
                self.width,
                self.height,
                self.blocked,
                max_expansions=self.width * self.height,
                cpu_check=self._safe if self.cpu is not None else None,
            )
            self.replans += 1
            self.active_goal = goal
            self.active_mode = mode
            self.active_epoch = int(obstacle_epoch)
            self.active_path = tuple(path)
            self.active_index = 0
            if len(path) > 1:
                direction = start.cardinal_direction_to(path[1])
                if self._legal(direction, can_step):
                    self.active_index = 1
                    self.history.append(start)
                    return direction
        self.history.append(start)
        return self._greedy(start, goals, can_step)

    def next_direction(
        self,
        start: Position,
        goal: Position,
        obstacle_epoch: int = 0,
        *,
        can_step: Callable[[Direction], bool] | None = None,
    ) -> Direction:
        return self._next(start, goal, obstacle_epoch, mode="tile", can_step=can_step)

    def next_direction_to_adjacent(
        self,
        start: Position,
        target: Position,
        obstacle_epoch: int = 0,
        *,
        can_step: Callable[[Direction], bool] | None = None,
    ) -> Direction:
        return self._next(start, target, obstacle_epoch, mode="adjacent", can_step=can_step)


def move_toward_or_fallback(
    ct: Controller,
    target: Position,
    *,
    cursor: int,
    actions: TurnActions | None = None,
) -> tuple[bool, int]:
    turn = actions or TurnActions(ct)
    preferred = ct.get_position().cardinal_direction_to(target)
    directions = ((preferred,) if preferred != Direction.CENTRE else ()) + CARDINALS
    seen: set[Direction] = set()
    for offset, direction in enumerate(directions):
        if direction in seen:
            continue
        seen.add(direction)
        if turn.move(direction):
            return True, (cursor + offset + 1) % 4
    return False, (cursor + 1) % 4
