from __future__ import annotations

import unittest

from fcode import Position

from bots.candidate.bot.comms import (
    PROJECT_COUNT,
    SCHEMA_VERSION,
    Slot,
    assignment_is_fresh,
    can_write,
    decode_assignment,
    decode_budget,
    decode_project,
    decode_strategy,
    encode_assignment,
    encode_project,
    encode_strategy,
    epoch_distance,
    pack_position,
    read_assignment,
    read_project,
    slot_owner,
    unpack_position,
    write_assignment,
    write_project,
    decode_global_strategy,
    encode_global_strategy,
)
from bots.candidate.bot.types import Budget, Opening, Phase, ProjectState
from tests.candidate_fakes import FakeController


class CandidateCommsTest(unittest.TestCase):
    def test_global_strategy_codec_preserves_legacy_fields(self) -> None:
        from bots.candidate.bot.types import StrategyPhase

        packed = encode_global_strategy(StrategyPhase.CORE_SIEGE, Phase.OFFENSE, Opening.WIDE_EXPANSION)
        self.assertEqual((StrategyPhase.CORE_SIEGE, Phase.OFFENSE, Opening.WIDE_EXPANSION), decode_global_strategy(packed))
    def controller(self) -> FakeController:
        controller = FakeController(width=30, height=30)
        controller.store[int(Slot.SCHEMA_VERSION)] = SCHEMA_VERSION
        return controller

    def test_every_coordinate_round_trips_and_unknown_is_distinct(self) -> None:
        for y in range(30):
            for x in range(30):
                position = Position(x, y)
                self.assertEqual(position, unpack_position(pack_position(position, 30, 30), 30, 30))
                encoded = encode_project(position, 4, ProjectState.CLAIMED, 30, 30)
                self.assertEqual(position, decode_project(encoded, 30, 30).position)
        self.assertIsNone(decode_project(encode_project(None, 4, ProjectState.IDLE, 30, 30), 30, 30).position)
        self.assertNotEqual(encode_project(Position(0, 0), 4, ProjectState.IDLE, 30, 30), encode_project(None, 4, ProjectState.IDLE, 30, 30))

    def test_assignment_epoch_wrap_and_stale_heartbeat(self) -> None:
        assignment = decode_assignment(encode_assignment(17, 63))
        self.assertEqual(17, assignment.owner_id)
        self.assertTrue(assignment_is_fresh(assignment, 0))
        self.assertEqual(1, epoch_distance(0, 63))
        self.assertFalse(assignment_is_fresh(assignment, 32))

    def test_invalid_values_fail_safe(self) -> None:
        self.assertIsNone(decode_assignment(True))
        self.assertIsNone(decode_assignment(-1))
        self.assertIsNone(decode_assignment(1 << 24))
        self.assertIsNone(decode_project(encode_project(Position(29, 29), 0, ProjectState.IDLE, 30, 30), 10, 10))
        with self.assertRaises(ValueError): encode_assignment(0, 0)
        with self.assertRaises(ValueError): encode_project(Position(30, 0), 0, ProjectState.IDLE, 30, 30)
        with self.assertRaises(ValueError): encode_project(None, 0, 99, 30, 30)

    def test_single_writer_ownership(self) -> None:
        self.assertEqual(4, SCHEMA_VERSION)
        self.assertEqual(4, PROJECT_COUNT)
        self.assertEqual("core", slot_owner(Slot.SCHEMA_VERSION))
        self.assertEqual(0, slot_owner(Slot.PROJECT_0))
        self.assertEqual(1, slot_owner(Slot.PROJECT_1))
        self.assertEqual(2, slot_owner(Slot.PROJECT_2))
        self.assertEqual(3, slot_owner(Slot.PROJECT_3))
        self.assertEqual("core", slot_owner(Slot.CLAIM_0))
        self.assertTrue(can_write(Slot.CLAIM_0, "core"))
        self.assertFalse(can_write(Slot.CLAIM_0, 0))
        self.assertTrue(can_write(Slot.PROJECT_0, 0))
        self.assertFalse(can_write(Slot.PROJECT_0, 1))
        controller = self.controller()
        self.assertFalse(write_assignment(controller, 0, 7, 1, writer=0))
        self.assertFalse(write_project(controller, 0, Position(1, 1), 1, ProjectState.CLAIMED, 30, 30, writer=1))

    def test_fourth_assignment_and_project_use_the_reserved_store_slots(self) -> None:
        controller = self.controller()
        self.assertTrue(write_assignment(controller, 3, 77, 9))
        self.assertTrue(write_project(controller, 3, Position(29, 29), 9, ProjectState.BUILDING, 30, 30, writer=3))
        self.assertIsNone(read_assignment(controller, 3))
        self.assertEqual(ProjectState.IDLE, read_project(controller, 3).state)
        controller.advance()
        self.assertEqual(77, read_assignment(controller, 3).owner_id)
        self.assertEqual(Position(29, 29), read_project(controller, 3).position)

    def test_delayed_assignment_and_project_snapshot(self) -> None:
        controller = self.controller()
        self.assertTrue(write_assignment(controller, 0, 7, 5))
        self.assertTrue(write_project(controller, 0, Position(2, 2), 5, ProjectState.CLAIMED, 30, 30, writer=0))
        self.assertIsNone(read_assignment(controller, 0))
        self.assertEqual(ProjectState.IDLE, read_project(controller, 0).state)
        controller.advance()
        self.assertEqual(7, read_assignment(controller, 0).owner_id)
        self.assertEqual(Position(2, 2), read_project(controller, 0).position)

    def test_schema_mismatch_is_safe_noop(self) -> None:
        controller = self.controller()
        controller.store[int(Slot.SCHEMA_VERSION)] = SCHEMA_VERSION - 1
        self.assertIsNone(read_assignment(controller, 0))
        self.assertIsNone(read_project(controller, 0))
        self.assertFalse(write_assignment(controller, 0, 7, 1))

    def test_failed_project_handoff_is_single_owner(self) -> None:
        controller = self.controller()
        self.assertTrue(write_assignment(controller, 0, 7, 1))
        self.assertTrue(write_project(controller, 0, Position(4, 4), 1, ProjectState.FAILED, 30, 30, writer=0))
        controller.advance()
        self.assertEqual(7, read_assignment(controller, 0).owner_id)
        self.assertEqual(ProjectState.FAILED, read_project(controller, 0).state)
        self.assertTrue(write_assignment(controller, 0, 8, 2))
        controller.advance()
        owners = [read_assignment(controller, index).owner_id for index in range(1) if read_assignment(controller, index) is not None]
        self.assertEqual([8], owners)

    def test_codec_round_trip(self) -> None:
        budget = Budget(30, 40, 50, 60, 70)
        self.assertEqual(budget, decode_budget(sum((value // 10) << (i * 6) for i, value in enumerate((30, 40, 50, 60, 70)))))
        self.assertEqual((Phase.DEFENSE, Opening.WIDE_EXPANSION), decode_strategy(encode_strategy(Phase.DEFENSE, Opening.WIDE_EXPANSION)))


if __name__ == "__main__":
    unittest.main()
