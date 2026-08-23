from __future__ import annotations

import unittest

from fcode import Environment, EntityType, Position

from bots.candidate.bot.constants import (
    ECONOMY_PHASE_CONVERTING,
    ECONOMY_PHASE_CRISIS,
    ECONOMY_PHASE_OPENING,
    ECONOMY_PHASE_PRESSURE,
    ECONOMY_STRONG_CHAINS,
    INCOME_HEARTBEAT_ROUNDS,
    OFFENSE_MIN_HARVESTERS,
    ORE_QUEUE_LEN,
    SLOT_HARVESTER_COUNT,
    SLOT_ORE_CURSOR,
    TASK_HARVEST,
    TASK_NONE,
    TASK_RAID,
    economy_phase_from_cursor,
    ore_cursor_from_packed,
    pack_economy_cursor,
)
from bots.candidate.bot.core_role import CoreMixin
from bots.candidate.bot.defender import DefenderMixin
from bots.candidate.bot.dynamic import DynamicMixin
from bots.candidate.bot.attacker import AttackerMixin
from tests.candidate_fakes import FakeController


class CorePhaseProbe(CoreMixin):
    def __init__(self) -> None:
        self.poor_streak = 0
        self.income_seen = 0
        self.income_quiet_rounds = 0


class DynamicPhaseProbe(DynamicMixin):
    pass


class AttackerPhaseProbe(AttackerMixin):
    pass


class EconomyPhaseTests(unittest.TestCase):
    def test_phase_cursor_round_trip_preserves_legacy_cursor(self) -> None:
        for phase in (
            ECONOMY_PHASE_OPENING,
            ECONOMY_PHASE_CONVERTING,
            ECONOMY_PHASE_PRESSURE,
            ECONOMY_PHASE_CRISIS,
        ):
            packed = pack_economy_cursor(phase, ORE_QUEUE_LEN - 1)
            self.assertEqual(phase, economy_phase_from_cursor(packed))
            self.assertEqual(ORE_QUEUE_LEN - 1, ore_cursor_from_packed(packed))

    def test_core_phase_requires_route_and_recent_income(self) -> None:
        probe = CorePhaseProbe()
        ct = FakeController(entity_type=EntityType.CORE)

        probe._publish_economy_phase(ct, 0, ct.get_harvester_cost() + 40)
        self.assertEqual(ECONOMY_PHASE_OPENING, economy_phase_from_cursor(ct.pending[SLOT_ORE_CURSOR]))

        probe.income_seen = 120
        probe.income_quiet_rounds = 0
        probe._publish_economy_phase(ct, ECONOMY_STRONG_CHAINS, ct.get_harvester_cost() + 40)
        self.assertEqual(ECONOMY_PHASE_PRESSURE, economy_phase_from_cursor(ct.pending[SLOT_ORE_CURSOR]))

        probe.income_quiet_rounds = INCOME_HEARTBEAT_ROUNDS + 1
        probe._publish_economy_phase(ct, ECONOMY_STRONG_CHAINS, ct.get_harvester_cost() + 40)
        self.assertEqual(ECONOMY_PHASE_CONVERTING, economy_phase_from_cursor(ct.pending[SLOT_ORE_CURSOR]))

        probe._publish_economy_phase(ct, ECONOMY_STRONG_CHAINS, 0)
        self.assertEqual(ECONOMY_PHASE_CRISIS, economy_phase_from_cursor(ct.pending[SLOT_ORE_CURSOR]))


    def test_ore_advertisement_retains_core_phase_bits(self) -> None:
        ct = FakeController(
            position=Position(1, 1),
            terrain={Position(2, 1): Environment.ORE_TITANIUM},
        )
        ct.store[SLOT_ORE_CURSOR] = pack_economy_cursor(ECONOMY_PHASE_PRESSURE, 1)

        DefenderMixin()._share_ore(ct)

        packed = ct.pending[SLOT_ORE_CURSOR]
        self.assertEqual(ECONOMY_PHASE_PRESSURE, economy_phase_from_cursor(packed))
        self.assertEqual(2, ore_cursor_from_packed(packed))

    def test_dynamic_workers_hold_economy_until_pressure_phase(self) -> None:
        ct = FakeController(position=Position(1, 1), width=10, height=10)
        ct.store[SLOT_HARVESTER_COUNT] = ECONOMY_STRONG_CHAINS
        probe = DynamicPhaseProbe()
        probe._find_home_threat = lambda _ct: None
        probe._find_belt_gap = lambda _ct: None
        probe._find_enemy_harvester = lambda _ct: None
        probe._find_damaged_building = lambda _ct: None
        probe._find_raid_target = lambda _ct: Position(8, 8)
        probe._find_denial_target = lambda _ct: None
        probe._enemy_core_target = lambda _ct: Position(9, 9)

        ct.store[SLOT_ORE_CURSOR] = pack_economy_cursor(ECONOMY_PHASE_CONVERTING, 0)
        self.assertEqual((TASK_HARVEST, None), probe._best_task(ct))

        ct.store[SLOT_ORE_CURSOR] = pack_economy_cursor(ECONOMY_PHASE_PRESSURE, 0)
        self.assertEqual((TASK_RAID, Position(8, 8)), probe._best_task(ct))

    def test_pressure_keeps_one_nearest_home_steward_on_economy(self) -> None:
        ct = FakeController(position=Position(1, 1), width=20, height=20)
        ct.store[SLOT_HARVESTER_COUNT] = ECONOMY_STRONG_CHAINS
        ct.store[SLOT_ORE_CURSOR] = pack_economy_cursor(ECONOMY_PHASE_PRESSURE, 0)
        probe = DynamicPhaseProbe()
        probe.core_pos = Position(1, 1)
        probe._find_home_threat = lambda _ct: None
        probe._find_belt_gap = lambda _ct: None
        probe._find_enemy_harvester = lambda _ct: None
        probe._find_damaged_building = lambda _ct: None
        probe._find_low_liquidity_gunner = lambda _ct: None
        probe._find_raid_target = lambda _ct: Position(18, 18)
        probe._find_denial_target = lambda _ct: None
        probe._enemy_core_target = lambda _ct: Position(19, 19)
        probe._harvest_available = lambda _ct: False

        self.assertEqual((TASK_HARVEST, None), probe._best_task(ct))

        # A farther home-side worker yields the lease to the closer one rather
        # than independently keeping the whole pressure pool on economy.
        ct.entities[10] = ct.entities[1].__class__(
            EntityType.BUILDER_BOT, Position(2, 1), ct.get_team()
        )
        ct.entities[1].position = Position(4, 1)
        self.assertEqual((TASK_RAID, Position(18, 18)), probe._best_task(ct))

    def test_siege_cage_depth_requires_healthy_pressure(self) -> None:
        ct = FakeController(entity_type=EntityType.BUILDER_BOT)
        ct.store[SLOT_HARVESTER_COUNT] = ECONOMY_STRONG_CHAINS
        probe = AttackerPhaseProbe()

        ct.store[SLOT_ORE_CURSOR] = pack_economy_cursor(ECONOMY_PHASE_PRESSURE, 0)
        self.assertGreater(probe._enemy_core_barrier_cap(ct), 6)
        ct.store[SLOT_ORE_CURSOR] = pack_economy_cursor(ECONOMY_PHASE_CRISIS, 0)
        self.assertEqual(6, probe._enemy_core_barrier_cap(ct))

if __name__ == "__main__":
    unittest.main()
