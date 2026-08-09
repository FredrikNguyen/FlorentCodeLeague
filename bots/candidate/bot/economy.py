
from __future__ import annotations

import math

from fcode import Position

from .types import BuilderState


def score_ore(
    ore: Position,
    *,
    origin: Position | None = None,
    route_cost: int = 0,
    harvester_cost: int = 0,
    expected_output_horizon: int = 0,
    exposure_risk: int = 0,
    congestion_penalty: int = 0,
) -> int:
    distance = 0 if origin is None else abs(ore.x - origin.x) + abs(ore.y - origin.y)
    return (
        int(expected_output_horizon)
        - max(0, int(harvester_cost))
        - max(0, int(route_cost))
        - distance * 2
        - max(0, int(exposure_risk))
        - max(0, int(congestion_penalty))
    )


def estimate_route_cost(
    route_length: int,
    conveyor_cost: int,
    *,
    splitter_count: int = 0,
    splitter_cost: int = 0,
    barrier_count: int = 0,
    barrier_cost: int = 0,
) -> int:
    return (
        max(0, int(route_length)) * max(0, int(conveyor_cost))
        + max(0, int(splitter_count)) * max(0, int(splitter_cost))
        + max(0, int(barrier_count)) * max(0, int(barrier_cost))
    )


def estimate_payback_round(
    total_cost: int,
    *,
    output_per_round: float = 2.5,
    start_round: int = 0,
    horizon: int = 1000,
) -> int | None:
    cost = max(0, int(total_cost))
    if cost == 0:
        return int(start_round)
    if output_per_round <= 0:
        return None
    payback = int(start_round) + math.ceil(cost / float(output_per_round))
    return payback if payback < int(horizon) else None


def expansion_allowed(
    *,
    projected_output: int,
    harvester_cost: int,
    route_cost: int,
    current_harvester_cost: int = 0,
    construction_reserve: int = 0,
    defense_reserve: int = 0,
    ammo_reserve: int = 0,
    liquidity_reserve: int = 0,
    available_resources: int | None = None,
    concurrent_projects: int = 0,
    max_projects: int = 3,
) -> bool:
    if int(concurrent_projects) >= min(4, max(1, int(max_projects))):
        return False
    total_cost = max(0, int(harvester_cost)) + max(0, int(route_cost))
    if int(projected_output) <= total_cost + max(0, int(current_harvester_cost)):
        return False
    reserves = sum(
        max(0, int(value))
        for value in (construction_reserve, defense_reserve, ammo_reserve, liquidity_reserve)
    )
    if available_resources is not None and int(available_resources) < total_cost + reserves:
        return False
    return True


def next_harvester_state(
    state: BuilderState,
    *,
    valid_ore: bool = True,
    claim_owned: bool = True,
    timed_out: bool = False,
    route_verified: bool = False,
    first_delivery_seen: bool = False,
) -> BuilderState:
    if not valid_ore or timed_out or not claim_owned:
        return BuilderState.DISCOVER
    transitions = {
        BuilderState.DISCOVER: BuilderState.CLAIM,
        BuilderState.CLAIM: BuilderState.APPROACH_BUILD_TILE,
        BuilderState.APPROACH_BUILD_TILE: BuilderState.ROUTE,
        BuilderState.ROUTE: BuilderState.BUILD,
        BuilderState.BUILD: BuilderState.VERIFY,
        BuilderState.VERIFY: BuilderState.DELIVER if route_verified else BuilderState.ROUTE,
        BuilderState.DELIVER: BuilderState.MAINTAIN if first_delivery_seen else BuilderState.DELIVER,
        BuilderState.MAINTAIN: BuilderState.MAINTAIN,
    }
    return transitions.get(state, BuilderState.DISCOVER)


def claim_should_release(valid_ore: bool, age: int, timeout: int, ownership_lost: bool) -> bool:
    return not valid_ore or ownership_lost or int(age) >= max(1, int(timeout))

