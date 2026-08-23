from __future__ import annotations

import unittest

from fcode import Direction, EntityType, Environment, Position, Team


from bots.candidate.bot.attacker import AttackerMixin
from bots.candidate.bot.constants import (
    MODE_CHAIN,
    MODE_SCOUT,
    DYNAMIC_ECONOMY_FLOOR,
    ECONOMY_PRIORITY_CHAINS,
    ECONOMY_STRONG_CHAINS,
    OFFENSE_MIN_HARVESTERS,
    SLOT_DEFENDER_ID,
    SLOT_HARVESTER_COUNT,
    SLOT_PERMA_ATTACKER_ID,
    SLOT_PERMA_DEFENDER_ID,
    SLOT_ORE_CURSOR,
    SLOT_SECOND_ATTACKER_ID,
    SLOT_SENTINEL_COUNT,
    TASK_ADVANCE,
    TASK_BELT_REPAIR,
    TASK_HARVEST,
    TASK_HOME_THREAT,
    TASK_RETIRE_GUNNER,
    TASK_RAID,
    CHAIN_BLOCKED_LIMIT,
    ROLE_ATTACKER,
    ROLE_DEFENDER,
)
from bots.candidate.bot.core_role import CoreMixin
from bots.candidate.bot.defender import DefenderMixin
from bots.candidate.bot.dynamic import DynamicMixin
from tests.candidate_fakes import FakeController, FakeEntity


class DynamicProbe(DynamicMixin):
    pass


class AttackerProbe(AttackerMixin):
    pass


class DynamicAttackerProbe(DynamicMixin, AttackerMixin):
    pass


class OrphanProbe(DefenderMixin):
    def __init__(self) -> None:
        self.core_pos = Position(5, 2)
        self.mode = MODE_SCOUT
        self.route_seed = None
        self.route_seed_pending = None
        self.hijack_harvester = None
        self.hijack_build_pos = None
        self.chain_pending = None
        self.chain_len = 0
        self.chain_limit = 0
        self.chain_blocked = 0
        self.chain_tiles: set[Position] = set()
        self.target = None
        self.best_dist = float("inf")
        self.no_progress = 0


class CoreProbe(CoreMixin):
    def __init__(self) -> None:
        self.gunner_ids: set[int] = set()
        self.gunner_history: set[int] = set()
        self.core_missing_hp = 0


class SpawnCoreProbe(CoreMixin):
    def __init__(self) -> None:
        self.builder_ids = list(range(10, 15))
        self.gunner_ids: set[int] = set()
        self.gunner_history: set[int] = set()
        self.ramp_established = False
        self.poor_streak = 0
        self.core_missing_hp = 0
        self.prev_resources = None
        self.last_conversion = 0
        self.income_seen = 0
        self.ammo_spent = 0


def add_builder(ct: FakeController, entity_id: int, position: Position) -> None:
    ct.entities[entity_id] = FakeEntity(
        EntityType.BUILDER_BOT,
        position,
        Team.A,
        Direction.EAST,
    )


def add_gunner(ct: FakeController, entity_id: int, position: Position) -> None:
    ct.entities[entity_id] = FakeEntity(
        EntityType.GUNNER,
        position,
        Team.A,
        Direction.EAST,
        hp=25,
        max_hp=25,
    )


class NearestDefenseTests(unittest.TestCase):
    def test_nearest_non_attacker_owns_shared_home_threat(self) -> None:
        ct = FakeController(position=Position(5, 1))
        add_builder(ct, 10, Position(4, 1))

        self.assertTrue(DynamicProbe()._is_nearest_home_responder(ct, Position(6, 1)))

        ct.entities[1].position = Position(3, 1)
        self.assertFalse(DynamicProbe()._is_nearest_home_responder(ct, Position(6, 1)))

    def test_permanent_attacker_does_not_steal_defense_assignment(self) -> None:
        ct = FakeController(position=Position(5, 1))
        add_builder(ct, 10, Position(2, 1))
        ct.store[12] = 10

        self.assertTrue(DynamicProbe()._is_nearest_home_responder(ct, Position(6, 1)))

    def test_remote_counter_turret_response_is_disabled(self) -> None:
        ct = FakeController(position=Position(5, 1))
        ct.resources = 1000

        result = DynamicProbe()._try_build_counter_turret(
            ct, Position(7, 1), set()
        )

        self.assertIsNone(result)
        self.assertFalse(any(call[0] == "build" for call in ct.calls))

    def test_home_gunner_waits_for_first_completed_route(self) -> None:
        ct = FakeController(position=Position(4, 1))
        ct.store[SLOT_DEFENDER_ID] = ct.get_id()
        probe = DefenderMixin()
        probe.core_pos = Position(1, 1)

        self.assertFalse(probe._try_build_gunner(ct))
        self.assertFalse(any(call[0] == "build" for call in ct.calls))

    def test_home_gunner_gate_opens_after_first_completed_route(self) -> None:
        ct = FakeController(position=Position(4, 1))
        ct.store[SLOT_DEFENDER_ID] = ct.get_id()
        ct.store[SLOT_HARVESTER_COUNT] = ECONOMY_PRIORITY_CHAINS
        probe = DefenderMixin()
        probe.core_pos = Position(1, 1)

        self.assertTrue(probe._try_build_gunner(ct))
        self.assertTrue(any(call[0] == "build" for call in ct.calls))

    def test_non_nearest_builder_skips_home_threat_at_task_selection(self) -> None:
        ct = FakeController(position=Position(5, 1))
        probe = DynamicProbe()
        probe._find_home_threat = lambda _ct: Position(6, 1)
        probe._is_nearest_home_responder = lambda _ct, _target: False
        probe._find_belt_gap = lambda _ct: None
        probe._find_enemy_harvester = lambda _ct: None
        probe._find_damaged_building = lambda _ct: None
        probe._should_harvest = lambda _ct: False
        probe._find_raid_target = lambda _ct: None
        probe._find_denial_target = lambda _ct: None
        probe._enemy_core_target = lambda _ct: Position(8, 8)

        self.assertEqual((TASK_ADVANCE, Position(8, 8)), probe._best_task(ct))

    def test_completed_raid_hands_off_to_visible_route_repair(self) -> None:
        ct = FakeController(position=Position(1, 1))
        probe = DynamicProbe()
        probe.task = TASK_RAID
        probe.task_target = Position(2, 1)
        probe.task_started = ct.get_current_round()
        probe._find_belt_gap = lambda _ct: Position(3, 1)
        probe._find_damaged_building = lambda _ct: None

        probe._validate_task(ct)

        self.assertEqual(TASK_BELT_REPAIR, probe.task)
        self.assertEqual(Position(3, 1), probe.task_target)

    def test_dynamic_builders_stay_in_economy_loop_before_three_routes(self) -> None:
        for route_count in range(3):
            ct = FakeController(position=Position(1, 1), width=10, height=10)
            ct.store[SLOT_HARVESTER_COUNT] = route_count
            probe = DynamicProbe()
            probe._find_home_threat = lambda _ct: None
            probe._find_belt_gap = lambda _ct: None
            probe._find_enemy_harvester = lambda _ct: None
            probe._find_damaged_building = lambda _ct: None
            probe._find_raid_target = lambda _ct: Position(8, 8)
            probe._find_denial_target = lambda _ct: Position(7, 7)
            probe._enemy_core_target = lambda _ct: Position(9, 9)

            self.assertEqual(
                (TASK_HARVEST, None),
                probe._best_task(ct),
                f"route count {route_count} should remain economic",
            )
            self.assertFalse(probe._offense_unlocked(ct))

    def test_three_routes_enable_pressure_path(self) -> None:
        ct = FakeController(position=Position(1, 1), width=10, height=10)
        ct.store[SLOT_HARVESTER_COUNT] = OFFENSE_MIN_HARVESTERS
        probe = DynamicProbe()
        probe._find_home_threat = lambda _ct: None
        probe._find_belt_gap = lambda _ct: None
        probe._find_enemy_harvester = lambda _ct: None
        probe._find_damaged_building = lambda _ct: None
        probe._find_raid_target = lambda _ct: Position(8, 8)
        probe._find_denial_target = lambda _ct: None
        probe._enemy_core_target = lambda _ct: Position(9, 9)

        self.assertEqual(OFFENSE_MIN_HARVESTERS, 3)
        self.assertTrue(probe._offense_unlocked(ct))
        self.assertEqual((TASK_RAID, Position(8, 8)), probe._best_task(ct))

    def test_liquidity_floor_keeps_dynamic_worker_in_economy_after_three_routes(self) -> None:
        ct = FakeController(position=Position(1, 1), width=10, height=10)
        ct.store[SLOT_HARVESTER_COUNT] = OFFENSE_MIN_HARVESTERS
        ct.resources = ct.get_harvester_cost() + 2 * ct.get_conveyor_cost() + 80 - 1
        probe = DynamicProbe()
        probe.core_pos = Position(1, 1)

        self.assertTrue(probe._should_harvest(ct))

    def test_liquidity_floor_has_one_nearest_dynamic_owner(self) -> None:
        ct = FakeController(position=Position(1, 1), width=10, height=10)
        ct.store[SLOT_HARVESTER_COUNT] = OFFENSE_MIN_HARVESTERS
        ct.resources = ct.get_harvester_cost() + 2 * ct.get_conveyor_cost() + 80 - 1
        add_builder(ct, 10, Position(4, 1))
        probe = DynamicProbe()
        probe.core_pos = Position(1, 1)

        self.assertTrue(probe._owns_liquidity_floor(ct))
        ct.entities[1].position = Position(6, 1)
        self.assertFalse(probe._owns_liquidity_floor(ct))

    def test_liquidity_floor_releases_pressure_when_bank_can_replace_route(self) -> None:
        ct = FakeController(position=Position(1, 1), width=10, height=10)
        ct.store[SLOT_HARVESTER_COUNT] = DYNAMIC_ECONOMY_FLOOR - 1
        ct.resources = ct.get_harvester_cost() + 2 * ct.get_conveyor_cost() + 80
        probe = DynamicProbe()

        probe._harvest_available = lambda _ct: False
        self.assertFalse(probe._should_harvest(ct))

    def test_three_route_gate_is_map_independent(self) -> None:
        ct = FakeController(position=Position(1, 1), width=30, height=30)
        ct.store[SLOT_HARVESTER_COUNT] = OFFENSE_MIN_HARVESTERS
        probe = DynamicProbe()
        probe._find_home_threat = lambda _ct: None
        probe._find_belt_gap = lambda _ct: None
        probe._find_enemy_harvester = lambda _ct: None
        probe._find_damaged_building = lambda _ct: None
        probe._find_raid_target = lambda _ct: Position(8, 8)
        probe._find_denial_target = lambda _ct: None
        probe._enemy_core_target = lambda _ct: Position(9, 9)

        self.assertEqual((TASK_RAID, Position(8, 8)), probe._best_task(ct))

    def test_low_liquidity_can_select_only_surplus_home_gunner(self) -> None:
        ct = FakeController(position=Position(6, 2), width=12, height=12)
        ct.store[SLOT_HARVESTER_COUNT] = OFFENSE_MIN_HARVESTERS + 1
        ct.resources = ct.get_harvester_cost() - 1
        probe = DynamicProbe()
        probe.core_pos = Position(1, 1)
        probe._find_belt_gap = lambda _ct: None
        probe._find_enemy_harvester = lambda _ct: None
        probe._find_damaged_building = lambda _ct: None
        probe._should_harvest = lambda _ct: False
        probe._find_raid_target = lambda _ct: None
        probe._find_denial_target = lambda _ct: None
        add_gunner(ct, 20, Position(2, 1))
        add_gunner(ct, 21, Position(3, 1))
        add_gunner(ct, 22, Position(5, 1))
        add_gunner(ct, 23, Position(6, 1))

        self.assertEqual((TASK_RETIRE_GUNNER, Position(6, 1)), probe._best_task(ct))

    def test_low_liquidity_retirement_preserves_three_gunner_floor(self) -> None:
        ct = FakeController(position=Position(6, 3), width=12, height=12)
        ct.store[SLOT_HARVESTER_COUNT] = OFFENSE_MIN_HARVESTERS + 1
        ct.resources = 0
        probe = DynamicProbe()
        probe.core_pos = Position(1, 1)
        add_gunner(ct, 20, Position(2, 1))
        add_gunner(ct, 21, Position(3, 1))
        add_gunner(ct, 22, Position(5, 1))

        self.assertIsNone(probe._find_low_liquidity_gunner(ct))

    def test_low_liquidity_retirement_destroy_is_legal_and_bounded(self) -> None:
        ct = FakeController(position=Position(2, 2), width=12, height=12)
        ct.store[SLOT_HARVESTER_COUNT] = OFFENSE_MIN_HARVESTERS + 1
        ct.resources = 0
        add_gunner(ct, 20, Position(2, 1))
        add_gunner(ct, 21, Position(3, 1))
        add_gunner(ct, 22, Position(4, 1))
        add_gunner(ct, 23, Position(5, 1))
        probe = DynamicProbe()
        probe.core_pos = Position(1, 1)
        probe.task = TASK_RETIRE_GUNNER
        probe.task_target = Position(2, 1)
        probe._execute_task(ct, set())

        self.assertIn(("destroy", Position(2, 1)), ct.calls)
        self.assertNotIn(Position(2, 1), [entity.position for entity in ct.entities.values()])

    def test_second_attacker_keeps_three_route_gate(self) -> None:
        for route_count in range(4):
            ct = FakeController(
                entity_type=EntityType.CORE,
                width=20,
                height=20,
                position=Position(1, 1),
            )
            for entity_id in range(10, 15):
                add_builder(ct, entity_id, Position(10 + entity_id - 10, 10))
            ct.round = 30  # permit the staged workforce to spawn
            ct.store[SLOT_HARVESTER_COUNT] = route_count
            ct.store[SLOT_PERMA_ATTACKER_ID] = 10
            ct.store[SLOT_PERMA_DEFENDER_ID] = 11
            probe = SpawnCoreProbe()
            probe._update_defense = lambda _ct, _cramped: False

            probe._run_core(ct)

            self.assertEqual(10, ct.store[SLOT_PERMA_ATTACKER_ID])
            if route_count < OFFENSE_MIN_HARVESTERS:
                self.assertNotIn(SLOT_SECOND_ATTACKER_ID, ct.pending)
            else:
                self.assertIn(SLOT_SECOND_ATTACKER_ID, ct.pending)

    def test_fixed_attacker_waits_for_confirmed_shell_before_sabotage(self) -> None:
        ct = FakeController(position=Position(1, 1))
        ct.entities[2] = FakeEntity(EntityType.HARVESTER, Position(2, 1), Team.B)
        probe = AttackerProbe()
        probe.attack_target = None
        probe.enemy_core_known = Position(8, 8)
        ct.store[SLOT_HARVESTER_COUNT] = OFFENSE_MIN_HARVESTERS

        self.assertFalse(probe._try_sabotage_with_attacker(ct, set()))
        self.assertNotIn(("fire", Position(2, 1)), ct.calls)

    def test_fixed_attacker_pulses_loaded_enemy_logistics(self) -> None:
        ct = FakeController(position=Position(5, 5))
        ct.store[SLOT_HARVESTER_COUNT] = OFFENSE_MIN_HARVESTERS
        ct.store[SLOT_SENTINEL_COUNT] = 1
        ct.entities[2] = FakeEntity(
            EntityType.SENTINEL, Position(7, 8), Team.A,
        )
        ct.entities[3] = FakeEntity(
            EntityType.CONVEYOR, Position(6, 5), Team.B, Direction.EAST, stored=True,
        )
        probe = AttackerProbe()
        probe.enemy_core_known = Position(8, 8)
        probe.attack_target = None

        self.assertTrue(probe._try_sabotage_with_attacker(ct, set()))
        self.assertIn(("fire", Position(6, 5)), ct.calls)

    def test_only_nearest_designated_attacker_claims_pulse(self) -> None:
        ct = FakeController(position=Position(8, 5))
        ct.store[SLOT_HARVESTER_COUNT] = OFFENSE_MIN_HARVESTERS
        ct.store[SLOT_PERMA_ATTACKER_ID] = 1
        ct.store[SLOT_SECOND_ATTACKER_ID] = 10
        ct.entities[10] = FakeEntity(EntityType.BUILDER_BOT, Position(5, 5), Team.A)
        ct.entities[2] = FakeEntity(EntityType.SENTINEL, Position(7, 8), Team.A)
        ct.entities[3] = FakeEntity(EntityType.HARVESTER, Position(6, 5), Team.B)
        probe = AttackerProbe()
        probe.enemy_core_known = Position(8, 8)
        probe.attack_target = None

        self.assertFalse(probe._try_sabotage_with_attacker(ct, set()))
        self.assertFalse(any(call[0] == "fire" for call in ct.calls))

    def test_dynamic_raid_waits_for_combat_shell_before_raid(self) -> None:
        ct = FakeController(position=Position(1, 1))
        ct.store[11] = 3  # economy gate: three completed chains
        ct.entities[2] = FakeEntity(EntityType.CONVEYOR, Position(2, 1), Team.B)
        probe = DynamicAttackerProbe()

        probe.core_pos = Position(1, 1)
        probe.enemy_core_known = Position(8, 8)

        self.assertIsNone(probe._find_raid_target(ct))

    def test_raid_drops_stale_non_logistics_target(self) -> None:
        ct = FakeController(position=Position(1, 1))
        ct.store[11] = 3
        ct.entities[2] = FakeEntity(EntityType.GUNNER, Position(2, 1), Team.B)
        probe = DynamicAttackerProbe()
        probe.attack_target = Position(2, 1)

        self.assertFalse(probe._try_sabotage_with_attacker(ct, set()))
        self.assertIsNone(probe.attack_target)

    def test_nearest_local_builder_seeds_disconnected_opening_harvester(self) -> None:
        source = Position(2, 2)
        ct = FakeController(position=Position(1, 1))
        ct.entities[2] = FakeEntity(EntityType.HARVESTER, source, Team.A)
        probe = OrphanProbe()

        self.assertTrue(probe._try_reconnect_orphaned_harvester(ct, set()))

        self.assertEqual(MODE_CHAIN, probe.mode)
        self.assertIsNotNone(probe.route_seed)
        self.assertTrue(any(call[0] == "build" and call[1] == EntityType.CONVEYOR for call in ct.calls))

    def test_opening_orphan_seed_skips_when_chain_owner_is_adjacent(self) -> None:
        source = Position(2, 2)
        ct = FakeController(position=Position(1, 1))
        ct.entities[2] = FakeEntity(EntityType.HARVESTER, source, Team.A)
        ct.entities[10] = FakeEntity(EntityType.BUILDER_BOT, Position(2, 1), Team.A, Direction.EAST)
        probe = OrphanProbe()

        self.assertFalse(probe._try_reconnect_orphaned_harvester(ct, set()))
        self.assertFalse(any(call[0] == "build" and call[1] == EntityType.CONVEYOR for call in ct.calls))

    def test_post_route_orphan_with_inward_belt_gets_a_new_accepting_sink(self) -> None:
        source = Position(2, 2)
        ct = FakeController(position=Position(1, 1))
        ct.store[SLOT_HARVESTER_COUNT] = 1
        ct.entities[2] = FakeEntity(EntityType.HARVESTER, source, Team.A)
        ct.entities[3] = FakeEntity(
            EntityType.CONVEYOR, Position(2, 1), Team.A, Direction.SOUTH,
        )
        probe = OrphanProbe()

        self.assertTrue(probe._try_reconnect_orphaned_harvester(ct, set()))
        self.assertTrue(
            any(call[0] == "build" and call[1] == EntityType.CONVEYOR for call in ct.calls)
        )

    def test_post_route_harvester_with_accepting_belt_is_not_reseeded(self) -> None:
        source = Position(2, 2)
        ct = FakeController(position=Position(1, 1))
        ct.store[SLOT_HARVESTER_COUNT] = 1
        ct.entities[2] = FakeEntity(EntityType.HARVESTER, source, Team.A)
        ct.entities[3] = FakeEntity(
            EntityType.CONVEYOR, Position(2, 1), Team.A, Direction.NORTH,
        )
        probe = OrphanProbe()

        self.assertFalse(probe._try_reconnect_orphaned_harvester(ct, set()))
        self.assertFalse(any(call[0] == "build" for call in ct.calls))

if __name__ == "__main__":
    unittest.main()
