# v181 verified conveyor-route join

## Objective

Test whether a Harvester chain could reduce conversion latency by joining a
visible friendly Conveyor path that was proven, by bounded forward inspection,
to reach our Core. Early routes retained direct-to-Core behavior in the first
repair after replay review showed that broad joins could enter scaffolding.

## Allowed files and non-goals

- Allowed: `bots/candidate/bot/defender.py`,
  `tests/test_candidate_nearest_defense.py`, this record, `UPDATES.md`, and
  durable state.
- Non-goals: no workforce thresholds, role/task gates, combat, ammo, unit
  costs, map branches, Store schema, baseline, package, or platform operation.

## Iteration evidence

- Initial bounded visible-route join passed focused **22/22**, compileall, and
  smoke **4/4**. The 18-game all-map screen regressed to **8-10**, collection
  **66,030 vs 80,180** (0.8235x), with one candidate no-delivery row; the
  candidate placed more Harvesters on average but fewer Sentinels
  (`reports/local-20260818T063536Z`, analysis
  `reports/iter-v181-verified-route-join-replay-analysis.json`).
- Repair 1 retained direct routing until three completed routes. Focused
  **23/23**, compileall, and smoke **4/4** passed. The screen remained **8-10**
  but collection became **83,570 vs 81,340** (1.0274x); one candidate
  no-delivery row remained and the Sentinel mean was still lower
  (`reports/local-20260818T063857Z`, analysis
  `reports/iter-v181-verified-route-join-repair1-replay-analysis.json`).
- Repair 2 capped joins at four conveyor hops. Focused **23/23**, compileall,
  and smoke **4/4** passed, but the screen fell to **7-11**, collection
  **64,060 vs 70,110** (0.9137x), with one candidate no-delivery row
  (`reports/local-20260818T064129Z`, analysis
  `reports/iter-v181-verified-route-join-repair2-replay-analysis.json`).

## Decision

Reject v181 after both bounded repairs. Neither the aggregate win rate nor
delivery reliability improved over v0040. The temporary source and test
changes were removed; recursive candidate-v0040 parity is **0 diff lines**
(`reports/iter-v181-rollback-source-diff.txt`). Rollback focused checks passed
**20/20**, compileall passed, and rollback smoke was **4/4**
(`reports/iter-v181-rollback-focused.log`,
`reports/local-20260818T064408Z`). No 60-game release, remote gate, package,
upload, activation, or baseline transition occurred.
