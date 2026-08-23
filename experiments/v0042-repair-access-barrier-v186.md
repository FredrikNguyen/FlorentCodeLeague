# v186 targeted enemy-Core repair-access barriers — rejected 2026-08-18

## Objective

Use the existing confirmed-Core barrier cage more deliberately: when an enemy
Builder was visible near the enemy Core, rank legal cage sites by Core repair
ring membership and adjacency to that Builder. Keep the existing six-site cap,
Sentinel-first order, Harvester reserve, belt-safety check, and escape guard.

## Scope and non-goals

- Changed only `bots/candidate/bot/attacker.py` and one focused cage fixture;
  `configs/eval_regression.toml` rotated `screen_seed` from 153 to 154 for the
  second screen.
- No Launcher, route/economy, Sentinel timing, home defense, navigation, Store,
  baseline, package, upload, or live-state change was retained.

## Validation

- Focused cage/nearest-defense tests: **29/29**; candidate compileall passed.
  Initial logs: `reports/iter-v186-repair-access/focused.log` and
  `reports/iter-v186-repair-access/compileall.log`.
- `make static` reproduced only the inherited 15 obsolete-module import
  errors and two navigation fast-path assertions; no v186-specific failure.
  Log: `reports/iter-v186-repair-access/static.log`.
- Smoke was **4/4 command-clean** before and after rollback. Logs:
  `reports/iter-v186-repair-access/smoke.log` and
  `reports/iter-v186-repair-access/rollback-smoke.log`.
- Screen with `screen_seed=153`: **8-7** candidate wins, 15/15 command-clean;
  candidate collected **72,390** versus **63,990** titanium, with no command,
  TLE, or suspicious-output rows. Report: `reports/local-20260818T085825Z`.
- Rotated screen with `screen_seed=154`: **6-9** candidate wins, 15/15
  command-clean; candidate collected **39,170** versus **58,300** titanium,
  again with no command, TLE, or suspicious-output rows. Report:
  `reports/local-20260818T090058Z`.

## Decision and rollback

The first one-game edge did not transfer to the rotated seed, so the hypothesis
is **rejected** without a 60-game release gate. The temporary ranking and test
were removed; candidate `attacker.py` and `constants.py` are byte-identical to
immutable v0042. Rollback focused tests passed, compileall passed, and rollback
smoke was 4/4 (`reports/iter-v186-repair-access/rollback-focused.log`,
`reports/iter-v186-repair-access/rollback-compileall.log`). No package, remote
gate, upload, activation, or baseline transition occurred.

Remaining risks: platform v105 still has no v105-specific rated observation;
the accepted baseline's local map-floor weaknesses remain; static remains red
from inherited legacy tests. The repair-access ranking must not be reintroduced
without new causal evidence.
