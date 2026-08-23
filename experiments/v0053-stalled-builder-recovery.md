# v0053 — stalled-builder recovery watchdog

## Objective

Convert persistent stationary ready-builder turns into a bounded replan. The
current role logic has an idle fallback, but a role can retain an unreachable
task/target and repeatedly re-enter that same dead end. A watchdog should reset
only after several consecutive turns where the builder was ready, performed no
action, and did not move.

## Allowed files

- `bots/candidate/main.py`
- `bots/candidate/bot/constants.py`
- `tests/test_candidate_nearest_defense.py`
- this experiment record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no economy thresholds, combat priorities, unit caps, or pathfinding changes;
- no map names, map-specific branches, or live/platform operations;
- never interrupt a builder while it owes a conveyor in `MODE_CHAIN`;
- rejected candidates must leave the moving best snapshot untouched.

## Implementation

Track a per-builder stalled-ready counter around the existing role dispatch and
idle fallback. After `BUILDER_STALL_LIMIT` consecutive no-action/no-move ready
turns, clear only the role's stale target/task, reset navigation memory, and let
the normal next-turn policy choose a new legal intent. Combat intel remains
known; route construction remains protected.

## Gate

Focused watchdog/unit tests, `make static`, `make smoke`, then the six-map weak
screen (three seeds and side swaps) against the current moving best v0030.
Promote only if the screen beats v0030 without command failures, TLEs,
suspicious output, or a protected-map/delivery regression. Otherwise revert the
candidate and retain v0030.
