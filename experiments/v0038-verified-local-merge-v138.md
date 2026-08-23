# v138 verified local conveyor merge

## Objective

Improve Ragnarok-style route conversion without changing the workforce phase or
opening seed. A chain segment may join an existing friendly Conveyor only when a
fully visible, bounded directed Conveyor walk reaches our Core; Splitters,
unseen tails, gaps, and cycles remain rejected.

## Allowed files

- `bots/candidate/bot/defender.py`
- `tests/test_candidate_seeded_route.py`
- this experiment record, reports, `UPDATES.md`, and durable state

## Non-goals

- No global workforce, role, task-priority, combat, ammo, navigation, Store,
  map-specific, baseline, package, upload, or activation changes.

## Results

- Initial verified-merge variant: focused 22/22, compileall passed, smoke 4/4,
  static inherited exit 2; 54-game screen **23-31**, candidate/comparator Ti
  **161,860/158,180**, zero command/TLE/suspicious-output failures. Icefloe
  was 0-6 and Drakkarfjord 2-4. Report: `reports/local-20260817T135748Z`.
- Repair 1 gated joins until one completed route: focused 22/22, compileall
  passed, smoke 4/4, static inherited exit 2; 54-game screen **27-27**,
  candidate/comparator Ti **185,510/178,720**, candidate no-delivery 2 versus
  comparator 0. Report: `reports/local-20260817T140404Z`.
- Both runs were command-clean with zero TLE/suspicious output. The neutral
  repair result and new no-delivery rows fail the promotion gate.

## Decision

Reject after the initial screen and one bounded repair. Restore all production
candidate files and focused tests byte-for-byte to v0038. Rollback focused
tests were 20/20, compileall passed, smoke 4/4, and static retained the
inherited failures. No 210-game gate, package, upload, activation, or live
baseline change was performed.

## Next hypothesis

Inspect v0038's map-adaptive exploration and local builder handoffs. Test one
bounded change that reduces same-ore/frontier pileups without changing the
three-route economy gate or direct opening chains.
