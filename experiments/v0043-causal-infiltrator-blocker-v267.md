# v267 causal home-route infiltrator blocker — rejected

## Objective and evidence

Fresh v106 replays showed repeated remove-then-replace events: an own home
Conveyor disappeared and an enemy Barrier occupied the same tile the next
round. v267 let only the nearest dynamic Builder react when a visible enemy
Barrier occupied the output of a visible friendly home Conveyor. After arrival
it destroyed the Barrier and rebuilt a Conveyor with a valid replacement
facing. Generic enemy-Builder pursuit, ordinary Barriers, route policy,
offensive hijack, and all purchase policies were unchanged.

## Validation

- Focused coverage: **29/29**; candidate compileall passed; `make smoke` was
  **4/4**; `make static` retained only the inherited 15 obsolete imports and
  two navigation fast-path assertions. Logs are under
  `reports/iter-v267-infiltration-blocker/`.
- Initial rotated 15-map screen was command-clean, all sides delivered, zero
  TLE/suspicious rows, and candidate-A finished **7-8** while collecting
  **76,570 vs 75,570 Ti** (`reports/local-20260819T094922Z`). Replay audit
  found five candidate remove/replace sequences and six baseline sequences;
  details: `reports/iter-v267-infiltration-blocker/blocker-audit.txt`.
- Independent rotation was command-clean with zero TLE/suspicious rows, but
  candidate-A fell to **6-9**, collected **48,070 vs 68,740 Ti**, and had one
  no-delivery game versus baseline **15/15** delivery
  (`reports/local-20260819T095225Z`). Parsed metrics are in
  `screen-replay-analysis.json` and `screen-rotation-replay-analysis.json`.

## Decision and rollback

The small initial collection edge did not repeat and the rotated screen
introduced a delivery regression. Reject v267 without a longer gate. Temporary
detector/task/repair code and tests were removed; recursive source parity with
exact v0043 is zero lines in `rollback-source.diff`. Rollback focused was
**26/26**, compileall passed, smoke **4/4**, and static retained the inherited
failures. No promotion, package, upload, activation, or live-state operation.

## Follow-up

The replay event is real, but a nearest dynamic repair is too opportunistic and
can displace route conversion on maps without a stable local owner. Keep the
generic infiltration branch closed. Any future defense or takeover hypothesis
must preserve first delivery and use shared event memory or an explicit route
owner rather than another per-Builder local detector.
