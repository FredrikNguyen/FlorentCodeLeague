# v0057 — direct-probe before alternate Core search

## Objective

Retain the v0030 direct 180-degree attacker lane on maps where it is correct,
while still recovering maps where that guess is wrong. The designated second
attacker first probes the direct target; only after it reaches that probe (or a
bounded timeout) without a confirmed Core does it rotate through alternate
counterparts. The first attacker, economy workers, sentinel safety, and shared
confirmed intel remain unchanged.

## Allowed files

- `bots/candidate/main.py`
- `bots/candidate/bot/attacker.py`
- `bots/candidate/bot/constants.py`
- `tests/test_candidate_core_search.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no map names or hard-coded map catalog;
- no guessed sentinel placement;
- no economy, route, ammo, workforce, or turret threshold changes;
- no changes to the first attacker or dynamic builder target logic;
- no platform operation before a local win-rate promotion gate.

## Promotion gate

Run focused tests, compileall, `make static`, and `make smoke`, then the same
six-map screen against moving v0030. Run the full 21-map/5-seed/side-swapped
matrix only for a strict, reliability-clean screen edge. Promote only if the
full result improves win rate without protected-map, delivery, or collection
regressions; otherwise revert all candidate edits and keep v0030.
