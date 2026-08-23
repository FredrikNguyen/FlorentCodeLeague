# v292 home route-blocker response — rejected

## Replay basis and objective

Fresh v107 loss replays repeatedly showed the candidate ending long games with
only 1–4 surviving Harvesters while the opponent had 6–13.  One live
Glacierkeep loss also showed an infiltrating opponent replacing destroyed home
Conveyors with Barriers.  The existing bot could repair or re-point its own
dead belt, but it never reacted to an enemy Barrier occupying the exact output
tile of a friendly Conveyor.  v292 tested whether one nearest dynamic Builder
should use the existing home-threat/Builder-fire path to remove only that
specific blocker.

## Scope and non-goals

Temporary production scope was one helper/branch in
`bots/candidate/bot/dynamic.py`; focused coverage was three tests in
`tests/test_candidate_nearest_defense.py`.  The economy phase, route FSM,
ordinary belt repair, hijack/raid scoring, fixed attackers, Store layout,
baseline/archive, and live platform state were non-goals.

## Validation

- Focused route/defense tests: **29/29**; economy-phase subset: **4/4**.
- Candidate compileall: **pass**.
- `make static`: inherited **exit 2** from 15 obsolete deleted-module imports
  and two navigation fast-path assertions; no v292-specific error.
- Candidate smoke: **4/4 command-clean**, report
  `reports/local-20260819T171217Z`.
- Rotated 15-map screen: report `reports/local-20260819T171251Z`, with zero
  command failures, TLEs, or suspicious rows. Candidate-A won **7-8** against
  immutable v0044, collected **60,370/46,680 Ti**, placed **109/109**
  Harvesters, and had **14/15 vs 15/15** first deliveries. Maximum
  p99/peak callback was **1,336/2,412 us**. The candidate Royale row had no
  delivery; the comparator had none.

## Decision and rollback

The route-blocker signal produced no aggregate win-rate or protected-map edge
and introduced a candidate no-delivery row, so v292 was rejected at the first
screen.  No repair, release gate, promotion, package, upload, activation, or
live transition was justified.  The temporary predicate and tests were
removed.  Rollback focused coverage was **30/30**, compileall passed, rollback
static retained the inherited exit 2, and rollback smoke was **4/4** at
`reports/local-20260819T171526Z`.  Recursive production-source parity with
immutable `bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`
was zero diff.  v0044 remains the local comparator; v107 remains
active-observing and v105 remains the operational rollback target.

Evidence is under `reports/iter-v292-route-blocker/`, including
`screen-analysis.json`, initial and rollback static/smoke logs, and the
screen/rollback reports.
