# v0040 Harvester route-progress marker — v151

Date: 2026-08-17

## Objective

Use a bounded visible sink/progress check when an opening Harvester already
has an apparently accepting Conveyor. The live-loss review suggested that a
Conveyor pointing into a short loop or dead building can make an abandoned
source look connected, preventing local recovery. The check was intentionally
limited to `SLOT_HARVESTER_COUNT == 0` and returned unknown outside vision.

## Allowed scope and non-goals

Allowed files were `bots/candidate/bot/defender.py` and focused coverage in
`tests/test_candidate_nearest_defense.py`. Economy thresholds, ordinary chain
facing, navigation, combat, workforce, Store layout, map selection, and
platform state were non-goals. All comparisons used immutable
`bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.

## Screen and repair attempts

1. Initial bounded sink verification followed visible Conveyor outputs for up
   to 32 nodes, treating definite loops/non-accepting buildings/gaps as
   abandoned and unseen paths as unknown. Focused **21/21**, compileall passed,
   smoke **4/4**, static retained inherited failures. The 54-game screen was
   **31-23** against v0040, with zero command failures/stderr and no candidate
   no-delivery rows (`reports/local-20260817T194541Z`, analysis
   `reports/iter-v151-harvester-route-progress-marker/screen-analysis.json`).
2. Repair 1 preserved an active visible gap when a friendly Builder was next
   to it. Focused **22/22**, compileall passed, smoke **4/4**; screen **30-24**
   (`reports/local-20260817T195332Z`).
3. Repair 2 treated every visible gap as unknown while retaining definite loop
   checks. Focused **22/22**, compileall passed, smoke **4/4**; screen **27-27**
   (`reports/local-20260817T195957Z`).

The initial 31-23 variant was the strongest screen candidate and was restored
for the long gate. The screen's positive aggregate was not treated as enough
to release without the long comparison.

## Long gate

The 210-game matrix completed command-clean against v0040 but scored **99-111**
for the candidate (−12 games). Candidate no-delivery was **3** versus
comparator **4**; replay reliability had zero TLEs and suspicious outputs,
maximum p99 callback **1,476 us**, and maximum peak **6,099 us**. Full report:
`reports/local-20260817T200602Z`; replay diagnostics:
`reports/iter-v151-harvester-route-progress-marker/long-analysis.json`.

## Decision

v151 is **rejected at the long gate** despite its 54-game screen win. No
package, upload, activation, archive, or baseline transition was performed.
The candidate and focused tests were restored byte-identically to v0040;
rollback focused **20/20**, compileall passed, rollback smoke **4/4**
(`reports/local-20260817T202833Z`).

## Next risk

The screen/long divergence shows that local opening sink verification is too
myopic. The next iteration should use a different bounded route-progress or
resource-conversion hypothesis and must start from v0040, with direct paired
win rate against that baseline as the primary promotion metric.
