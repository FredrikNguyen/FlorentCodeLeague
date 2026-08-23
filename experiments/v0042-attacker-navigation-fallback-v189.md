# v189 failed-attacker-navigation fallback

## Objective

When a fixed attacker cannot advance toward the enemy Core under the current
danger map, fall through to its existing action/reposition fallback instead of
returning a ready turn idle. Successful direct navigation and all economy,
Sentinel, barrier, and sabotage gates remain unchanged.

## Scope and non-goals

- Temporary source: `bots/candidate/bot/attacker.py`.
- Focused coverage: `tests/test_candidate_attacker_navigation_fallback.py`.
- Screen schedule: `configs/eval_regression.toml` rotated to seed 158; the
  15-game all-map quick gate remains the minimum complete-map screen.
- No changes to economy, route construction, workforce, turret/ammo policy,
  Launcher/Splitter behavior, baseline snapshots, package, or live state.

## Validation

- Focused branch plus cage coverage: **8/8**; compileall passed
  (`reports/iter-v189-attacker-navigation/focused-retry.log`,
  `reports/iter-v189-attacker-navigation/compileall.log`).
- `make smoke`: **4/4** command-clean
  (`reports/iter-v189-attacker-navigation/smoke.log`).
- `make static`: inherited repository failures only: 15 obsolete-module import
  errors and two navigation fast-path assertions; no v189-specific failure
  (`reports/iter-v189-attacker-navigation/static.log`).
- Seed 157 screen: **8-7** candidate wins, 15/15 command-clean, no TLE or
  suspicious output (`reports/local-20260818T094342Z`, replay analysis in
  `reports/iter-v189-attacker-navigation/replay-analysis.json`).
- Rotated seed 158 screen: **7-8** candidate wins, 15/15 command-clean, no
  TLE or suspicious output (`reports/local-20260818T094537Z`, replay analysis
  in `reports/iter-v189-attacker-navigation/replay-analysis-rotated.json`).

## Decision and rollback

The first narrow edge reversed on the independent rotated screen, so v189 did
not show a reliable aggregate improvement and did not earn the 60-game release
gate. The temporary source and test were removed; `attacker.py` is byte-
identical to immutable v0042 and the candidate tree has no source difference.
Rollback focused coverage passed, compileall passed, static retained only the
known inherited failures, and rollback smoke was **4/4**:

- `reports/iter-v189-attacker-navigation/rollback-focused.log`
- `reports/iter-v189-attacker-navigation/rollback-compileall.log`
- `reports/iter-v189-attacker-navigation/rollback-static.log`
- `reports/iter-v189-attacker-navigation/rollback-smoke.log`

No release matrix, package, remote gate, upload, activation, or baseline
transition was performed.
