# v0063 — resource-backed economy floor

## Objective

Retain the v0031 dynamic raid/recovery behavior while making the economy floor
state-aware. When the team has fewer than four completed routes *and* cannot
afford a fresh harvester plus a short conveyor seed and the fixed attack
reserve, dynamic Builders choose harvest/exploration before opportunistic
hijack, base repair, raid, denial, or advance. When the bank is already rich,
the worker remains free to convert surplus into defense and sabotage. This
addresses v0062's unconditional-floor regression on Atoll, Runestone, Showdown,
and Vault.

## Allowed files

- `bots/candidate/bot/constants.py`
- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to fixed attacker lanes, Core spawning, ammo, sentinels,
  navigation, map branches, or v0061 raid recovery;
- no unconditional four-route lock and no new store slot;
- no edits to `bots/baseline/` or immutable snapshots;
- no platform upload or activation before the local promotion gate passes.

## Promotion gate

Run the focused tests, compileall, `make static`, and `make smoke`, then the
six-map weak screen against immutable v0031. Run the 210-game matrix only for
a strict clean screen edge. Promote only if paired win rate improves without
delivery, collection, protected-map, or reliability regressions; otherwise
revert and retain v0031.
