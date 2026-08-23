# v139 map-adaptive frontier exploration

## Objective

Reduce idle exploration by preferring visible passable tiles adjacent to unseen
cardinal neighbors, while retaining a bounded deterministic fallback for maps
whose visible area has no frontier.

## Allowed files

- `bots/candidate/bot/defender.py`
- `tests/test_candidate_seeded_route.py`
- this experiment record, reports, `UPDATES.md`, and durable state

## Non-goals

- No workforce, role/task priority, economy gate, route FSM, combat, ammo,
  navigation, Store, map branch, baseline, package, upload, or activation
  changes.

## Results

- Initial frontier preference: focused 21/21, compileall passed, smoke 4/4,
  static inherited exit 2; 54-game screen **25-29**, candidate/comparator Ti
  **209,390/195,880**, candidate no-delivery **2** versus comparator **0**.
  Nordkap was 5-1, while Antler and Glacierkeep were each 1-5. Report:
  `reports/local-20260817T141419Z`.
- Repair 1 retained the v0038 arbitrary opening picker until one completed
  route, then enabled frontier preference: focused 21/21, compileall passed,
  smoke 4/4, static inherited exit 2; 54-game screen **21-33**, candidate/
  comparator Ti **151,350/197,980**, candidate no-delivery **2** versus 0.
  Archipelago was 0-6 and Nordkap 1-5. Report:
  `reports/local-20260817T142004Z`.
- Both runs were command-clean with zero TLE/suspicious-output failures, but
  neither met the paired win-rate or delivery gate.

## Decision

Reject after the initial screen and one bounded repair. Restore all production
candidate files and focused tests byte-for-byte to v0038. Rollback focused
tests were 21/21, compileall passed, smoke 4/4, and static retained inherited
failures. No 210-game gate, package, upload, activation, or live baseline
change was performed.

## Next hypothesis

Inspect route-owner and ore-claim handoffs in the v0038 opening. Test one local
claim change that prevents a Builder already committed to a non-economic task
from suppressing an eligible Harvester, without changing role gates.
