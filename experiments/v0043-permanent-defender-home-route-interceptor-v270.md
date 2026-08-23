# v270 permanent-Defender home-route interceptor — rejected

## Objective and replay basis

Fresh v106 replays showed a real remove-then-replace infiltration event: an
enemy Builder removed a friendly home Conveyor and placed an enemy Barrier on
the exact output tile on the next round. v267 and v268 showed that assigning a
dynamic Builder or the active route owner to repair the tile displaced route
conversion. v270 tested a different ownership contract: only the already-
designated permanent Defender would respond, and only to a visible enemy
Barrier occupying the exact output of a friendly home Conveyor.

The implementation was corrected to the game rules during review. Enemy
buildings cannot be removed with `destroy`; the Defender navigated to legal
adjacency and used `can_fire`/`fire` to chip the Barrier. The existing belt
repair path would rebuild the empty output after it disappeared. No enemy
Builder pursuit, dynamic-worker assignment, Store change, or offensive policy
was included.

## Validation

- Focused nearest-defense coverage: **31/31**;
  `reports/iter-v270-permanent-defender-home-route-interceptor/` initial logs.
- Candidate compileall passed. `make static` retained only the inherited
  15 obsolete-module import errors and two rolled-back navigation fast-path
  assertions; no v270-specific static error.
- Smoke was **4/4** command-clean at
  `reports/local-20260819T103556Z`.
- Configured all-map 15-game screen (screen seed 172) was command- and
  delivery-clean but candidate lost **7-8**, collected **62,860 vs 75,850 Ti**,
  and placed **99 vs 132 Harvesters**. Reliability was zero TLE/suspicious
  rows, max p99 **1,479 us**. Raw report:
  `reports/local-20260819T103626Z`; parsed replay diagnostics:
  `reports/iter-v270-permanent-defender-home-route-interceptor/screen-172-analysis.json`.
- Independent rotated 15-game screen (screen seed 175) was command-clean but
  candidate again lost **7-8**, collected **54,820 vs 61,510 Ti**, placed
  **110 vs 124 Harvesters**, and had **14/15 vs 15/15** first deliveries.
  Reliability was zero TLE/suspicious rows, max p99 **1,393 us**. Raw report:
  `reports/local-20260819T103844Z`; parsed diagnostics:
  `reports/iter-v270-permanent-defender-home-route-interceptor/screen-175-analysis.json`.

## Decision and rollback

The interceptor is legal and narrowly scoped, but it produced no repeatable
win-rate, collection, or delivery edge. Reject v270 without a longer gate.
The temporary method, imports, tests, and screen config were removed with
`apply_patch`. Recursive candidate parity with immutable v0043 is zero lines
at `reports/iter-v270-permanent-defender-home-route-interceptor/rollback-source.diff`.
Rollback focused coverage was **26/26**, compileall passed, static retained
the same inherited failures, and rollback smoke was **4/4** at
`reports/local-20260819T104118Z`. No package, upload, activation, promotion,
or live-state operation occurred.

## Follow-up

The causal infiltration event remains useful evidence, but a single permanent
Defender is too slow to clear a 30-HP Barrier and does not improve the local
economy. The next hypothesis should target resource conversion or a stronger
offensive/infiltration mechanism without diverting the opening route workforce.
