# v0058 — aspect-aware alternate Core search

## Objective

Give the second attacker a deterministic alternate-Core search order derived
from map aspect ratio. On a wide map it tests the horizontal counterpart first;
on a tall map it tests the vertical counterpart first; square maps retain the
existing order. The first attacker still uses the direct 180-degree target,
and confirmed Core intel still overrides all guesses.

## Allowed files

- `bots/candidate/main.py`
- `bots/candidate/bot/attacker.py`
- `bots/candidate/bot/constants.py`
- `tests/test_candidate_core_search.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no map names, hashes, or hard-coded map catalog;
- no delayed or speculative sentinel placement;
- no economy, route, ammo, workforce, or turret threshold changes;
- no first-attacker or dynamic-builder target changes;
- no platform operation before local promotion gates.

## Promotion gate

Run focused tests, compileall, `make static`, and `make smoke`, then the same
36-game screen against v0030. Run the 210-game gate only for a strict,
reliability-clean screen edge. Promote only without protected-map, delivery, or
collection regressions; otherwise revert all candidate edits and retain v0030.
