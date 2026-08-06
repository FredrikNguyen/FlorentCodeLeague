from __future__ import annotations

import unittest

from fcode import Direction, EntityType, Position, Team

from bots.candidate.bot.comms import decode_threat_report, encode_threat_report, read_shared_threat, write_shared_threat
from bots.candidate.bot.defense import (
    DefenseState,
    choose_defenders,
    choose_defense_mode,
    merge_threat_reports,
    observe_local_threats,
    required_defender_count,
    update_defense_overlay,
)
from bots.candidate.bot.turrets import choose_defensive_fire_target, choose_gunner_rotation, maybe_convert_ammo, turret_ammo_demand
from bots.candidate.bot.types import DefenseMode, EconomySnapshot, ThreatKind, ThreatReport
from tests.candidate_fakes import FakeController, FakeEntity


class CandidateDefenseTest(unittest.TestCase):
    def test_threat_codec_and_fresh_shared_report(self) -> None:
        controller = FakeController(entity_type=EntityType.BUILDER_BOT, width=10, height=10)
        report = ThreatReport(ThreatKind.ENEMY_BUILDER, Position(3, 3), Position(1, 1), 12, 4, 4, 8, 1)
        packed = encode_threat_report(report, 10, 10)
        decoded = decode_threat_report(packed, 10, 10)
        self.assertEqual(report.position, decoded.position)
        self.assertEqual(report.severity, decoded.severity)
        self.assertTrue(write_shared_threat(controller, report))
        controller.store[int(8)] = controller.pending[8]
        self.assertIsNotNone(read_shared_threat(controller, current_round=5))
        self.assertIsNone(read_shared_threat(controller, current_round=20))

    def test_fresh_core_damage_is_critical_and_stale_recovers(self) -> None:
        controller = FakeController(entity_type=EntityType.BUILDER_BOT, position=Position(1, 1))
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(2, 2), Team.A, hp=40, max_hp=40)
        state = update_defense_overlay(controller, DefenseState())
        self.assertIn(state.mode, (DefenseMode.CLEAR, DefenseMode.WATCH))
        controller.entities[2].hp = 20
        controller.advance()
        state = update_defense_overlay(controller, state)
        self.assertEqual(DefenseMode.CRITICAL, state.mode)
        for _ in range(10):
            controller.advance()
        state.threat = None
        state = update_defense_overlay(controller, state)
        self.assertIn(state.mode, (DefenseMode.RECOVERY, DefenseMode.CLEAR))

    def test_enemy_builder_and_turret_observation_order(self) -> None:
        controller = FakeController(entity_type=EntityType.GUNNER, position=Position(1, 1))
        controller.entities[2] = FakeEntity(EntityType.CORE, Position(2, 2), Team.A)
        controller.entities[3] = FakeEntity(EntityType.BUILDER_BOT, Position(2, 1), Team.B)
        controller.entities[4] = FakeEntity(EntityType.HARVESTER, Position(1, 2), Team.B)
        reports = observe_local_threats(controller)
        self.assertTrue(reports)
        self.assertEqual(ThreatKind.ENEMY_BUILDER, reports[0].kind)
        self.assertEqual(Position(2, 1), choose_defensive_fire_target(controller, (Position(2, 1), Position(1, 2)), protected_asset=Position(2, 2)))

    def test_stable_defender_selection_and_hysteresis(self) -> None:
        candidates = ((1, Position(1, 1), 40, False), (2, Position(8, 8), 40, True), (3, Position(2, 1), 20, False))
        selected = choose_defenders(candidates, 2, threat_position=Position(2, 2))
        self.assertEqual((3, 1), selected)
        self.assertEqual(2, required_defender_count(DefenseMode.ACTIVE, 8))
        self.assertEqual(DefenseMode.RECOVERY, choose_defense_mode(None, previous=DefenseMode.ACTIVE, current_round=10, last_threat_round=5))

    def test_zero_value_rotation_and_ammo_reserve(self) -> None:
        controller = FakeController(entity_type=EntityType.GUNNER, position=Position(1, 1))
        self.assertIsNone(choose_gunner_rotation(controller))
        self.assertEqual(0, turret_ammo_demand(FakeController(entity_type=EntityType.CORE)))
        snapshot = EconomySnapshot(ammo=0, free_titanium=3)
        self.assertEqual(3, maybe_convert_ammo(controller, snapshot, 10, max_per_turn=4))
        self.assertEqual(3, controller.ammo)


if __name__ == "__main__":
    unittest.main()
