# v257 bounded dynamic task rechecks — rejected after one repair

## Replay basis and objective

The fresh v106 live refresh exposed a reliability failure before any new
strategy was justified. In match `72338be4-29ed-49e0-882f-8a357f16ceb6`, the
active v106 side incurred 63 TLEs on Midgard and 1,082 on Nordkap. The dynamic
role re-ran several vision-bounded detectors every ready round, and its
targetless `TASK_HARVEST` path reset its start time repeatedly. v257 changed
only that scheduling hot path.

## Scope

The temporary production files were `bots/candidate/main.py`,
`bots/candidate/bot/constants.py`, and `bots/candidate/bot/dynamic.py`.
Focused additions were in `tests/test_candidate_nearest_defense.py`. The
immutable comparator was
`bots/versions/v0043_liquidity-backed-dynamic-floor_20260819-0415_eeafad8f`.
The candidate was never packaged, uploaded, activated, or used for live state.

The initial change added a two-round detector recheck cadence after each task's
commitment floor and stopped same-priority targetless tasks from resetting
`task_started`. The one permitted repair kept targetless `TASK_HARVEST` valid
through the generic 40-round timeout so the workforce could remain in the
economy loop until a different task priority was actually selected.

## Validation

- Initial focused coverage: **28/28**; compileall passed; smoke **4/4**.
  `make static` retained the inherited deleted-module imports and navigation
  fast-path assertions.
- Exact-v0043 15-map screen (seed 172): candidate-A **8-7**, all 15 candidate
  deliveries, **82,510 vs 72,920 Ti**, zero TLE/suspicious rows, max
  p99/peak **1,447/5,964 us**. Raw report:
  `reports/local-20260819T064302Z`; analysis:
  `reports/iter-v257-task-recheck/screen-analysis.json`.
- Independent side-swapped 30-game screen (seed 173): **17-13**, all 30
  candidate deliveries, **126,510 vs 117,880 Ti**, zero TLE/suspicious rows,
  max p99/peak **1,477/2,987 us**. Candidate collapsed Glacierkeep,
  Archipelago, and Nordkap to **0-2**. Raw report:
  `reports/local-20260819T064552Z`; analysis:
  `reports/iter-v257-task-recheck/screen30-analysis.json`.
- The bounded timeout repair passed focused **29/29**, compileall, and smoke
  **4/4**. Its independent 30-game screen reached **18-12** and
  **135,000 vs 114,300 Ti**, with 29/30 candidate deliveries, zero
  TLE/suspicious rows, max p99/peak **1,492/5,212 us**. Archipelago and
  Nordkap recovered to 1-1, but Glacierkeep remained **0-2**. Raw report:
  `reports/local-20260819T065127Z`; analysis:
  `reports/iter-v257-task-recheck/repair/screen30-analysis.json`.

## Decision and rollback

Reject v257. The reliability improvement is real locally, but the protected
Glacierkeep collapse blocks promotion despite the aggregate edge. Temporary
source and test edits are being removed; v0043 remains the baseline. No longer
gate, package, remote test, upload, activation, promotion, or live transition
is justified.

## Remaining risk

The live TLE signal still needs a fix, but the broad task cadence is too
behaviorally coupled on Glacierkeep. The next iteration must use a map-local
replay cause (likely route/workforce starvation) rather than widen task
rechecks globally.
