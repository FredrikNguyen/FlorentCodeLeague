from __future__ import annotations

import unittest
from unittest.mock import patch

from fcode import Direction, EntityType, Environment, Position, Team

from bots.candidate.bot.comms import PROJECT_SLOTS, SCHEMA_VERSION, Slot, claim_slot, encode_alert, encode_assignment, encode_project, read_assignment, read_project
from bots.candidate.bot.player import Player
from bots.candidate.bot.builder import BuilderStateData, run_builder
from bots.candidate.bot.core import CoreState
from bots.candidate.bot.types import BuilderState, Opening, Role, RoutePlan
from bots.candidate.bot.types import ProjectState
from tests.candidate_fakes import FakeEntity, FakeController


class BrokenController(FakeController):
    def get_entity_type(self, entity_id=None):
        raise RuntimeError("scripted failure")


class ExpensiveHarvesterController(FakeController):
    def get_harvester_cost(self) -> int:
        return 3000


def _install_route(controller: FakeController, *, stored_final: bool = False) -> RoutePlan:
    controller.entities[2] = FakeEntity(EntityType.CORE, Position(4, 4), Team.A)
    ore = Position(0, 2)
    cells = (Position(1, 2), Position(2, 2), Position(3, 2), Position(3, 3), Position(3, 4))
    directions = (Direction.EAST, Direction.EAST, Direction.SOUTH, Direction.SOUTH, Direction.EAST)
    footprint = (Position(4, 4), Position(5, 4), Position(4, 5), Position(5, 5))
    for entity_id, (position, direction) in enumerate(zip(cells, directions), 10):
        controller.entities[entity_id] = FakeEntity(EntityType.CONVEYOR, position, Team.A, direction, stored=stored_final and position == cells[-1])
    controller.entities[20] = FakeEntity(EntityType.HARVESTER, ore, Team.A)
    return RoutePlan(ore, cells, directions, footprint)


def _one_link_route() -> RoutePlan:
    return RoutePlan(Position(0, 1), (Position(2, 1),), (Direction.EAST,), (Position(3, 1),))


def _seed_assignment(controller: FakeController, index: int, owner: int, target: Position | None, epoch: int = 0, state: ProjectState = ProjectState.CLAIMED) -> None:
    controller.store[int(Slot.SCHEMA_VERSION)] = SCHEMA_VERSION
    controller.store[int(claim_slot(index))] = encode_assignment(owner, epoch)
    controller.store[int(PROJECT_SLOTS[index])] = encode_project(target, epoch, state, controller.width, controller.height)


class CandidatePlayerTest(unittest.TestCase):
    def test_all_entity_types_dispatch_and_infrastructure_is_inert(self) -> None:
        for entity_type in EntityType:
            controller = FakeController(entity_type=entity_type)
            player = Player()
            player.run(controller)
            if entity_type in (EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.HARVESTER, EntityType.BARRIER):
                self.assertEqual([], [call for call in controller.calls if call[0] not in ("write_store",)])

    def test_no_exception_escapes_and_fourth_failure_is_silent(self) -> None:
        controller = BrokenController()
        player = Player()
        for _ in range(4):
            player.run(controller)
        dots = [call for call in controller.calls if call[0] == "dot"]
        self.assertEqual(3, len(dots))
        self.assertTrue(player._safe_mode)

    def test_fault_injection_scenarios_are_safe(self) -> None:
        scenarios = [
            FakeController(terrain={Position(2, 1): Environment.WALL}),
            FakeController(width=2, height=2, position=Position(0, 0)),
            FakeController(position=Position(0, 0)),
        ]
        scenarios[0].resources = 0
        scenarios[0].ammo = 0
        scenarios[0].cpu = 7000
        for controller in scenarios:
            controller.denied.add("move")
            Player().run(controller)

    def test_defender_reserves_opening_economy(self) -> None:
        controller = FakeController()
        controller.round = 100
        run_builder(controller, BuilderStateData(role=Role.DEFENDER))
        self.assertEqual([], [call for call in controller.calls if call[0] == "build"])

    def test_player_observes_real_delivery_and_transitions_to_maintain(self) -> None:
        controller = FakeController(width=10, height=10, position=Position(2, 4))
        route = _install_route(controller)
        controller.round = 1
        controller.resources = 100
        state = BuilderStateData(
            role=Role.REPAIR,
            state=BuilderState.DELIVER,
            route=route,
            route_index=-1,
            delivery_started_round=0,
            last_resource_total=100,
            last_resource_round=0,
        )
        player = Player()
        player._builder_state = state
        player.run(controller)
        self.assertIsNone(state.last_delivery_round)
        self.assertEqual(BuilderState.DELIVER, state.state)
        controller.entities[14].stored = True
        controller.advance()
        player.run(controller)
        self.assertIsNone(state.last_delivery_round)
        controller.entities[14].stored = False
        controller.advance()
        player.run(controller)
        self.assertEqual(3, state.last_delivery_round)
        self.assertEqual(BuilderState.MAINTAIN, state.state)

    def test_unrelated_global_income_does_not_mark_delivery(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 1))
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
        controller.entities[10] = FakeEntity(EntityType.CONVEYOR, Position(2, 1), Team.A, Direction.EAST)
        route = _one_link_route()
        controller.round, controller.resources = 1, 120
        state = BuilderStateData(role=Role.REPAIR, state=BuilderState.DELIVER, route=route, route_index=-1, delivery_started_round=0, last_resource_total=100, last_resource_round=0)
        player = Player()
        player._builder_state = state
        player.run(controller)
        self.assertIsNone(state.last_delivery_round)
        self.assertEqual(BuilderState.DELIVER, state.state)
        self.assertEqual([], [call for call in controller.calls if call[0] in ("build", "destroy")])

    def test_backlog_and_timeout_teardown_then_rebuild_through_player(self) -> None:
        for timeout, stored in ((False, True), (True, False)):
            controller = FakeController(width=8, height=8, position=Position(1, 1))
            controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
            controller.entities[10] = FakeEntity(EntityType.CONVEYOR, Position(2, 1), Team.A, Direction.EAST, stored=stored)
            controller.round = 20 if timeout else 2
            state = BuilderStateData(role=Role.REPAIR, state=BuilderState.DELIVER, route=_one_link_route(), route_index=-1, delivery_started_round=0, last_delivery_round=1 if timeout else None, last_resource_total=500, last_resource_round=controller.round - 1, backlog_rounds=0 if timeout else 3)
            player = Player()
            player._builder_state = state
            player.run(controller)
            self.assertEqual([], [call for call in controller.calls if call[0] == "destroy"])
            self.assertEqual([], [call for call in controller.calls if call[0] == "build"])
            controller.advance()
            player.run(controller)
            self.assertEqual([], [call for call in controller.calls if call[0] == "destroy"])

    def test_player_repairs_a_destroyed_link_and_marks_timeout(self) -> None:
        controller = FakeController(width=8, height=8, position=Position(1, 0))
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
        controller.entities[10] = FakeEntity(EntityType.CONVEYOR, Position(2, 1), Team.A, Direction.EAST)
        route = RoutePlan(
            Position(0, 1),
            (Position(1, 1), Position(2, 1)),
            (Direction.EAST, Direction.EAST),
            (Position(3, 1), Position(4, 1), Position(3, 2), Position(4, 2)),
        )
        state = BuilderStateData(role=Role.REPAIR, state=BuilderState.MAINTAIN, route=route, route_index=-1, last_delivery_round=1)
        controller.round = 2
        player = Player()
        player._builder_state = state
        player.run(controller)
        self.assertIn(("build", EntityType.CONVEYOR, Position(1, 1), Direction.EAST), controller.calls)

        timeout_controller = FakeController(width=8, height=8, position=Position(1, 0))
        timeout_controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 1), Team.A)
        timeout_controller.entities[10] = FakeEntity(EntityType.CONVEYOR, Position(1, 1), Team.A, Direction.EAST)
        timeout_controller.entities[11] = FakeEntity(EntityType.CONVEYOR, Position(2, 1), Team.A, Direction.EAST)
        timeout_controller.entities[12] = FakeEntity(EntityType.HARVESTER, Position(0, 1), Team.A)
        timeout_controller.round = 20
        timeout_controller.resources = 100
        timeout_state = BuilderStateData(
            role=Role.REPAIR,
            state=BuilderState.DELIVER,
            route=route,
            route_index=-1,
            delivery_started_round=0,
            last_resource_total=100,
            last_resource_round=19,
        )
        timeout_player = Player()
        timeout_player._builder_state = timeout_state
        timeout_player.run(timeout_controller)
        self.assertEqual(1, timeout_state.repair_attempts)

    def test_player_heartbeats_claim_for_any_tactical_role_and_rejects_stale_owner(self) -> None:
        controller = FakeController(width=10, height=10, position=Position(1, 1), terrain={Position(4, 4): Environment.ORE_TITANIUM})
        controller.round = 8
        _seed_assignment(controller, 0, 1, Position(4, 4))
        state = BuilderStateData(role=Role.DEFENDER)
        player = Player()
        player._builder_state = state
        player.run(controller)
        self.assertEqual(0, state.claim_slot)
        self.assertTrue(any(call[0] == "write_store" and call[1] == int(Slot.PROJECT_0) for call in controller.calls))
        controller.advance()
        refreshed = read_assignment(controller, 0)
        self.assertEqual(0, refreshed.generation)

        stale = FakeController(width=10, height=10, position=Position(1, 1), terrain={Position(4, 4): Environment.ORE_TITANIUM})
        stale.round = 40
        _seed_assignment(stale, 0, 1, Position(4, 4))
        stale_state = BuilderStateData(role=Role.SIEGE, claim_slot=0)
        stale_player = Player()
        stale_player._builder_state = stale_state
        stale_player.run(stale)
        self.assertIsNone(stale_state.claim_slot)
        self.assertEqual([], [call for call in stale.calls if call[0] == "write_store" and call[1] == int(Slot.CLAIM_0)])

    def test_player_core_reassigns_wrap_safe_stale_owner_and_observes_opening(self) -> None:
        controller = FakeController(entity_type=EntityType.CORE, width=10, height=10, position=Position(1, 1))
        controller.round = 40
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(3, 3), Team.B)
        for index, owner in enumerate((101, 102, 103)):
            _seed_assignment(controller, index, owner, Position(0, 0))
        state = CoreState(claim_owners={0: 101, 1: 102, 2: 103})
        player = Player()
        player._core_state = state
        player.run(controller)
        self.assertEqual(10, state.claim_owners[0])
        self.assertTrue(any(call[0] == "write_store" and call[1] == int(Slot.CLAIM_0) for call in controller.calls))
        self.assertEqual(Opening.ANTI_RUSH, state.opening)
        controller.advance()
        replacement = read_assignment(controller, 0)
        self.assertEqual(10, replacement.owner_id)

    def test_player_route_start_and_late_game_spending_are_gated(self) -> None:
        controller = FakeController(width=10, height=10, position=Position(1, 1), terrain={Position(4, 4): Environment.ORE_TITANIUM})
        controller.resources = 10
        _seed_assignment(controller, 0, 1, Position(4, 4))
        player = Player()
        player.run(controller)
        self.assertEqual([], [call for call in controller.calls if call[0] == "build"])

        late = FakeController(width=10, height=10, position=Position(1, 1))
        late.round = 900
        late_player = Player()
        late_player._builder_state = BuilderStateData(role=Role.DEFENDER)
        late_player.run(late)
        self.assertEqual([], [call for call in late.calls if call[0] == "build"])

    def test_builder_reserve_boundary_rejects_harvester_spend(self) -> None:
        controller = FakeController(width=10, height=10, position=Position(1, 2))
        route = _install_route(controller)
        controller.entities.pop(20)
        controller.resources = 123
        state = BuilderStateData(role=Role.REPAIR, state=BuilderState.DELIVER, route=route, route_index=-1, ore_target=route.ore)
        player = Player()
        player._builder_state = state
        player.run(controller)
        self.assertEqual([], [call for call in controller.calls if call[0] == "build"])

    def test_builder_accepts_fourth_live_project_and_keeps_project_state_bounded(self) -> None:
        terrain = {Position(3 + index, 4): Environment.ORE_TITANIUM for index in range(4)}
        controller = FakeController(width=10, height=10, position=Position(1, 1), terrain=terrain)
        controller.entities[2] = FakeEntity(EntityType.BUILDER_BOT, Position(1, 2), Team.A)
        controller.entities[3] = FakeEntity(EntityType.BUILDER_BOT, Position(1, 3), Team.A)
        controller.entities[4] = FakeEntity(EntityType.BUILDER_BOT, Position(2, 1), Team.A)
        controller.entities[20] = FakeEntity(EntityType.CORE, Position(7, 7), Team.A)
        owners = (1, 2, 3, 4); players = tuple(Player() for _ in owners)
        for index, (owner, player) in enumerate(zip(owners, players)):
            _seed_assignment(controller, index, owner, Position(3 + index, 4))
            controller.self_id = owner; player.run(controller); controller.advance()
        controller.self_id = 1; player = Player(); player.run(controller); state = player._builder_state
        self.assertIsNotNone(state.route)
        self.assertLessEqual(4, sum(read_project(controller, index).state != ProjectState.IDLE for index in range(4)))

    def test_reserved_project_can_replan_at_shared_cap(self) -> None:
        controller = FakeController(width=10, height=10, position=Position(1, 1), terrain={Position(0, 1): Environment.ORE_TITANIUM})
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(4, 4), Team.A)
        ore = Position(0, 1)
        route = RoutePlan(ore, (Position(2, 1),), (Direction.EAST,), (Position(3, 4), Position(4, 4)))
        for index, owner in enumerate((1, 2, 3, 4)):
            _seed_assignment(controller, index, owner, ore, state=ProjectState.BUILDING)
        state = BuilderStateData(role=Role.ECONOMY, claim_slot=0, project_count=1, route=_one_link_route(), route_index=0, blocked_steps=3)
        player = Player()
        player._builder_state = state
        with patch("bots.candidate.bot.builder.plan_core_outward_route", return_value=route) as planner:
            player.run(controller)
        self.assertTrue(planner.called)
        self.assertEqual(route, state.route)
        self.assertEqual(1, state.project_count)
        self.assertIn(("build", EntityType.CONVEYOR, Position(2, 1), Direction.EAST), controller.calls)
        self.assertEqual(4, sum(read_project(controller, index).state != ProjectState.IDLE for index in range(4)))

    def test_three_shared_projects_gate_all_new_project_builds(self) -> None:
        def seed_projects(controller: FakeController) -> None:
            for index, owner in enumerate((101, 102, 103, 104)):
                _seed_assignment(controller, index, owner, Position(4 + index, 4), controller.round & 63, ProjectState.BUILDING)

        splitter = FakeController(width=10, height=10, position=Position(1, 0))
        seed_projects(splitter)
        splitter_state = BuilderStateData(role=Role.REPAIR, state=BuilderState.MAINTAIN, route=_install_route(splitter), route_index=-1, last_delivery_round=1, claim_slot=0)
        splitter_player = Player()
        splitter_player._builder_state = splitter_state
        splitter_player.run(splitter)
        self.assertEqual([], [call for call in splitter.calls if call[0] == "build" and call[1] == EntityType.SPLITTER])

        barrier = FakeController(width=10, height=10, position=Position(2, 2))
        barrier.round = 240
        seed_projects(barrier)
        barrier.entities[2] = FakeEntity(EntityType.CORE, Position(6, 6), Team.A)
        barrier.entities[3] = FakeEntity(EntityType.BUILDER_BOT, Position(3, 2), Team.B)
        barrier_player = Player()
        barrier_player._builder_state = BuilderStateData(role=Role.DEFENDER, claim_slot=0)
        barrier_player.run(barrier)
        self.assertEqual([], [call for call in barrier.calls if call[0] == "build" and call[1] in (EntityType.BARRIER, EntityType.GUNNER, EntityType.SENTINEL)])

        launcher = FakeController(width=10, height=10, position=Position(2, 2))
        launcher.round = 100
        seed_projects(launcher)
        launcher.entities[30] = FakeEntity(EntityType.CORE, Position(8, 8), Team.B)
        launcher.store[int(Slot.RALLY)] = encode_alert(Position(8, 8), 10, 108)
        launcher_player = Player()
        launcher_player._builder_state = BuilderStateData(role=Role.SIEGE, claim_slot=0)
        launcher_player.run(launcher)
        self.assertEqual([], [call for call in launcher.calls if call[0] == "build" and call[1] == EntityType.LAUNCHER])

    def test_builder_rejects_late_negative_payback(self) -> None:
        controller = ExpensiveHarvesterController(width=10, height=10, position=Position(1, 2))
        route = _install_route(controller)
        controller.entities.pop(20)
        controller.round, controller.resources = 900, 10000
        state = BuilderStateData(role=Role.REPAIR, state=BuilderState.DELIVER, route=route, route_index=-1, ore_target=route.ore)
        player = Player()
        player._builder_state = state
        player.run(controller)
        self.assertEqual([], [call for call in controller.calls if call[0] == "build"])

    def test_iteration5_defense_is_reactive_and_other_advanced_builds_stay_off(self) -> None:
        splitter = FakeController(width=10, height=10, position=Position(1, 0))
        splitter.entities[30] = FakeEntity(EntityType.BUILDER_BOT, Position(3, 1), Team.B)
        _seed_assignment(splitter, 0, 1, None, splitter.round & 63)
        splitter_state = BuilderStateData(role=Role.REPAIR, state=BuilderState.MAINTAIN, route=_install_route(splitter), route_index=-1, last_delivery_round=1, claim_slot=0)
        splitter_player = Player()
        splitter_player._builder_state = splitter_state
        splitter_player.run(splitter)
        splitter.advance(); splitter_player.run(splitter)
        self.assertFalse(any(call[0] == "build" and call[1] == EntityType.SPLITTER for call in splitter.calls))

        barrier = FakeController(width=10, height=10, position=Position(2, 2))
        barrier.round = 240
        barrier.entities[2] = FakeEntity(EntityType.CORE, Position(2, 4), Team.A)
        barrier.entities[3] = FakeEntity(EntityType.BUILDER_BOT, Position(2, 3), Team.B)
        barrier_player = Player()
        barrier_player._builder_state = BuilderStateData(role=Role.DEFENDER)
        barrier_player.run(barrier)
        barrier.advance(); barrier_player.run(barrier)
        self.assertTrue(any(call[0] == "build" and call[1] == EntityType.BARRIER for call in barrier.calls))

        geometry = FakeController(width=10, height=10, position=Position(2, 2))
        geometry.round = 240
        geometry.entities[2] = FakeEntity(EntityType.CORE, Position(6, 6), Team.A)
        geometry.entities[3] = FakeEntity(EntityType.BUILDER_BOT, Position(7, 2), Team.B)
        _seed_assignment(geometry, 0, 1, None, geometry.round & 63)
        geometry_player = Player()
        geometry_player._builder_state = BuilderStateData(role=Role.DEFENDER, claim_slot=0)
        geometry_player.run(geometry)
        geometry.advance(); geometry_player.run(geometry)
        self.assertFalse(any(call[0] == "build" and call[1] == EntityType.GUNNER for call in geometry.calls))

        unverified_launcher = FakeController(width=10, height=10, position=Position(2, 2))
        unverified_launcher.round = 100
        unverified_launcher.store[int(Slot.RALLY)] = encode_alert(Position(8, 8), 10, 108)
        unverified_player = Player()
        unverified_player._builder_state = BuilderStateData(role=Role.SIEGE)
        unverified_player.run(unverified_launcher)
        self.assertEqual([], [call for call in unverified_launcher.calls if call[0] == "build" and call[1] == EntityType.LAUNCHER])

        launcher = FakeController(width=10, height=10, position=Position(2, 2))
        launcher.round = 100
        launcher.entities[30] = FakeEntity(EntityType.CORE, Position(8, 8), Team.B)
        launcher.store[int(Slot.RALLY)] = encode_alert(Position(8, 8), 10, 108)
        _seed_assignment(launcher, 0, 1, None, launcher.round & 63)
        launcher_player = Player()
        launcher_player._builder_state = BuilderStateData(role=Role.SIEGE, claim_slot=0)
        launcher_player.run(launcher)
        launcher.advance(); launcher_player.run(launcher)
        self.assertFalse(any(call[0] == "build" and call[1] == EntityType.LAUNCHER for call in launcher.calls))

    def test_identical_scripted_matches_have_identical_traces(self) -> None:
        terrain = {Position(4, 4): Environment.ORE_TITANIUM, Position(2, 2): Environment.WALL}
        left = FakeController(terrain=terrain)
        right = FakeController(terrain=terrain)
        left_player, right_player = Player(), Player()
        for _ in range(12):
            left_player.run(left)
            right_player.run(right)
            self.assertEqual(left.calls, right.calls)
            left.advance()
            right.advance()


if __name__ == "__main__":
    unittest.main()
