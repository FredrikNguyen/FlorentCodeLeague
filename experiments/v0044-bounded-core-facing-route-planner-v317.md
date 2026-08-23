# v317 bounded Core-facing route planner — rejected after one repair

Date: 2026-08-20

## Objective and scope

Top-team economy-first bots build deliberate Core-outward route geometry and
verify each link.  v317 replaced the v0044 CHAIN walk with a visible bounded
cardinal BFS plan, building ordered links and waiting through transient
occupancy before falling back to the existing local walker.  The first
implementation applied to every fully visible route; the one repair activated
it only for a genuine obstacle detour longer than Manhattan distance.

Temporary production scope was `bots/candidate/main.py` and
`bots/candidate/bot/defender.py`, with focused coverage in
`tests/test_candidate_planned_route.py`.  Source selection, Store, spending,
workforce, roles/tasks, combat, source reuse, baseline, package, upload,
activation, and live state were non-goals.

## Validation

- Initial focused planner/seed/economy/defense coverage was **39/39**,
  compileall passed, smoke **4/4** at `reports/local-20260820T012000Z`, and
  static retained the inherited 15 stale imports plus two navigation
  assertions.
- Initial 15-map screen was command-clean but **2-13**, collection
  **44,160/61,230 Ti**, zero no-delivery/TLE/suspicious rows, and max
  p99/peak **1,437/5,173 us**.  Report:
  `reports/local-20260820T012025Z`; diagnostics:
  `reports/iter-v317-planned-route-screen-analysis.json`.
- One planner-only repair restricted activation to obstacle detours.  Focused
  stayed **39/39**, compileall passed, smoke **4/4** at
  `reports/local-20260820T012311Z`, static retained the same inherited
  profile, and the screen reached **8-7** but still collected only
  **45,280/59,000 Ti** (zero no-delivery/TLE/suspicious rows; max p99/peak
  **1,451/2,839 us**).  Report:
  `reports/local-20260820T012333Z`; diagnostics:
  `reports/iter-v317-planned-route-repair-screen-analysis.json`.

## Decision and rollback

Reject v317 after its permitted repair; the planner harmed conversion even
when the screen win count recovered.  The temporary BFS state, route executor,
and focused test were removed.  Recursive candidate parity with immutable v0044
is zero in `reports/iter-v317-planned-route-rollback-source-parity.diff` and
`reports/iter-v317-planned-route-rollback-main-parity.diff`.

Rollback focused coverage was **34/34**, compileall passed, static retained
the inherited exit-2 profile, and rollback smoke was **4/4** at
`reports/local-20260820T012606Z`.  No long gate, promotion, package, upload,
activation, or live transition occurred.

## Next risk

Replacing the proven chain walker with local BFS is not robust.  The next
structural experiment should preserve that walker and add explicit route-health
ownership/repair or a post-delivery verification pulse, with no source-reuse or
global role/lease rewrite.
