# v182 home-economy scout

## Objective

Keep one deterministic, nearest non-fixed dynamic Builder in the Core
neighborhood on the harvest/exploration loop after the three-route milestone,
so a quiet home pool does not convert entirely into forward pressure. The
second repair made the scout conditional on visible home Harvester health.

## Allowed files and non-goals

- Allowed: `bots/candidate/bot/dynamic.py`,
  `tests/test_candidate_nearest_defense.py`, this record, `UPDATES.md`, and
  durable state.
- Non-goals: no route FSM, conveyor geometry, workforce spawn target, Store
  schema, combat, ammo, cost, map branch, baseline, or platform operation.

## Iteration evidence

- Initial scout passed focused **22/22**, compileall, and smoke **4/4**. The
  18-game all-map screen reached **12-6**, collection **64,180 vs 67,110**
  (0.9563x), with zero candidate no-delivery rows; mean placed Harvesters
  were **8.00 vs 7.28**. It advanced to the 60-game gate
  (`reports/local-20260818T064845Z`, analysis
  `reports/iter-v182-home-economy-scout-replay-analysis.json`).
- The 60-game release gate was command-clean and scored **30-30**, collection
  **321,370 vs 316,160** (1.0165x), with one candidate no-delivery row, max
  p99/peak **1,495/5,001 us**, and weak floors on Glacierkeep **0-4**,
  Icefloe **0-4**, Nordkap **1-3**, and Frostgate **1-3**
  (`reports/local-20260818T065043Z`, analysis
  `reports/iter-v182-home-economy-scout-release60-replay-analysis.json`).
- Repair 1 disabled the scout on cramped maps. Focused **23/23**, compileall,
  and smoke **4/4** passed; the screen fell to **8-10**, collection
  **72,430 vs 73,540** (0.9849x), with one candidate no-delivery row
  (`reports/local-20260818T065835Z`, analysis
  `reports/iter-v182-home-economy-scout-repair1-replay-analysis.json`).
- Repair 2 retained the scout only while fewer than three home Harvesters were
  visible. Focused **24/24**, compileall, and smoke **4/4** passed; the screen
  was **8-10**, collection **72,680 vs 78,210** (0.9293x), with no candidate
  no-delivery rows (`reports/local-20260818T070148Z`, analysis
  `reports/iter-v182-home-economy-scout-repair2-replay-analysis.json`).

## Decision

Reject v182 after the tied release gate and two failed repairs. The temporary
scout logic/tests were removed; recursive candidate-v0040 parity is **0 diff
lines** (`reports/iter-v182-rollback-source-diff.txt`). Rollback focused tests
passed **20/20**, compileall passed, and rollback smoke was **4/4**
(`reports/local-20260818T070441Z`). No remote gate, package, upload,
activation, or baseline transition occurred.
