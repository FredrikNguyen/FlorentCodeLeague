from __future__ import annotations

import unittest

from fcode import Direction, EntityType, Position, Team

from bots.candidate.bot.constants import MODE_CHAIN, MODE_SCOUT
from bots.candidate.bot.defender import DefenderMixin
from tests.candidate_fakes import FakeController, FakeEntity


class SeededRouteProbe(DefenderMixin):
    def __init__(self, seed: Position | None = None) -> None:
        if seed is None:
            seed = Position(2, 1)
        self.route_seed = seed
        self.route_seed_pending = None
        self.core_pos = Position(5, 1)
        self.mode = MODE_CHAIN
        self.chain_pending = None
        self.chain_len = 0
        self.chain_blocked = 0
        self.chain_tiles: set[Position] = set()
        self.target = None
        self.best_dist = float("inf")
        self.no_progress = 0


class SeededRouteTests(unittest.TestCase):
    def test_wrong_type_seed_clears_route_without_get_direction_exception(self) -> None:
        seed = Position(2, 1)
        ct = FakeController(position=seed)
        ct.entities[2] = FakeEntity(EntityType.BARRIER, seed, Team.A)
        probe = SeededRouteProbe(seed)

        self.assertTrue(probe._run_seeded_route(ct, set()))
        self.assertIsNone(probe.route_seed)
        self.assertEqual(MODE_SCOUT, probe.mode)
        self.assertIsNone(probe.route_seed_pending)

    def test_wrong_team_seed_clears_route(self) -> None:
        seed = Position(2, 1)
        ct = FakeController(position=seed)
        ct.entities[2] = FakeEntity(EntityType.BARRIER, seed, Team.B)
        probe = SeededRouteProbe(seed)

        probe._run_seeded_route(ct, set())

        self.assertIsNone(probe.route_seed)
        self.assertEqual(MODE_SCOUT, probe.mode)

    def test_empty_seed_keeps_existing_recovery(self) -> None:
        seed = Position(2, 1)
        ct = FakeController(position=seed)
        probe = SeededRouteProbe(seed)

        probe._run_seeded_route(ct, set())

        self.assertIsNone(probe.route_seed)
        self.assertEqual(MODE_SCOUT, probe.mode)

    def test_friendly_conveyor_seed_still_advances(self) -> None:
        seed = Position(2, 1)
        ct = FakeController(position=seed)
        ct.entities[2] = FakeEntity(EntityType.CONVEYOR, seed, Team.A, Direction.EAST)
        probe = SeededRouteProbe(seed)

        self.assertTrue(probe._run_seeded_route(ct, set()))
        self.assertEqual(seed, probe.route_seed)
        self.assertEqual(Position(3, 1), probe.route_seed_pending)
        self.assertEqual(("move", Direction.EAST), ct.calls[-1])

if __name__ == "__main__":
    unittest.main()
