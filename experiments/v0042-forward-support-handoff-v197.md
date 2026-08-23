# v197 — forward-support handoff

## Objective

Convert an idle dynamic Builder into durable offence/defence support without
adding another enemy-route takeover: after confirmed enemy-Core intel, three
completed routes, a live friendly forward Sentinel, and the normal 80-Ti idle
reserve, assign one nearest dynamic Builder to heal a damaged friendly
forward Sentinel or Core-side Barrier.

## Scope and non-goals

- Temporary source: `bots/candidate/bot/dynamic.py`.
- Temporary focused coverage: `tests/test_candidate_forward_support.py`.
- No attacker, defender, main dispatch, route, Launcher/teleport, baseline,
  package, upload, activation, or live-state changes.
- The one bounded repair tightened the forward target to at most half HP so
  light chip could not pull a worker away from economy or pressure.

## Validation

- Initial focused coverage was **33/33** with nearest-defense and seeded-route
  regressions; compileall passed, static retained only inherited failures, and
  smoke was **4/4** command-clean. The seed-162 15-game screen was **6-9**
  candidate wins, 15/15 command-clean, zero TLE/suspicious rows, and max
  p99/peak **1415/3103 us** (`reports/local-20260818T120418Z`; analysis
  `reports/iter-v197-forward-support-replay-analysis.json`).
- The bounded half-HP repair again passed focused **33/33**, compileall, static
  with the same inherited failures, and smoke **4/4**. Its screen fell to
  **5-10**, remained 15/15 command-clean with zero TLE/suspicious rows, and
  had max p99/peak **1382/3052 us** (`reports/local-20260818T120705Z`;
  analysis `reports/iter-v197-forward-support-replay-analysis-repair1.json`).
- Rollback focused coverage was **27/27**, compileall passed, static retained
  the inherited failures, and rollback smoke was **4/4** at
  `reports/local-20260818T121003Z`. Candidate source is recursively
  identical to immutable v0042.

## Decision

Reject v197 after the one bounded repair. Repairing forward Sentinels/Barriers
did not convert the 6-9 screen and the stricter damage threshold regressed to
5-10; no 60-game gate is justified. No release, package, upload, activation,
or baseline transition occurred. The candidate was restored exactly to v0042.

## Strategic wall and next direction

The current direct offence/sabotage/support branch has now failed: parallel
enemy outlets (v195), destroy/reclaim (v196), and forward repair support (v197)
all failed to beat the paired baseline screen. Do not keep adding local raid,
repair, or barrier selectors without new causal replay evidence. The next
hypothesis should be a different mechanic or phase transition, selected only
after inspecting the actual v197 losses and the rules—candidate options are a
map-context workforce/route phase change or a carefully isolated unit-control
experiment, not another steal variant.
