# v178 reactive home-Builder blocker

## Objective

Stop a dynamic responder from idling when `_find_home_threat` selects an enemy
Builder, because Builder-vs-Builder fire is illegal. The intended response was
to keep the threat local to the Core, use a bounded Barrier only when it was
safe and reserve-funded, and otherwise choose a legal movement fallback.

## Allowed files

- `bots/candidate/bot/constants.py`
- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and durable project state

## Non-goals

No route geometry, harvester/workforce policy, Sentinel or Gunner policy,
Launcher/teleport policy, Store schema, map-specific branch, baseline/archive,
package, upload, activation, or live-state change.

## Evidence

- Initial blocker variant passed focused checks **22/22**, compileall, and smoke
  **4/4**; `make static` retained the inherited 15 obsolete-import errors and
  two navigation assertions. The 21-game all-map screen regressed to **7-14**
  versus v0040, collection **84,480 vs 108,260** (0.7803x), with zero command
  failures/no-delivery rows and max p99/peak **1,614/3,364 us**. Replay
  analysis: `reports/local-20260818T052427Z` and
  `reports/iter-v178-home-builder-blocker-screen-replay-analysis.json`.
- Baseline-vs-itself control on the same 21-game schedule was **11-10** with
  collection **105,260 vs 111,360**; this confirms the v178 regression was not
  just side-order noise (`reports/local-20260818T053049Z`, analysis
  `reports/iter-v178-baseline-self-screen-replay-analysis.json`).
- Repair 1 narrowed the paid blocker to one site per Builder and the Core
  perimeter. It passed focused **22/22**, compileall, and smoke **4/4**; the
  screen improved to **10-11**, collection **71,610 vs 82,720** (0.8657x),
  still not a material edge. Reports: `reports/local-20260818T053410Z` and
  `reports/iter-v178-repair1-screen-replay-analysis.json`.
- Repair 2 removed the paid Barrier and retained only a movement handoff for
  an adjacent Core-perimeter intruder. It passed focused **22/22**, compileall,
  and smoke **4/4**; the screen reached **11-10**, collection **100,300 vs
  97,560** (1.0281x), max p99/peak **1,320/2,625 us**, but this only matched
  the baseline self-control and was not a significant paired improvement.
  Reports: `reports/local-20260818T053722Z` and
  `reports/iter-v178-repair2-screen-replay-analysis.json`.

## Decision and rollback

v178 is **rejected** after the initial screen and both bounded repairs. The
repair-2 edge is not material and did not justify a 60-game release gate. The
temporary dynamic logic and tests were removed with `apply_patch`; recursive
candidate-versus-v0040 source parity is **0 diff lines** at
`reports/iter-v178-rollback-source-diff.txt`. Rollback focused checks passed
**20/20**, compileall passed, and rollback smoke was **4/4**
(`reports/local-20260818T054043Z`). No release, remote gate, package, upload,
activation, or baseline transition occurred.
