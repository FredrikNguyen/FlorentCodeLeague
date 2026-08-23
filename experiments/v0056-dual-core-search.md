# v0056 — dual-attacker core search

## Objective

Prevent both fixed attackers from committing to the same wrong 180-degree
enemy-Core guess. Several fixed maps place the opponent across a horizontal,
vertical, or offset symmetry. The first attacker remains on the existing direct
lane; only the designated second attacker searches alternate geometric
counterparts until a real Core sighting is shared.

## Allowed files

- `bots/candidate/main.py`
- `bots/candidate/bot/attacker.py`
- `bots/candidate/bot/constants.py`
- `tests/test_candidate_core_search.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no map names or hard-coded map catalog;
- no sentinel placement from an unconfirmed target;
- no economy, route, ammo, workforce, or turret threshold changes;
- the first fixed attacker and all dynamic builders retain their current target
  logic;
- no platform operation before a local win-rate promotion gate.

## Implementation

Give the second attacker a deterministic sequence of vertical, horizontal,
and rotational counterparts, advancing only after a bounded search epoch while
the Core remains unconfirmed. Once either attacker sees the Core, the shared
confirmed position immediately overrides the search. The candidate remains
cardinal/BFS-routed and uses existing sentinel safety checks.

## Promotion gate

Run focused tests, `make static`, and `make smoke`, then the six-map weak screen
against the moving v0030. Only a strict, reliability-clean screen edge earns
the full 21-map/5-seed/side-swapped gate. A passing full gate is archived as a
new immutable snapshot and the moving baseline pointer is updated before the
next promotion attempt.
