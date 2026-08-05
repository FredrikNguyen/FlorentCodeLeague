from __future__ import annotations

from enum import IntEnum
from fcode import Position
from .types import Assignment, Budget, Opening, Phase, Project, ProjectState, Threat, ThreatKind


class Slot(IntEnum):
    SCHEMA_VERSION = 0; STRATEGY = 1; PROJECT_0 = 2; ENEMY_CORE = 3; PROJECT_2 = 4; PROJECT_1 = 5; DESIRED_BUILDERS = 6; AMMO_TARGET = 7; DEFENSE_ALERT = 8; RALLY = 9; CLAIM_0 = 10; CLAIM_1 = 11; CLAIM_2 = 12; BUDGET = 13; DIAGNOSTICS = 14; EPOCH = 15
    PRIMARY_ORE = PROJECT_0; LOGISTICS = PROJECT_1; THREAT = PROJECT_2; RESERVED = DIAGNOSTICS


SCHEMA_VERSION = 3; UNKNOWN = 0; COORD_BITS = 10; EPOCH_BITS = 6; STATE_BITS = 3; OWNER_BITS = 16; COORD_MASK = (1 << COORD_BITS) - 1; EPOCH_MASK = (1 << EPOCH_BITS) - 1; STATE_MASK = (1 << STATE_BITS) - 1; OWNER_MASK = (1 << OWNER_BITS) - 1; MAX_U32 = 0xFFFFFFFF
PROJECT_SLOTS = (Slot.PROJECT_0, Slot.PROJECT_1, Slot.PROJECT_2); CLAIM_SLOTS = (Slot.CLAIM_0, Slot.CLAIM_1, Slot.CLAIM_2)
PROJECT_STATES = tuple(ProjectState); PROJECT_STATE_INDEX = {state: index for index, state in enumerate(PROJECT_STATES)}
SLOT_OWNER = {slot: "core" for slot in Slot}
for _index, _slot in enumerate(PROJECT_SLOTS): SLOT_OWNER[_slot] = _index
SLOT_OWNER.update({Slot.ENEMY_CORE: "scout", Slot.RALLY: "scout", Slot.DEFENSE_ALERT: "defender", Slot.DIAGNOSTICS: "core"})


def _valid(pos: Position, width: int, height: int | None = None) -> bool: return isinstance(pos, Position) and width > 0 and pos.x >= 0 and pos.y >= 0 and pos.x < width and (height is None or pos.y < height)
def _number(value: object) -> bool: return isinstance(value, int) and not isinstance(value, bool)
def _store(ct: object, slot: Slot) -> int | None:
    try: return int(ct.read_store(int(slot)))
    except Exception: return None
def _write(ct: object, slot: Slot, value: int) -> bool:
    try: ct.write_store(int(slot), value); return True
    except Exception: return False


def pack_position(pos: Position, width: int, height: int | None = None) -> int:
    if not _valid(pos, width, height): raise ValueError("position outside map")
    value = 1 + pos.y * width + pos.x; return value if value <= COORD_MASK else (_ for _ in ()).throw(ValueError("position does not fit ten-bit coordinate"))


def unpack_position(value: int, width: int, height: int | None = None) -> Position | None:
    if not _number(value) or not 1 <= value <= COORD_MASK or width <= 0: return None
    position = Position((value - 1) % width, (value - 1) // width); return position if _valid(position, width, height) else None


pack_epoch = lambda epoch: epoch if _number(epoch) and 0 <= epoch <= EPOCH_MASK else (_ for _ in ()).throw(ValueError("epoch must be a six-bit integer"))


epoch_distance = lambda now, then: (int(now) - int(then)) & EPOCH_MASK
assignment_is_fresh = lambda assignment, now_epoch: assignment is not None and assignment.owner_id > 0 and epoch_distance(now_epoch, assignment.generation) <= 31


def encode_assignment(owner_id: int, generation: int) -> int:
    if not _number(owner_id) or not 0 < owner_id <= OWNER_MASK: raise ValueError("owner id does not fit codec")
    return (pack_epoch(generation) << OWNER_BITS) | owner_id


def decode_assignment(value: int) -> Assignment | None:
    if not _number(value) or not 0 < value <= (EPOCH_MASK << OWNER_BITS) | OWNER_MASK: return None
    return Assignment(value & OWNER_MASK, (value >> OWNER_BITS) & EPOCH_MASK)


def _slot(owner_index: int, slots: tuple[Slot, ...]) -> Slot:
    if owner_index not in (0, 1, 2): raise ValueError("slot owner must be 0, 1, or 2")
    return slots[owner_index]
def claim_slot(owner_index: int) -> Slot: return _slot(owner_index, CLAIM_SLOTS)
def project_slot(owner_index: int) -> Slot: return _slot(owner_index, PROJECT_SLOTS)


def slot_owner(slot: int | Slot) -> str | int | None: return SLOT_OWNER.get(Slot(slot)) if _number(slot) and 0 <= int(slot) < 16 else None


can_write = lambda slot, writer: (owner := slot_owner(slot)) is not None and owner == writer


def _schema_ok(ct: object) -> bool:
    return _store(ct, Slot.SCHEMA_VERSION) in (0, SCHEMA_VERSION)


def read_assignment(ct: object, index: int) -> Assignment | None:
    if index not in (0, 1, 2) or not _schema_ok(ct): return None
    return decode_assignment(_store(ct, claim_slot(index)) or 0)


def write_assignment(ct: object, index: int, owner_id: int | None, generation: int, *, writer: str | int = "core") -> bool:
    try: slot = claim_slot(index)
    except Exception: return False
    return _schema_ok(ct) and can_write(slot, writer) and _write(ct, slot, 0 if owner_id is None else encode_assignment(owner_id, generation))


def encode_project(position: Position | None, epoch: int, project_state: ProjectState | int, width: int, height: int | None = None) -> int:
    coordinate = 0 if position is None else pack_position(position, width, height)
    state_index = int(project_state) if isinstance(project_state, int) and not isinstance(project_state, bool) else PROJECT_STATE_INDEX.get(project_state, -1)
    if not 0 <= state_index < len(PROJECT_STATES): raise ValueError("project state is invalid")
    return coordinate | (pack_epoch(epoch) << COORD_BITS) | (state_index << (COORD_BITS + EPOCH_BITS))


def decode_project(value: int, width: int, height: int | None = None) -> Project | None:
    if not _number(value) or not 0 <= value <= MAX_U32: return None
    coordinate, epoch, state_value = value & COORD_MASK, (value >> COORD_BITS) & EPOCH_MASK, (value >> (COORD_BITS + EPOCH_BITS)) & STATE_MASK
    state = PROJECT_STATES[state_value]
    position = None if coordinate == 0 else unpack_position(coordinate, width, height); return None if coordinate and position is None else Project(position, epoch, state)


def read_project(ct: object, index: int) -> Project | None:
    if index not in (0, 1, 2) or not _schema_ok(ct): return None
    value = _store(ct, project_slot(index))
    if value is None: return None
    try: return decode_project(value, int(ct.get_map_width()), int(ct.get_map_height()))
    except Exception: return None


def write_project(ct: object, index: int, position: Position | None, epoch: int, project_state: ProjectState | int, width: int, height: int | None = None, *, writer: str | int | None = None) -> bool:
    try: slot = project_slot(index)
    except Exception: return False
    writer = index if writer is None else writer
    return _schema_ok(ct) and can_write(slot, writer) and _write(ct, slot, encode_project(position, epoch, project_state, width, height))


def encode_strategy(phase: Phase, opening: Opening) -> int: return tuple(Phase).index(phase) | (tuple(Opening).index(opening) << 4)


def decode_strategy(value: int) -> tuple[Phase, Opening] | None:
    if not _number(value) or value < 0: return None
    phases, openings = tuple(Phase), tuple(Opening); return (phases[value & 15], openings[(value >> 4) & 15]) if (value & 15) < len(phases) and ((value >> 4) & 15) < len(openings) else None


def encode_threat(threat: Threat, width: int, height: int | None = None) -> int: return pack_position(threat.position, width, height) | (tuple(ThreatKind).index(threat.kind) << COORD_BITS)


def decode_threat(value: int, width: int, height: int | None = None) -> Threat | None:
    if not _number(value) or not 0 < value <= MAX_U32: return None
    position, kind = unpack_position(value & COORD_MASK, width, height), (value >> COORD_BITS) & 15
    return None if position is None or kind >= len(tuple(ThreatKind)) else Threat(position, tuple(ThreatKind)[kind])


def encode_budget(budget: Budget) -> int:
    return sum(max(0, min(63, int(value // 10))) << index * 6 for index, value in enumerate((budget.construction, budget.defense, budget.ammo, budget.expansion, budget.liquidity)))


def decode_budget(value: int) -> Budget | None:
    if not _number(value) or not 0 <= value <= MAX_U32: return None
    return Budget(*(((value >> index * 6) & 63) * 10 for index in range(5)))


def encode_alert(position: Position | None, width: int, expires_epoch: int = 0) -> int: return (0 if position is None else pack_position(position, width)) | ((int(expires_epoch) & EPOCH_MASK) << COORD_BITS)


def decode_alert(value: int, width: int, height: int | None = None) -> tuple[Position | None, int] | None:
    return (lambda coordinate, position: None if coordinate and position is None else (position, (value >> COORD_BITS) & EPOCH_MASK))(value & COORD_MASK, unpack_position(value & COORD_MASK, width, height) if value & COORD_MASK else None) if _number(value) and 0 <= value <= MAX_U32 else None
