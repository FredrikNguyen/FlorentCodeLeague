# v175 temporary second-wave economy anchor

## Objective

Keep the first Builder of the stage-2 wave on route work while the economy is
still small, then release it to the existing dynamic pressure pool. The
hypothesis came from the v174 server losses: the candidate often reached a
first delivery but ended with fewer Harvesters and less titanium than v0040.
This was a single designated Builder change, not a global low-liquidity guard.

## Allowed files

- `bots/candidate/main.py`
- `bots/candidate/bot/constants.py`
- `bots/candidate/bot/core_role.py`
- `bots/candidate/bot/attacker.py`
- `bots/candidate/bot/defender.py`
- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and durable project state

## Non-goals

No route geometry, navigation, ammo conversion, turret/Sentinel/Barrier/
Launcher policy, map-specific branch, baseline/archive, package, upload,
activation, or live-state change.

## Evidence

- Initial implementation kept the stage-2 slot as an economy anchor from the
  first completed route through four routes and removed that slot from fixed
  attacker claims. Focused checks were **21/21**, compileall passed, static
  retained the inherited 15 obsolete-import errors and two navigation
  assertions, and smoke was **4/4**. The shortened 21-game all-map screen was
  **8-13** versus v0040, with zero delivery failures and max p99/peak
  **1,445/5,190 us**; collection was **124,840 vs 144,500**.
  Reports: `reports/local-20260818T043505Z` and
  `reports/iter-v175-economy-anchor-screen-replay-analysis.json`.
- Repair 1 released the anchor after three completed routes. Focused checks
  remained **21/21**, compileall passed, static retained the same inherited
  failures, and smoke was **4/4**. The screen fell to **7-14**, included one
  candidate no-delivery row, and collected **120,390 vs 146,750**; max
  p99/peak was **1,429/2,455 us**. Reports:
  `reports/local-20260818T043909Z` and
  `reports/iter-v175-economy-anchor-repair1-screen-replay-analysis.json`.

## Decision and rollback

v175 is **rejected** after two bounded screen attempts. The anchor did not
convert the remote workforce deficit into a local edge and reduced paired
wins/collection. No 60-game release gate, remote comparison, package, upload,
activation, or baseline transition was justified. All temporary source and
test edits were removed with `apply_patch`; recursive candidate-versus-v0040
source diff is **0 lines** (`reports/iter-v175-economy-anchor-rollback-source-diff.txt`).
Rollback focused checks passed **20/20**, compileall passed, and rollback smoke
was **4/4** (`reports/local-20260818T044311Z`).
