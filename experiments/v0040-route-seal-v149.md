# v0040 route-seal audit — v149

Date: 2026-08-17

## Objective

Use the Glacierkeep seed-149 no-delivery replay to make opening conveyor
repairs recognize directed cycles longer than the existing mutual two-cycle
check.

## Allowed scope and non-goals

The candidate scope was `bots/candidate/bot/defender.py`,
`bots/candidate/bot/dynamic.py`, and focused tests. The two bounded attempts
did not alter economy thresholds, navigation, combat, workforce, Store layout,
or platform state. The candidate always remained compared with immutable
`v0040_shared-route-progress_20260817-1853_eeafad8f`.

## Attempts

1. Add a bounded visible-conveyor cycle walk (64 nodes) to
   `_belt_output_status` while `SLOT_HARVESTER_COUNT == 0`. Focused tests
   passed 22/22, compileall passed, static retained the inherited failures,
   smoke was 4/4 (`reports/iter-v149-route-seal/`). The 54-game screen was
   **25-29**, with one candidate no-delivery row, zero command failures/TLEs,
   and max p99 1.507 ms (`reports/local-20260817T190156Z`, analysis
   `reports/iter-v149-route-seal/screen-replay-analysis.json`).
2. Restrict cycle detection to dynamic belt-gap selection, keeping immediate
   defender repairs unchanged. Focused 22/22, compileall, and smoke 4/4
   remained clean; the screen improved to **28-26** but still failed to beat
   v0040. Candidate no-delivery rose to three rows; reliability remained
   command-clean with max p99 1.473 ms (`reports/local-20260817T191038Z`,
   analysis `reports/iter-v149-route-seal/repair1-replay-analysis.json`).

## Live evidence reviewed

Downloaded v102 losses against Atlas v76, TRRR v40, and Landers v93. The
current platform bot showed zero delivery in the latest Atlas loss, 2–7
Harvesters and 25–102 conveyors in other losses, and repeated TRRR TLEs; the
opponents reached delivery earlier and converted more resources. Raw replay
analysis is `reports/iter-v149-route-seal/live-replay-analysis.json` and the
downloaded files are under `reports/live-v102-replays/`.

## Decision

After the two permitted bounded repairs, v149 is **rejected** and all source
changes are rolled back. Candidate Python is byte-identical to v0040. Rollback
focused tests are 20/20, compileall passes, and rollback smoke is 4/4
(`reports/local-20260817T191654Z`). No v149 package, upload, activation, or
baseline transition occurred.

## Next risk

The remaining failure is not safely addressed by a global cycle classifier.
Next iteration should use a single Harvester-owned route-progress or sink
verification action, bounded to the first route, and must start from v0040.
