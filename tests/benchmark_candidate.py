from __future__ import annotations

import json
from pathlib import Path
from statistics import quantiles
import sys
from time import perf_counter_ns

from fcode import Direction, EntityType, Position, Team

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bots.candidate.bot.defense import choose_defensive_build
from bots.candidate.bot.logistics import plan_core_outward_route
from bots.candidate.bot.navigation import Navigator, bounded_bfs
from bots.candidate.bot.turrets import choose_launch
from tests.candidate_fakes import FakeEntity, FakeController


def _percentile(values: list[float], percentile: float) -> float:
    if len(values) < 2:
        return values[0] if values else 0.0
    return float(quantiles(values, n=100, method="inclusive")[int(percentile) - 1])


def _sample(label: str, function, count: int = 64) -> dict[str, float | int | str]:
    for _ in range(4):
        function()
    samples: list[float] = []
    for _ in range(count):
        start = perf_counter_ns()
        function()
        samples.append((perf_counter_ns() - start) / 1_000_000.0)
    return {
        "label": label,
        "samples": len(samples),
        "p50_ms": round(_percentile(samples, 50), 6),
        "p95_ms": round(_percentile(samples, 95), 6),
        "p99_ms": round(_percentile(samples, 99), 6),
        "max_ms": round(max(samples), 6),
    }


def main() -> int:
    walls = {Position(x, 15) for x in range(30) if x not in (0, 29)}
    route_ore = Position(0, 0)
    route_core = (Position(29, 29), Position(28, 29), Position(29, 28), Position(28, 28))
    placement_positions = tuple(Position(x, y) for y in range(10, 20) for x in range(10, 20))
    attackable = {
        (position, direction): 4
        for position in placement_positions
        for direction in Direction
    }
    launcher = FakeController(entity_type=EntityType.LAUNCHER, width=30, height=30, position=Position(15, 15))
    launcher.entities[2] = FakeEntity(EntityType.BUILDER_BOT, Position(16, 15), Team.A)
    destinations = tuple(Position(x, y) for y in range(11, 18) for x in range(11, 18))[:32]

    def blocked_step_invalidation() -> None:
        local_walls: set[Position] = set()
        local_navigator = Navigator(30, 30, local_walls)
        local_navigator.next_direction(Position(0, 0), Position(29, 29), 0)
        local_walls.add(Position(1, 0))
        local_navigator.next_direction(Position(0, 0), Position(29, 29), 0)

    def route_cpu_stop_resume() -> None:
        search: dict[str, object] = {}
        checks = iter((0, 7000))
        first = plan_core_outward_route(
            route_ore,
            route_core,
            30,
            30,
            walls,
            cpu_check=lambda: next(checks, 7000),
            search_state=search,
        )
        if first is not None or search.get("complete"):
            raise AssertionError("route search did not preserve CPU-stopped state")
        resumed = plan_core_outward_route(
            route_ore,
            route_core,
            30,
            30,
            walls,
            cpu_check=lambda: 0,
            search_state=search,
        )
        if resumed is None:
            raise AssertionError("route search did not resume")

    cases = [
        _sample("bfs_30x30", lambda: bounded_bfs(Position(0, 0), Position(29, 29), 30, 30, walls)),
        _sample(
            "route_plan_30x30_worst_case",
            lambda: plan_core_outward_route(route_ore, route_core, 30, 30, walls),
        ),
        _sample("route_cpu_stop_resume", route_cpu_stop_resume),
        _sample("blocked_step_invalidation", blocked_step_invalidation),
        _sample(
            "defense_placement",
            lambda: choose_defensive_build(
                placement_positions,
                reserved_core_exits=frozenset(),
                route_cells=frozenset(),
                escape_tiles=frozenset(),
                attackable=attackable,
            ),
        ),
        _sample(
            "launcher_destinations",
            lambda: choose_launch(
                launcher,
                pickup_tiles=(Position(16, 15),),
                destinations=destinations,
                enemy_target=Position(29, 29),
            ),
        ),
    ]
    summary = {
        "samples": cases,
        "p99_ms": max(case["p99_ms"] for case in cases),
        "max_ms": max(case["max_ms"] for case in cases),
        "p99_threshold_ms": 8.0,
        "sample_max_threshold_ms": 10.0,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if any(
        case["p99_ms"] >= 8.0 or case["max_ms"] >= 10.0 for case in cases
    ) else 0


if __name__ == "__main__":
    raise SystemExit(main())
