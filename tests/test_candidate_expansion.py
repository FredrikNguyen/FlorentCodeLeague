from __future__ import annotations

import unittest

from fcode import EntityType, Environment, Position, Team

from bots.candidate.bot.comms import SCHEMA_VERSION, Slot, encode_assignment, encode_project, read_assignment, read_project, write_project
from bots.candidate.bot.player import Player
from bots.candidate.bot.core import CoreState, run_core
from bots.candidate.bot.types import ProjectState
from tests.candidate_fakes import FakeController, FakeEntity


class CandidateExpansionTest(unittest.TestCase):
    def test_secondary_assignment_waits_for_first_route_maintain(self) -> None:
        controller = FakeController(entity_type=EntityType.CORE, width=10, height=10, position=Position(1, 1))
        controller.entities[2] = FakeEntity(EntityType.BUILDER_BOT, Position(1, 2), Team.A)
        state = CoreState()

        run_core(controller, state)
        controller.advance()
        run_core(controller, state)
        controller.advance()
        self.assertIsNone(read_assignment(controller, 1))

        self.assertTrue(write_project(controller, 0, Position(4, 4), controller.round & 63, ProjectState.MAINTAIN, 10, 10))
        controller.advance()
        run_core(controller, state)
        controller.advance()
        self.assertIsNotNone(read_assignment(controller, 1))
        controller.entities[3] = FakeEntity(EntityType.BUILDER_BOT, Position(1, 3), Team.A)
        controller.advance()
        run_core(controller, state)
        controller.advance()
        self.assertIsNotNone(read_assignment(controller, 2))
        self.assertIsNone(read_assignment(controller, 3))

    def test_two_secondary_projects_are_authorized_but_route_three_waits(self) -> None:
        controller = FakeController(entity_type=EntityType.CORE, width=10, height=10, position=Position(1, 1))
        controller.entities[2] = FakeEntity(EntityType.BUILDER_BOT, Position(1, 2), Team.A)
        controller.entities[3] = FakeEntity(EntityType.BUILDER_BOT, Position(1, 3), Team.A)
        controller.entities[4] = FakeEntity(EntityType.BUILDER_BOT, Position(2, 1), Team.A)
        state = CoreState()
        run_core(controller, state)
        controller.advance()
        run_core(controller, state)
        controller.advance()
        write_project(controller, 0, Position(4, 4), controller.round & 63, ProjectState.MAINTAIN, 10, 10)
        controller.advance()
        run_core(controller, state)
        controller.advance()
        run_core(controller, state)
        controller.advance()
        self.assertIsNotNone(read_assignment(controller, 1))
        self.assertIsNotNone(read_assignment(controller, 2))
        self.assertIsNone(read_assignment(controller, 3))

    def test_delayed_ore_collision_keeps_lower_project_and_releases_other(self) -> None:
        ore = Position(4, 4)
        controller = FakeController(width=10, height=10, position=Position(1, 1), terrain={ore: Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.BUILDER_BOT, Position(1, 2), Team.A)
        controller.store[int(Slot.SCHEMA_VERSION)] = SCHEMA_VERSION
        controller.store[int(Slot.CLAIM_1)] = encode_assignment(1, 0)
        controller.store[int(Slot.CLAIM_2)] = encode_assignment(2, 0)
        controller.store[int(Slot.PROJECT_1)] = encode_project(None, 0, ProjectState.CLAIMED, 10, 10)
        controller.store[int(Slot.PROJECT_2)] = encode_project(None, 0, ProjectState.CLAIMED, 10, 10)
        lower = Player(); controller.self_id = 1; lower.run(controller); controller.advance()
        upper = Player(); controller.self_id = 2; upper.run(controller)
        controller.advance()
        self.assertEqual(ore, read_project(controller, 1).position)
        self.assertEqual(ProjectState.IDLE, read_project(controller, 2).state)

    def test_failed_secondary_route_does_not_reset_healthy_routes(self) -> None:
        controller = FakeController(entity_type=EntityType.CORE, width=10, height=10, position=Position(1, 1))
        controller.store[int(Slot.SCHEMA_VERSION)] = SCHEMA_VERSION
        for index, target, state_value, owner in (
            (0, Position(4, 4), ProjectState.MAINTAIN, 10),
            (1, Position(5, 4), ProjectState.FAILED, 11),
            (2, Position(6, 4), ProjectState.MAINTAIN, 12),
        ):
            controller.store[int(Slot.CLAIM_0 + index)] = encode_assignment(owner, 0)
            controller.store[int((Slot.PROJECT_0, Slot.PROJECT_1, Slot.PROJECT_2)[index])] = encode_project(target, 0, state_value, 10, 10)
        state = CoreState(claim_owners={0: 10, 1: 11, 2: 12})
        controller.round = 1
        run_core(controller, state)
        self.assertEqual(ProjectState.MAINTAIN, read_project(controller, 0).state)
        self.assertEqual(ProjectState.MAINTAIN, read_project(controller, 2).state)
        self.assertIn(1, state.claim_owners)
        self.assertIn(Position(5, 4), state.failed_ore_cooldowns)

    def test_four_healthy_projects_are_counted_as_the_stable_economy(self) -> None:
        ores = tuple(Position(3 + index, 4) for index in range(4))
        controller = FakeController(entity_type=EntityType.CORE, width=10, height=10, position=Position(1, 1), terrain={ore: Environment.ORE_TITANIUM for ore in ores})
        controller.store[int(Slot.SCHEMA_VERSION)] = SCHEMA_VERSION
        owners = {}
        project_slots = (Slot.PROJECT_0, Slot.PROJECT_1, Slot.PROJECT_2, Slot.PROJECT_3)
        for index, ore in enumerate(ores):
            owner = 20 + index
            owners[index] = owner
            controller.store[int(Slot.CLAIM_0 + index)] = encode_assignment(owner, 4)
            controller.store[int(project_slots[index])] = encode_project(ore, 4, ProjectState.MAINTAIN, 10, 10)
        state = CoreState(claim_owners=owners)
        controller.round = 5
        run_core(controller, state)
        self.assertEqual(4, state.snapshot.maintaining_routes)
        self.assertEqual(7, state.snapshot.desired_builders)


if __name__ == "__main__":
    unittest.main()
