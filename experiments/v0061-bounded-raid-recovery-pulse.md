# v0061 — bounded raid-recovery pulse

## Objective

Make a dynamic Builder hand off from a completed or invalidated logistics raid
to one visible owned belt/core-ring repair (or damaged home building) before it
re-enters the normal task picker. This gives raiders a recover/build phase
without touching fixed attackers, route owners in CHAIN mode, opening economy,
or target scoring.

## Allowed files

- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to Core search, spawning, sentinel/gunner placement, ammo, raid
  target ranking, or navigation;
- no new Store slots, timers, map catalog, or unbounded scans;
- no edits to `bots/baseline/` or immutable snapshots;
- no platform upload, activation, or live-state transition.

## Promotion gate

Run focused tests, compileall, `make static`, and `make smoke`, then the
six-map screen against v0030. Run the 210-game matrix only for a strict,
reliability-clean screen edge. Promote only if the full matrix improves
win-rate without delivery, protected-map, or reliability regressions; otherwise
revert and retain v0030.
