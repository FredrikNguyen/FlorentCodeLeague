# v0029 dynamic logistics raid

## Objective

Convert surplus resources into offense without pulling the opening economy off
its route. After three completed harvester chains, the nearest dynamic builder
may claim one visible enemy harvester, splitter, or conveyor and use the
existing cardinal approach/builder-fire primitive. The fixed 80-Ti reserve
blocks raids below the economy floor. Stale targets are dropped when vision
confirms they are gone, friendly, or no longer logistics.

## Evidence and review

- Live/top replay evidence: `reports/live-v94-strategy-analysis.txt` and
  `reports/top-live-strategy-summary.txt`.
- Candidate source delta is limited to `bot/attacker.py`, `bot/dynamic.py`,
  and the task constants; no immutable snapshot or baseline was edited.
- Focused tests: 21 passed (`tests.test_candidate_nearest_defense`,
  `tests.test_analyze_replay`, `tests.test_static_contract`,
  `tests.test_startup_context`).
- Compileall and `git diff --check`: passed.
- `make smoke`: passed, 4/4, report
  `reports/local-20260812T211302Z`.
- `make static`: failed in the pre-existing obsolete test imports (15 errors;
  e.g. removed `bots.candidate.bot.economy`, `comms`, `builder`, `policy`, and
  old `Navigator` APIs), log `reports/v0029-dynamic-logistics-raid-static.log`.

## Protected comparison

Candidate versus immutable v0024
(`bots/versions/v0024_bootstrap-deterministic-frontier_20260812-1939_eeafad8f`):

- Full 21-map / 5-seed gate: 128-82, zero command failures, report
  `reports/local-20260812T205222Z`.
- v0024 previous sabotage candidate (v0028) was 110-100 on the same gate.
- Candidate map wins: atoll 5-5, aurora 6-4, bridge 4-6, crossfire 6-4,
  duel 8-2, fjord 4-6, hive 6-4, jackpot 6-4, longship 4-6, pinch 6-4,
  quarry 5-5, runestone 8-2, showdown 7-3, skerry 9-1, sprint 6-4,
  strait 6-4, string 7-3, sweden 7-3, twins 5-5, vase 4-6, vault 9-1.
- Candidate averages: 7.66 builders, 7.05 harvesters, 57.39 conveyors,
  2.59 gunners, 7.00 sentinels, 0.15 barriers, 4,351 Ti collected.
  First delivery averaged turn 62 with 9 missing deliveries; v0024 averaged
  turn 39 with 4 missing. This is the primary remaining risk.
- Reliability: no command failures; maximum analyzed p99 bot time 1,371 us.
- Platform verification: downloading v96 produced `artifacts/platform/v96-v0029/submission.zip` (189,117 unpacked bytes); its extracted source is byte-identical to the immutable v0025 snapshot. Download log: `reports/download-v96.log`.

## Status

Accepted as the current local best for packaging, with v94 retained as the
live rollback. Do not call this a live-performance improvement until a new
ladder series using the package is observed.
