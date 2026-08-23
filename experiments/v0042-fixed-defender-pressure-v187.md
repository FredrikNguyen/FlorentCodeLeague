# v187 fixed-defender pressure handoff — rejected 2026-08-18

## Objective

After five completed routes, release the permanent economy defender to the
attacker lane only when it had no visible or advertised ore, no visible home
threat, no active chain, and no current home-Gunner assignment. The goal was
to convert an otherwise idle economy-floor Builder into the offensive
barrier/Sentinel/sabotage policy already used by fixed attackers.

## Scope and non-goals

- Temporary source scope was `bots/candidate/main.py` plus one focused test;
  `configs/eval_regression.toml` rotated the deterministic screen seed for
  each map-complete screen.
- The handoff did not change route construction, fixed-attacker behavior,
  combat constants, Launcher/Splitter policy, baseline snapshots, packaging,
  upload, activation, or live state.

## Validation

- Initial focused checks were **26/26**, candidate compileall passed, and
  smoke was **4/4 command-clean**. `make static` retained only the inherited
  15 obsolete-module import errors and two navigation fast-path assertions.
- Screen seed **154**: **10-5** candidate wins, 15/15 command-clean;
  candidate/baseline collected **69,160/72,000 Ti**. Replay analysis found no
  TLE or suspicious output. Report: `reports/local-20260818T091314Z`;
  analysis: `reports/iter-v187-defender-pressure/replay-analysis.jsonl`.
- Rotated screen seed **155** reversed to **7-8**, 15/15 command-clean, with
  **58,380/68,220 Ti**. Report: `reports/local-20260818T091550Z`;
  analysis: `reports/iter-v187-defender-pressure/replay-analysis-rotated.json`.
- Repair 1 added a dynamic 400-Ti-class bank requirement (or the current
  Harvester plus attack reserve) before handoff, guarding against a high
  lifetime route counter with a depleted active economy. Focused/compile/smoke
  stayed **26/26**, clean, and **4/4**; static remained the inherited exit 2.
- Repair 1 screen seed **156**: **5-10**, 15/15 command-clean, with
  **50,660/66,180 Ti**. Report: `reports/local-20260818T091925Z`.

## Decision and rollback

The initial edge did not transfer to seed 155, and the resource-backed repair
was decisively worse on seed 156. Reject after one bounded repair. The
temporary handoff and focused test were removed; candidate `main.py` is
byte-identical to immutable v0042. Rollback focused checks were **28/28**,
compileall passed, and rollback smoke was **4/4**:

- `reports/iter-v187-defender-pressure/rollback-focused.log`
- `reports/iter-v187-defender-pressure/rollback-compileall.log`
- `reports/iter-v187-defender-pressure/rollback-smoke.log`

No release gate, package, remote gate, upload, activation, or baseline
transition occurred. The reduced routine screen remains 15 map-complete games;
the release gate remains 60 games. Platform v105 is still active-observing
with v101 retained as the last-known-good rollback.
