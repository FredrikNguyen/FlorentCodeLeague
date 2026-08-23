# v0060 — urgent route-health preemption

## Objective

Make a newly visible home threat or broken conveyor output interrupt a stale
dynamic task immediately. The existing commitment floor is retained for
ordinary target changes, but it must not keep a Builder on an advance, denial,
raid, or other low-value intent while a route is visibly losing income.

## Allowed files

- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this experiment record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to raid target scoring, Core search, spawning, route FSM internals,
  ammo conversion, turret/sentinel placement, or map-specific behavior;
- no new Store slots, random choices, or unbounded scans;
- no edits to `bots/baseline/` or immutable snapshots;
- no platform upload, activation, or live-state transition.

## Promotion gate

Run focused tests, compileall, `make static`, and `make smoke`, then the
six-map screen against v0030. Run the 210-game matrix only for a strict,
reliability-clean screen edge. Promote only if the full matrix improves
win-rate without delivery, protected-map, or reliability regressions; otherwise
revert the candidate and retain v0030.
