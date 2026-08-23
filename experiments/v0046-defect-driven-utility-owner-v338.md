# v338 defect-driven utility ownership

## Objective

Test a structural local-work contract on immutable v0046: a dynamic Builder
should be the deterministic nearest responder for a verified visible belt/base
defect, release the work when another responder is closer or the defect is
gone, and avoid a global Store lease.  The opening spend, route geometry,
fixed attacker/defender roles, unit caps, Launcher behavior, and live platform
state were out of scope.

## Allowed files and done criteria

Production scope was `bots/candidate/bot/dynamic.py`, with focused coverage in
`tests/test_candidate_nearest_defense.py` and
`tests/test_candidate_economy_phase.py`.  This experiment record,
`UPDATES.md`, `state/project_state.json`, `docs/CURRENT_PLAN.md`, and generated
`docs/START_HERE.md` were the durable files.  The candidate had to compile,
pass focused tests, remain command-clean in smoke and the all-map screen, and
show a paired edge without a reliability regression before promotion.

## Evidence and bounded repairs

- Initial local ownership assigned only the nearest visible dynamic Builder to
  belt gaps and damaged home buildings, with release-on-closer-observer
  validation.  Focused coverage passed **35/35**, compileall passed, the
  inherited `make static` profile remained (15 obsolete imports and two
  navigation assertions), and the 20-game smoke was command-clean.  The
  15-map screen was **7-8 candidate-A**, with zero TLE/suspicious rows;
  replay analysis is at `reports/iter-v338-utility-owner-replay-analysis.json`
  (`reports/local-20260820T062213Z`).
- Repair 1 restricted enemy-Harvester hijack to the Core's `PRESSURE` phase
  while retaining local ownership.  Focused coverage passed **36/36**,
  compileall passed, smoke was **20/20** command-clean, and the screen fell to
  **5-10** (`reports/local-20260820T062804Z`).  Replay analysis remained
  command/reliability-clean (`reports/iter-v338-utility-owner-repair1-replay-analysis.json`).
- Repair 2 corrected the scheduler contract so live `HARVEST` work is selected
  before damaged-building maintenance.  Focused coverage passed **37/37**,
  compileall passed, `make static` retained the inherited failures, and
  `make smoke` was **4/4** (`reports/local-20260820T063345Z`).  The fresh
  all-map screen improved to **10-5**, zero TLE/suspicious rows, max p99
  **1,298 us** (`reports/local-20260820T063408Z`,
  `reports/iter-v338-utility-owner-repair2-replay-analysis.json`).
- The release-sized 60-game local gate was command-clean and **33-27** for the
  candidate, with **292,950 vs 283,710 Ti**, max p99/peak **1,436/4,903 us**,
  and zero TLE/suspicious rows (`reports/local-20260820T063701Z`,
  `reports/iter-v338-utility-owner-repair2-local-gate-replay-analysis.json`).
  It nevertheless contained one candidate no-delivery game on Glacierkeep
  (`0030_glacierkeep_s1_candidate-B.replay26`) while v0046 delivered there.
  That is a reliability regression under the promotion guard, despite the
  aggregate edge.

## Decision and rollback

Reject v338 after its two bounded repairs.  Restore candidate production to
exact recursive parity with immutable v0046 (zero source diff in
`reports/iter-v338-utility-owner-rollback-source-parity.diff`).  Rollback
focused coverage passed **31/31**, compileall passed, `make static` retained
the inherited 15 import errors and two navigation assertions, and rollback
`make smoke` was **4/4** command-clean (`reports/local-20260820T064600Z`).
No local baseline promotion, package, upload, activation, or live-state
transition occurred.

## Remaining risks and next direction

The nearest-owner contract improved one screen and the full gate's aggregate
score, but it did not prevent a map-specific no-delivery failure.  Future work
must diagnose the Glacierkeep route/first-delivery replay and add a verified
route-health signal before changing utility ownership again; do not retry this
nearest-owner/hijack gate unchanged.  v0046 remains the frozen baseline and
platform v108 remains `active_observing` with no live change.
