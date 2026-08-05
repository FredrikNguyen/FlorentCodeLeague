from __future__ import annotations

import unittest
from unittest.mock import patch

from fcode import Direction, EntityType, Position, Team

from bots.candidate.bot.navigation import Navigator, bounded_bfs
from bots.candidate.bot.world import DynamicObservation, WorldMemory


class CandidateNavigationTest(unittest.TestCase):
    def test_shortest_deterministic_empty_grid(self) -> None:
        path = bounded_bfs(Position(0, 0), Position(3, 2), 6, 6)
        self.assertEqual(5, len(path) - 1)
        self.assertEqual(Position(0, 0), path[0])
        self.assertEqual(Position(3, 2), path[-1])
        self.assertEqual(path, bounded_bfs(Position(0, 0), Position(3, 2), 6, 6))

    def test_wall_detour_and_no_path(self) -> None:
        walls = {Position(1, 0), Position(1, 1)}
        path = bounded_bfs(Position(0, 1), Position(2, 1), 3, 3, walls)
        self.assertGreater(len(path), 3)
        self.assertTrue(set(path).isdisjoint(walls))
        self.assertEqual([], bounded_bfs(Position(0, 0), Position(2, 0), 3, 1, {Position(1, 0)}))

    def test_active_path_reuse_goal_change_and_epoch_invalidation(self) -> None:
        walls: set[Position] = set()
        navigator = Navigator(8, 8, walls)
        self.assertEqual(Direction.EAST, navigator.next_direction_to_tile(Position(0, 0), Position(4, 0), 0))
        self.assertEqual(Direction.EAST, navigator.next_direction_to_tile(Position(1, 0), Position(4, 0), 0))
        self.assertGreaterEqual(navigator.cache_hits, 1)
        replans = navigator.replans
        navigator.next_direction_to_tile(Position(2, 0), Position(5, 0), 0)
        replans_after_goal = navigator.replans
        self.assertGreater(replans_after_goal, replans)
        navigator.next_direction_to_tile(Position(2, 0), Position(5, 0), 1)
        self.assertGreater(navigator.replans, replans_after_goal)
        walls.add(Position(1, 0))
        fallback = navigator.next_direction_to_tile(Position(0, 0), Position(4, 0), 2)
        self.assertIn(fallback, (Direction.SOUTH, Direction.EAST, Direction.WEST, Direction.NORTH))

    def test_blocked_step_triggers_one_deterministic_replan(self) -> None:
        walls: set[Position] = set()
        navigator = Navigator(30, 30, walls)
        navigator.next_direction(Position(0, 0), Position(29, 29), 0)
        walls.add(Position(1, 0))
        with patch("bots.candidate.bot.navigation.bounded_bfs", wraps=bounded_bfs) as search:
            direction = navigator.next_direction(Position(0, 0), Position(29, 29), 0)
        self.assertTrue(direction.is_cardinal())
        self.assertEqual(2, navigator.replans)
        self.assertEqual(1, search.call_count)

    def test_adjacent_navigation_never_enters_build_target(self) -> None:
        target = Position(4, 2)
        navigator = Navigator(8, 8, set())
        position = Position(0, 2)
        visited = {position}
        for _ in range(8):
            direction = navigator.next_direction_to_adjacent(position, target, 0)
            if direction == Direction.CENTRE:
                break
            self.assertTrue(direction.is_cardinal())
            position = position.add(direction)
            visited.add(position)
        self.assertNotIn(target, visited)
        self.assertEqual(1, abs(position.x - target.x) + abs(position.y - target.y))

    def test_already_adjacent_returns_centre(self) -> None:
        target = Position(4, 2)
        navigator = Navigator(8, 8, set())
        self.assertEqual(Direction.CENTRE, navigator.next_direction_to_adjacent(Position(3, 2), target, 0))

    def test_cpu_cutoff_returns_bounded_fallback(self) -> None:
        navigator = Navigator(30, 30, set(), cpu=lambda: 7000)
        direction = navigator.next_direction_to_tile(Position(0, 0), Position(29, 29), 0)
        self.assertIn(direction, (Direction.EAST, Direction.SOUTH, Direction.CENTRE))
        self.assertEqual((), navigator.active_path)

    def test_transient_builder_changes_navigation_not_layout_epoch(self) -> None:
        world = WorldMemory(10, 10)
        position = Position(4, 4)
        layout_epoch = world.layout_epoch
        navigation_epoch = world.navigation_epoch
        world._set_dynamic(position, DynamicObservation(EntityType.BUILDER_BOT, Team.A, 0, True))
        self.assertTrue(world.is_navigation_blocked(position))
        self.assertFalse(world.is_route_planning_blocked(position))
        self.assertGreater(world.navigation_epoch, navigation_epoch)
        self.assertEqual(layout_epoch, world.layout_epoch)
        world._remove_dynamic(position)
        self.assertEqual(layout_epoch, world.layout_epoch)

    def test_permanent_obstacle_changes_layout_epoch(self) -> None:
        world = WorldMemory(10, 10)
        position = Position(4, 4)
        layout_epoch = world.layout_epoch
        world._set_dynamic(position, DynamicObservation(EntityType.BARRIER, Team.A, 0, True))
        self.assertTrue(world.is_route_planning_blocked(position))
        self.assertGreater(world.layout_epoch, layout_epoch)

    def test_greedy_fallback_oscillation_and_edge_safety(self) -> None:
        walls = {Position(1, 0), Position(0, 1)}
        navigator = Navigator(2, 2, walls)
        self.assertEqual(Direction.CENTRE, navigator.next_direction(Position(0, 0), Position(1, 1), 0))
        navigator = Navigator(4, 4, set())
        positions = [Position(1, 1), Position(1, 2), Position(1, 1), Position(1, 2), Position(1, 1)]
        directions = [navigator.next_direction(position, Position(3, 3), 0) for position in positions]
        self.assertTrue(all(direction.is_cardinal() for direction in directions))
        self.assertEqual(Direction.SOUTH, Navigator(4, 4, set()).next_direction(Position(0, 0), Position(0, 3), 0))

    def test_expansion_bound_on_30_by_30(self) -> None:
        stats: dict[str, int] = {}
        bounded_bfs(Position(0, 0), Position(29, 29), 30, 30, {Position(x, 15) for x in range(30)}, stats=stats)
        self.assertLessEqual(stats["expansions"], 900)

if __name__ == "__main__":
    unittest.main()
