# v316 verified source-route reuse — rejected at release gate

Date: 2026-08-20

## Objective and scope

Top-team economy-first openings reuse deliberate route ownership instead of
building parallel conveyor trails.  v316 tested a bounded source-side form of
that idea: after at least one completed route, a Builder could build a new
Harvester directly beside a visible friendly Conveyor only if a fixed-output
walk of at most 64 nodes reached our Core.  Splitters, cycles, gaps, enemy or
unknown tiles rejected reuse and preserved the existing Harvester-then-chain
path.

Temporary production scope was `bots/candidate/bot/defender.py`, with focused
coverage in `tests/test_candidate_route_reuse.py`.  Store layout, source
selection, unserved route geometry, role/task policy, combat units, navigation,
baseline, package, upload, activation, and live state were non-goals.

## Validation

- Initial focused route/seed/economy/defense tests: **37/37**; compileall
  passed; smoke **4/4** at `reports/local-20260820T010212Z`; static retained
  the inherited 15 stale imports and two navigation assertions.
- Initial 15-map screen: command-clean, **6-9**, collection
  **69,490/78,790 Ti** (raw
  replay report `reports/local-20260820T010238Z`; parsed diagnostics
  `reports/iter-v316-route-reuse-screen-analysis.json`), zero TLE/suspicious
  rows and zero candidate no-delivery rows.
- One permitted repair limited reuse to exactly the second route.  Focused
  stayed **37/37**, compileall passed, smoke **4/4** at
  `reports/local-20260820T010449Z`, and the screen improved to **8-7** with
  **93,840/81,370 Ti**, zero no-delivery/TLE/suspicious rows and max
  p99/peak **1,509/2,625 us** (`reports/local-20260820T010509Z`; analysis
  `reports/iter-v316-route-reuse-repair-screen-analysis.json`).
- The defined 60-game release gate was command-clean but reversed the screen:
  **24-36**, collection **260,460/289,270 Ti**, one comparator no-delivery,
  zero candidate no-delivery/TLE/suspicious rows, max p99/peak
  **1,540/5,506 us**.  Report:
  `reports/local-20260820T010727Z`; diagnostics:
  `reports/iter-v316-route-reuse-long-analysis.json`.

## Decision and rollback

Reject v316 at the release gate.  The screen edge was seed-sensitive and did
not survive the paired endpoint matrix.  The temporary helper and focused
test were removed; recursive candidate parity with immutable v0044 is zero in
`reports/iter-v316-route-reuse-rollback-source-parity.diff` and
`reports/iter-v316-route-reuse-rollback-main-parity.diff`.

Rollback focused coverage was **34/34**, compileall passed, static retained
the inherited exit-2 profile, and rollback smoke was **4/4** at
`reports/local-20260820T011408Z`.  No promotion, package, upload, activation,
or live transition occurred.

## Next risk

Source-side route reuse is not enough; the long gate shows that suppressing
parallel routes can starve map-specific throughput.  The next hypothesis must
coordinate route ownership/repair without declaring a shared outlet a completed
route, or implement a genuinely Core-outward planned route with explicit
verification.
