# Evaluation policy quick-screen reduction — 2026-08-18

## Objective

Trim the routine comparison by one redundant game while preserving complete
configured-map coverage. Keep the 60-game release gate unchanged.

## Scope and non-goals

- Changed `configs/eval_regression.toml`, `tests/test_eval_schedule.py`,
  `docs/EVALUATION_PLAN.md`, `docs/CURRENT_PLAN.md`, `state/project_state.json`,
  `UPDATES.md`, and generated `docs/START_HERE.md`.
- No bot source, baseline snapshot, package, upload, activation, or live state
  changed.
- The quick screen is now 15 candidate-A games: one stratified pair per map.
  The release gate remains 15 maps × 2 endpoint seeds × 2 side orders = 60.

## Validation

- Schedule unit tests: **6/6 passed** (`python -m unittest -v
  tests.test_eval_schedule`).
- Reduced regression: **15/15 command-clean**, all 15 maps represented, zero
  TLE or CLI failures; candidate side was **7-8** against the byte-identical
  v0042 snapshot. Report: `reports/local-20260818T081919Z`.
- Smoke: **4/4 command-clean**. Report: `reports/local-20260818T081858Z`.
- Static: exit 2 from the pre-existing 15 obsolete test imports and two
  navigation fast-path assertions; no policy-related error. Log:
  `reports/policy-quick15-static.log`.
- Regression log: `reports/policy-quick15-regression.log`.

## Decision

Accepted as the routine policy. Fifteen games is the minimum that still
represents every configured map; side-order confidence remains a release-gate
responsibility. The bot baseline remains v0042 and the platform remains v105
under observation.
