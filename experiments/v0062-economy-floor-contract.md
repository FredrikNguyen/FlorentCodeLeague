# v0062 — staged economy-floor contract

## Objective

Keep the scalable workforce converting titanium into routes until at least four
completed harvester chains exist. While that floor is active, a dynamic Builder
still repairs a visible critical belt gap first, but otherwise keeps the
harvest/exploration task ahead of opportunistic enemy-harvester hijacks,
base-repair detours, raids, ore denial, and advance. The contract addresses the
low-production loss pattern without changing fixed attackers, Core spawning,
ammo, sentinel placement, or the v0061 post-raid recovery pulse.

## Allowed files

- `bots/candidate/bot/constants.py`
- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to fixed attacker lanes, Core search, sentinel placement, ammo,
  navigation, map branches, or live platform state;
- no removal of the v0061 bounded raid-recovery handoff;
- no edits to `bots/baseline/` or immutable version snapshots;
- no package, upload, or activation unless the local promotion gate passes.

## Promotion gate

Run the focused tests, compileall, `make static`, and `make smoke`, then the
six-map weak screen against immutable v0031. Run the 210-game matrix only for
a strict screen edge. Promote only if paired win rate improves with clean
runtime, delivery, collection, and protected-map floors; otherwise revert all
candidate edits and retain v0031.
