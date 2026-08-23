# v356 persistent frontier escape — rejected

Date: 2026-08-20

## Objective

Use the live-v108 Yulerune replay to test one bounded, attacker-local escape
from the static central-wall oscillation.  A fixed attacker that had stalled
behind a locally visible wall received one deterministic edge-lane waypoint
and a finite cardinal move budget.  The route retained bounds, occupancy,
danger filtering, and `can_move` checks, and did not change the economy,
turret, Launcher, Sentinel, or Store policies.

The comparator was immutable
`bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`.
The live-v108 and top-team replay evidence is retained at
`reports/live-observe-20260820T140438Z`.

## Scope and implementation

The temporary candidate touched `bots/candidate/main.py`,
`bots/candidate/bot/attacker.py`, `bots/candidate/bot/constants.py`, and
focused tests in `tests/test_candidate_nearest_defense.py`.  The initial
implementation tracked best Core distance and, after one paying route, sent a
stalled attacker toward the nearer outer map lane.  One bounded repair used
the Core's already-published converting/pressure economy phase as delivery
proof when the delayed historical Harvester counter was still zero.  No
navigation rewrite, danger bypass, route/source, unit-count, baseline, or
platform policy changed.

## Results

- Initial candidate: focused **30/30**, compileall passed, smoke **4/4**, and
  the inherited static profile only; the explicit immutable-v0046 15-map
  seed-179 screen was **6-9**, command-clean.
- One allowed repair: focused **31/31**, compileall passed, smoke **4/4**, and
  static remained only the inherited 15 obsolete-module imports plus two
  navigation assertions.  The identical seed-179 screen remained **6-9**
  (zero command failures, TLEs, suspicious output, or candidate delivery
  failures).  Yulerune's collection gap narrowed, but the attacker still did
  not produce a repeatable win.

The required first-screen floor is **9-6**, so v356 is rejected.  No rotated
screen, 60-game release matrix, remote gate, package, upload, activation, or
promotion ran.

## Rollback and evidence

The temporary source and tests were removed.  Recursive production source
parity with immutable v0046 is empty in
`reports/iter-v356-persistent-frontier/rollback-source-parity.diff`.
Rollback focused coverage is **26/26** (`rollback-focused.log`), compileall
is clean (`rollback-compileall.log`), and rollback smoke is **4/4** at
`reports/local-20260820T152205Z` (`rollback-smoke.log`).  The final static
profile remains the inherited exit-2 result (`rollback-static.log`).  The
repair screen and replay analysis are recorded at
`reports/local-20260820T151846Z` and
`reports/iter-v356-persistent-frontier/repair-screen-analysis.json`.

## Decision and remaining risk

Reject v356 and retain immutable v0046 as the local baseline.  The phase-gate
repair fixed a real delayed-signal defect but did not alter the screen result;
static wall/topology escape remains unresolved.  The next experiment must use
new replay evidence and a distinct mechanism rather than retuning this
frontier route or its timer.
