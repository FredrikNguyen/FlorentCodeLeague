# v171 guarded idle-Harvester chain handoff

## Objective

Repair one early idle path without repeating v164's unconditional change. When
fewer than three completed routes exist and an otherwise idle Builder is
standing beside eligible ore, reuse `_try_build_harvester` so the new source
enters the normal `MODE_CHAIN` route state. Once the economy gate reaches three
routes, retain the shipped direct fallback exactly.

The v0040 fallback can build a Harvester but return without initializing a
conveyor chain. That creates a nominal producer with no path and consumes the
same opening capital needed for connected economy. v164 fixed this for every
phase but lost the guarded remote comparison; v171 isolates the early failure
mode only.

## Comparator and allowed files

- Comparator: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Source: `bots/candidate/main.py`.
- Focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, `UPDATES.md`, and durable project state.

## Non-goals

No route geometry/slack, workforce target, role/task order, combat, Sentinel,
Gunner, Launcher, Barrier, cost/reserve, Store schema, map branch,
baseline/archive, package, upload, activation, or live-state change.

## Implementation

- Import the existing `ECONOMY_PRIORITY_CHAINS` threshold in `main.py`.
- In `_idle_fallback`, call `_try_build_harvester` before the duplicated bare-
  ore fallback only while the completed-route count is below that threshold.
- Preserve the existing direct bare-ore fallback at and above three routes.
- Add a focused test that loads the submission entry point, invokes the idle
  fallback on adjacent ore, and proves `MODE_CHAIN` and route state initialize.

## Done criteria

- Focused tests and compileall pass; `make static` is checked and inherited
  failures are recorded; smoke is command-clean.
- The 21-game all-map screen improves aggregate paired win rate over v0040
  with no candidate no-delivery, command, TLE, or suspicious-output failures.
- Only a materially positive screen advances to the 60-game release gate; a
  tie/regression or reliability/delivery failure requires exact v0040 rollback.
- Self-review confirms the post-three-route fallback remains unchanged.

## Evidence

- Focused checks passed **21/21** in
  `reports/iter-v171-guarded-idle-harvester-chain-focused.log`; compileall
  passed; smoke was **4/4** in `reports/local-20260818T031318Z`.
- `make static` was checked and retained the inherited 15 obsolete-import
  errors plus two navigation fast-path assertions in
  `reports/iter-v171-guarded-idle-harvester-chain-static.log`.
- The rotated 21-game all-map screen was command-clean, but the candidate
  lost **9-12** to v0040. It had lower mean final resources (**3,170 vs
  3,976**) and fewer living Harvesters (**6.10 vs 7.57**); mean first delivery
  was effectively level (**22.9 vs 23.4**), with no command, TLE, or
  suspicious-output failures. Replay metrics are in
  `reports/local-20260818T031345Z` and
  `reports/iter-v171-guarded-idle-harvester-chain-screen-replay-analysis.json`.

## Decision

Rejected at the quick screen. The early chain handoff did not improve
conversion and reduced workforce/resources, so no repair or 60-game gate was
justified. The guarded import, branch, and focused test were removed; the
candidate now has exact recursive v0040 parity (**0 diff lines**) recorded in
`reports/iter-v171-guarded-idle-harvester-chain-rollback-source-diff.txt`.
Rollback focused checks passed **20/20**, compileall passed, and rollback smoke
was **4/4** in `reports/local-20260818T031703Z`. No package, release, remote
match, upload, activation, or baseline transition occurred.
