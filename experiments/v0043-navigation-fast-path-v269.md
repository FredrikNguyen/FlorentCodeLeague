# v269 — cardinal navigation fast path for live TLEs

## Hypothesis and replay basis

The fresh v106 audit found a reliability failure in the active v0043: live
replays reached the 10 ms per-unit budget, including a Torsko game with 1,082
TLE callbacks and several Coreflood/Torsko rows with p99 execution between
6.8 and 10.0 ms. `_navigate` rebuilt a visible-tile BFS even for a clear
cardinal walk, while the existing navigation tests specified a missing
fast-path contract. v269 tried to remove that scan for direct aligned movement
and safe fleeing, preserving `can_move`, danger, visited-state, and BFS
fallback behavior.

## Scope

Temporary source was `bots/candidate/bot/navigation.py`; focused coverage was
`tests/test_candidate_navigation_fast_path.py` plus the nearest-defense
regression suite. The live/replay audit artifacts are
`reports/iter-v269-v106-analysis.json` and
`reports/iter-v269-replay-audit-v105.json`. No strategy selector, Store,
route, workforce, baseline, package, upload, activation, or live state was
changed.

## Validation — initial candidate

- Focused tests: **32/32**; compileall passed.
- `make static`: exit 2 from the inherited 15 obsolete-module imports; the
  navigation fast-path assertions passed in this run.
- Smoke: **4/4**, `reports/local-20260819T101545Z`.
- Configured 15-map screen: **7-8**, candidate collection **80,420** vs
  baseline **88,030 Ti**, both sides delivered in 14/15 rows, zero TLE or
  suspicious output, p99/peak aggregate **1,004/1,937 us**;
  `reports/local-20260819T101614Z` and
  `reports/iter-v269-navigation-fast-path/screen-analysis.json`.
- Independent rotation: **5-10**, collection **100,660 vs 110,090 Ti**, all
  deliveries, zero TLE/suspicious, p99/peak aggregate **1,032/2,409 us**;
  `reports/local-20260819T101827Z` and
  `reports/iter-v269-navigation-fast-path/rotation-analysis.json`.

## Bounded repair and decision

The direct diagonal shortcut could alter route tie-breaking, so one repair
restricted the fast path to already row/column-aligned targets and retained
the old BFS for diagonals. Repair focused was **31/31**, compileall passed,
static retained the same inherited imports, and smoke was **4/4** at
`reports/local-20260819T102155Z`. Its configured screen fell to **6-9** with
**64,760 vs 75,140 Ti** (`reports/local-20260819T102222Z`), so no second
rotation or long gate was justified.

Reject v269. The live TLE problem is credible, but the shortcut did not yield
a repeatable local edge or material p99 improvement. Temporary source/tests
were removed; recursive candidate parity with immutable v0043 is zero at
`reports/iter-v269-navigation-fast-path/rollback-source.diff`. Rollback
focused was **26/26**, compileall passed, and rollback smoke was **4/4** at
`reports/local-20260819T102500Z`. Rollback `make static` returned the inherited
15 import errors plus the two navigation fast-path assertions at
`reports/iter-v269-navigation-fast-path/rollback-static.log`. No promotion,
package, upload, activation,
or live-state operation occurred.

## Next direction

Keep the server CPU/TLE evidence, but do not tune this shortcut. A future
optimization must preserve route-choice semantics more completely or reduce a
different measured hot path while proving a paired edge and independent
reliability improvement.
