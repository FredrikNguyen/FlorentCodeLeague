# v170 early route-site ranking

## Objective

When an economy Builder is adjacent to more than one eligible ore tile during
the first three completed routes, choose the site with the shortest Manhattan
distance to our published Core. The shipped bot currently scans a fixed
compass order, which can select a farther site and pay for a longer conveyor
chain even when a shorter adjacent route is available.

This is a narrow map-context route-conversion hypothesis motivated by the
v0040 loss audit: several losses delivered once but accumulated fewer
Harvesters and much less titanium, while the route code otherwise remained
reliable. Shorter early paths should get the next delivery online sooner and
leave more resources for later Harvesters and the combat shell.

## Comparator and allowed files

- Comparator: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Source: `bots/candidate/bot/defender.py`.
- Focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, `UPDATES.md`, and durable project state.

## Non-goals

No workforce target, role/task order, route FSM/slack, navigation, combat,
Sentinel/Gunner/Launcher policy, costs/reserves, Store schema, map branch,
baseline/archive, package, upload, activation, or live-state change.

## Implementation

- During the existing `ECONOMY_PRIORITY_CHAINS` opening, sort the already
  eligible adjacent ore directions by Core distance with deterministic
  coordinate tie-breaks.
- If the Core is unpublished or the economy has reached three completed routes,
  retain the existing `CARDINALS` order exactly.
- Add a focused FakeController test with two adjacent ore sites where compass
  order chooses the longer route.

## Done criteria

- Focused tests and compileall pass; `make static` is checked and inherited
  failures are recorded; smoke is command-clean.
- The 21-game all-map screen improves aggregate paired win rate over v0040
  with no candidate no-delivery, command, TLE, or suspicious-output failures.
- Only a materially positive screen advances to the 60-game release gate; a
  tie/regression or reliability/delivery failure requires exact v0040 rollback.
- Self-review confirms no post-three-route ordering or unrelated strategy path
  changed.

## Evidence and decision

Focused checks passed **21/21**, compileall passed, smoke was **4/4**, and
static retained only the inherited 15 obsolete imports plus two navigation
assertions. The 21-game screen was **11-10** versus v0040 with zero candidate
or comparator no-delivery games and zero TLE/suspicious-output rows. Candidate
mean Harvesters were **8.00 vs 8.43**, first delivery **29.5 vs 22.6**, and
Sentinels **3.14 vs 4.00**; max p99/peak was **1,415/5,395 us**. Evidence:
`reports/local-20260818T030353Z` and
`reports/iter-v170-early-route-site-ranking-screen-replay-analysis.json`.

v170 is rejected as a tie-level result; no repair or 60-game gate was
warranted. The opening ranking and focused test were removed. Candidate source
is exact recursive v0040 parity (**0 diff lines** in
`reports/iter-v170-early-route-site-ranking-rollback-source-diff.txt`).
Rollback focused checks passed **20/20**, compileall passed, and rollback
smoke was **4/4** (`reports/local-20260818T030659Z`). No release, remote,
package, upload, activation, or baseline transition occurred.
