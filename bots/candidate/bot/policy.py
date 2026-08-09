from __future__ import annotations

from .types import Opening, OpeningDescriptor, Phase, Role, Scenario


def assign_role(
    entity_id: int,
    phase: Phase = Phase.OPENING,
    opening: Opening | None = None,
    *,
    route_owner: bool = False,
    large_map: bool = False,
    compact_map: bool = False,
    scenario: Scenario = Scenario.STANDARD,
) -> Role:
    """Small role grammar: economy by default, combat only on demand."""
    del opening, compact_map
    value = max(1, abs(int(entity_id)))
    if route_owner:
        return Role.ECONOMY
    if phase == Phase.DEFENSE or scenario == Scenario.CONTESTED:
        # Exact front count is unknown here; deterministic prefix gives immediate
        # response while extra workers remain repair/scout support.
        mod = (value - 1) % (6 if large_map else 5)
        if mod in (0, 1):
            return Role.DEFENDER
        if large_map and mod == 2:
            return Role.DEFENDER
        return Role.REPAIR if mod == (3 if large_map else 2) else Role.SCOUT
    if scenario == Scenario.ECONOMY_RESCUE:
        return Role.REPAIR if value == 1 else Role.SCOUT
    if phase in (Phase.OFFENSE, Phase.ENDGAME) or scenario in (Scenario.SIEGE, Scenario.ENDGAME):
        # Combat never consumes the information/economic frontier. Keep exactly
        # one network repairer, one persistent saboteur, and one dedicated scout
        # on *every* map; the resource-backed workforce curve supplies the strike
        # group on top. This avoids going blind on compact maps as soon as the
        # first Core rally flips the team into OFFENSE.
        if value == 1:
            return Role.REPAIR
        if value == 2:
            return Role.SABOTEUR
        if value == 3:
            return Role.SCOUT
        if value == 4:
            return Role.SIEGE
        return Role.RAIDER
    # Quiet/opening/expansion: no standing Defender and no speculative Raider.
    # One mobile specialist keeps probing enemy logistics after the first producer
    # while the other Scouts remain primarily economic survey / frontier workers.
    if value == 1:
        return Role.REPAIR
    if value == 2:
        return Role.SABOTEUR
    return Role.SCOUT

def describe_opening(
    width: int,
    height: int,
    nearby_ore_count: int = 0,
    nearest_ore_distance: int = 999,
    wall_density: float = 0.0,
    low_degree_passable_tiles: int = 0,
    route_exposure: float = 0.0,
    estimated_enemy_distance: int = 999,
) -> OpeningDescriptor:
    width = max(0, int(width))
    height = max(0, int(height))
    return OpeningDescriptor(
        width=width,
        height=height,
        area=width * height,
        nearby_ore_count=max(0, int(nearby_ore_count)),
        nearest_ore_distance=max(0, int(nearest_ore_distance)),
        wall_density=max(0.0, min(1.0, float(wall_density))),
        low_degree_passable_tiles=max(0, int(low_degree_passable_tiles)),
        route_exposure=max(0.0, min(1.0, float(route_exposure))),
        estimated_enemy_distance=max(0, int(estimated_enemy_distance)),
    )


def choose_opening(descriptor: OpeningDescriptor) -> Opening:
    compact = descriptor.area <= 196
    near_enemy = descriptor.estimated_enemy_distance <= max(
        5, min(descriptor.width, descriptor.height) // 2
    )
    chokepoint = descriptor.wall_density >= 0.28 or descriptor.low_degree_passable_tiles >= max(
        4, descriptor.area // 18
    )
    wide = descriptor.area >= 500 or descriptor.width >= 25 or descriptor.height >= 25
    if near_enemy:
        return Opening.ANTI_RUSH
    if chokepoint:
        return Opening.CHOKEPOINT_CONTROL
    if compact:
        return Opening.COMPACT_PRESSURE
    if wide:
        return Opening.WIDE_EXPANSION
    return Opening.BALANCED_ECONOMY
