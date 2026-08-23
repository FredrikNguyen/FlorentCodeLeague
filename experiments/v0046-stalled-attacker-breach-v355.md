# v355 stalled-attacker breach window — rejected

Date: 2026-08-20

## Objective

Use the fresh live-v108 Yulerune replay to test one bounded, attacker-local
response to a builder oscillating behind a visible firing lane.  After a
stagnation epoch and one completed paying route, the fixed attacker could make
one three-move flank/breach attempt.  The attempt still had to use the normal
visibility, terrain, occupancy, bounds, and `can_move` legality checks.

The comparator was immutable
`bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`.
The live v108 snapshot and top-team replay evidence are retained at
`reports/live-observe-20260820T140438Z`.

## Scope and implementation

The temporary candidate touched `bots/candidate/main.py`,
`bots/candidate/bot/attacker.py`, `bots/candidate/bot/navigation.py`,
`bots/candidate/bot/constants.py`, and focused tests in
`tests/test_candidate_nearest_defense.py`.  The first implementation allowed a
three-move danger-window after ten stalled rounds.  One bounded repair changed
the eligibility to the first paying route and selected an outer-row waypoint
to try to escape static central walls.  No Launcher, unit-count, route/source,
Store, map catalog, baseline, package, or platform policy was changed.

## Results

- Initial temporary candidate: focused **30/30**, compileall passed, smoke
  **4/4**, inherited static profile only; explicit-v0046 15-map seed-172
  screen **6-9**, command-clean.
- Bounded repair: focused **30/30**, compileall passed, smoke **4/4**, and
  inherited static profile only; explicit-v0046 15-map seed-172 screen
  **8-7**, command/delivery/TLE/suspicious-clean.  This still misses the
  required **9-6** screen floor.
- A single Yulerune diagnostic remained command-clean but showed the same
  `(8,9)/(8,10)` oscillation through the central wall.  The breach did not
  establish a repeatable escape, so the mechanism is not promoted.

## Rollback and evidence

The temporary source and test changes were removed.  Recursive production
source parity with immutable v0046 is empty in
`reports/iter-v355-stalled-attacker-breach/rollback-source-parity.diff`.
Rollback focused coverage is **26/26** (`rollback-focused.log`), compileall
is clean (`rollback-compileall.log`), and rollback smoke is **4/4** at
`reports/local-20260820T145838Z` (`rollback-smoke.log`).  The final static
profile remains the inherited exit-2 result: 15 obsolete-module import errors
and two stale navigation fast-path assertions, with no v355-specific failure
(`rollback-static.log`).  Candidate and live v108 remain unchanged; no
release matrix, remote gate, package, upload, activation, or promotion ran.

## Decision and remaining risk

Reject v355 and retain immutable v0046 as the local baseline.  The unresolved
failure is static wall/topology escape, not simply danger-threshold tuning;
the next experiment must be a distinct wall-aware exploration/frontier
mechanism and must preserve the same delivery/reliability gates.
