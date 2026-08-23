# v142 chain-only non-progress detour — rejected

## Objective

Use the Ragnarok replay diagnosis to test whether a chain Builder needs a
bounded local detour when the visible safe frontier is temporarily farther
from Core than its current tile. Preserve v0038 as the moving baseline unless
the paired win-rate and delivery evidence improves at release scale.

## Allowed files

- `bots/candidate/bot/navigation.py`
- `bots/candidate/bot/defender.py`
- `bots/candidate/bot/constants.py`
- focused route/navigation tests
- this experiment record, report artifacts, `UPDATES.md`, and durable state

## Non-goals

No workforce, economy, task priority, route merge, pending-chain recovery,
combat, danger-map, Store, map-config, baseline, package, upload, activation,
or live-state change.

## Hypothesis and implementation

The normal navigator requires strict target-distance progress. v142 added an
opt-in `allow_nonprogress` mode and let `_run_chain` spend at most four stalled
rounds on a safe local detour, retaining the pending conveyor. Repair 1 kept
that operator only while `SLOT_HARVESTER_COUNT == 0`, so established routes kept
v0038 behavior. Turret-fire danger remained excluded in both variants.

## Evidence

- Initial focused tests: **26/26**; compileall passed; smoke **4/4**;
  `make static` remained inherited exit 2 (15 obsolete imports plus two
  navigation fast-path assertions).
- Initial 54-game screen: **30-24**, candidate/comparator **187,240/165,450
  Ti**, no-delivery **1/3**, zero command/TLE/suspicious-output failures,
  max p99/peak **1,441/4,841 us**. Report:
  `reports/local-20260817T150550Z`.
- Initial 210-game gate: **99-111**, **913,170/922,400 Ti**, no-delivery
  **8/2**, zero command failures/TLEs/suspicious output, max p99/peak
  **1,500/5,426 us**. Report:
  `reports/local-20260817T151133Z` and analysis
  `reports/iter-v142-chain-detour/full210-analysis.log`.
- Repair 1 focused tests: **26/26**; compileall passed; smoke **4/4**;
  static retained the same inherited exit 2. Its 54-game screen regressed to
  **24-30**, **181,190/206,990 Ti**, no-delivery **1/1**, zero command/TLE/
  suspicious-output failures, max p99/peak **1,449/5,654 us**. Report:
  `reports/local-20260817T153443Z` and analysis
  `reports/iter-v142-chain-detour/repair1-analysis.log`.

## Decision and rollback

Reject after the release-gate regression and one bounded repair. Candidate
production Python is byte-identical to immutable v0038; rollback focused tests
were **25/25**, compileall passed, smoke **4/4**, and static retained the
inherited red result. Rollback logs are under
`reports/iter-v142-chain-detour/rollback-*` and smoke report
`reports/local-20260817T154031Z`. No package, upload, activation, or baseline
transition occurred.

## Remaining risk

Ragnarok's low-connected-route losses remain map-local, but allowing temporary
non-progress movement globally harms delivery and map floors. Future work must
use replay-derived route ownership or sink-conversion evidence without
weakening the v0038 opening and established-route behavior.
