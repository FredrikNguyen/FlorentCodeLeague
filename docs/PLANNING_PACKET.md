# ChatGPT planning packet

## Instructions

# Prompt for Sol High planning

You are the principal planner for a Florent Code League bot. The attached packet contains current project state, concise rules and architecture, candidate source, recent updates, and the current diff.

Create a **bounded implementation plan** for the stated planning request. Do not write implementation code.

Return at most 900 words with exactly these sections:

1. **Objective** — one sentence.
2. **Current diagnosis** — concrete evidence from the packet.
3. **Hypothesis** — what should improve and why.
4. **Scope** — exact files, symbols, and behavior allowed to change.
5. **Non-goals** — what must remain untouched.
6. **Implementation steps** — ordered and specific enough for Luna to execute without redesigning.
7. **Focused tests** — exact tests or commands for the implementation session.
8. **Evaluation checkpoint** — primary metric, guardrails, maps/seeds if needed.
9. **Rollback** — how to undo or disable the change.
10. **Done criteria** — binary checklist.

Prioritize correctness, CPU bounds, current game rules, and experiment isolation. Avoid broad refactors and avoid requiring a second planning agent.


## Current planning request

# Current planning request

Plan the next milestone: safe dispatch, versioned Store coordinate packing, and bounded cached cardinal BFS. Keep it small enough for one Luna XHigh implementation session.


## Current project handoff

# Start here

> Concise generated handoff. Read this first; do not load every long document.

## Current focus

| Field | Value |
|---|---|
| Milestone | Milestones 1-2: safe deterministic baseline, shared state, and bounded navigation |
| Hypothesis | unknown |
| Experiment | unknown |
| Next task | Generate a Sol High plan with make chatgpt-bundle, save it to docs/CURRENT_PLAN.md, then use one Luna XHigh session to implement and run focused tests. |
| Last Luna task | unknown |
| Last Luna outcome | unknown |
| Last report | unknown |
| Last local evaluation | unknown |

## Live snapshot

| Field | Value |
|---|---|
| Phase | `idle` |
| Active version | unknown |
| Pending version | unknown |
| Last known-good version | unknown |
| Last known-good score | unknown |
| Candidate score | unknown |
| Last decision | unknown |

## Working tree

- Branch: `unknown`
- Commit: `unknown`
- Status: git metadata unavailable

Run `git status --short` yourself before editing.

## Normal implementation path

- Default: one **Luna XHigh** session; no subagents.
- For an externally planned task, read `docs/CURRENT_PLAN.md`.
- Read the nearest nested `AGENTS.md` and only task-relevant source/docs.
- Run focused tests and self-review the diff in the same session.
- Full evaluation and external Sol review are release gates, not routine steps.

## Document routing

| Work | Read |
|---|---|
| Bot mechanics/strategy | `bots/candidate/AGENTS.md`, relevant `GAME_RULES.md` and roadmap sections |
| Evaluation | relevant `docs/EVALUATION_PLAN.md` sections and experiment record |
| Packaging/live | `scripts/AGENTS.md`, submission/live docs, fresh live state |
| External Sol plan | generate `artifacts/chatgpt/PLANNING_PACKET.md` with `make chatgpt-bundle` |
| External Sol release review | use `artifacts/chatgpt/RELEASE_REVIEW_PACKET.md` |

## Useful commands

```bash
make luna TASK="<bounded task>"
make luna-plan
make chatgpt-bundle
make handoff
make static
make smoke
make eval-regression
make live-status
make live-autopilot
```

Generated at `2026-08-05T14:06:34Z`.


## Stable project brief

# Florent Code League project brief

## Objective

Build a reliable Python bot that establishes titanium delivery, adapts to map geometry, protects its Core, and converts economic advantage into enemy-Core pressure.

## Match constraints

- Two teams on an 8×8 to 30×30 grid.
- Destroy the enemy Core to win; maximum 1000 rounds.
- Ladder series contain five games.
- Approximately 10 ms CPU per unit per round on the ladder.
- An uncaught exception permanently destroys the affected unit.
- Builders move cardinally and cannot move and act in the same round.
- Build, attack, heal, and destroy target orthogonally adjacent tiles.
- Prices scale with currently live entities; query costs through the API.
- Team communication is 16 delayed integer Store slots.

## Main systems

- **Core:** Builder spawning, global budget, ammunition conversion.
- **Builders:** sensing, movement, construction, healing, sabotage.
- **Economy:** ore discovery, Harvester placement, payback-aware expansion.
- **Logistics:** directed Conveyors, Splitters, Core last mile, route repair.
- **Combat:** Gunner, Sentinel, Launcher, barriers, ammunition budgeting.
- **Coordination:** per-unit state plus a small versioned Store protocol.

## Current implementation direction

1. Safe deterministic dispatch and fallback behavior.
2. Versioned shared coordinate protocol.
3. Bounded cached cardinal BFS and stale-path recovery.
4. Verified Harvester-to-Core delivery route.
5. Payback-aware expansion and route repair.
6. Defense/ammo policy, then offense and map-adaptive openings.

## Engineering priorities

1. No illegal actions or escaping exceptions.
2. Bounded tail CPU.
3. End-to-end delivered titanium, not merely placed structures.
4. Deterministic paired evaluation across maps, seeds, and sides.
5. One isolated hypothesis per candidate and instant rollback to known-good live version.

## Workflow

- Sol High in ordinary ChatGPT creates an occasional bounded plan from the generated planning packet.
- Luna XHigh in Codex implements, tests, and self-reviews in one session.
- Deterministic Python scripts run broad evaluation, package, submit, monitor, score, promote, and roll back.
- External Sol review is optional and used primarily for release candidates or difficult regressions.


## Current external plan

# Current external plan

No external plan has been approved yet.

To create one:

1. Run `make chatgpt-bundle`.
2. Upload `artifacts/chatgpt/PLANNING_PACKET.md` to standard ChatGPT using Sol High.
3. Replace this file with the returned bounded plan.
4. Run `make luna-plan`.

Keep only the current plan here. Historical hypotheses and results belong in `experiments/` and `UPDATES.md`.


## Current machine state

### `state/project_state.json`

```json
{
  "baseline_path": "bots/baseline",
  "candidate_path": "bots/candidate",
  "current_experiment": null,
  "current_hypothesis": null,
  "current_milestone": "Milestones 1-2: safe deterministic baseline, shared state, and bounded navigation",
  "last_codex_outcome": null,
  "last_codex_report": null,
  "last_codex_task": null,
  "last_local_report": null,
  "next_recommended_task": "Generate a Sol High plan with make chatgpt-bundle, save it to docs/CURRENT_PLAN.md, then use one Luna XHigh session to implement and run focused tests.",
  "schema_version": 1,
  "updated_at": "2026-08-05T14:00:00Z"
}

```

### `state/live_state.json`

```json
{
  "activated_at": null,
  "active_version": null,
  "baseline_match_ids": [],
  "candidate": null,
  "current_adjusted_score": null,
  "current_live_score": null,
  "last_decision": null,
  "last_known_good_adjusted_score": null,
  "last_known_good_live_score": null,
  "last_known_good_version": null,
  "last_observation_at": null,
  "last_report_dir": null,
  "observed_match_ids": [],
  "pending_version": null,
  "phase": "idle",
  "previous_active_version": null,
  "rank_after": null,
  "rank_before": null,
  "rating_after": null,
  "rating_before": null,
  "schema_version": 1,
  "updated_at": "2026-08-05T00:00:00Z"
}

```

## Git snapshot

- Branch: `unavailable`
- Commit: `unavailable`

```diff
unavailable
```

## Recent updates

### Usage-efficient Luna workflow — 2026-08-05T14:00:00Z

- Replaced mandatory Sol → Luna → Sol orchestration with one Luna XHigh implementation/test/self-review session.
- Removed V1/V2 subagent workarounds and routine custom planner/reviewer agents.
- Added generated one-file ChatGPT planning and release-review packets.
- Full evaluation and external Sol review are now release gates rather than per-edit requirements.
- Live polling, score calculation, promotion, and rollback remain deterministic Python operations.


### Session startup and scoped document routing added — 2026-08-05T00:25:00Z

- Added generated `docs/START_HERE.md` plus machine-readable `state/project_state.json` for cross-session development focus.
- Root `AGENTS.md` now requires a startup bootstrap but routes agents to detailed documents conditionally instead of loading everything every time.
- Added nested instructions for `bots/candidate/`, `scripts/`, and `tests/`.
- Updated Sol planner, Luna implementer, and Sol reviewer instructions to read startup state and nearest nested guidance.
- Added project-state/update scripts, automatic startup-summary refresh, Make targets, and regression tests.
- Resolved the orchestration-skill conflict: Luna implementation tasks cannot deploy, while the approved primary Sol/operator live workflow remains authorized by policy.


### Codex harness and live operator audited — 2026-08-05

- Found that the original custom-agent TOML did not prove Luna execution under the current Sol/Terra V2 versus Luna V1 mismatch.
- Added a reversible native-V1 route and an explicit process-isolated Sol → Luna Max → Sol fallback with exact command evidence.
- Added autonomous resumable upload, activation, live scoring, promotion, and rollback using `state/live_state.json`.
- Separated V1 and V2 configuration modes to avoid a boolean/table key conflict.
- Kept Sol as the only live reviewer/operator; Luna implements code but cannot modify live state or perform platform writes.


### Repository initialized — 2026-08-05

- Created the rules reference, Codex harness, starter bot, local/remote evaluation scripts, and submission workflow.
- Initial live state is unknown because no authenticated `fcode` session was available when the repository was generated.

## Latest report summary

No latest report recorded.

## Current candidate source

### `bots/candidate/bot/__init__.py`

```python
"""Candidate bot package; must remain pure Python and self-contained."""

```

### `bots/candidate/bot/comms.py`

```python
"""Versioned helpers for the 16-slot, one-round-delayed team store."""

from __future__ import annotations

from enum import IntEnum

from fcode import Position


class Slot(IntEnum):
    SCHEMA_VERSION = 0
    STRATEGY = 1
    PRIMARY_ORE = 2
    ENEMY_CORE = 3
    THREAT = 4
    LOGISTICS = 5
    DESIRED_BUILDERS = 6
    AMMO_TARGET = 7
    DEFENSE_ALERT = 8
    RALLY = 9


SCHEMA_VERSION = 1
UNKNOWN = 0


def pack_position(pos: Position, width: int) -> int:
    """Encode every in-bounds coordinate as a positive integer."""
    if width <= 0 or pos.x < 0 or pos.y < 0:
        raise ValueError("invalid position or map width")
    return 1 + pos.y * width + pos.x


def unpack_position(value: int, width: int) -> Position | None:
    """Decode a position; zero means unknown."""
    if value == UNKNOWN:
        return None
    if value < 0 or width <= 0:
        raise ValueError("invalid packed position or map width")
    index = value - 1
    return Position(index % width, index // width)

```

### `bots/candidate/bot/navigation.py`

```python
"""Small deterministic navigation helpers.

The initial candidate intentionally uses a cheap fallback. Replace it with the bounded
cached BFS described in docs/IMPLEMENTATION_PLAN.md through an evaluated experiment.
"""

from __future__ import annotations

from fcode import Controller, Direction, Position


CARDINALS = (
    Direction.NORTH,
    Direction.EAST,
    Direction.SOUTH,
    Direction.WEST,
)


def move_toward_or_fallback(
    ct: Controller,
    target: Position,
    *,
    cursor: int,
) -> tuple[bool, int]:
    """Attempt a cardinal step toward target, then deterministic alternatives."""
    preferred = ct.get_position().cardinal_direction_to(target)
    if preferred != Direction.CENTRE and ct.can_move(preferred):
        ct.move(preferred)
        return True, cursor

    for offset in range(len(CARDINALS)):
        direction = CARDINALS[(cursor + offset) % len(CARDINALS)]
        if ct.can_move(direction):
            ct.move(direction)
            return True, (cursor + offset + 1) % len(CARDINALS)

    return False, (cursor + 1) % len(CARDINALS)

```

### `bots/candidate/bot/player.py`

```python
"""Safe starter candidate.

This is deliberately a capability baseline, not a competitive final strategy.
"""

from __future__ import annotations

from fcode import Controller, Direction, EntityType, Environment

from .comms import SCHEMA_VERSION, Slot, pack_position, unpack_position
from .navigation import CARDINALS, move_toward_or_fallback


class Player:
    def __init__(self) -> None:
        self._cursor = 0
        self._error_count = 0

    def run(self, ct: Controller) -> None:
        try:
            self._run(ct)
        except Exception:
            # Preserve the unit. During development, inspect replay/console and tests.
            self._error_count += 1
            if self._error_count <= 3:
                try:
                    pos = ct.get_position()
                    ct.draw_indicator_dot(pos, 255, 0, 0)
                except Exception:
                    pass

    def _run(self, ct: Controller) -> None:
        entity_type = ct.get_entity_type()
        if entity_type == EntityType.CORE:
            self._run_core(ct)
        elif entity_type == EntityType.BUILDER_BOT:
            self._run_builder(ct)
        elif entity_type in (EntityType.GUNNER, EntityType.SENTINEL):
            self._run_firing_turret(ct)
        elif entity_type == EntityType.LAUNCHER:
            self._run_launcher(ct)

    def _run_core(self, ct: Controller) -> None:
        ct.write_store(int(Slot.SCHEMA_VERSION), SCHEMA_VERSION)

        desired_builders = 4
        ct.write_store(int(Slot.DESIRED_BUILDERS), desired_builders)
        # get_unit_count() includes the Core, so add one.
        if ct.get_unit_count() < desired_builders + 1:
            for pos in ct.get_nearby_tiles(dist_sq=2):
                if ct.can_spawn(pos):
                    ct.spawn_builder(pos)
                    return

    def _run_builder(self, ct: Controller) -> None:
        pos = ct.get_position()
        width = ct.get_map_width()

        # Build a visible adjacent first Harvester when legal.
        for direction in CARDINALS:
            target = pos.add(direction)
            if not self._in_bounds(ct, target):
                continue
            if ct.get_tile_env(target) == Environment.ORE_TITANIUM:
                if ct.can_build_harvester(target):
                    ct.build_harvester(target)
                    return

        # Publish one visible ore target. Multiple writers are tolerated only in this starter;
        # Milestone 2 must designate a single scout writer and add an epoch.
        for tile in ct.get_nearby_tiles():
            if ct.get_tile_env(tile) == Environment.ORE_TITANIUM:
                ct.write_store(int(Slot.PRIMARY_ORE), pack_position(tile, width))
                target = tile
                break
        else:
            target = unpack_position(ct.read_store(int(Slot.PRIMARY_ORE)), width)

        if target is not None:
            moved, self._cursor = move_toward_or_fallback(
                ct, target, cursor=self._cursor
            )
            if moved:
                return

        for offset in range(len(CARDINALS)):
            direction = CARDINALS[(self._cursor + offset) % len(CARDINALS)]
            if ct.can_move(direction):
                ct.move(direction)
                self._cursor = (self._cursor + offset + 1) % len(CARDINALS)
                return
        self._cursor = (self._cursor + 1) % len(CARDINALS)

    def _run_firing_turret(self, ct: Controller) -> None:
        for target in ct.get_attackable_tiles():
            if ct.can_fire(target):
                ct.fire(target)
                return

    def _run_launcher(self, ct: Controller) -> None:
        # Launcher policy is intentionally deferred until destination scoring exists.
        return

    @staticmethod
    def _in_bounds(ct: Controller, pos) -> bool:
        return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()

```

### `bots/candidate/main.py`

```python
"""Florent Code League submission entry point."""

from bot.player import Player

__all__ = ["Player"]

```

## Additional detailed sources available in the repository

- `GAME_RULES.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/EVALUATION_PLAN.md`
- `docs/SUBMISSION_AND_VERSIONING.md`
- `docs/LIVE_AUTOPILOT.md`

Generated at 2026-08-05T14:06:34Z.
