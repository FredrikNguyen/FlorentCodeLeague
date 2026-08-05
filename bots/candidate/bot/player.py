
from __future__ import annotations

from fcode import Controller, EntityType

from .builder import BuilderStateData, run_builder
from .core import CoreState, run_core
from .turrets import run_gunner, run_launcher, run_sentinel


class Player:
    def __init__(self) -> None:
        self._error_count = 0
        self._safe_mode = False
        self._core_state = CoreState()
        self._builder_state = BuilderStateData()

    def run(self, ct: Controller) -> None:
        if self._safe_mode:
            return
        try:
            self._run(ct)
        except Exception:
            self._error_count += 1
            if self._error_count <= 3:
                try:
                    ct.draw_indicator_dot(ct.get_position(), 255, 0, 0)
                except Exception:
                    pass
            if self._error_count >= 3:
                self._safe_mode = True

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
        elif entity_type in (
            EntityType.CONVEYOR,
            EntityType.SPLITTER,
            EntityType.HARVESTER,
            EntityType.BARRIER,
        ):
            return

