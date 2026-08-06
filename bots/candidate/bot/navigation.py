from __future__ import annotations

from collections import deque
from typing import Callable, Iterable
from fcode import Direction, Position

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


def _inside(pos: Position, width: int, height: int) -> bool: return 0 <= pos.x < width and 0 <= pos.y < height


def _safe(check: Callable[[], bool] | None) -> bool:
    try: value = check() if check is not None else True; return value if isinstance(value, bool) else int(value) < 7000
    except Exception: return False


def bounded_bfs(start: Position, goal: Position | Iterable[Position], width: int, height: int, blocked: Callable[[Position], bool] | set[Position] | frozenset[Position] | None = None, *, max_expansions: int | None = None, cpu_check: Callable[[], bool] | None = None, stats: dict[str, int] | None = None) -> list[Position]:
    if stats is not None: stats["expansions"] = 0
    width, height = int(width), int(height)
    goals = (goal,) if isinstance(goal, Position) else tuple(goal)
    goals = tuple(sorted({pos for pos in goals if _inside(pos, width, height)}, key=lambda pos: (pos.y, pos.x)))
    if width <= 0 or height <= 0 or not _inside(start, width, height) or not goals: return []
    area = width * height; start_i = start.y * width + start.x; goal_i = {pos.y * width + pos.x for pos in goals}
    blocked_i: set[int] | None = None; blocked_fn: Callable[[Position], bool] | None = None
    if isinstance(blocked, (set, frozenset)): blocked_i = {pos.y * width + pos.x for pos in blocked if _inside(pos, width, height)}
    elif blocked is not None: blocked_fn = blocked
    def is_blocked(index: int, x: int, y: int) -> bool:
        if blocked_i is not None: return index in blocked_i
        if blocked_fn is None: return False
        try: return bool(blocked_fn(Position(x, y)))
        except Exception: return True
    if is_blocked(start_i, start.x, start.y): return []
    if start_i in goal_i: return [start]
    limit = min(area, max(1, area if max_expansions is None else int(max_expansions))); parents = [-2] * area; parents[start_i] = -1; queue = deque((start_i,)); found = -1; expansions = 0
    while queue and expansions < limit:
        if not _safe(cpu_check): break
        current = queue.popleft(); expansions += 1; x, y = current % width, current // width
        for dx, dy, delta in ((0, -1, -width), (1, 0, 1), (0, 1, width), (-1, 0, -1)):
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= width or ny < 0 or ny >= height: continue
            neighbour = current + delta
            if parents[neighbour] != -2 or is_blocked(neighbour, nx, ny): continue
            parents[neighbour] = current
            if neighbour in goal_i: found = neighbour; break
            queue.append(neighbour)
        if found >= 0: break
    if stats is not None: stats["expansions"] = expansions
    if found < 0: return []
    path: list[Position] = []; cursor = found
    while cursor >= 0: path.append(Position(cursor % width, cursor // width)); cursor = parents[cursor]
    path.reverse(); return path


class Navigator:
    __slots__ = ("width", "height", "blocked", "cpu", "history", "active_goal_key", "active_obstacle_epoch", "active_path", "active_index", "replans", "cache_hits")

    def __init__(self, width: int, height: int, blocked=None, *, cpu: Callable[[], int] | None = None, cache_limit: int = 12) -> None:
        self.width, self.height, self.blocked, self.cpu = max(0, int(width)), max(0, int(height)), blocked, cpu; self.history = deque(maxlen=4); self.active_goal_key = None; self.active_obstacle_epoch = None; self.active_path: tuple[Position, ...] = (); self.active_index = 0; self.replans = 0; self.cache_hits = 0

    def _blocked(self, pos: Position) -> bool:
        try: return (pos in self.blocked) if self.blocked is not None and not callable(self.blocked) else bool(self.blocked(pos)) if self.blocked is not None else False
        except Exception: return True

    def invalidate(self) -> None:
        self.active_goal_key = self.active_obstacle_epoch = None; self.active_path = (); self.active_index = 0

    def _locate(self, start: Position) -> int | None:
        if not self.active_path: return None
        if self.active_index < len(self.active_path) and self.active_path[self.active_index] == start: return self.active_index
        return next((index for index in range(self.active_index, len(self.active_path)) if self.active_path[index] == start), None)

    def _fallback(self, start: Position, goals: tuple[Position, ...], can_step: Callable[[Direction], bool] | None, forbidden: frozenset[Position]) -> Direction:
        if not goals: return Direction.CENTRE
        choices: list[tuple[int, int, Direction]] = []
        for order, direction in enumerate(CARDINALS):
            candidate = start.add(direction)
            if candidate in forbidden or not _inside(candidate, self.width, self.height) or self._blocked(candidate): continue
            try: legal = can_step is None or bool(can_step(direction))
            except Exception: legal = False
            if legal: choices.append((min(abs(candidate.x - goal.x) + abs(candidate.y - goal.y) for goal in goals), order, direction))
        return min(choices, default=(0, 0, Direction.CENTRE))[2]

    def _search(self, start: Position, goals: tuple[Position, ...], key: tuple[object, ...], epoch: int, blocked=None) -> tuple[Position, ...]:
        self.active_goal_key, self.active_obstacle_epoch, self.active_index = key, epoch, 0; self.active_path = tuple(bounded_bfs(start, goals, self.width, self.height, self.blocked if blocked is None else blocked, max_expansions=self.width * self.height, cpu_check=self.cpu if self.cpu is not None else None)) if _safe(self.cpu) else ()
        self.replans += 1; return self.active_path

    def _next(self, start: Position, goals: tuple[Position, ...], key: tuple[object, ...], epoch: int, *, can_step: Callable[[Direction], bool] | None, forbidden: frozenset[Position] = frozenset()) -> Direction:
        if start in goals:
            self.history.clear(); self.history.append(start)
            if (self.active_goal_key, self.active_obstacle_epoch) != (key, int(epoch)): self.active_path, self.active_index = (start,), 0; self.active_goal_key, self.active_obstacle_epoch = key, int(epoch); self.replans += 1
            else: self.active_index = self._locate(start) or self.active_index
            return Direction.CENTRE
        oscillating = len(self.history) == 4 and start in self.history; self.history.append(start); same = (self.active_goal_key, self.active_obstacle_epoch) == (key, int(epoch)); index = self._locate(start) if same else None
        if same and index is not None and self.active_path: self.active_index = index; self.cache_hits += 1
        else: self._search(start, goals, key, int(epoch)) if _safe(self.cpu) and not oscillating else (self.invalidate(), setattr(self, "active_goal_key", key), setattr(self, "active_obstacle_epoch", int(epoch)), setattr(self, "replans", self.replans + 1))
        if self.active_path and self.active_index + 1 < len(self.active_path):
            step = self.active_path[self.active_index + 1]; direction = start.cardinal_direction_to(step)
            try: legal = can_step is None or bool(can_step(direction))
            except Exception: legal = False
            if step not in forbidden and not self._blocked(step) and legal: return direction
            blocked_step, base = step, self.blocked
            def retry(pos: Position) -> bool:
                if pos == blocked_step: return True
                try: return (pos in base) if base is not None and not callable(base) else bool(base(pos)) if base is not None else False
                except Exception: return True
            self._search(start, goals, key, int(epoch), retry) if _safe(self.cpu) else None
            if self.active_path and len(self.active_path) > 1:
                step, direction = self.active_path[1], start.cardinal_direction_to(self.active_path[1])
                try: legal = can_step is None or bool(can_step(direction))
                except Exception: legal = False
                if step not in forbidden and not self._blocked(step) and legal: return direction
        return self._fallback(start, goals, can_step, forbidden)

    def next_direction_to_tile(self, start: Position, target: Position, obstacle_epoch: int = 0, *, can_step: Callable[[Direction], bool] | None = None) -> Direction:
        return self._next(start, (target,), ("tile", target), int(obstacle_epoch), can_step=can_step)

    def next_direction_to_adjacent(self, start: Position, target: Position, obstacle_epoch: int = 0, *, can_step: Callable[[Direction], bool] | None = None) -> Direction:
        goals = tuple(target.add(direction) for direction in CARDINALS if _inside(target.add(direction), self.width, self.height) and not self._blocked(target.add(direction)))
        return self._next(start, goals, ("adjacent", target), int(obstacle_epoch), can_step=can_step, forbidden=frozenset({target}))

    def next_direction(self, start: Position, goal: Position, obstacle_epoch: int = 0, *, can_step: Callable[[Direction], bool] | None = None) -> Direction:
        return self.next_direction_to_tile(start, goal, obstacle_epoch, can_step=can_step)
