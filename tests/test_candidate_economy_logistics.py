from __future__ import annotations

import unittest

from fcode import Direction, EntityType, Position

from bots.candidate.bot.economy import claim_should_release, estimate_payback_round, estimate_route_cost, expansion_allowed, next_harvester_state
from bots.candidate.bot.logistics import (
    directions_for_route,
    find_broken_link,
    plan_core_outward_route,
    repair_priority,
    splitter_redundancy_justified,
    teardown_allowed,
    verify_route,
)
from bots.candidate.bot.types import BuilderState, RoutePlan


class CandidateEconomyLogisticsTest(unittest.TestCase):
    def test_payback_positive_and_negative_expansion(self) -> None:
        self.assertIsNotNone(estimate_payback_round(30, output_per_round=5))
        self.assertIsNone(estimate_payback_round(30, output_per_round=1, horizon=20))
        self.assertTrue(
            expansion_allowed(
                projected_output=200,
                harvester_cost=20,
                route_cost=30,
                current_harvester_cost=10,
                construction_reserve=20,
                defense_reserve=20,
                ammo_reserve=10,
                liquidity_reserve=20,
                available_resources=150,
            )
        )
        self.assertFalse(
            expansion_allowed(
                projected_output=40,
                harvester_cost=20,
                route_cost=30,
                current_harvester_cost=10,
                available_resources=150,
            )
        )
        self.assertEqual(30, estimate_route_cost(10, 3))

    def test_three_project_cap_and_reserve_preservation(self) -> None:
        self.assertFalse(expansion_allowed(projected_output=1000, harvester_cost=1, route_cost=1, concurrent_projects=3))
        self.assertFalse(
            expansion_allowed(
                projected_output=500,
                harvester_cost=20,
                route_cost=20,
                construction_reserve=40,
                defense_reserve=40,
                ammo_reserve=40,
                liquidity_reserve=40,
                available_resources=100,
            )
        )

    def test_harvester_fsm_and_claim_release_guards(self) -> None:
        state = next_harvester_state(next_harvester_state(BuilderState.DISCOVER))
        self.assertEqual("approach_build_tile", state.value)
        self.assertTrue(claim_should_release(valid_ore=False, age=1, timeout=12, ownership_lost=False))
        self.assertTrue(claim_should_release(valid_ore=True, age=12, timeout=12, ownership_lost=False))
        self.assertFalse(claim_should_release(valid_ore=True, age=1, timeout=12, ownership_lost=False))

    def test_core_outward_directions_and_last_mile(self) -> None:
        ore = Position(1, 5)
        footprint = (Position(5, 5), Position(6, 5), Position(5, 6), Position(6, 6))
        route = plan_core_outward_route(ore, footprint, 10, 10)
        self.assertIsNotNone(route)
        self.assertEqual(ore.distance_squared(route.cells[0]), 1)
        self.assertEqual(route.cells[-1].add(route.directions[-1]) in set(footprint), True)
        self.assertEqual(route.directions, directions_for_route(route.cells, footprint))

    def test_route_planning_stops_at_cpu_limit_and_resumes(self) -> None:
        search: dict[str, object] = {}
        stats: dict[str, int] = {}
        checks = iter((0, 7000))
        route = plan_core_outward_route(
            Position(1, 5),
            (Position(5, 5), Position(6, 5), Position(5, 6), Position(6, 6)),
            10,
            10,
            cpu_check=lambda: next(checks, 7000),
            search_state=search,
            stats=stats,
        )
        self.assertIsNone(route)
        self.assertEqual(1, stats["stopped_cpu"])
        self.assertFalse(search["complete"])
        resumed = plan_core_outward_route(
            Position(1, 5),
            (Position(5, 5), Position(6, 5), Position(5, 6), Position(6, 6)),
            10,
            10,
            cpu_check=lambda: 0,
            search_state=search,
        )
        self.assertIsNotNone(resumed)

    def test_exact_visible_route_verification(self) -> None:
        route = RoutePlan(
            ore=Position(0, 1),
            cells=(Position(1, 1), Position(2, 1)),
            directions=(Direction.EAST, Direction.EAST),
            core_footprint=(Position(3, 1),),
        )
        visible = {Position(1, 1): (EntityType.CONVEYOR, Direction.EAST), Position(2, 1): (EntityType.CONVEYOR, Direction.EAST)}
        self.assertTrue(verify_route(route, visible))
        visible[Position(2, 1)] = (EntityType.SPLITTER, Direction.EAST)
        self.assertFalse(verify_route(route, visible))
        visible[Position(2, 1)] = (EntityType.CONVEYOR, Direction.SOUTH)
        self.assertFalse(verify_route(route, visible))

    def test_destroyed_link_bounded_repair_and_teardown_gate(self) -> None:
        route = RoutePlan(Position(0, 1), (Position(1, 1),), (Direction.EAST,), (Position(2, 1),))
        self.assertEqual(0, find_broken_link(route, {}))
        self.assertGreater(repair_priority(0, 8, backlog=10), 0)
        self.assertTrue(teardown_allowed(verified_obsolete=True))
        self.assertFalse(teardown_allowed())

    def test_redundancy_strict_threshold(self) -> None:
        args = dict(
            probability_of_cut=0.5,
            remaining_expected_route_output=100,
            splitter_cost=10,
            branch_cost=20,
            estimated_latency_penalty=5,
            mature_route=True,
            exposed_segment=True,
            disjoint_branch=True,
            branch_length=4,
        )
        self.assertTrue(splitter_redundancy_justified(**args))
        args["probability_of_cut"] = 0.35
        self.assertFalse(splitter_redundancy_justified(**args))


if __name__ == "__main__":
    unittest.main()
