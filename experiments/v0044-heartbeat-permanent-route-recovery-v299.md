# v299 — heartbeat-driven permanent route recovery

Date: 2026-08-19

## Hypothesis and scope

Fresh v107 replay losses showed routes going quiet after a Conveyor link was
removed while the Core-designated defender remained in its normal scout loop.
The candidate already publishes a delayed economy phase when income goes quiet.
v299 gave only that permanent defender a bounded home sweep during
`CONVERTING`/`CRISIS` after one completed route: travel to the Core vicinity,
claim one visible gap using the existing classifier, repair it from an adjacent
standing tile, and expire after eight blocked attempts.  Scope was limited to
`bots/candidate/bot/constants.py`, `bots/candidate/bot/defender.py`, and one
temporary focused test module.  No Store, route, combat, or role policy changed.

## Validation and evidence

- Focused coverage passed **39/39**, compileall passed, and smoke was **4/4** at
  `reports/local-20260819T192240Z`.  `make static` retained the inherited
  15 removed-module imports and two navigation fast-path assertions; the new
  route-recovery tests passed.
- The rotated seed-174 all-map screen was command-clean but not
  delivery-clean: candidate-A finished **8–7**, collected **66,440 vs 74,880
  Ti**, and had one no-delivery game versus zero for the comparator
  (`reports/local-20260819T192317Z`).  Replay analysis reported max p99/peak
  callback times **1,247/2,456 us**, with zero TLE or suspicious rows.  The
  detailed analysis is `reports/iter-v299-route-recovery/replay-analysis.log`.

## Decision and rollback

Reject v299 at the first screen without repair or release.  The temporary sweep
and test were removed; exact recursive v0044 parity is proven by the empty
`reports/iter-v299-route-recovery/rollback-source-parity.diff`.  Rollback
focused coverage was **34/34**, compileall passed, and rollback smoke was
**4/4** at `reports/local-20260819T192608Z`.  No 60-game gate, package,
upload, activation, or live transition occurred.  v105 remains the operational
rollback target and live v107 remains `active_observing`.
