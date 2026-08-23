# v140 ore-claim handoff

## Objective

Prevent a closer non-attacker Builder that may already be committed to a
non-economic task from suppressing an eligible Builder's visible ore claim
after the three-route economy milestone.

## Allowed files

- `bots/candidate/bot/defender.py`
- `tests/test_candidate_seeded_route.py`
- this experiment record, reports, `UPDATES.md`, and durable state

## Non-goals

- No role/task priority, workforce phase, route FSM, exploration, combat, ammo,
  Store layout, map branch, baseline, package, upload, or activation changes.

## Results

- Initial post-milestone no-yield variant: focused 21/21, compileall passed,
  smoke 4/4, static inherited exit 2; 54-game screen **27-27**, candidate/
  comparator Ti **215,170/208,250**, candidate/comparator no-delivery **2/2**.
  Report: `reports/local-20260817T142848Z`.
- Repair 1 disabled yielding only at exactly three completed routes and restored
  it afterward: focused 21/21, compileall passed, smoke 4/4, static inherited
  exit 2; screen **28-26**, candidate/comparator Ti **180,530/152,770**, but
  candidate no-delivery **1** versus comparator **0**. Report:
  `reports/local-20260817T143431Z`.
- Both runs were command-clean with zero TLE/suspicious-output failures. The
  two-game repair edge is not significant and its delivery regression fails the
  promotion gate.

## Decision

Reject after the initial screen and one bounded repair. Restore production
candidate files and focused tests byte-for-byte to v0038. Rollback focused
tests were 21/21, compileall passed, smoke 4/4, and static retained inherited
failures. No 210-game gate, package, upload, activation, or live baseline
change was performed.

## Next hypothesis

Inspect v0038's route-owner and chain-pending handoffs in replay losses. Test
one local, non-global recovery action for a Builder that loses its target while
preserving the opening chain and three-route gate.
