from __future__ import annotations

import unittest

from fcode import EntityType, Position, Team

from bots.candidate.bot.comms import Slot, encode_alert
from bots.candidate.bot.offense import (
    choose_raid_action,
    choose_rally,
    score_ally_insertion,
    score_enemy_ejection,
    score_sabotage_target,
)
from bots.candidate.bot.policy import late_game_policy
from bots.candidate.bot.player import Player
from tests.candidate_fakes import FakeEntity, FakeController


class CandidateOffenseEndgameTest(unittest.TestCase):
    def test_sabotage_ordering(self) -> None:
        self.assertGreater(score_sabotage_target(EntityType.HARVESTER), score_sabotage_target(EntityType.SPLITTER))
        self.assertGreater(score_sabotage_target(EntityType.SPLITTER), score_sabotage_target(EntityType.CONVEYOR, loaded=True))
        self.assertGreater(score_sabotage_target(EntityType.CONVEYOR, loaded=True), score_sabotage_target(EntityType.CONVEYOR))

    def test_reserve_blocks_paid_builder_attacks(self) -> None:
        targets = ((Position(1, 1), EntityType.HARVESTER, False, 0),)
        self.assertIsNone(choose_raid_action(targets, resources=20, economy_reserve=20, attack_cost=2))
        self.assertIsNotNone(choose_raid_action(targets, resources=30, economy_reserve=20, attack_cost=2))

    def test_stale_rally_and_core_fallback(self) -> None:
        current = Position(1, 1)
        self.assertEqual(Position(4, 4), choose_rally(current, verified_target=Position(2, 2), target_age=30, enemy_core=Position(4, 4)))
        self.assertEqual(current, choose_rally(current, target_age=100))

    def test_ally_insertion_requires_positive_progress(self) -> None:
        self.assertGreater(score_ally_insertion(10, 5), 0)
        self.assertLessEqual(score_ally_insertion(5, 10), 0)
        self.assertLessEqual(score_ally_insertion(10, 5, threat_penalty=6), 0)

    def test_enemy_ejection_and_deterministic_tie(self) -> None:
        score = score_enemy_ejection(Position(9, 9), own_core=Position(0, 0), logistics=(Position(1, 0),))
        self.assertGreater(score, 0)
        targets = ((Position(2, 1), EntityType.CONVEYOR, False, 0), (Position(1, 2), EntityType.CONVEYOR, False, 0))
        first = choose_raid_action(targets, resources=100, economy_reserve=20, attack_cost=2)
        second = choose_raid_action(targets, resources=100, economy_reserve=20, attack_cost=2)
        self.assertEqual(first, second)

    def test_round_850_priorities_and_spending_suppression(self) -> None:
        priorities = late_game_policy(
            850,
            delivery_due=True,
            route_repair_due=True,
            harvester_payback_positive=True,
            collected_titanium=100,
            harvester_count=2,
            stored_titanium=50,
        )
        self.assertLess(priorities.index("delivery"), priorities.index("combat") if "combat" in priorities else len(priorities))
        self.assertLess(priorities.index("repair"), priorities.index("defense"))
        self.assertLess(priorities.index("harvester"), priorities.index("defense"))
        self.assertIn("no_ammo_conversion", priorities)
        self.assertIn("no_paid_attack", priorities)
        self.assertLess(priorities.index("collected_titanium"), priorities.index("harvester_count"))
        self.assertLess(priorities.index("harvester_count"), priorities.index("stored_titanium"))
        self.assertEqual(("core_kill", "defense", "delivery", "repair", "stored_titanium"), late_game_policy(900, verified_near_term_core_kill=True))

    def test_player_launcher_requires_fresh_verified_progress_context(self) -> None:
        without_context = FakeController(entity_type=EntityType.LAUNCHER, width=10, height=10, position=Position(3, 3))
        without_context.entities[2] = FakeEntity(EntityType.BUILDER_BOT, Position(4, 3), Team.A)
        without_context.entities[3] = FakeEntity(EntityType.CORE, Position(1, 1), Team.A)
        Player().run(without_context)
        self.assertEqual([], [call for call in without_context.calls if call[0] == "launch"])

        stale = FakeController(entity_type=EntityType.LAUNCHER, width=10, height=10, position=Position(3, 3))
        stale.round = 32
        stale.entities[2] = FakeEntity(EntityType.BUILDER_BOT, Position(4, 3), Team.A)
        stale.entities[3] = FakeEntity(EntityType.CORE, Position(1, 1), Team.A)
        stale.store[int(Slot.RALLY)] = encode_alert(Position(0, 0), 10, 8)
        Player().run(stale)
        self.assertEqual([], [call for call in stale.calls if call[0] == "launch"])

        fresh = FakeController(entity_type=EntityType.LAUNCHER, width=10, height=10, position=Position(3, 3))
        fresh.entities[2] = FakeEntity(EntityType.BUILDER_BOT, Position(4, 3), Team.A)
        fresh.entities[3] = FakeEntity(EntityType.CORE, Position(1, 1), Team.A)
        fresh.entities[4] = FakeEntity(EntityType.CORE, Position(0, 0), Team.B)
        fresh.store[int(Slot.RALLY)] = encode_alert(Position(0, 0), 10, 8)
        Player().run(fresh)
        launches = [call for call in fresh.calls if call[0] == "launch"]
        self.assertEqual(1, len(launches))


if __name__ == "__main__":
    unittest.main()
