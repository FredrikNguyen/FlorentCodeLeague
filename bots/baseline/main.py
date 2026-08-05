"""Frozen minimal baseline.

Replace this only through an explicit promotion after a candidate passes evaluation.
"""

from fcode import Controller, Direction, EntityType


_CARDINALS = (
    Direction.NORTH,
    Direction.EAST,
    Direction.SOUTH,
    Direction.WEST,
)


class Player:
    def __init__(self) -> None:
        self._cursor = 0

    def run(self, ct: Controller) -> None:
        try:
            entity_type = ct.get_entity_type()
            if entity_type == EntityType.CORE:
                self._core(ct)
            elif entity_type == EntityType.BUILDER_BOT:
                self._builder(ct)
            elif entity_type in (EntityType.GUNNER, EntityType.SENTINEL):
                self._turret(ct)
        except Exception:
            # An escaping exception permanently destroys the unit.
            return

    def _core(self, ct: Controller) -> None:
        if ct.get_unit_count() >= 3:
            return
        for pos in ct.get_nearby_tiles(dist_sq=2):
            if ct.can_spawn(pos):
                ct.spawn_builder(pos)
                return

    def _builder(self, ct: Controller) -> None:
        for offset in range(len(_CARDINALS)):
            direction = _CARDINALS[(self._cursor + offset) % len(_CARDINALS)]
            if ct.can_move(direction):
                ct.move(direction)
                self._cursor = (self._cursor + offset + 1) % len(_CARDINALS)
                return
        self._cursor = (self._cursor + 1) % len(_CARDINALS)

    def _turret(self, ct: Controller) -> None:
        for target in ct.get_attackable_tiles():
            if ct.can_fire(target):
                ct.fire(target)
                return
