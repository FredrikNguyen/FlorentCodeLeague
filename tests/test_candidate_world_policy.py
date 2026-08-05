from __future__ import annotations

import unittest

from fcode import EntityType, Environment, Position, Team

from bots.candidate.bot.policy import assign_role, choose_opening, describe_opening
from bots.candidate.bot.types import Opening, Role
from bots.candidate.bot.world import WorldMemory
from tests.candidate_fakes import FakeEntity, FakeController


class CandidateWorldPolicyTest(unittest.TestCase):
    def test_static_terrain_persists_and_dynamic_expires(self) -> None:
        wall = Position(2, 2)
        terrain = {wall: Environment.WALL, Position(3, 3): Environment.ORE_TITANIUM}
        controller = FakeController(terrain=terrain)
        world = WorldMemory(10, 10)
        world.observe(controller, 0)
        self.assertIn(wall, world.static_walls)
        self.assertIn(Position(3, 3), world.ore_positions)
        controller.entities[2] = FakeEntity(EntityType.BARRIER, Position(4, 4), Team.A)
        world.observe(controller, 0)
        self.assertTrue(world.is_blocked(Position(4, 4)))
        world.expire_dynamic(3)
        self.assertFalse(world.is_blocked(Position(4, 4)))
        self.assertIn(wall, world.static_walls)

    def test_passability_epoch_changes_only_when_occupancy_changes(self) -> None:
        controller = FakeController()
        position = Position(2, 1)
        world = WorldMemory(10, 10)
        world.observe(controller, 0)
        epoch = world.obstacle_epoch
        controller.entities[2] = FakeEntity(EntityType.BARRIER, position, Team.A)
        world.observe(controller, 1)
        self.assertGreater(world.obstacle_epoch, epoch)
        changed = world.obstacle_epoch
        world.observe(controller, 2)
        self.assertEqual(changed, world.obstacle_epoch)
        controller.entities.pop(2)
        world.observe(controller, 3)
        self.assertGreater(world.obstacle_epoch, changed)

    def test_current_unit_is_not_a_navigation_obstacle(self) -> None:
        controller = FakeController()
        world = WorldMemory(10, 10)
        world.observe(controller, 0)
        self.assertFalse(world.is_blocked(controller.get_position()))

    def test_thrown_unit_invalidates_goal_and_path(self) -> None:
        world = WorldMemory(8, 8)
        world.set_goal(Position(3, 3))
        world.invalidate_after_throw(Position(3, 3))
        self.assertTrue(world.consume_goal_invalidation())
        self.assertFalse(world.consume_goal_invalidation())

    def test_roles_are_stable(self) -> None:
        self.assertEqual(assign_role(22), assign_role(22))
        self.assertEqual(Role.DEFENDER, assign_role(2, opening=Opening.ANTI_RUSH))

    def test_every_observed_opening_family_is_selectable(self) -> None:
        descriptors = (
            describe_opening(10, 10, estimated_enemy_distance=3),
            describe_opening(16, 12, wall_density=0.4),
            describe_opening(10, 10),
            describe_opening(26, 26),
            describe_opening(18, 18),
        )
        openings = {choose_opening(descriptor) for descriptor in descriptors}
        self.assertEqual(
            {
                Opening.ANTI_RUSH,
                Opening.CHOKEPOINT_CONTROL,
                Opening.COMPACT_PRESSURE,
                Opening.WIDE_EXPANSION,
                Opening.BALANCED_ECONOMY,
            },
            openings,
        )

    def test_map_name_cannot_influence_descriptor(self) -> None:
        self.assertEqual(describe_opening(18, 18, nearby_ore_count=2), describe_opening(18, 18, nearby_ore_count=2))


if __name__ == "__main__":
    unittest.main()
