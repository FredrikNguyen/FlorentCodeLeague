# v243 opening route-context ore ranking — rejected

## Objective

Use the Glacierkeep replay signal to test whether early Builders should rank
visible ore by estimated route-to-Core conversion rather than nearest-builder
distance. The change was enabled only before three completed routes and only
on boards whose width-plus-height was at least 48; compact maps and
established economies kept the v0042 nearest-ore policy.

## Allowed files and non-goals

- `bots/candidate/bot/constants.py`;
- `bots/candidate/bot/defender.py`;
- one focused ore-target test module;
- this record, `UPDATES.md`, `docs/CURRENT_PLAN.md`, and durable reports/state.

No route FSM, navigation, workforce, combat, infiltration, Store, map-name
branch, baseline/archive, package, upload, activation, or live-state change
was allowed.

## Validation

- New route-context plus nearest-defense/seeded-route coverage: **31/31**;
  compileall passed.
- `make static` retained the inherited exit 2 from 15 obsolete deleted-module
  imports and two navigation fast-path assertions; no v243-specific failure.
- `make smoke` was **4/4** command-clean (`reports/local-20260819T015507Z`).
- The rotated 15-map screen was command-clean with zero TLE/suspicious rows,
  but candidate-A lost **4-11**, collected **62,240 vs 73,780 Ti**, placed
  **99 vs 134 Harvesters**, and had mean first delivery **28.2 vs 22.4**.
  Raw report: `reports/local-20260819T015537Z`; parsed diagnostics:
  `reports/iter-v243-opening-route-context/replay-analysis.json`.

## Decision and rollback

Reject v243 without a repair or long gate. The route-weighted selector sent
opening workers toward less productive/farther ore often enough to collapse
the economy, despite helping one Glacierkeep-shaped route. Temporary source
and test edits were removed. Recursive source parity with immutable v0042 is
zero-line (`rollback-source.diff`); rollback focused coverage was **27/27**,
compileall passed, and rollback smoke was **4/4** at
`reports/local-20260819T015759Z`. No promotion, package, upload, activation,
or live-state transition occurred.

## Follow-up

Keep nearest-ore selection. A future route fix needs direct evidence of a
specific blocked or misdirected chain, not a global early ore-ranking change.
