
from __future__ import annotations

import math
from dataclasses import dataclass
from collections.abc import Iterable, Mapping

from fcode import Position

from .types import BuilderState, EconomyPhase, ProjectState


MIN_EXPANSION_MARGIN = 40; LAST_EXPANSION_START_ROUND = 820; MAX_SIMULTANEOUS_BUILD_PROJECTS = 2; MAX_HEALTHY_ROUTES = 4; EMERGENCY_LIQUIDITY_RESERVE = 40; UNKNOWN_ROUTE_UPTIME = 0.75


@dataclass(frozen=True, slots=True)
class OreProjectEstimate: position: Position; route_length: int; travel_distance: int; first_delivery_round: int; total_cost: int; net_value: int; score: int


def conservative_project_cost(route_length: int, conveyor_cost: int, harvester_cost: int, *, scale_percent: int = 100) -> int:
    """Estimate missing infrastructure without duplicating engine pricing."""
    links = max(1, int(route_length))
    base = max(0, int(conveyor_cost))
    scale = max(0, int(scale_percent))
    conveyor_total = sum(math.ceil(base * (100 + scale * index / 100) / 100) for index in range(links))
    infrastructure = conveyor_total + max(0, int(harvester_cost))
    repair_contingency = max(2 * base, math.ceil(infrastructure * 0.10))
    return infrastructure + repair_contingency


def estimate_ore_project(position: Position, *, origin: Position, route_length: int, round_no: int, conveyor_cost: int, harvester_cost: int, scale_percent: int = 100, exposure_penalty: int = 0, congestion_penalty: int = 0, uptime_factor: float = UNKNOWN_ROUTE_UPTIME) -> OreProjectEstimate:
    travel_distance = abs(position.x - origin.x) + abs(position.y - origin.y)
    total_cost = conservative_project_cost(route_length, conveyor_cost, harvester_cost, scale_percent=scale_percent)
    delivery_latency = max(1, int(route_length)) + travel_distance + 1
    first_delivery_round = int(round_no) + delivery_latency
    remaining = max(0, 1000 - first_delivery_round)
    effective_rate = max(0.0, min(2.5, float(uptime_factor) * 2.5))
    gross_return = math.floor(remaining * effective_rate)
    risk_penalty = max(0, int(exposure_penalty)) + max(0, int(congestion_penalty))
    net_value = gross_return - total_cost - risk_penalty
    score = net_value - max(0, travel_distance - 1)
    return OreProjectEstimate(position, max(1, int(route_length)), travel_distance, first_delivery_round, total_cost, net_value, score)


def rank_ore_projects(ores: Iterable[Position], *, origin: Position, claimed: Iterable[Position] = (), unreachable: Iterable[Position] = (), route_lengths: Mapping[Position, int] | None = None, round_no: int = 0, conveyor_cost: int = 0, harvester_cost: int = 0, scale_percent: int = 100, free_titanium: int | None = None, exposure_penalty: Mapping[Position, int] | None = None, congestion_penalty: Mapping[Position, int] | None = None, min_margin: int = MIN_EXPANSION_MARGIN) -> tuple[OreProjectEstimate, ...]:
    claimed_set, unreachable_set = set(claimed), set(unreachable)
    lengths = route_lengths or {}
    exposure, congestion = exposure_penalty or {}, congestion_penalty or {}
    estimates: list[OreProjectEstimate] = []
    for ore in set(ores):
        if ore in claimed_set or ore in unreachable_set:
            continue
        estimate = estimate_ore_project(
            ore,
            origin=origin,
            route_length=max(1, int(lengths.get(ore, abs(ore.x - origin.x) + abs(ore.y - origin.y)))),
            round_no=round_no,
            conveyor_cost=conveyor_cost,
            harvester_cost=harvester_cost,
            scale_percent=scale_percent,
            exposure_penalty=exposure.get(ore, 0),
            congestion_penalty=congestion.get(ore, 0),
        )
        if estimate.net_value < int(min_margin):
            continue
        if free_titanium is not None and int(free_titanium) < estimate.total_cost:
            continue
        estimates.append(estimate)
    return tuple(sorted(estimates, key=lambda item: (-item.score, item.route_length, item.position.y, item.position.x)))


def compute_desired_builders(*, active_building_projects: int, maintaining_routes: int, known_ore_count: int, builder_cap: int = 7) -> int:
    maintaining = max(0, int(maintaining_routes))
    if maintaining >= MAX_HEALTHY_ROUTES:
        target = 7
    elif maintaining > 0:
        target = 6
    else:
        # Route 0 is deliberately built with five workers.  Once it has a
        # delivery heartbeat, the extra worker funds two secondary projects
        # and keeps one Builder available for exploration/repair.
        target = 5
    return max(3, min(max(3, int(builder_cap)), target))


def free_titanium_after_reserves(titanium: int, *, completion_reserve: int = 0, repair_reserve: int = 0, liquidity_reserve: int = EMERGENCY_LIQUIDITY_RESERVE, defense_reserve: int = 0, ammo_reserve: int = 0) -> int:
    return max(0, int(titanium) - sum(max(0, int(value)) for value in (completion_reserve, repair_reserve, liquidity_reserve, defense_reserve, ammo_reserve)))


def choose_economy_phase(project_states: Iterable[ProjectState], *, round_no: int, broken_routes: int = 0, profitable_expansion: bool = False) -> EconomyPhase:
    states = tuple(project_states)
    if int(round_no) >= LAST_EXPANSION_START_ROUND:
        return EconomyPhase.ENDGAME_HOLD
    if int(broken_routes) > 0:
        return EconomyPhase.REPAIR_PRIORITY
    first = states[0] if states else ProjectState.IDLE
    maintaining = sum(state == ProjectState.MAINTAIN for state in states)
    building = sum(state in (ProjectState.CLAIMED, ProjectState.PLANNING, ProjectState.BUILDING, ProjectState.VERIFYING, ProjectState.DELIVERING) for state in states)
    if first in (ProjectState.IDLE, ProjectState.FAILED):
        return EconomyPhase.BOOTSTRAP
    if first != ProjectState.MAINTAIN:
        return EconomyPhase.FIRST_ROUTE_BUILDING
    if any(state in (ProjectState.CLAIMED, ProjectState.PLANNING, ProjectState.BUILDING, ProjectState.VERIFYING, ProjectState.DELIVERING) for state in states[1:]):
        return EconomyPhase.SECONDARY_ROUTE_BUILDING
    if maintaining >= MAX_HEALTHY_ROUTES or not profitable_expansion:
        return EconomyPhase.ECONOMY_SATURATED if maintaining >= MAX_HEALTHY_ROUTES else EconomyPhase.MULTI_ROUTE_MAINTAINING
    if maintaining == 1:
        return EconomyPhase.EXPANSION_EVALUATION
    return EconomyPhase.MULTI_ROUTE_MAINTAINING


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
    max_projects: int = MAX_HEALTHY_ROUTES,
) -> bool:
    if int(concurrent_projects) >= min(MAX_HEALTHY_ROUTES, max(1, int(max_projects))):
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
