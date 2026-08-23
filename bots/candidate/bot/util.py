"""Small stateless helpers shared by every role — store (de)serialization,
distance math, and the two adjacency checks used throughout movement/building
logic. Kept dependency-free (no Player state) so any module can import them.
"""

from fcode import Controller, Position


def pack_pos(pos: Position) -> int:
    """Encode a position into a single value for the communication store.

    Offset by +1 so that position (0, 0) doesn't encode as 0, which we reserve
    to mean "no data".
    """
    return ((pos.x + 1) << 16) | (pos.y + 1)


def unpack_pos(val: int) -> Position | None:
    """Decode a position from the communication store. Returns None if empty (0)."""
    if val == 0:
        return None
    return Position((val >> 16) - 1, (val & 0xFFFF) - 1)


def manhattan(a: Position, b: Position) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def in_bounds(ct: Controller, pos: Position) -> bool:
    return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()


def adjacent(a: Position, b: Position) -> bool:
    """True if a and b are orthogonally adjacent (a legal build/heal/fire target)."""
    return abs(a.x - b.x) + abs(a.y - b.y) == 1


def core_footprint(anchor: Position) -> list[Position]:
    """The 4 tiles a core occupies. get_position() on a core reports the
    NORTHWEST corner of its 2x2 footprint (verified against the engine — see
    core_spawn_ring below for the probe that establishes it).
    """
    return [Position(anchor.x + dx, anchor.y + dy) for dx in (0, 1) for dy in (0, 1)]


def core_spawn_ring(ct: Controller, anchor: Position) -> list[Position]:
    """Every in-bounds tile a core at `anchor` may spawn a builder onto: the
    12-tile ring touching its 2x2 footprint, minus the footprint itself.

    This exists because iterating `anchor.add(d)` over the 8 compass
    directions — the obvious thing, and what this bot used to do — is WRONG
    for a 2x2 building. Three of those 8 tiles ARE the core's own other
    footprint tiles, and the remaining 5 only cover the footprint's
    northwest corner. Probed directly against the engine on jackpot:

        CORE at (0, 0): legal spawn tiles = [(2,0), (2,1), (0,2), (1,2), (2,2)]
          anchor.add(d) for the 8 directions = [(0,-1), (1,-1), (1,0), (1,1),
                                                (0,1), (-1,1), (-1,0), (-1,-1)]
          intersection = []   <-- every candidate OOB or inside ourselves

    So a core flush against the north AND west edges could never spawn a
    single builder for the entire match: 0 units, 0 titanium mined, a
    guaranteed loss. Three maps in the current pool put team A's core at
    (0, 0) — jackpot, sweden, vase — and all three were unconditional
    losses before this fix; `string` was crippled the same way (2 builders
    all game). A core merely on one edge silently loses candidates too, so
    this matters beyond the corner case.

    The ring below reproduces the engine's own legal set exactly at both
    cores probed above, which is also what confirms the anchor is the
    northwest corner rather than some other convention.

    Returned unshuffled and in a stable order; the caller randomises.
    """
    ring: list[Position] = []
    fx, fy = anchor.x, anchor.y
    for x in range(fx - 1, fx + 3):
        for y in range(fy - 1, fy + 3):
            if fx <= x <= fx + 1 and fy <= y <= fy + 1:
                continue  # the footprint itself
            pos = Position(x, y)
            if in_bounds(ct, pos):
                ring.append(pos)
    return ring
