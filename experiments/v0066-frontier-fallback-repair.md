# v0066 — frontier prospecting with visible fallback

## Objective

Repair v0065's over-strict prospecting edge case. Prefer an unseen frontier
when one exists, but retain the previous deterministic exploration candidates
when the Builder already sees the whole harvestable area. This keeps the early
delivery benefit on sparse/elongated maps without turning a fully visible
small/edge map into a no-target idle loop.

## Allowed files

- `bots/candidate/bot/defender.py`
- `tests/test_candidate_exploration.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to role assignment, spending, route construction, navigation,
  combat, raids, Store layout, map-specific constants, or platform state;
- no edits to `bots/baseline/` or immutable snapshots;
- no upload, activation, or baseline transition before the local gate.

## Promotion gate

Run focused tests, compileall, `make static`, and `make smoke`, then the
54-game regression screen against immutable v0031. Run the 210-game matrix
only for a strict clean screen edge. Promote only if paired win rate improves
without delivery, collection, protected-map, or reliability regressions;
otherwise revert and retain v0031.
