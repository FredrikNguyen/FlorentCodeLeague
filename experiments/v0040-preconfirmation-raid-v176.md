# v176 pre-confirmation loaded-logistics raid

## Objective

Give the fixed attacker one bounded early job when the enemy Core has not yet
been confirmed: destroy a visible enemy Conveyor/Splitter carrying a resource
stack before returning to the direct pressure lane. The intent was to convert
surplus resources into early sabotage without adding an economy handoff,
changing route construction, or changing Sentinel/spawn policy.

## Allowed files

- `bots/candidate/bot/attacker.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and durable project state

## Non-goals

No Harvester targeting in the repaired variant, route geometry or workforce
changes, map-specific branch, new global Store protocol, Sentinel/Barrier/
Launcher policy, baseline/archive, package, upload, activation, or live-state
change.

## Evidence

- Initial v176 allowed a visible enemy Harvester or loaded Conveyor/Splitter
  before Core confirmation. Focused checks were **22/22**, compileall passed,
  smoke was **4/4**, and static retained the inherited 15 obsolete-import
  errors plus two navigation fast-path assertions. The 21-game all-map screen
  regressed to **5-16**, with one candidate no-delivery row and collection
  **56,780 vs 92,220**. Replay reliability was clean (max p99/peak
  **1,410/5,190 us**). Reports: `reports/local-20260818T045041Z` and
  `reports/iter-v176-preconfirmation-raid-screen-replay-analysis.json`.
- Repair 1 restricted the pulse to loaded Conveyor/Splitter tiles and added a
  Harvester-skip regression test. Focused checks were **23/23**, compileall
  passed, smoke was **4/4**, and static retained the same inherited failures.
  The 21-game screen recovered to **12-9**, with zero no-delivery rows and
  collection **127,260 vs 122,410**; max p99/peak was **1,439/5,098 us**.
  Reports: `reports/local-20260818T045415Z` and
  `reports/iter-v176-preconfirmation-raid-repair1-screen-replay-analysis.json`.
- The required 60-game release gate then regressed to **29-31**, collection
  **274,290 vs 317,820** (ratio **0.863**), and one candidate no-delivery row.
  All commands were clean with zero TLE/suspicious-output rows; max p99/peak
  was **1,503/4,723 us**. Reports: `reports/local-20260818T045802Z` and
  `reports/iter-v176-preconfirmation-raid-repair1-release-replay-analysis.json`.

## Decision and rollback

v176 is **rejected** after the release gate. The early visible-belt pulse did
not transfer from the short screen to the full seed/side matrix. Both source
and tests were removed with `apply_patch`; candidate-versus-v0040 recursive
source parity is **0 diff lines** at
`reports/iter-v176-preconfirmation-raid-rollback-source-diff.txt`. Rollback
focused checks passed **20/20**, compileall passed, and rollback smoke was
**4/4** (`reports/local-20260818T050521Z`). No package, upload, activation,
remote gate, or baseline transition occurred.
