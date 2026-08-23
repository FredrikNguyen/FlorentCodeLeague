# v263 bounded dynamic economy rotation — rejected

## Replay basis and objective

Fresh v106 Coreflood and Torsko losses showed a phase handoff problem: after
three to five completed routes, dynamic Builders could remain on the fallback
pressure task while the Harvester curve stopped at four to six. The candidate
already had fixed attackers and a liquidity-backed economy floor, so the
bounded hypothesis was to rotate one otherwise unproductive dynamic Builder
back through the existing SCOUT/CHAIN loop until six completed routes. This was
deliberately different from the rejected always-on home scout in v182 and did
not add an infiltration detector.

## Exact scope

- `bots/candidate/main.py`: per-Builder pulse state;
- `bots/candidate/bot/constants.py`: route target and pulse timing;
- `bots/candidate/bot/dynamic.py`: stale `TASK_ADVANCE` rotation only;
- `tests/test_candidate_nearest_defense.py`: ownership/trigger/expiry tests;
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable metadata.

No route geometry, SCOUT ranking, Store schema, costs/reserves, fixed attacker,
turret/Sentinel/Launcher/Barrier purchase, hijack/raid selector, map branch,
baseline, package, upload, activation, or live operation changed.

## Validation

- Focused tests: **30/30** (`reports/iter-v263-bounded-economy-rotation/
  focused.log`); the first run exposed only fake-controller assumptions,
  which were corrected before the green run.
- Candidate compileall passed at
  `reports/iter-v263-bounded-economy-rotation/compileall.log`.
- `make static` retained the known inherited exit 2: 15 obsolete legacy-module
  imports and two navigation fast-path assertions, with no v263-specific
  static error (`reports/iter-v263-bounded-economy-rotation/static.log`).
- Smoke was **4/4** command-clean at `reports/local-20260819T083415Z`.
- Exact-v0043 rotated 15-map screen was command-clean with zero TLE/suspicious
  rows but rejected at **4-11**. Candidate collected **53,550 vs 73,790 Ti**,
  placed **91 vs 147 Harvesters** (6.07 vs 9.80 per side), and delivered in
  **14/15 vs 15/15** games. Maximum p99/peak were **1,440/4,963 us**. Raw
  report: `reports/local-20260819T083440Z`; replay diagnostics:
  `reports/iter-v263-bounded-economy-rotation/replay-analysis.json`.

## Decision and rollback

The pulse did not repair the Harvester plateau and introduced a Valkyrie
no-delivery loss. The screen had no win-rate, collection, delivery, or
protected-map edge, so no repair or longer gate was justified. The temporary
source/constants/tests were removed with `apply_patch`; recursive candidate
parity with immutable v0043 is zero at
`reports/iter-v263-bounded-economy-rotation/rollback-source.diff`. Rollback
focused coverage was **26/26**, compileall passed, and rollback smoke was
**4/4** at `reports/local-20260819T083806Z`. No package, upload, activation,
promotion, or live-state transition occurred.

## Remaining risk and next direction

The replay confirms the economy deficit but not that a timed return from the
pressure lane is the right remedy. The next hypothesis should address the
actual source/route commitment contract or builder allocation, not another
rotation interval or generic infiltrator priority.
