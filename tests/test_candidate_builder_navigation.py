from __future__ import annotations

import unittest
from unittest.mock import patch

from fcode import Direction, EntityType, Environment, Position

from bots.candidate.bot.actions import TurnActions
from bots.candidate.bot.builder import BuilderStateData, _build_route, _harvester, _move
from bots.candidate.bot.navigation import Navigator
from bots.candidate.bot.types import BuilderState, RoutePlan
from bots.candidate.bot.world import WorldMemory
from tests.candidate_fakes import FakeController, FakeEntity


class CandidateBuilderNavigationTest(unittest.TestCase):
    def test_move_to_adjacent_stance_never_steps_on_build_tile(self) -> None:
        controller = FakeController(position=Position(0, 2), width=8, height=8)
        state = BuilderStateData(world=WorldMemory(8, 8), navigator=Navigator(8, 8, set()))
        target = Position(4, 2)
        for _ in range(6):
            actions = TurnActions(controller)
            _move(controller, state, target, actions, adjacent=True)
            self.assertNotEqual(target, controller.get_position())
            controller.advance()
            if abs(controller.get_position().x - target.x) + abs(controller.get_position().y - target.y) == 1:
                break
        self.assertEqual(1, abs(controller.get_position().x - target.x) + abs(controller.get_position().y - target.y))

    def test_route_builder_uses_adjacent_navigation(self) -> None:
        controller = FakeController(position=Position(1, 1), width=8, height=8)
        route = RoutePlan(
            ore=Position(6, 1),
            cells=(Position(4, 1),),
            directions=(Direction.EAST,),
            core_footprint=(Position(3, 1),),
        )
        state = BuilderStateData(world=WorldMemory(8, 8), route=route, route_index=0, state=BuilderState.ROUTE)
        with patch("bots.candidate.bot.builder._move", return_value=True) as move:
            self.assertTrue(_build_route(controller, state, TurnActions(controller)))
        self.assertTrue(move.call_args.kwargs["adjacent"])

    def test_harvester_approach_uses_adjacent_navigation(self) -> None:
        controller = FakeController(position=Position(1, 1), width=8, height=8)
        controller.terrain[Position(6, 1)] = Environment.ORE_TITANIUM
        # Keep the route visible and verified while the Builder is still far
        # from the ore tile.
        controller.entities[30] = FakeEntity(EntityType.CONVEYOR, Position(4, 1), controller.get_team(), Direction.EAST)
        route = RoutePlan(
            ore=Position(6, 1),
            cells=(Position(4, 1),),
            directions=(Direction.EAST,),
            core_footprint=(Position(5, 1),),
        )
        world = WorldMemory(8, 8)
        world.ore_positions.add(Position(6, 1))
        state = BuilderStateData(world=world, route=route, ore_target=Position(6, 1), state=BuilderState.VERIFY)
        with patch("bots.candidate.bot.builder._move", return_value=True) as move:
            self.assertTrue(_harvester(controller, state, TurnActions(controller)))
        self.assertTrue(move.call_args.kwargs["adjacent"])


if __name__ == "__main__":
    unittest.main()
