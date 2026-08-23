# v0040 shared Core intel — v168

Date: 2026-08-18

## Objective

Reduce the confirmed-Core delay visible in the v167 loss replays. The Store
contract says any unit that spots the enemy Core may publish `SLOT_ENEMY_CORE`,
but the current code only calls `_update_enemy_intel` from the fixed attacker.
Defender and Dynamic workers can therefore see the Core and continue their
normal task without giving the attack shell a confirmed target.

## Comparator and allowed files

- Comparator: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Source: `bots/candidate/bot/defender.py` and `bots/candidate/bot/dynamic.py`.
- Focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, reports, `UPDATES.md`, and durable project state.

## Non-goals

No Sentinel pool or placement geometry, route navigation/chain policy, Builder
spawn/role assignment, ore ranking, combat target selection, ammo, barriers,
Store schema, map-specific branch, baseline/archive, package, upload,
activation, or live-state change.

## Hypothesis and implementation

At the start of Defender and Dynamic turns, opportunistically invoke the
existing `_update_enemy_intel` method when the concrete Player provides it.
The helper remains a no-op for isolated mixin probes, and its existing
confirmed-sighting/store guards stay authoritative. This lets any visible
worker publish the same Core position before choosing or executing its task;
fixed attackers keep their current call and see no duplicate work.

## Done criteria

- Focused tests prove a Defender and Dynamic worker publish a visible enemy
  Core position and preserve the no-helper mixin behavior; existing role/route
  tests remain green.
- Candidate compileall passes; `make static` is checked and inherited failures
  are recorded; smoke is command-clean.
- The shortened 24-game all-map screen materially improves aggregate paired
  win rate over v0040 without systematic TLE/suspicious output or candidate
  delivery collapse. Only a qualifying screen advances to the 60-game gate.
- A failed screen or release requires exact v0040 rollback and no platform
  operation. Remote comparison is attempted only after a qualifying release.

## Validation and decision

The unguarded hook passed the final focused suite **27/27**, compileall, and
command-clean smoke (`reports/local-20260818T022804Z`); static retained the
inherited 15 obsolete-import errors plus two navigation assertions. Its
24-game screen was command-clean but collapsed to **5-19** versus v0040.
There were no candidate no-delivery, TLE, or suspicious-output games, but
candidate first delivery averaged **32.5** versus **25.7** turns, Harvesters
averaged **6.67** versus **8.25**, and Sentinels **2.54** versus **3.54**
(`reports/local-20260818T022819Z` and
`reports/iter-v168-shared-core-intel-screen-replay-analysis.json`). Replay
review shows that early publication changed remote-ore/advance decisions
before the economy was funded, so the nominal intel gain harmed the workforce.

Repair 1 gated publication on the existing three-route offense milestone.
Focused checks remained **27/27**, compileall passed, smoke was command-clean
(`reports/local-20260818T023201Z`), and static retained the same inherited
failures. The 24-game screen recovered to **12-12** with zero candidate
no-delivery games; candidate first delivery averaged **24.9** versus **42.1**
for the comparator and Sentinel counts **2.79** versus **2.75**, but the tie
did not qualify (`reports/local-20260818T023212Z` and
`reports/iter-v168-shared-core-intel-repair1-screen-replay-analysis.json`).

v168 is rejected after one bounded repair without a 60-game release, remote
comparison, package, upload, activation, or baseline transition. Both hooks,
imports, and tests were rolled back to exact recursive v0040 parity (**0 diff
lines**; `reports/iter-v168-shared-core-intel-rollback-source-diff.txt`).
Rollback focused checks passed **25/25**, compileall passed, and rollback
smoke was command-clean (`reports/local-20260818T023459Z`). Future confirmed
Core work must avoid changing early Defender economy decisions; the next
hypothesis should target a different pressure or route failure.
