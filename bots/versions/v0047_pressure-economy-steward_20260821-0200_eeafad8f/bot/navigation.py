"""Movement primitives shared by both builder roles: reading enemy turret fire
lines, and BFS-based step-by-step pathing around walls/hazards. Everything
else (economy, combat) is built on top of `_navigate`.
"""

from collections import deque

from fcode import Controller, Direction, EntityType, Position

from .constants import CARDINALS, VISITED_MAX


class NavigationMixin:
    def _danger_tiles(self, ct: Controller) -> set[Position]:
        """Tiles currently in a visible enemy gunner's or sentinel's line of fire.

        Builder bots have no combat capability beyond adjacent fire, so the main
        defense against turret fire is not walking into it. get_attackable_tiles_from()
        gives the turret's raw firing pattern (ignores ammo/cooldown — conservative,
        since even a temporarily out-of-ammo turret may be topped up before we cross).
        """
        team = ct.get_team()
        danger: set[Position] = set()
        for bid in ct.get_nearby_buildings():
            etype = ct.get_entity_type(bid)
            if etype not in (EntityType.GUNNER, EntityType.SENTINEL):
                continue
            if ct.get_team(bid) == team:
                continue
            danger.update(ct.get_attackable_tiles_from(ct.get_position(bid), ct.get_direction(bid), etype))
        return danger

    def _navigate(
        self,
        ct: Controller,
        target: Position | None,
        avoid: set[Position] = frozenset(),
        flee: bool = False,
    ) -> Direction | None:
        """Take one step toward `target`, routing around walls with a BFS over the
        tiles we can currently see. We pick the reachable visible tile closest to
        the target (breaking ties toward less-visited tiles so we don't loop) and
        step along the shortest path to it. Because we replan every round as new
        tiles come into view, these local paths chain into global navigation.

        `avoid` (typically enemy turret fire lines from _danger_tiles) is treated
        as impassable for any tile other than our own — we never route a builder
        through a kill zone it isn't already standing in. If `flee` is set,
        `target` is ignored and we instead step toward the nearest reachable tile
        outside `avoid` — every such tile is safe by construction, since `avoid`
        tiles are excluded from the passable set below.

        Returns the direction actually moved, or None if we couldn't move.
        """
        if ct.get_move_cooldown() != 0:
            return None
        pos = ct.get_position()

        # Passable tiles we can see right now (plus our own tile, even if unsafe —
        # that's where we are; only *other* tiles are excluded for being unsafe).
        passable = {pos}
        for t in ct.get_nearby_tiles():
            if t in avoid:
                continue
            if ct.is_tile_passable(t):
                passable.add(t)

        # BFS outward from our position over those passable tiles.
        prev: dict[Position, Position | None] = {pos: None}
        queue = deque([pos])
        while queue:
            cur = queue.popleft()
            for d in CARDINALS:
                n = cur.add(d)
                if n in passable and n not in prev:
                    prev[n] = cur
                    queue.append(n)

        # Sub-goal: while fleeing, the nearest reachable tile (all safe by
        # construction); otherwise the reachable tile minimising (distance to
        # target, visits).
        best = pos
        if flee:
            best_dist = None
            for tile in prev:
                if tile == pos:
                    continue
                d = pos.distance_squared(tile)
                if best_dist is None or d < best_dist:
                    best_dist = d
                    best = tile
        else:
            best_key = (pos.distance_squared(target), self.visited.get(pos, 0))
            for tile in prev:
                if tile == pos:
                    continue
                key = (tile.distance_squared(target), self.visited.get(tile, 0))
                if key < best_key:
                    best_key = key
                    best = tile
        if best == pos:
            return None  # boxed in / can't improve — caller handles giving up

        # Walk back to the first step off our current tile.
        node = best
        while prev[node] != pos:
            node = prev[node]
        d = pos.cardinal_direction_to(node)
        if d == Direction.CENTRE or not ct.can_move(d):
            return None
        ct.move(d)
        new_pos = pos.add(d)
        self.visited[new_pos] = self.visited.get(new_pos, 0) + 1
        if len(self.visited) > VISITED_MAX:
            self.visited.clear()
        return d
