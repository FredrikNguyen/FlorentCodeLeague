from __future__ import annotations

import unittest
from unittest.mock import patch

from fcode import Direction, EntityType, Environment, Position, Team

from bots.candidate.bot.builder import BuilderStateData, run_builder
from bots.candidate.bot.comms import CLAIM_SLOTS, PROJECT_SLOTS, SCHEMA_VERSION, Slot, encode_assignment, encode_project, read_project
from bots.candidate.bot.logistics import directions_for_route, plan_core_outward_route
from bots.candidate.bot.types import BuilderState, ProjectState, Role, RoutePlan, WorkIntent
from tests.candidate_fakes import FakeController, FakeEntity


def seed_project(controller: FakeController, target: Position, *, state: ProjectState = ProjectState.CLAIMED) -> None:
    controller.store[int(Slot.SCHEMA_VERSION)] = SCHEMA_VERSION
    controller.store[int(Slot.CLAIM_0)] = encode_assignment(1, controller.round & 63)
    controller.store[int(Slot.PROJECT_0)] = encode_project(target, controller.round & 63, state, controller.width, controller.height)


def one_link_route() -> RoutePlan:
    return RoutePlan(Position(0, 1), (Position(2, 1),), (Direction.EAST,), (Position(3, 1),))


class CandidateRouteFSMTest(unittest.TestCase):
    def test_straight_routes_enter_each_side_of_core(self) -> None:
        footprint = (Position(3, 3), Position(4, 3), Position(3, 4), Position(4, 4))
        for ore in (Position(3, 1), Position(6, 3), Position(3, 6), Position(1, 3)):
            route = plan_core_outward_route(ore, footprint, 8, 8)
            self.assertIsNotNone(route)
            assert route is not None
            self.assertIn(route.cells[-1].add(route.directions[-1]), set(footprint))
            self.assertEqual(route.directions, directions_for_route(route.cells, footprint))

    def test_route_around_wall(self) -> None:
        ore, footprint = Position(0, 3), (Position(5, 3), Position(6, 3), Position(5, 4), Position(6, 4))
        wall = {Position(x, 2) for x in range(1, 5)}
        route = plan_core_outward_route(ore, footprint, 8, 8, wall)
        self.assertIsNotNone(route)
        assert route is not None
        self.assertTrue(set(route.cells).isdisjoint(wall))

    def test_harvester_waits_for_receiver_verification(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 1), terrain={Position(0, 1): Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
        route = one_link_route()
        state = BuilderStateData(role=Role.ECONOMY, state=BuilderState.DELIVER, route=route, route_index=-1, ore_target=route.ore)
        run_builder(controller, state)
        self.assertIsNone(controller.get_tile_building_id(route.ore))
        self.assertTrue(any(call[0] == "build" and call[1] == EntityType.CONVEYOR for call in controller.calls))

    def test_matching_conveyor_is_reused(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 1), terrain={Position(0, 1): Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
        controller.entities[10] = FakeEntity(EntityType.CONVEYOR, Position(2, 1), Team.A, Direction.EAST)
        seed_project(controller, Position(0, 1))
        state = BuilderStateData(role=Role.ECONOMY, route=one_link_route(), route_index=0, claim_slot=0)
        run_builder(controller, state)
        self.assertEqual(-1, state.route_index)
        self.assertEqual([], [call for call in controller.calls if call[0] in ("build", "destroy")])

    def test_wrong_direction_friendly_conveyor_is_rebuilt(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 1), terrain={Position(0, 1): Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
        controller.entities[10] = FakeEntity(EntityType.CONVEYOR, Position(2, 1), Team.A, Direction.NORTH)
        seed_project(controller, Position(0, 1))
        state = BuilderStateData(role=Role.ECONOMY, route=one_link_route(), route_index=0, claim_slot=0)
        run_builder(controller, state)
        self.assertIn(("destroy", Position(2, 1)), controller.calls)
        controller.advance()
        run_builder(controller, state)
        self.assertIn(("build", EntityType.CONVEYOR, Position(2, 1), Direction.EAST), controller.calls)

    def test_enemy_occupied_route_cell_replans_and_is_bounded(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 1), terrain={Position(0, 1): Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
        controller.entities[10] = FakeEntity(EntityType.CONVEYOR, Position(2, 1), Team.B, Direction.EAST)
        seed_project(controller, Position(0, 1))
        state = BuilderStateData(role=Role.ECONOMY, route=one_link_route(), route_index=0, claim_slot=0)
        run_builder(controller, state)
        self.assertIsNone(state.route)
        self.assertEqual("occupied_enemy", state.route_failure_reason)
        self.assertEqual([], [call for call in controller.calls if call[0] == "destroy"])

    def test_other_builder_does_not_block_static_route_planning(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 1), terrain={Position(0, 1): Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
        controller.entities[30] = FakeEntity(EntityType.BUILDER_BOT, Position(2, 1), Team.A)
        seed_project(controller, Position(0, 1))
        state = BuilderStateData(role=Role.ECONOMY, claim_slot=0)
        run_builder(controller, state)
        self.assertIsNotNone(state.route)
        assert state.route is not None
        self.assertIn(Position(2, 1), state.route.cells)
        self.assertEqual("transient_builder_occupancy", state.route_failure_reason)

    def test_current_builder_tile_remains_available_for_route_planning(self) -> None:
        controller = FakeController(width=4, height=2, position=Position(1, 0), terrain={Position(0, 0): Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(2, 0), Team.A)
        seed_project(controller, Position(0, 0))
        state = BuilderStateData(role=Role.ECONOMY, claim_slot=0)
        run_builder(controller, state)
        self.assertIsNotNone(state.route)
        assert state.route is not None
        self.assertIn(Position(1, 0), state.route.cells)

    def test_transient_builders_wait_without_changing_static_route(self) -> None:
        ore = Position(0, 0)
        controller = FakeController(width=5, height=1, position=Position(1, 0), terrain={ore: Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 0), Team.A)
        controller.entities[30] = FakeEntity(EntityType.BUILDER_BOT, Position(2, 0), Team.A)
        seed_project(controller, ore)
        state = BuilderStateData(role=Role.ECONOMY, claim_slot=0)

        run_builder(controller, state)

        self.assertIsNotNone(state.route)
        assert state.route is not None
        self.assertEqual((Position(1, 0), Position(2, 0)), state.route.cells)
        self.assertEqual("transient_builder_occupancy", state.route_failure_reason)
        self.assertEqual(1, state.blocked_steps)
        self.assertEqual([], [call for call in controller.calls if call[0] == "build"])

        controller.entities[30].position = ore
        controller.advance()
        run_builder(controller, state)

        self.assertIn(("build", EntityType.CONVEYOR, Position(2, 0), Direction.EAST), controller.calls)
        self.assertEqual(0, state.route_replans)

    def test_scout_leaves_known_ore_instead_of_occupying_harvester_target(self) -> None:
        ore = Position(1, 1)
        controller = FakeController(width=6, height=6, position=ore, terrain={ore: Environment.ORE_TITANIUM})
        state = BuilderStateData(role=Role.SCOUT, last_position=ore)
        run_builder(controller, state)
        self.assertNotEqual(ore, controller.get_position())
        self.assertTrue(any(call[0] == "move" for call in controller.calls))
        self.assertEqual(WorkIntent.DISCOVER_ORE, state.work_intent)

    def test_scout_does_not_enter_known_ore_on_unreachable_waypoint_path(self) -> None:
        ore = Position(2, 1)
        controller = FakeController(width=6, height=6, position=Position(2, 2), terrain={ore: Environment.ORE_TITANIUM})
        state = BuilderStateData(role=Role.SCOUT, last_position=controller.get_position())
        for _ in range(6):
            run_builder(controller, state)
            self.assertNotEqual(ore, controller.get_position())
            controller.advance()

    def test_targetless_delayed_claim_keeps_builder_scouting(self) -> None:
        controller = FakeController(width=6, height=6, position=Position(1, 1))
        controller.store[int(Slot.SCHEMA_VERSION)] = SCHEMA_VERSION
        controller.store[int(Slot.CLAIM_1)] = encode_assignment(1, controller.round & 63)
        controller.store[int(Slot.PROJECT_1)] = encode_project(None, controller.round & 63, ProjectState.CLAIMED, controller.width, controller.height)
        state = BuilderStateData(role=Role.SCOUT)

        run_builder(controller, state)

        self.assertEqual(WorkIntent.DISCOVER_ORE, state.work_intent)
        self.assertEqual(0, state.project_count)
        self.assertTrue(any(call[0] == "move" for call in controller.calls))

    def test_route_owner_moves_while_incremental_search_is_pending(self) -> None:
        ore = Position(5, 5)
        controller = FakeController(width=8, height=8, position=Position(1, 1), terrain={ore: Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(6, 6), Team.A)
        seed_project(controller, ore)
        state = BuilderStateData(role=Role.ECONOMY, claim_slot=0)

        def partial_search(*args, **kwargs):
            search_state = kwargs["search_state"]
            search_state["complete"] = False
            return None

        with patch("bots.candidate.bot.builder.plan_core_outward_route", side_effect=partial_search):
            run_builder(controller, state)

        self.assertEqual(WorkIntent.ROUTE_OWNER, state.work_intent)
        self.assertIsNotNone(state.route_search)
        self.assertTrue(any(call[0] == "move" for call in controller.calls))

    def test_unassigned_builder_repairs_visible_one_cell_logistics_gap(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(2, 0))
        controller.entities[10] = FakeEntity(EntityType.CONVEYOR, Position(1, 1), Team.A, Direction.EAST)
        controller.entities[11] = FakeEntity(EntityType.CONVEYOR, Position(3, 1), Team.A, Direction.EAST)
        controller.store[int(Slot.SCHEMA_VERSION)] = SCHEMA_VERSION
        for index in range(4):
            controller.store[int(CLAIM_SLOTS[index])] = encode_assignment(100 + index, 0)
            controller.store[int(PROJECT_SLOTS[index])] = encode_project(Position(4 + index, 4), 0, ProjectState.MAINTAIN, controller.width, controller.height)
        state = BuilderStateData(role=Role.SCOUT, last_position=controller.get_position())
        run_builder(controller, state)
        self.assertEqual(WorkIntent.PATROL_LOGISTICS, state.work_intent)
        self.assertIn(("build", EntityType.CONVEYOR, Position(2, 1), Direction.EAST), controller.calls)

    def test_free_builder_takes_fresh_core_critical_threat_before_patrol(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 3))
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(1, 1), Team.A)
        controller.entities[3] = FakeEntity(EntityType.BUILDER_BOT, Position(1, 2), Team.B)
        state = BuilderStateData(role=Role.SCOUT, last_position=controller.get_position())
        run_builder(controller, state)
        self.assertEqual(WorkIntent.CRITICAL_DEFENSE, state.work_intent)

    def test_broken_middle_link_is_repaired(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(2, 0), terrain={Position(0, 1): Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(4, 1), Team.A)
        controller.entities[11] = FakeEntity(EntityType.CONVEYOR, Position(1, 1), Team.A, Direction.EAST)
        controller.entities[10] = FakeEntity(EntityType.CONVEYOR, Position(3, 1), Team.A, Direction.EAST)
        route = RoutePlan(Position(0, 1), (Position(1, 1), Position(2, 1), Position(3, 1)), (Direction.EAST,) * 3, (Position(4, 1),))
        state = BuilderStateData(role=Role.REPAIR, state=BuilderState.MAINTAIN, route=route, route_index=-1, last_delivery_round=1)
        run_builder(controller, state)
        self.assertIn(("build", EntityType.CONVEYOR, Position(2, 1), Direction.EAST), controller.calls)

    def test_correct_final_link_is_not_destroyed_by_unrelated_spending(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 1))
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
        controller.entities[10] = FakeEntity(EntityType.CONVEYOR, Position(2, 1), Team.A, Direction.EAST, stored=True)
        state = BuilderStateData(role=Role.REPAIR, state=BuilderState.DELIVER, route=one_link_route(), route_index=-1, delivery_started_round=0, last_resource_total=100, last_resource_round=0)
        controller.resources = 140
        run_builder(controller, state)
        self.assertEqual([], [call for call in controller.calls if call[0] == "destroy"])

    def test_first_confirmed_delivery_moves_to_maintain(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 1))
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
        controller.entities[10] = FakeEntity(EntityType.CONVEYOR, Position(2, 1), Team.A, Direction.EAST, stored=True)
        state = BuilderStateData(role=Role.REPAIR, state=BuilderState.DELIVER, route=one_link_route(), route_index=-1, delivery_started_round=0)
        run_builder(controller, state)
        controller.entities[10].stored = False
        controller.advance()
        run_builder(controller, state)
        self.assertEqual(1, state.last_delivery_round)
        self.assertEqual(BuilderState.MAINTAIN, state.state)

    def test_delivery_timeout_fails_after_three_bounded_attempts(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 1))
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
        controller.entities[10] = FakeEntity(EntityType.CONVEYOR, Position(2, 1), Team.A, Direction.EAST)
        state = BuilderStateData(role=Role.REPAIR, state=BuilderState.DELIVER, route=one_link_route(), route_index=-1, delivery_started_round=0)
        controller.round = 12
        for _ in range(3):
            run_builder(controller, state)
            controller.advance()
        self.assertEqual("delivery_timeout", state.route_failure_reason)
        self.assertIsNone(state.route)
        project = read_project(controller, 0)
        self.assertTrue(project is None or project.state in (ProjectState.IDLE, ProjectState.FAILED))

    def test_active_project_heartbeat_keeps_stale_assignment_claim(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 1), terrain={Position(0, 1): Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
        controller.round = 32
        controller.store[int(Slot.SCHEMA_VERSION)] = SCHEMA_VERSION
        controller.store[int(Slot.CLAIM_0)] = encode_assignment(1, 0)
        controller.store[int(Slot.PROJECT_0)] = encode_project(Position(0, 1), 31, ProjectState.BUILDING, controller.width, controller.height)
        state = BuilderStateData(role=Role.ECONOMY, route=one_link_route(), route_index=0, claim_slot=0, ore_target=Position(0, 1))
        run_builder(controller, state)
        self.assertEqual(0, state.claim_slot)
        self.assertIn(("build", EntityType.CONVEYOR, Position(2, 1), Direction.EAST), controller.calls)

    def test_build_path_approaches_without_entering_target(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 1), terrain={Position(4, 1): Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(6, 1), Team.A)
        route = RoutePlan(Position(4, 1), (Position(5, 1),), (Direction.EAST,), (Position(6, 1),))
        state = BuilderStateData(role=Role.ECONOMY, state=BuilderState.ROUTE, route=route, route_index=0, ore_target=route.ore)
        seed_project(controller, route.ore)
        for _ in range(4):
            run_builder(controller, state)
            self.assertNotEqual(route.cells[0], controller.get_position())
            controller.advance()

    def test_iteration7_integrates_phase_strategy_and_keeps_launchers_off(self) -> None:
        from bots.candidate.bot.feature_flags import ENABLE_DEFENSIVE_BUILDING, ENABLE_FORWARD_GUNNERS, ENABLE_LAUNCHERS, ENABLE_PHASE_STRATEGY, ENABLE_RAIDS, ENABLE_REDUNDANCY, ENABLE_SECONDARY_EXPANSION

        self.assertTrue(ENABLE_SECONDARY_EXPANSION)
        self.assertTrue(ENABLE_DEFENSIVE_BUILDING)
        self.assertTrue(ENABLE_RAIDS)
        self.assertTrue(ENABLE_FORWARD_GUNNERS)
        self.assertTrue(ENABLE_PHASE_STRATEGY)
        self.assertFalse(any((ENABLE_REDUNDANCY, ENABLE_LAUNCHERS)))


if __name__ == "__main__":
    unittest.main()
