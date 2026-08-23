# v210 — sentinel-witnessed local pressure phase

## Objective and scope

Replay review after the blocked v209 Launcher lease found several losses with
fewer Barriers/Sentinels than their winners, while O(1) winners often used no
Launcher. v210 tested whether the existing delayed `SLOT_SENTINEL_COUNT` plus
the existing Harvester offense gate could safely authorize one private local
pressure event for an already-forward dynamic Builder. The event reused the
existing escape-safe enemy-Core cage helper or adjacent Builder fire, then
returned to the prior task. No new Store writes, slots, leases, Launcher
logic, opener, cap, or map branch were allowed.

## Validation

- Luna implementation added private `support_phase`/`support_events` state in
  `main.py`, a guarded support phase in `bot/dynamic.py`, and eight focused
  tests. The first code was rejected by the platform syntax validator because
  it contained a forbidden `finally`; the bounded repair removed that construct
  without changing the phase contract. Final focused coverage was **32/32**
  with compileall passing (`reports/iter-v210-sentinel-pressure/focused.log`,
  `compileall.log`).
- The repair passed `make smoke` **4/4 command-clean** at
  `reports/local-20260818T154530Z`; the initial smoke failure and validator
  evidence are in `root-smoke.log` and `reports/local-20260818T154424Z`.
- `make static` retained the inherited exit **2** (15 deleted-module imports
  plus two navigation fast-path assertions), with no v210-specific error:
  `reports/iter-v210-sentinel-pressure/root-static.log`.
- The exact pre-v210 candidate snapshot scored **3-12** on rotated seed 174,
  15/15 command-clean and delivery-clean, collection **77,640 vs 97,200 Ti**;
  report `reports/parallel-v210-screen/replay-analysis.json`.
- The edited candidate improved to **6-9**, still 15/15 command-clean and
  delivery-clean, with collection **79,560 vs 78,740 Ti** summarized in
  `reports/iter-v210-sentinel-pressure/edited-screen-replay-analysis.json`;
  raw run `reports/local-20260818T154607Z`. It did not clear the positive
  paired screen gate, so no 60-game long gate was run.

## Decision and rollback

Reject v210 after the one syntax repair: the six-win edited screen is not a
clear improvement over v0042, and the pre-edit worktree itself was a severe
3-12 regression. Restore the exact pre-v210 `main.py` and `bot/dynamic.py`
from `/tmp/florent-v210-candidate-DYV2gW/candidate`; remove the temporary test.
Rollback focused coverage was **28/28** (Launcher lifecycle plus preserved
nearest-defense tests) and compileall passed; rollback logs are under
`reports/iter-v210-sentinel-pressure/`. Preserve the v210 replay evidence, but
do not promote, package, upload, activate, or change the v0042 baseline.

## Remaining lesson

The pressure gap is real in some losses, but a per-builder Sentinel witness
without stronger phase budgeting did not convert into a positive screen. The
next hypothesis must come from fresh replay causality and preserve existing
Store ownership; do not retry this support selector or widen the Store schema
without new evidence.
