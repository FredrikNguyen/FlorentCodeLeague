# v262 visit-aware nearby frontier discovery — rejected after one repair

## Objective and scope

The v0043 SCOUT fallback used a bounded pseudo-random stride when no visible
or advertised ore existed. v262 tested whether a Builder should prefer its
unvisited nearby frontier before spending route time on a distant tile. The
change was limited to `DefenderMixin._explore_target`; existing ore ranking,
danger/range filters, route FSM, navigation, workforce, combat, and Store
behavior were unchanged. Focused tests covered visit ordering, danger and
minimum-distance filtering, and deterministic ties.

## Validation

- Initial implementation passed focused **29/29**, compileall, smoke **4/4**
  (`reports/local-20260819T080620Z`);
  static retained the inherited 15 obsolete-module import errors and two
  navigation fast-path assertions. The exact-v0043 15-map screen regressed to
  **3-12**, **44,400/82,070 Ti**, all deliveries, zero TLE/suspicious rows,
  max p99/peak **1,381/5,768 us** (`reports/local-20260819T080653Z`). Replay
  rows showed route-conversion collapses, including Glacierkeep **2 vs 11**
  Harvesters and Archipelago **6 vs 12**.
- One replay-confirmed repair restored deterministic per-Builder rotation
  within equal visit/geometric shells. Focused remained **29/29**, compileall
  passed, smoke **4/4**, and static kept the inherited profile. The first
  repaired screen reached **8-7**, all deliveries, **86,990/98,820 Ti**, zero
  TLE/suspicious rows, max p99/peak **1,374/3,452 us**
  (`reports/local-20260819T081242Z`).
- The independent all-15-map rotation failed to reproduce the edge at **4-11**
  with **48,270/77,650 Ti**, all deliveries, zero TLE/suspicious rows, max
  p99/peak **1,380/6,035 us** (`reports/local-20260819T081508Z`).

## Decision and rollback

Reject v262 after the initial result and one bounded repair. The repaired
nearest-shell policy was not a reliable improvement and collection remained
below v0043. Temporary source/tests were removed; candidate is recursively
byte-identical to immutable v0043 (`reports/iter-v262-frontier-discovery/rollback-source.diff`).
Rollback focused tests were **26/26**, compileall passed, and smoke was **4/4**
(`reports/iter-v262-frontier-discovery/rollback-focused.log`,
`reports/iter-v262-frontier-discovery/rollback-compileall.log`,
`reports/iter-v262-frontier-discovery/rollback-smoke.log`). No long gate,
package, upload, activation, promotion, or live-state operation occurred.

## Remaining risk

Route discovery and chain conversion remain the dominant local/live loss
shape. A future exploration change must preserve per-Builder spread and prove
repeatability on rotated maps before any broader gate.
