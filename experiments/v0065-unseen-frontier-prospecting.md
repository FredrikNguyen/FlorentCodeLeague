# v0065 — unseen-frontier prospecting

## Objective

Change only the defender's no-ore prospecting target selection. The current
explorer can select a map tile that is already in the Builder's vision; that
spends movement rounds without revealing new terrain and contributes to the
late first-delivery profile on Sweden, Showdown, and other elongated maps.
Prospecting should select a deterministic, not-currently-visible frontier tile
so each economic Builder moves to reveal new terrain before falling back to the
normal visible/advertised ore selectors.

## Allowed files

- `bots/candidate/bot/defender.py`
- `tests/test_candidate_exploration.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to spending, role assignment, route construction, navigation,
  combat, raids, map-specific branches, or Store layout;
- no edits to `bots/baseline/` or immutable snapshots;
- no platform upload, activation, or baseline transition before the local gate.

## Promotion gate

Run focused tests, compileall, `make static`, and `make smoke`, then the
six-map weak screen against immutable v0031. Run the 210-game matrix only for
a strict clean screen edge. Promote only if paired win rate improves without
delivery, collection, protected-map, or reliability regressions; otherwise
revert and retain v0031.
