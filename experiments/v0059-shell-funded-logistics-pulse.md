# v0059 — shell-funded logistics pulse

## Objective

After the opening economy has completed five routes and the full forward
sentinel pool has been observed, let fixed attackers spend ready turns on one
visible loaded conveyor/splitter/harvester before returning to the direct Core
lane. This is a structural role handoff: economy funds the combat shell, the
shell funds a bounded sabotage pulse, and no early attacker detour is allowed.

## Allowed files

- `bots/candidate/bot/attacker.py`
- `tests/test_candidate_nearest_defense.py`
- this experiment record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no change to opening Builder spawning, route construction, Core search, turret
  placement, ammo conversion, or sentinel thresholds;
- no map catalog, random policy, or unbounded target search;
- no changes to `bots/baseline/` or immutable version snapshots;
- no platform upload, activation, or live-state transition.

## Promotion gate

Run the focused attacker/dynamic tests, compileall, `make static`, and
`make smoke`, then the six-map screen against v0030. Run the 210-game matrix
only for a strict reliability-clean screen edge. Promote only if the full
matrix improves win rate without protected-map, delivery, or reliability
regressions; otherwise revert the candidate and retain v0030.
