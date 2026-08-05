from __future__ import annotations

import unittest

from fcode import Direction, EntityType, GameConstants, Position, Team

from bots.candidate.bot.core import CoreState, compute_budget, desired_ammo, run_core
from bots.candidate.bot.defense import choose_defensive_build, choose_turret_type
from bots.candidate.bot.turrets import choose_fire_target, choose_launch
from bots.candidate.bot.types import Threat, ThreatKind
from bots.candidate.bot.world import WorldMemory
from tests.candidate_fakes import FakeEntity, FakeController


class CandidateCoreCombatTest(unittest.TestCase):
    def test_current_turret_constants(self) -> None:
        self.assertEqual(7, GameConstants.GUNNER_DAMAGE)
        self.assertEqual(4, GameConstants.GUNNER_AMMO_COST)
        self.assertEqual(18, GameConstants.SENTINEL_DAMAGE)
        self.assertEqual(10, GameConstants.SENTINEL_AMMO_COST)

    def test_ammo_target_is_deficit_and_reserves_survive(self) -> None:
        controller = FakeController(entity_type=EntityType.CORE, position=Position(1, 1))
        controller.entities[2] = FakeEntity(EntityType.GUNNER, Position(2, 1), Team.A, Direction.EAST)
        controller.entities[3] = FakeEntity(EntityType.SENTINEL, Position(1, 2), Team.A, Direction.EAST)
        self.assertEqual(6 * 4 + 3 * 10, desired_ammo(controller))
        budget = compute_budget(controller)
        state = run_core(controller, CoreState())
        conversions = [call for call in controller.calls if call[0] == "convert_ammo"]
        self.assertLessEqual(sum(call[1] for call in conversions), 500 - budget.construction - budget.defense - budget.liquidity)
        self.assertGreaterEqual(controller.resources, 0)
        self.assertIsNotNone(state)

    def test_no_turret_no_threat_keeps_ammo_unconverted(self) -> None:
        controller = FakeController(entity_type=EntityType.CORE)
        run_core(controller, CoreState())
        self.assertEqual([], [call for call in controller.calls if call[0] == "convert_ammo"])

    def test_geometry_driven_turret_choice(self) -> None:
        self.assertEqual(EntityType.GUNNER, choose_turret_type(lane_length=2, changing_corridor=True))
        self.assertEqual(EntityType.SENTINEL, choose_turret_type(lane_length=8, changing_corridor=False))
        self.assertEqual(EntityType.SENTINEL, choose_turret_type(wall_crossing=True))

    def test_threat_expiry_and_defense_reservations(self) -> None:
        threat = Threat(Position(4, 4), ThreatKind.BUILDER_RUSH, 10, 0, 3, EntityType.BUILDER_BOT)
        positions = (Position(1, 1), Position(2, 2), Position(3, 3))
        choice = choose_defensive_build(
            positions,
            threat=threat,
            reserved_core_exits={Position(1, 1)},
            route_cells={Position(2, 2)},
            escape_tiles={Position(3, 3)},
        )
        self.assertIsNone(choice)
        world = WorldMemory(8, 8)
        world.threats[threat.position] = threat
        self.assertEqual(1, len(world.threat_list(2)))
        self.assertEqual(0, len(world.threat_list(3)))

    def test_target_priority_and_no_ammo_safety(self) -> None:
        controller = FakeController(entity_type=EntityType.GUNNER, position=Position(1, 1))
        controller.entities[2] = FakeEntity(EntityType.CONVEYOR, Position(2, 1), Team.B, Direction.EAST, stored=True)
        controller.entities[3] = FakeEntity(EntityType.HARVESTER, Position(1, 2), Team.B)
        target = choose_fire_target(controller)
        self.assertEqual(Position(1, 2), target)
        controller.denied.add("fire")
        self.assertIsNone(choose_fire_target(controller))

    def test_bounded_launcher_destination_scoring(self) -> None:
        controller = FakeController(entity_type=EntityType.LAUNCHER, position=Position(3, 3))
        controller.entities[2] = FakeEntity(EntityType.BUILDER_BOT, Position(4, 3), Team.A)
        choice = choose_launch(
            controller,
            pickup_tiles=(Position(4, 3),),
            destinations=tuple(Position(x, 3) for x in range(10)),
            enemy_target=Position(9, 3),
        )
        self.assertIsNotNone(choice)
        self.assertGreater(choice[2], 0)


if __name__ == "__main__":
    unittest.main()
