# v0064 — locality-ranked raid recovery

## Objective

Keep v0061's one-shot post-raid handoff, but rank the visible damaged-home
building and visible belt-gap repair by travel distance from the raider. This
preserves immediate route repair when it is local, while choosing production
healing when that is the nearer useful recovery. The change is a recovery-state
contract, not a generic preemption or economy-floor change.

## Allowed files

- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to fixed attacker lanes, Core search/spawn, spending, navigation,
  sentinel/ammo policy, or map branches;
- no changes to v0061's target scoring or CHAIN mode;
- no edits to `bots/baseline/` or immutable snapshots;
- no platform upload or activation before the local promotion gate passes.

## Promotion gate

Run focused tests, compileall, `make static`, and `make smoke`, then the
six-map weak screen against immutable v0031. Run the 210-game matrix only for
a strict clean screen edge. Promote only if paired win rate improves without
delivery, collection, protected-map, or reliability regressions; otherwise
revert and retain v0031.
