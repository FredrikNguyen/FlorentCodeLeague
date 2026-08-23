# v246 topology-aware home Barrier response

## Objective

The v105 Drakkarfjord loss shows a failure mode that the existing
anti-infiltrator policy cannot address: enemy Barriers occupied the Core ring
and later blocked friendly Conveyor outputs. The current home-threat detector
intentionally ignores Barriers, so dynamic Builders did not clear the
obstruction and the team's early route stopped converting resources.

v246 tests a narrow response. A dynamic Builder may select an enemy Barrier
only when it is visibly on the cardinal ring of our 2x2 Core or when a visible
friendly Conveyor points directly into it. The existing nearest-owner,
commitment, danger, and legal adjacent fire/movement behavior remains the
executor. Unrelated enemy Barriers are not threats.

## Scope and non-goals

- `bots/candidate/bot/dynamic.py`;
- `tests/test_candidate_nearest_defense.py`;
- this record and durable plan/update/state metadata.

No opening, workforce, route FSM, ordinary raid/hijack, fixed-attacker,
purchase, Store, map, baseline, package, upload, activation, or live-state
change is included. Active `MODE_CHAIN` behavior remains unchanged.

## Validation plan

Run the focused nearest-defense suite, candidate compileall, `make static`,
and `make smoke`. If those retain the inherited profile, run the configured
rotated 15-map screen against exact v0042. Promote or run a longer gate only
if the screen is command/delivery-clean and supplies a clear aggregate
win-rate or collection edge without a new reliability fault.

## Result

Focused topology/legality coverage passed **30/30** before rollback (26
nearest-defense tests plus seeded-route coverage), candidate compileall passed,
and `make smoke` was **4/4** command-clean. `make static` retained the
inherited failure profile: 15 obsolete deleted-module imports and two
navigation fast-path assertions. The rotated 15-map screen was command- and
delivery-clean with zero TLE/suspicious rows, but candidate-A lost **6-9** and
collected **73,120 vs 73,780 Ti**; both sides delivered on all 15 maps and the
maximum p99/peak callback time was **1,467/4,917 us**. Replay analysis is in
`reports/iter-v246-home-barrier/replay-analysis.json`, with the raw run at
`reports/local-20260819T023956Z`.

The experiment was rejected without a repair or long gate. Temporary
source/test edits were removed and recursive candidate parity with immutable
v0042 is zero-line at
`reports/iter-v246-home-barrier/rollback-source.diff`; rollback focused
coverage was **27/27** and rollback compileall passed. No promotion, package,
upload, activation, or live-state transition occurred. Post-rollback smoke
was **4/4** at `reports/local-20260819T024516Z`; rollback static retained the
same inherited failures.
