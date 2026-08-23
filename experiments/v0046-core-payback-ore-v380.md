# v380 Core-payback ore ranking — rejected

## Objective and scope

Starting from immutable v0046, v380 changed visible uncovered-ore selection to
rank the shortest profitable Core route before local Builder travel distance,
then deterministic coordinates.  Existing harvest-range, danger, claim,
blacklist, route FSM, combat, workforce, Store, baseline, package, and live
policy were unchanged.  Production scope was `bots/candidate/bot/defender.py`,
with temporary focused coverage in `tests/test_candidate_nearest_defense.py`.

## Validation

- Focused coverage passed **27/27**, compileall passed, `make smoke` was **4/4**
  at `reports/local-20260820T220119Z`, and static retained only the inherited
  workspace failures (15 obsolete imports and two navigation assertions).
- The first rotated all-15-map/30-game screen (`screen_seed=547`) was
  command-clean but **14–16**, with 29/30 candidate first deliveries and zero
  TLE/suspicious rows.  Candidate collection was **141,680 Ti** aggregate;
  among delivered games first delivery averaged **28.66** rounds, with average
  surviving Harvesters 7.10, Sentinels 1.20, Gunners 1.67, and Builders 8.30.
  Raw games are under `reports/local-20260820T220148Z`; diagnostics are in
  `reports/iter-v380-core-payback-ore/analysis.json`.

The first-screen floor failed, so no second screen or release matrix was
justified.

## Rollback and decision

The temporary Core-payback ranking, focused test, and screen config were
removed.  Candidate production is recursively byte-identical to immutable
v0046; the empty proof is at
`reports/iter-v380-core-payback-ore/rollback-source-parity.diff`.
Rollback focused coverage was **26/26**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260820T220516Z`.  No baseline, package, upload,
activation, promotion, or live-state transition occurred.

Reject v380.  Core-distance-first ore selection did not clear the first-screen
floor; choose a distinct conversion mechanism next.
