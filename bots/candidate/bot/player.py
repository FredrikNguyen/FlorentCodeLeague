from __future__ import annotations

from fcode import Controller, Direction, EntityType

from .builder import BuilderStateData, run_builder
from .core import CoreState, run_core
from .turrets import run_gunner, run_launcher, run_sentinel

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


class Player:
    def __init__(self) -> None:
        self._error_count = 0
        self._core_state = CoreState()
        self._builder_state = BuilderStateData()

    def run(self, ct: Controller) -> None:
        try:
            self._run(ct)
        except Exception:
            # Catching the exception prevents the engine from permanently
            # destroying this unit. Do not enter a permanent safe-mode idle state:
            # a visibility/API edge case on three turns should not disable a Core,
            # route owner or turret for the remaining match.
            self._error_count += 1
            self._fallback(ct)

    def _run(self, ct: Controller) -> None:
        entity_type = ct.get_entity_type()
        if entity_type == EntityType.CORE:
            self._core_state = run_core(ct, self._core_state)
        elif entity_type == EntityType.BUILDER_BOT:
            self._builder_state = run_builder(ct, self._builder_state)
        elif entity_type == EntityType.GUNNER:
            run_gunner(ct)
        elif entity_type == EntityType.SENTINEL:
            run_sentinel(ct)
        elif entity_type == EntityType.LAUNCHER:
            run_launcher(ct)

    def _fallback(self, ct: Controller) -> None:
        """Tiny legal fallback used only after an unexpected caught exception."""
        try:
            entity_type = ct.get_entity_type()
            round_no = int(ct.get_current_round())
            entity_id = int(ct.get_id())
        except Exception:
            return
        try:
            ct.draw_indicator_dot(ct.get_position(), 255, 0, 0)
        except Exception:
            pass

        if entity_type == EntityType.CORE:
            try:
                for position in tuple(ct.get_nearby_tiles(dist_sq=2)):
                    if ct.can_spawn(position):
                        ct.spawn_builder(position)
                        break
            except Exception:
                pass
            return

        if entity_type == EntityType.BUILDER_BOT:
            try:
                current = ct.get_position()
                for direction in CARDINALS:
                    target = current.add(direction)
                    if ct.can_heal(target):
                        ct.heal(target)
                        return
            except Exception:
                pass
            for offset in range(4):
                direction = CARDINALS[(entity_id + round_no + offset) % 4]
                try:
                    if ct.can_move(direction):
                        ct.move(direction)
                        return
                except Exception:
                    continue
            return

        if entity_type in (EntityType.GUNNER, EntityType.SENTINEL):
            try:
                for target in tuple(ct.get_attackable_tiles())[:64]:
                    if ct.can_fire(target):
                        ct.fire(target)
                        return
            except Exception:
                pass
