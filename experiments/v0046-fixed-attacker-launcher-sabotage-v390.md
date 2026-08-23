# v390 Fixed-attacker Launcher sabotage — rejected

Date: 2026-08-21

## Objective and scope

Starting from immutable v0046, v390 tested whether the designated fixed
attacker should target an enemy Launcher as a high-value control denial after
the first forward Sentinel, rather than only targeting Harvesters, Conveyors,
and Splitters. Dynamic raiders retained their existing logistics-only target
pool. The temporary production edit was limited to
`bots/candidate/bot/attacker.py`, with focused coverage in
`tests/test_candidate_nearest_defense.py` and a temporary screen config.

## Validation

- Initial focused coverage was **33/33**, compileall passed, and smoke was
  **4/4** at `reports/local-20260821T004525Z`; static retained the inherited
  candidate import/assertion failures (`reports/iter-v390-launcher-sabotage/static.log`).
- The initial rotated all-map 30-game screen (`screen_seed=761`) was
  command/reliability-clean but only **16–14** against v0046. Collection was
  **151,080/166,770 Ti**, deliveries **30/29**, and max p99/peak was
  **1,390/5,415 us**, with zero TLE/suspicious rows. Raw games are at
  `reports/local-20260821T004552Z`; parsed evidence is
  `reports/iter-v390-launcher-sabotage/replay-analysis.json` and
  `summary.json`.
- Repair 1 reduced Launcher priority below loaded logistics. Focused coverage
  was **33/33** and compileall passed; its rotated screen (`screen_seed=769`)
  improved to **18–12**, with **156,540/138,530 Ti**, **30/30** deliveries,
  and max p99/peak **1,443/3,581 us**, still below the **19–11** promotion
  floor. Raw games are at `reports/local-20260821T005026Z`; parsed evidence is
  `repair-replay-analysis.json` and `repair-summary.json`.
- Repair 2 delayed Launcher detours until four completed routes. Focused
  coverage was **34/34** and compileall passed; its rotated screen
  (`screen_seed=773`) fell back to **16–14**, with **166,680/157,120 Ti**,
  **30/30** deliveries, and max p99/peak **1,426/5,692 us**, again with zero
  TLE/suspicious rows. Raw games are at `reports/local-20260821T005433Z`;
  parsed evidence is `repair2-replay-analysis.json` and `repair2-summary.json`.

## Decision and rollback

Reject v390 after the two bounded repairs: no screen cleared the 19–11 gate,
and the Launcher detour reduced early conversion on the initial screen. The
temporary code, focused tests, and config were removed. Rollback focused
coverage was **31/31**, compileall passed, smoke was **4/4** at
`reports/local-20260821T005947Z`, and recursive candidate parity with v0046 is
empty at `reports/iter-v390-launcher-sabotage/rollback-source-parity.diff`.
Rollback static retains the same inherited failures in
`reports/iter-v390-launcher-sabotage/rollback-static.log`. No promotion,
package, upload, activation, or live transition occurred.

## Remaining risk

Launcher denial remains a plausible late-game control tactic, but this direct
fixed-attacker diversion is not reliable enough for the current baseline.
Future experiments should preserve early logistics conversion and use replay
evidence to select a different pressure mechanism rather than reviving this
target ranking unchanged.
