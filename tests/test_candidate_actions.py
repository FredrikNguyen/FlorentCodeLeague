from __future__ import annotations

import unittest

from fcode import Direction, EntityType, Position

from bots.candidate.bot.actions import TurnActions
from tests.candidate_fakes import FakeController


class CandidateActionsTest(unittest.TestCase):
    def test_false_can_methods_prevent_mutation(self) -> None:
        controller = FakeController()
        controller.denied.update({"move", "build", "fire", "heal", "destroy", "rotate", "launch", "spawn", "convert"})
        actions = TurnActions(controller)
        self.assertFalse(actions.move(Direction.EAST))
        self.assertIsNone(actions.build_conveyor(Position(2, 1), Direction.EAST))
        self.assertFalse(actions.fire(Position(2, 1)))
        self.assertFalse(actions.heal(Position(2, 1)))
        self.assertFalse(actions.destroy(Position(2, 1)))
        self.assertFalse(actions.rotate(Direction.NORTH))
        self.assertFalse(actions.launch(Position(2, 1), Position(3, 1)))
        self.assertIsNone(actions.spawn(Position(2, 1)))
        self.assertFalse(actions.convert_ammo(3))
        self.assertEqual([], controller.calls)

    def test_cardinal_move_and_diagonal_rejection(self) -> None:
        controller = FakeController()
        actions = TurnActions(controller)
        self.assertFalse(actions.move(Direction.SOUTHEAST))
        self.assertTrue(actions.move(Direction.EAST))
        self.assertEqual(("move", Direction.EAST), controller.calls[-1])

    def test_move_action_mutual_exclusion(self) -> None:
        controller = FakeController()
        actions = TurnActions(controller)
        self.assertTrue(actions.move(Direction.EAST))
        self.assertIsNone(actions.build_conveyor(Position(3, 1), Direction.EAST))
        controller = FakeController()
        actions = TurnActions(controller)
        self.assertIsNotNone(actions.build_conveyor(Position(2, 1), Direction.EAST))
        self.assertFalse(actions.move(Direction.EAST))
        self.assertFalse(actions.fire(Position(2, 1)))

    def test_destroy_uses_engine_gate_without_consuming_wrapper_action(self) -> None:
        controller = FakeController()
        controller.entities[20] = controller.entities.pop(1)
        controller.self_id = 20
        controller.entities[21] = controller.entities[20].__class__(EntityType.CONVEYOR, Position(2, 1), controller.get_team(), Direction.EAST)
        controller.entities[22] = controller.entities[20].__class__(EntityType.CONVEYOR, Position(1, 2), controller.get_team(), Direction.EAST)
        actions = TurnActions(controller)
        self.assertTrue(actions.destroy(Position(2, 1)))
        self.assertTrue(actions.destroy(Position(1, 2)))
        self.assertFalse(actions.acted)
        self.assertEqual(2, sum(call[0] == "destroy" for call in controller.calls))

    def test_launcher_requires_can_launch(self) -> None:
        controller = FakeController(entity_type=EntityType.LAUNCHER)
        controller.denied.add("launch")
        controller.entities[2] = controller.entities[1].__class__(EntityType.BUILDER_BOT, Position(2, 1), controller.get_team())
        self.assertFalse(TurnActions(controller).launch(Position(2, 1), Position(4, 1)))


if __name__ == "__main__":
    unittest.main()
