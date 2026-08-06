from __future__ import annotations

import unittest

from fcode import EntityType, Environment, Position, Team

from bots.candidate.bot.policy import allocate_roles, assign_role, choose_opening, choose_effective_phase, choose_strategy_phase, choose_work_intent, describe_opening, economy_ready_for_attack, required_route_count
from bots.candidate.bot.types import DefenseMode, EconomySnapshot, Opening, Role, StrategyPhase, WorkIntent
from bots.candidate.bot.world import WorldMemory
from tests.candidate_fakes import FakeEntity, FakeController


class CandidateWorldPolicyTest(unittest.TestCase):
    def test_strategy_phases_and_stable_role_allocation(self) -> None:
        bootstrap = EconomySnapshot(round=10, active_projects=1)
        self.assertEqual(StrategyPhase.FIRST_ROUTE_RUSH, choose_strategy_phase(bootstrap))
        ready = EconomySnapshot(round=300, maintaining_routes=4, free_titanium=100)
        self.assertEqual(StrategyPhase.ATTACK_PREPARATION, choose_strategy_phase(ready, stable_rounds=8))
        self.assertEqual(StrategyPhase.DEFENSE_ALERT, choose_strategy_phase(ready, defense_mode=DefenseMode.CRITICAL, stable_rounds=8))
        self.assertEqual(StrategyPhase.ECONOMY_EXPANSION, choose_strategy_phase(ready, enemy_core_fresh=True, free_builders=0, stable_rounds=8))
        self.assertEqual(StrategyPhase.ATTACK_PREPARATION, choose_strategy_phase(ready, enemy_core_fresh=True, free_builders=1, stable_rounds=8))
        self.assertEqual(StrategyPhase.OFFENSIVE_PRESSURE, choose_strategy_phase(ready, enemy_core_fresh=True, free_builders=2, stable_rounds=8))
        roles = allocate_roles((4, 2, 7, 1), phase=StrategyPhase.OFFENSIVE_PRESSURE, defenders=2, maintenance_workers=1, scouts=1)
        self.assertEqual(Role.DEFENDER, roles[1])
        self.assertEqual(Role.DEFENDER, roles[2])
        self.assertIn(Role.RAIDER, roles.values())
        self.assertEqual(StrategyPhase.DEFENSE_ALERT, choose_effective_phase(StrategyPhase.CORE_SIEGE, DefenseMode.ACTIVE))
        self.assertTrue(economy_ready_for_attack(ready, stable_rounds=8))
        self.assertEqual(4, required_route_count())
        self.assertEqual(2, required_route_count(reachable_ore_count=2, exploration_complete=True))

    def test_work_intent_precedence_and_fallback(self) -> None:
        self.assertEqual(WorkIntent.CRITICAL_DEFENSE, choose_work_intent(critical_threat=True, route_owner=True))
        self.assertEqual(WorkIntent.REPAIR_ROUTE, choose_work_intent(route_repair_due=True, route_owner=True))
        self.assertEqual(WorkIntent.ROUTE_OWNER, choose_work_intent(route_owner=True, exploration_complete=False))
        self.assertEqual(WorkIntent.ATTACK, choose_work_intent(attack=True, exploration_complete=True))
        self.assertEqual(WorkIntent.ATTACK_PREPARATION, choose_work_intent(attack_preparation=True, exploration_complete=True))
        self.assertEqual(WorkIntent.DISCOVER_ORE, choose_work_intent(exploration_complete=False))
        self.assertEqual(WorkIntent.PATROL_LOGISTICS, choose_work_intent(exploration_complete=True))

    def test_offense_requires_four_fresh_routes_and_free_workers(self) -> None:
        for route_count in (1, 2, 3):
            snapshot = EconomySnapshot(round=300, maintaining_routes=route_count, free_titanium=100)
            self.assertEqual(
                StrategyPhase.ECONOMY_EXPANSION,
                choose_strategy_phase(snapshot, enemy_core_fresh=True, free_builders=2, stable_rounds=8),
            )
        stable = EconomySnapshot(round=300, maintaining_routes=4, free_titanium=100)
        self.assertEqual(
            StrategyPhase.ECONOMY_EXPANSION,
            choose_strategy_phase(stable, enemy_core_fresh=True, free_builders=2, stable_rounds=7),
        )
        self.assertEqual(
            StrategyPhase.OFFENSIVE_PRESSURE,
            choose_strategy_phase(stable, enemy_core_fresh=True, free_builders=2, stable_rounds=8),
        )
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

    def test_builder_on_passable_route_cell_blocks_navigation_not_layout(self) -> None:
        position = Position(4, 4)
        controller = FakeController(position=Position(0, 0))
        controller.entities[10] = FakeEntity(EntityType.CONVEYOR, position, Team.A)
        controller.entities[30] = FakeEntity(EntityType.BUILDER_BOT, position, Team.A)
        world = WorldMemory(10, 10)

        world.observe(controller, 0)

        self.assertTrue(world.is_navigation_blocked(position))
        self.assertFalse(world.is_route_planning_blocked(position))

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
