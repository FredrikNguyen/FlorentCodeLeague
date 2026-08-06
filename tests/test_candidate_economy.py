from __future__ import annotations

import unittest

from fcode import Position

from bots.candidate.bot.economy import (
    choose_economy_phase,
    compute_desired_builders,
    conservative_project_cost,
    free_titanium_after_reserves,
    rank_ore_projects,
)
from bots.candidate.bot.types import EconomyPhase, ProjectState


class CandidateEconomyTest(unittest.TestCase):
    def test_project_cost_includes_scale_and_repair_contingency(self) -> None:
        base = conservative_project_cost(4, 5, 36, scale_percent=100)
        scaled = conservative_project_cost(4, 5, 36, scale_percent=125)
        self.assertGreaterEqual(scaled, base)
        self.assertGreaterEqual(base, 36 + 4 * 5 + 10)

    def test_ranking_excludes_claimed_unreachable_and_unprofitable_ore(self) -> None:
        origin = Position(1, 1)
        near = Position(2, 1)
        safe = Position(5, 5)
        late = Position(29, 29)
        ranked = rank_ore_projects(
            (near, safe, late),
            origin=origin,
            claimed=(near,),
            unreachable=(late,),
            route_lengths={safe: 5, late: 58},
            round_no=100,
            conveyor_cost=5,
            harvester_cost=36,
            free_titanium=500,
            min_margin=0,
        )
        self.assertEqual((safe,), tuple(item.position for item in ranked))

    def test_reserve_math_and_builder_demand_are_bounded(self) -> None:
        self.assertEqual(0, free_titanium_after_reserves(100, completion_reserve=30, repair_reserve=20, liquidity_reserve=50))
        self.assertEqual(6, compute_desired_builders(active_building_projects=1, maintaining_routes=3, known_ore_count=0, builder_cap=7))
        self.assertEqual(5, compute_desired_builders(active_building_projects=0, maintaining_routes=0, known_ore_count=5, builder_cap=7))
        self.assertEqual(7, compute_desired_builders(active_building_projects=0, maintaining_routes=4, known_ore_count=0, builder_cap=7))

    def test_economy_phase_requires_previous_route_heartbeat(self) -> None:
        self.assertEqual(EconomyPhase.FIRST_ROUTE_BUILDING, choose_economy_phase((ProjectState.BUILDING, ProjectState.IDLE, ProjectState.IDLE), round_no=100, profitable_expansion=True))
        self.assertEqual(EconomyPhase.EXPANSION_EVALUATION, choose_economy_phase((ProjectState.MAINTAIN, ProjectState.IDLE, ProjectState.IDLE), round_no=100, profitable_expansion=True))
        self.assertEqual(EconomyPhase.SECONDARY_ROUTE_BUILDING, choose_economy_phase((ProjectState.MAINTAIN, ProjectState.BUILDING, ProjectState.IDLE), round_no=100, profitable_expansion=True))
        self.assertEqual(EconomyPhase.ENDGAME_HOLD, choose_economy_phase((ProjectState.MAINTAIN,), round_no=900, profitable_expansion=True))


if __name__ == "__main__":
    unittest.main()
