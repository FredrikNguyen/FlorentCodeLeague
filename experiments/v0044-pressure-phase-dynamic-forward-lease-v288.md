# v288 pressure-phase dynamic forward lease — rejected

Date: 2026-08-19

## Parent and hypothesis

- Parent/comparator: immutable `bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`.
- Candidate: `bots/candidate`.
- Live context: v107 remained `active_observing`; v105 was the user-requested
  operational rollback target and v101 the previous fallback.  No platform
  operation was authorized by this experiment.
- Hypothesis: during the Core-published `PRESSURE` phase, after at least
  three completed routes and before the existing early Sentinel target is
  observed, one nearest non-fixed Dynamic Builder can use the existing
  `TASK_ADVANCE` executor without harming the economy.  Other workers, fixed
  roles, routes, prices, Store layout, and Sentinel legality remain unchanged.

## Temporary changes

- `bots/candidate/bot/dynamic.py`: pressure-phase lease and deterministic
  nearest non-fixed owner.
- `tests/test_candidate_nearest_defense.py`: pressure/route/core/shell/owner
  coverage.

The temporary source and test edits were removed after the first screen.
Candidate source parity with immutable v0044 is zero diff at
`reports/iter-v288-pressure-lease/rollback-source-parity.diff`.

## Validation and evidence

- Initial focused tests: **34/34** (`focused.log`).
- Initial compileall: pass (`compileall.log`).
- Initial `make static`: inherited exit 2, with 15 obsolete-module import
  errors and two navigation assertion failures (`static.log`).
- Initial `make smoke`: **4/4** command-clean,
  `reports/local-20260819T155105Z` (`smoke.log`).
- First rotated 15-map screen: `reports/local-20260819T155200Z`, analysis in
  `screen-analysis.json`; all 15 commands completed without delivery
  failures, TLEs, or suspicious output.  Candidate-A won **9-6**, but
  collection was **82,570/88,150 Ti**, placed Sentinels **47/56**, and mean
  first delivery was **28.7/50.4** turns.  The manifest had
  `screen_side_swapped_pairs=0`; protected-map economy collapses included
  Fjordgate **40/5,890 Ti** and Valkyrie **360/7,230 Ti**.  Maximum replay
  p99 was **1,455 us** and maximum peak was **5,252 us**.
- Rollback focused tests: **30/30** (`rollback-focused.log`).
- Rollback compileall: pass (`rollback-compileall.log`).
- Rollback `make static`: inherited exit 2 (`rollback-static.log`).
- Rollback `make smoke`: **4/4** command-clean,
  `reports/local-20260819T155633Z` (`rollback-smoke.log`).

## Decision

Reject v288 at the first screen.  The one-sided 9-6 result is not repeatable
evidence and the candidate regressed aggregate collection, forward Sentinel
count, and protected-map economy.  Per the plan, no repair, second screen,
long gate, promotion, package, upload, activation, or live-state transition
was performed.  Preserve exact v0044 as the local comparator and retain v105
as the operational rollback target.
