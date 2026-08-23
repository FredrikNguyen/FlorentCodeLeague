# v177 enemy-logistics breadcrumb scout

## Objective

Improve Core confirmation on maps where the fixed attacker follows a wrong
180-degree mirror guess and never places a forward Sentinel. When a visible
enemy logistics target was closer than that guess, the attacker would use only
movement to approach it and reveal more terrain; it would not fire, build,
raid, or alter economy/workforce policy.

## Allowed files

- `bots/candidate/bot/attacker.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and durable project state

## Non-goals

No resource spending, route geometry, workforce/timing, Sentinel/Barrier/
Launcher policy, Store schema, map-specific branch, baseline/archive,
package, upload, activation, or live-state change.

## Evidence

- Initial v177 followed the nearest visible enemy Harvester/Conveyor/Splitter
  as a movement-only breadcrumb when it was closer than the mirror guess.
  Focused checks were **22/22**, compileall passed, smoke was **4/4**, and
  static retained the inherited 15 obsolete-import errors plus two navigation
  fast-path assertions. The 21-game screen regressed to **9-12**, collection
  **89,170 vs 98,320**, with zero no-delivery rows; max p99/peak was
  **1,461/2,980 us**. Reports: `reports/local-20260818T051245Z` and
  `reports/iter-v177-logistics-breadcrumb-screen-replay-analysis.json`.
- Repair 1 restricted the breadcrumb to a visible enemy Harvester source and
  added a belt-only negative test. Focused checks were **23/23**, compileall
  passed, smoke was **4/4**, and static retained the same inherited failures.
  The screen reached **10-11**, collection **107,350 vs 119,980**, with zero
  candidate no-delivery rows versus one for v0040; max p99/peak was
  **1,455/2,217 us**. Reports: `reports/local-20260818T051621Z` and
  `reports/iter-v177-logistics-breadcrumb-repair1-screen-replay-analysis.json`.

## Decision and rollback

v177 is **rejected** after both bounded screens. The movement-only scout did
not produce a material paired win edge or collection improvement. The source
and tests were removed with `apply_patch`; recursive candidate-versus-v0040
source parity is **0 diff lines** at
`reports/iter-v177-logistics-breadcrumb-rollback-source-diff.txt`. Rollback
focused checks passed **20/20**, compileall passed, and rollback smoke was
**4/4** (`reports/local-20260818T051939Z`). No 60-game release gate, remote
gate, package, upload, activation, or baseline transition occurred.
