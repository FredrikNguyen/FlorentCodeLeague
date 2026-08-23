#!/usr/bin/env python3
"""Extract compact, deterministic diagnostics from Florent .replay26 files."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

ENTITY_KIND_FIELDS = {
    10: "builder",
    11: "conveyor",
    12: "splitter",
    15: "harvester",
    18: "barrier",
    20: "core",
    21: "gunner",
    22: "sentinel",
    24: "launcher",
}
TEAM_NAMES = {0: "A", 1: "B"}


def _varint(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while offset < len(data) and shift < 70:
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        if byte < 0x80:
            return value, offset
        shift += 7
    raise ValueError("invalid protobuf varint")


def _fields(data: bytes) -> list[tuple[int, int, int | bytes]]:
    result: list[tuple[int, int, int | bytes]] = []
    offset = 0
    while offset < len(data):
        key, offset = _varint(data, offset)
        field_no, wire_type = key >> 3, key & 7
        if field_no <= 0:
            raise ValueError("invalid protobuf field number")
        if wire_type == 0:
            value, offset = _varint(data, offset)
        elif wire_type == 1:
            if offset + 8 > len(data):
                raise ValueError("truncated fixed64 field")
            value = data[offset : offset + 8]
            offset += 8
        elif wire_type == 2:
            size, offset = _varint(data, offset)
            if offset + size > len(data):
                raise ValueError("truncated length-delimited field")
            value = data[offset : offset + size]
            offset += size
        elif wire_type == 5:
            if offset + 4 > len(data):
                raise ValueError("truncated fixed32 field")
            value = data[offset : offset + 4]
            offset += 4
        else:
            raise ValueError(f"unsupported protobuf wire type {wire_type}")
        result.append((field_no, wire_type, value))
    return result


def _messages(data: bytes, field_no: int) -> list[bytes]:
    return [
        value
        for number, wire_type, value in _fields(data)
        if number == field_no and wire_type == 2 and isinstance(value, bytes)
    ]


def _integer(data: bytes, field_no: int, default: int = 0) -> int:
    for number, wire_type, value in _fields(data):
        if number == field_no and wire_type == 0 and isinstance(value, int):
            return value
    return default


def _text(data: bytes, field_no: int) -> str:
    messages = _messages(data, field_no)
    return messages[0].decode("utf-8", errors="replace") if messages else ""


def _entity(data: bytes) -> dict[str, Any]:
    parsed = _fields(data)
    kind = next(
        (
            name
            for number, name in ENTITY_KIND_FIELDS.items()
            if any(
                field_no == number and wire_type == 2
                for field_no, wire_type, _ in parsed
            )
        ),
        "unknown",
    )
    return {
        "id": _integer(data, 1, -1),
        # TEAM_A is protobuf enum value zero, so valid Team A entities commonly
        # omit the field entirely and rely on the proto3 default.
        "team": TEAM_NAMES.get(_integer(data, 2, 0), "unknown"),
        "kind": kind,
    }


def _players(data: bytes) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for team_field, team_name in ((1, "A"), (2, "B")):
        payloads = _messages(data, team_field)
        if not payloads:
            continue
        player = payloads[0]
        result[team_name] = {
            "titanium": _integer(player, 1),
            "resources_collected": _integer(player, 3),
            "titanium_collected": _integer(player, 4),
            "ammo": _integer(player, 7),
        }
    return result


def analyze_replay(path: Path) -> dict[str, Any]:
    replay = path.read_bytes()
    map_payloads = _messages(replay, 1)
    if not map_payloads:
        raise ValueError("replay has no map payload")
    map_payload = map_payloads[0]
    turns = _messages(replay, 3)
    winner = TEAM_NAMES.get(_integer(replay, 4, -1))

    entities: dict[int, tuple[str, str]] = {}
    # A replay update repeats every still-alive entity, so counting every
    # `place` message overstates persistent buildings (a 5-Gunner game used to
    # look like dozens of purchases).  Keep ids for true unique placements and
    # retain update counts separately for diagnostics.
    placed_ids: dict[str, dict[str, set[int]]] = {
        "A": {},
        "B": {},
    }
    placement_updates: dict[str, Counter[str]] = {"A": Counter(), "B": Counter()}
    first_placed: dict[str, dict[str, int]] = {"A": {}, "B": {}}
    first_delivery: dict[str, int | None] = {"A": None, "B": None}
    latest_players: dict[str, dict[str, int]] = {}
    tle_count = 0
    suspicious_output_count = 0
    peak_exec_time_us = 0
    exec_times_us: list[int] = []

    for turn_no, turn in enumerate(turns):
        for update in _messages(turn, 1):
            for place in _messages(update, 1):
                payloads = _messages(place, 1)
                if not payloads:
                    continue
                entity = _entity(payloads[0])
                team = entity["team"]
                kind = entity["kind"]
                entity_id = entity["id"]
                entities[entity_id] = (team, kind)
                if team in placed_ids:
                    placed_ids[team].setdefault(kind, set()).add(entity_id)
                    placement_updates[team][kind] += 1
                    first_placed[team].setdefault(kind, turn_no)
            for remove in _messages(update, 3):
                entities.pop(_integer(remove, 1, -1), None)
            for players_update in _messages(update, 6):
                payloads = _messages(players_update, 1)
                if not payloads:
                    continue
                latest_players = _players(payloads[0])
                for team, stats in latest_players.items():
                    if stats["titanium_collected"] > 0 and first_delivery[team] is None:
                        first_delivery[team] = turn_no
            for bot_output in _messages(update, 9):
                exec_time_us = _integer(bot_output, 3)
                exec_times_us.append(exec_time_us)
                peak_exec_time_us = max(peak_exec_time_us, exec_time_us)
                tle_count += int(_integer(bot_output, 4) != 0)
                output = _text(bot_output, 2).lower()
                if any(marker in output for marker in ("traceback", "exception", "error")):
                    suspicious_output_count += 1

    alive: dict[str, Counter[str]] = {"A": Counter(), "B": Counter()}
    for team, kind in entities.values():
        if team in alive:
            alive[team][kind] += 1
    ordered_exec_times = sorted(exec_times_us)
    p99_index = max(0, math.ceil(0.99 * len(ordered_exec_times)) - 1)
    p99_exec_time_us = ordered_exec_times[p99_index] if ordered_exec_times else 0

    return {
        "path": str(path),
        "width": _integer(map_payload, 1),
        "height": _integer(map_payload, 2),
        "turns": max(0, len(turns) - 1),
        "winner": winner,
        "teams": {
            team: {
                "placed": {
                    kind: len(ids)
                    for kind, ids in sorted(placed_ids[team].items())
                },
                "placement_update_count": dict(sorted(placement_updates[team].items())),
                "first_placed_turn": dict(sorted(first_placed[team].items())),
                "first_titanium_delivery_turn": first_delivery[team],
                "final_players": latest_players.get(team, {}),
                "alive": dict(sorted(alive[team].items())),
            }
            for team in ("A", "B")
        },
        "reliability": {
            "bot_call_count": len(exec_times_us),
            "tle_count": tle_count,
            "suspicious_output_count": suspicious_output_count,
            "p99_exec_time_us": p99_exec_time_us,
            "peak_exec_time_us": peak_exec_time_us,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("replays", nargs="+", type=Path)
    args = parser.parse_args()
    results = [analyze_replay(path) for path in args.replays]
    print(json.dumps(results[0] if len(results) == 1 else results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
