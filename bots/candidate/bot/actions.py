from __future__ import annotations

from fcode import Direction, EntityType, Position

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


def cpu_is_safe(ct: object, limit_us: int = 7000) -> bool:
    try: return int(ct.get_cpu_time_elapsed()) < limit_us
    except (AttributeError, TypeError, ValueError): return True


class TurnActions:
    __slots__ = ("ct", "moved", "acted", "ammo_converted")

    def __init__(self, ct: object) -> None:
        self.ct, self.moved, self.acted, self.ammo_converted = ct, False, False, False

    def _ready_action(self) -> bool:
        if self.moved or self.acted: return False
        try: return bool(self.ct.can_act())
        except AttributeError: return True
        except Exception: return False

    def move(self, direction: Direction) -> bool:
        if self.moved or self.acted or direction not in CARDINALS: return False
        try:
            if not self.ct.can_move(direction): return False
            self.ct.move(direction)
        except Exception: return False
        self.moved = True; return True

    def _build(self, method: str, can_method: str, *args: object) -> int | None:
        if not self._ready_action(): return None
        try:
            if not getattr(self.ct, can_method)(*args): return None
            result = getattr(self.ct, method)(*args)
        except Exception: return None
        self.acted = True; return result if isinstance(result, int) else 1

    def build_conveyor(self, position: Position, direction: Direction) -> int | None: return self._build("build_conveyor", "can_build_conveyor", position, direction)
    def build_splitter(self, position: Position, direction: Direction) -> int | None: return self._build("build_splitter", "can_build_splitter", position, direction)
    def build_harvester(self, position: Position) -> int | None: return self._build("build_harvester", "can_build_harvester", position)
    def build_barrier(self, position: Position) -> int | None: return self._build("build_barrier", "can_build_barrier", position)
    def build_gunner(self, position: Position, direction: Direction) -> int | None: return self._build("build_gunner", "can_build_gunner", position, direction)
    def build_sentinel(self, position: Position, direction: Direction) -> int | None: return self._build("build_sentinel", "can_build_sentinel", position, direction)
    def build_launcher(self, position: Position) -> int | None: return self._build("build_launcher", "can_build_launcher", position)

    def build(self, entity_type: EntityType, position: Position, extra: Direction | Position | None = None) -> int | None:
        return self._build("build", "can_build", entity_type, position, extra)

    def fire(self, target: Position) -> bool:
        if not self._ready_action(): return False
        try:
            if not self.ct.can_fire(target): return False
            self.ct.fire(target)
        except Exception: return False
        self.acted = True; return True

    def heal(self, target: Position) -> bool:
        if not self._ready_action(): return False
        try:
            if not self.ct.can_heal(target): return False
            self.ct.heal(target)
        except Exception: return False
        self.acted = True; return True

    def destroy(self, target: Position) -> bool:
        # Friendly destruction is a separate engine operation: it is gated by
        # the controller's own can_destroy() contract, but it does not consume
        # this wrapper's ordinary action slot.  The engine therefore remains
        # the authority on whether a later build, move, or destroy is legal.
        try:
            if not self.ct.can_destroy(target): return False
            self.ct.destroy(target)
        except Exception: return False
        return True

    def rotate(self, direction: Direction) -> bool:
        if not self._ready_action(): return False
        try:
            if not self.ct.can_rotate(direction): return False
            self.ct.rotate(direction)
        except Exception: return False
        self.acted = True; return True

    def launch(self, bot_position: Position, target: Position) -> bool:
        if not self._ready_action(): return False
        try:
            if not self.ct.can_launch(bot_position, target): return False
            self.ct.launch(bot_position, target)
        except Exception: return False
        self.acted = True; return True

    def spawn(self, position: Position) -> int | None: return self._build("spawn_builder", "can_spawn", position)

    def convert_ammo(self, amount: int) -> bool:
        if self.ammo_converted or isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0: return False
        try:
            if not self.ct.can_convert_ammo(amount): return False
            self.ct.convert_ammo(amount)
        except Exception: return False
        self.ammo_converted = True; return True
