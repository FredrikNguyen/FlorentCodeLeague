from __future__ import annotations

import unittest

from bots.candidate.bot.builder import (
    BuilderStateData,
    _bootstrap_defense_build_allowed,
    _bootstrap_owner_builder_interrupt_allowed,
)
from bots.candidate.bot.types import Opening, Role
from bots.candidate.bot.world import WorldMemory


class BootstrapDefenseTests(unittest.TestCase):
    def test_close_specialized_opening_uses_one_free_defender(self) -> None:
        world = WorldMemory(28, 20)
        designated = BuilderStateData(
            role=Role.DEFENDER,
            role_key=1,
            opening=Opening.WIDE_EXPANSION,
            world=world,
        )
        self.assertTrue(_bootstrap_defense_build_allowed(designated))
        designated.bootstrap_defense_built = True
        self.assertFalse(_bootstrap_defense_build_allowed(designated))
        self.assertFalse(
            _bootstrap_defense_build_allowed(
                BuilderStateData(
                    role=Role.DEFENDER,
                    role_key=2,
                    opening=Opening.WIDE_EXPANSION,
                    world=world,
                )
            )
        )

    def test_distant_balanced_and_post_income_keep_existing_policy(self) -> None:
        for world, opening in (
            (WorldMemory(26, 26), Opening.WIDE_EXPANSION),
            (WorldMemory(16, 16), Opening.BALANCED_ECONOMY),
        ):
            state = BuilderStateData(
                role=Role.ECONOMY,
                role_key=9,
                opening=opening,
                world=world,
                bootstrap_defense_built=True,
            )
            self.assertTrue(_bootstrap_defense_build_allowed(state))

        funded = BuilderStateData(
            role=Role.ECONOMY,
            role_key=9,
            opening=Opening.WIDE_EXPANSION,
            world=WorldMemory(28, 20),
            team_maintaining_routes=1,
            bootstrap_defense_built=True,
        )
        self.assertTrue(_bootstrap_defense_build_allowed(funded))

        recovering = BuilderStateData(
            role=Role.ECONOMY,
            role_key=9,
            opening=Opening.WIDE_EXPANSION,
            world=WorldMemory(28, 20),
            economy_established=True,
            bootstrap_defense_built=True,
        )
        self.assertTrue(_bootstrap_defense_build_allowed(recovering))

    def test_pre_income_owner_ignores_only_non_adjacent_builder_rush(self) -> None:
        owner = BuilderStateData(
            claim_slot=0,
            opening=Opening.WIDE_EXPANSION,
            world=WorldMemory(25, 15),
        )
        self.assertFalse(
            _bootstrap_owner_builder_interrupt_allowed(
                owner,
                local=False,
                distance_squared=1,
            )
        )
        self.assertFalse(
            _bootstrap_owner_builder_interrupt_allowed(
                owner,
                local=True,
                distance_squared=3,
            )
        )
        self.assertTrue(
            _bootstrap_owner_builder_interrupt_allowed(
                owner,
                local=True,
                distance_squared=2,
            )
        )

        for state in (
            BuilderStateData(
                opening=Opening.WIDE_EXPANSION,
                world=WorldMemory(25, 15),
            ),
            BuilderStateData(
                claim_slot=0,
                team_maintaining_routes=1,
                opening=Opening.WIDE_EXPANSION,
                world=WorldMemory(25, 15),
            ),
            BuilderStateData(
                claim_slot=0,
                economy_established=True,
                opening=Opening.WIDE_EXPANSION,
                world=WorldMemory(25, 15),
            ),
            BuilderStateData(
                claim_slot=0,
                opening=Opening.BALANCED_ECONOMY,
                world=WorldMemory(16, 16),
            ),
        ):
            self.assertTrue(
                _bootstrap_owner_builder_interrupt_allowed(
                    state,
                    local=False,
                    distance_squared=99,
                )
            )


if __name__ == "__main__":
    unittest.main()
