# v378 Core-ring sink join — rejected

## Objective and scope

Starting from immutable v0046, v378 allowed a pending route Conveyor to feed
into a visible friendly Conveyor only when that existing Conveyor's output was
verified to enter the Core directly.  Arbitrary unfinished-belt joins, BFS,
route ownership, combat, workforce, Store, baseline, package, and live policy
were unchanged.  Production scope was `bots/candidate/bot/defender.py`, with
temporary focused coverage in `tests/test_candidate_nearest_defense.py`.

## Validation

- Focused coverage passed **27/27**, compileall passed, `make smoke` was **4/4**
  at `reports/local-20260820T214345Z`, and static retained only the inherited
  workspace failures (15 obsolete imports and two navigation assertions).
- The first rotated all-15-map/30-game screen (`screen_seed=521`) was
  command-clean but **9–21**, with no delivery/runtime failures.  Candidate
  collection was **106,330 Ti**, first delivery averaged **27.73** rounds, and
  average surviving units were 5.93 Harvesters, 1.03 Sentinels, 1.50 Gunners,
  and 7.87 Builders.  Raw games are under
  `reports/local-20260820T214409Z`; diagnostics are in
  `reports/iter-v378-core-ring-sink/analysis.json`.

The 9–6 first-screen floor failed decisively, so no second screen or release
matrix was justified.

## Rollback and decision

The temporary Core-ring branch, focused test, and screen config were removed.
Candidate production is recursively byte-identical to immutable v0046; the
empty proof is at `reports/iter-v378-core-ring-sink/rollback-source-parity.diff`.
Rollback focused coverage was **26/26**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260820T214732Z`.  No baseline, package, upload,
activation, promotion, or live-state transition occurred.

Reject v378.  The narrower verified join still reduced conversion on this
schedule; the next iteration must use a different resource-conversion path.
