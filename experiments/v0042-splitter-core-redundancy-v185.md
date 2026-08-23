# v185 mature-route Splitter core-ring redundancy — rejected 2026-08-18

## Objective

Test whether a Splitter at a verified Core-ring gap can preserve delivery
through a second Core-facing branch after a route cut, without changing the
opening economy, workforce, combat, navigation, or live deployment.

## Allowed files and non-goals

- Temporary candidate files: `bots/candidate/main.py`,
  `bots/candidate/bot/constants.py`, `bots/candidate/bot/defender.py`, and one
  focused `tests/test_candidate_splitter_redundancy.py`.
- The action was gated to three completed routes, a dynamic Splitter plus
  Harvester reserve, one nearby junction maximum, an upstream Conveyor facing
  into an empty Core-ring gap, and either an existing or buildable
  Core-facing side branch.
- No baseline snapshot, evaluation policy, package, upload, activation, or
  live state was changed.

## Evidence

- Initial implementation focused tests passed **30/30**, compileall passed,
  smoke was **4/4**, and static retained the inherited 15 obsolete-import
  errors plus two navigation assertions. The 15-game screen was **8-7**,
  command-clean on all maps; only two candidate Splitters were placed.
  Reports: `reports/iter-v185-splitter-focused.log`,
  `reports/iter-v185-splitter-compileall.log`,
  `reports/iter-v185-splitter-static.log`,
  `reports/iter-v185-splitter-smoke.log`,
  `reports/local-20260818T083022Z`, and
  `reports/iter-v185-splitter-screen-analysis.json`.
- Repair 1 allowed one empty Core-facing side branch to be completed after the
  junction. Focused tests passed **31/31**, compileall passed, smoke was
  **4/4**, static remained inherited-red, and the 15-game screen was **9-6**
  with zero command/TLE/suspicious rows but no candidate Splitter placements.
  The required 60-game release gate was **32-28 (53.33%)**, zero
  no-delivery/TLE/suspicious rows, max p99/peak **1,407/5,101 us**, with weak
  1-3 floors on Antler, Archipelago, and Icefloe. Reports:
  `reports/iter-v185-splitter-repair1-focused.log`,
  `reports/iter-v185-splitter-repair1-compileall.log`,
  `reports/iter-v185-splitter-repair1-static.log`,
  `reports/iter-v185-splitter-repair1-smoke.log`,
  `reports/local-20260818T083417Z`,
  `reports/iter-v185-splitter-repair1-screen-analysis.json`,
  `reports/local-20260818T083616Z`, and
  `reports/iter-v185-splitter-repair1-release-analysis.json`.
- Repair 2 lowered only the surplus reserve from 80 to 30 while retaining
  dynamic costs and all topology guards. Focused tests passed **31/31**,
  compileall passed, smoke was **4/4**, static remained inherited-red, and the
  15-game screen regressed to **7-8**, including one candidate no-delivery row.
  It placed four Splitters and collected **51,220 vs 56,600 Ti**. Reports:
  `reports/iter-v185-splitter-repair2-focused.log`,
  `reports/iter-v185-splitter-repair2-compileall.log`,
  `reports/iter-v185-splitter-repair2-static.log`,
  `reports/iter-v185-splitter-repair2-smoke.log`,
  `reports/local-20260818T084335Z`, and
  `reports/iter-v185-splitter-repair2-screen-analysis.json`.

## Decision and rollback

v185 is **rejected**. Neither the initial screen nor the repair-1 release
produced a material, reliable edge over v0042; repair 2 regressed and caused a
no-delivery game. All temporary candidate code and tests were removed. The
candidate's `main.py`, `bot/constants.py`, and `bot/defender.py` now have zero
diff lines against immutable v0042. Rollback focused checks passed **33/33**,
compileall passed, rollback smoke was **4/4**, and static remains the same
inherited exit 2. Rollback evidence:
`reports/iter-v185-splitter-rollback-focused.log`,
`reports/iter-v185-splitter-rollback-compileall.log`,
`reports/iter-v185-splitter-rollback-static.log`, and
`reports/iter-v185-splitter-rollback-smoke.log`.
