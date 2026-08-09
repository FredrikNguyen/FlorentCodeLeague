from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from fcode import Position
from .types import Budget, Claim, Opening, Phase, Scenario, Threat, ThreatKind


class Slot(IntEnum):
    SCHEMA_VERSION = 0; STRATEGY = 1; PRIMARY_ORE = 2; ENEMY_CORE = 3; THREAT = 4; LOGISTICS = 5; DESIRED_BUILDERS = 6; AMMO_TARGET = 7; DEFENSE_ALERT = 8; RALLY = 9; CLAIM_0 = 10; CLAIM_1 = 11; CLAIM_2 = 12; BUDGET = 13; CLAIM_3 = 14; EPOCH = 15


SCHEMA_VERSION = 15; UNKNOWN = 0; COORD_BITS = 10; EPOCH_BITS = 6; OWNER_BITS = 16; COORD_MASK = 1023; EPOCH_MASK = 63; OWNER_MASK = 65535; MAX_U32 = 0xFFFFFFFF
CORE_SLOTS = frozenset({Slot.SCHEMA_VERSION, Slot.STRATEGY, Slot.DESIRED_BUILDERS, Slot.AMMO_TARGET, Slot.BUDGET, Slot.EPOCH})
CLAIM_OWNER_SLOTS = {0: frozenset({Slot.PRIMARY_ORE, Slot.CLAIM_0}), 1: frozenset({Slot.LOGISTICS, Slot.CLAIM_1}), 2: frozenset({Slot.THREAT, Slot.CLAIM_2}), 3: frozenset({Slot.ENEMY_CORE, Slot.CLAIM_3})}
SLOT_OWNER = {slot: "core" for slot in CORE_SLOTS}
for _owner, _slots in CLAIM_OWNER_SLOTS.items():
    for _slot in _slots: SLOT_OWNER[_slot] = _owner


def _valid(pos: Position, width: int, height: int | None = None) -> bool:
    return width > 0 and pos.x >= 0 and pos.y >= 0 and pos.x < width and (height is None or pos.y < height)


def pack_position(pos: Position, width: int, height: int | None = None) -> int:
    if not _valid(pos, width, height): raise ValueError("position outside map")
    value = 1 + pos.y * width + pos.x
    if value > COORD_MASK: raise ValueError("position does not fit ten-bit coordinate")
    return value


def unpack_position(value: int, width: int, height: int | None = None) -> Position | None:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= COORD_MASK or width <= 0: return None
    position = Position((value - 1) % width, (value - 1) // width)
    return position if _valid(position, width, height) else None


def pack_epoch(epoch: int) -> int:
    if isinstance(epoch, bool) or not isinstance(epoch, int): raise ValueError("epoch must be an integer")
    return epoch & EPOCH_MASK


def epoch_distance(now: int, then: int) -> int: return (int(now) - int(then)) & EPOCH_MASK
def claim_is_fresh(claim: Claim | None, now_epoch: int) -> bool:
    # Live route owners refresh every four rounds. A 15-round lease replaces a
    # destroyed or permanently faulting owner much faster than the old 31-round
    # half-epoch timeout while remaining tolerant of transient missed turns.
    return (
        claim is not None
        and claim.owner_id > 0
        and epoch_distance(now_epoch, claim.epoch) <= 15
    )


def pack_claim(position: Position | None, width: int, epoch: int, owner_id: int, height: int | None = None) -> int:
    if isinstance(owner_id, bool) or not isinstance(owner_id, int) or not 0 <= owner_id <= OWNER_MASK: raise ValueError("owner id does not fit codec")
    coordinate = 0 if position is None else pack_position(position, width, height)
    return (coordinate << 22) | (pack_epoch(epoch) << 16) | owner_id


def unpack_claim(value: int, width: int, height: int | None = None) -> Claim | None:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 < value <= MAX_U32: return None
    coordinate, epoch, owner = (value >> 22) & COORD_MASK, (value >> 16) & EPOCH_MASK, value & OWNER_MASK
    if owner == 0: return None
    position = None if coordinate == 0 else unpack_position(coordinate, width, height)
    return None if coordinate and position is None else Claim(position, epoch, owner)


def claim_slot(owner_index: int) -> Slot:
    try:
        return (Slot.CLAIM_0, Slot.CLAIM_1, Slot.CLAIM_2, Slot.CLAIM_3)[owner_index]
    except (IndexError, TypeError):
        raise ValueError("claim owner must be 0, 1, 2, or 3") from None


def slot_owner(slot: int | Slot) -> str | int | None:
    try: return SLOT_OWNER.get(Slot(slot))
    except (TypeError, ValueError): return None


def can_write(slot: int | Slot, writer: str | int) -> bool: return (owner := slot_owner(slot)) is not None and owner == writer


@dataclass(frozen=True, slots=True)
class TeamStatus:
    """Compressed Core-authored team snapshot carried in STRATEGY high bits.

    The low twelve bits remain the existing phase/opening/scenario codec.  The
    upper twenty bits are intentionally single-writer and one-round delayed,
    matching Store semantics while giving every Builder the same macro picture.
    """

    route_target: int = 0
    route_capacity: int = 0
    maintaining_routes: int = 0
    active_projects: int = 0
    defense_severity: int = 0
    attack_priority: int = 0


def encode_strategy(
    phase: Phase,
    opening: Opening,
    scenario: Scenario = Scenario.STANDARD,
    *,
    route_target: int = 0,
    route_capacity: int = 0,
    maintaining_routes: int = 0,
    active_projects: int = 0,
    defense_severity: int = 0,
    attack_priority: int = 0,
) -> int:
    value = (
        tuple(Phase).index(phase)
        | (tuple(Opening).index(opening) << 4)
        | (tuple(Scenario).index(scenario) << 8)
    )
    value |= (max(0, min(7, int(route_target))) & 7) << 12
    value |= (max(0, min(7, int(route_capacity))) & 7) << 15
    value |= (max(0, min(7, int(maintaining_routes))) & 7) << 18
    value |= (max(0, min(7, int(active_projects))) & 7) << 21
    value |= (max(0, min(15, int(defense_severity))) & 15) << 24
    value |= (max(0, min(15, int(attack_priority))) & 15) << 28
    return value


def decode_team_status(value: int) -> TeamStatus:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return TeamStatus()
    return TeamStatus(
        route_target=(value >> 12) & 7,
        route_capacity=(value >> 15) & 7,
        maintaining_routes=(value >> 18) & 7,
        active_projects=(value >> 21) & 7,
        defense_severity=(value >> 24) & 15,
        attack_priority=(value >> 28) & 15,
    )

@dataclass(frozen=True, slots=True)
class TeamPulse:
    """Core-authored progress/congestion pulse packed into the EPOCH slot.

    Low six bits remain the ordinary round epoch.  The upper bits are a
    single-writer delayed snapshot used only for coordination; legacy epoch
    readers can continue masking with 63.
    """

    epoch: int = 0
    route_progress_age: int = 0
    core_congestion: int = 0


def encode_epoch_pulse(
    epoch: int,
    *,
    route_progress_age: int = 0,
    core_congestion: int = 0,
) -> int:
    return (
        (int(epoch) & EPOCH_MASK)
        | ((max(0, min(63, int(route_progress_age))) & 63) << 6)
        | ((max(0, min(15, int(core_congestion))) & 15) << 12)
    )


def decode_epoch_pulse(value: int) -> TeamPulse:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return TeamPulse()
    return TeamPulse(
        epoch=value & EPOCH_MASK,
        route_progress_age=(value >> 6) & 63,
        core_congestion=(value >> 12) & 15,
    )


def decode_strategy(value: int) -> tuple[Phase, Opening] | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0: return None
    try: return tuple(Phase)[value & 15], tuple(Opening)[(value >> 4) & 15]
    except IndexError: return None




def decode_scenario(value: int) -> Scenario:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return Scenario.STANDARD
    index = (value >> 8) & 15
    try:
        return tuple(Scenario)[index]
    except IndexError:
        return Scenario.STANDARD


def encode_threat(threat: Threat, width: int, height: int | None = None) -> int: return pack_position(threat.position, width, height) | (tuple(ThreatKind).index(threat.kind) << 10)


def decode_threat(value: int, width: int, height: int | None = None) -> Threat | None:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 < value <= MAX_U32: return None
    position, kind = unpack_position(value & COORD_MASK, width, height), (value >> 10) & 15
    return None if position is None or kind >= len(tuple(ThreatKind)) else Threat(position, tuple(ThreatKind)[kind])


def encode_budget(budget: Budget) -> int:
    encoded = 0
    for index, value in enumerate((budget.construction, budget.defense, budget.ammo, budget.expansion, budget.liquidity)): encoded |= max(0, min(63, int(value // 10))) << index * 6
    return encoded


def decode_budget(value: int) -> Budget | None:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= MAX_U32: return None
    return Budget(*(((value >> index * 6) & 63) * 10 for index in range(5)))


def encode_alert(position: Position | None, width: int, expires_epoch: int = 0) -> int: return (0 if position is None else pack_position(position, width)) | ((expires_epoch & EPOCH_MASK) << 10)


def decode_alert(value: int, width: int, height: int | None = None) -> tuple[Position | None, int] | None:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= MAX_U32: return None
    coordinate, position = value & COORD_MASK, None
    if coordinate: position = unpack_position(coordinate, width, height)
    return None if coordinate and position is None else (position, (value >> 10) & EPOCH_MASK)


def encode_defense_alert(
    position: Position | None,
    width: int,
    expires_epoch: int = 0,
    severity: int = 0,
    kind: ThreatKind = ThreatKind.UNKNOWN,
) -> int:
    """Pack a backward-compatible alert with severity and threat kind.

    The low 16 bits retain ``encode_alert`` so an older reader still receives a
    valid position and expiry.  New readers use the extra metadata to distinguish
    a harmless scout sighting from an active Core/Harvester sabotage emergency.
    """
    try:
        kind_index = tuple(ThreatKind).index(kind)
    except (TypeError, ValueError):
        kind_index = tuple(ThreatKind).index(ThreatKind.UNKNOWN)
    return (
        encode_alert(position, width, expires_epoch)
        | ((max(0, min(15, int(severity))) & 15) << 16)
        | ((kind_index & 7) << 20)
    )


def decode_defense_alert(
    value: int,
    width: int,
    height: int | None = None,
) -> tuple[Position | None, int, int, ThreatKind] | None:
    decoded = decode_alert(value, width, height)
    if decoded is None:
        return None
    position, expires = decoded
    severity = (int(value) >> 16) & 15
    kind_index = (int(value) >> 20) & 7
    try:
        kind = tuple(ThreatKind)[kind_index]
    except IndexError:
        kind = ThreatKind.UNKNOWN
    return position, expires, severity, kind


def encode_rally(
    position: Position | None,
    width: int,
    expires_epoch: int = 0,
    priority: int = 0,
) -> int:
    """Pack an alert-compatible rally with a 4-bit objective priority.

    The low 16 bits retain the original alert codec, so older readers still see
    the position and expiry.  The priority lets scouts avoid overwriting a known
    enemy Core with a lower-value conveyor sighting.
    """
    return encode_alert(position, width, expires_epoch) | ((max(0, min(15, int(priority))) & 15) << 16)


def decode_rally(
    value: int,
    width: int,
    height: int | None = None,
) -> tuple[Position | None, int, int] | None:
    decoded = decode_alert(value, width, height)
    if decoded is None:
        return None
    position, expires = decoded
    return position, expires, (int(value) >> 16) & 15

