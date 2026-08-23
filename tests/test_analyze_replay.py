from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.analyze_replay import analyze_replay


def _varint(value: int) -> bytes:
    encoded = bytearray()
    while value >= 0x80:
        encoded.append((value & 0x7F) | 0x80)
        value >>= 7
    encoded.append(value)
    return bytes(encoded)


def _field(field_no: int, value: int | bytes) -> bytes:
    if isinstance(value, int):
        return _varint(field_no << 3) + _varint(value)
    return _varint((field_no << 3) | 2) + _varint(len(value)) + value


class ReplayAnalysisTests(unittest.TestCase):
    def test_tracks_economy_and_reliability(self) -> None:
        map_payload = _field(1, 25) + _field(2, 15)
        # Team A is enum zero and therefore omitted by normal proto3 encoding.
        harvester = _field(1, 7) + _field(15, b"")
        place = _field(1, harvester)
        player_a = _field(1, 120) + _field(4, 10)
        player_b = _field(1, 80)
        players = _field(1, player_a) + _field(2, player_b)
        output = _field(1, 4) + _field(2, b"ok") + _field(3, 7000) + _field(4, 1)
        turn = _field(1, _field(1, place)) + _field(1, _field(6, _field(1, players)))
        turn += _field(1, _field(9, output))
        replay = _field(1, map_payload) + _field(3, b"") + _field(3, turn) + _field(4, 0)
        with tempfile.TemporaryDirectory() as directory:
            replay_path = Path(directory) / "sample.replay26"
            replay_path.write_bytes(replay)
            result = analyze_replay(replay_path)

        self.assertEqual((25, 15, 1), (result["width"], result["height"], result["turns"]))
        self.assertEqual("A", result["winner"])
        self.assertEqual({"harvester": 1}, result["teams"]["A"]["placed"])
        self.assertEqual({"harvester": 1}, result["teams"]["A"]["first_placed_turn"])
        self.assertEqual(1, result["teams"]["A"]["first_titanium_delivery_turn"])
        self.assertEqual(
            {
                "bot_call_count": 1,
                "peak_exec_time_us": 7000,
                "p99_exec_time_us": 7000,
                "suspicious_output_count": 0,
                "tle_count": 1,
            },
            result["reliability"],
        )


if __name__ == "__main__":
    unittest.main()
