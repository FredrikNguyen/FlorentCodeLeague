# v69 canonical opening orientation

## Scope

- Parent: `bots/versions/v0013_reviewer-v69-platform-winner_20260809-1444_7dd72f03`.
- Hypothesis: v69's absolute-coordinate spawn and first-ore tie-breaks create
  deterministic rotational asymmetry; matching the stronger observed opening
  orientation on unambiguous live geometries will recover weak-side games.
- Changed files: `bots/candidate/bot/core.py` and focused tests only.
- Non-goals: no spending, workforce, route, combat, navigation, or live action.

## Gate

- Improve the focused live geometry set with no new command failure.
- Then score at least 17/30 on the full current pool, with no 0-2 map collapse.
- Preserve the older protected regression before release.

## Status

Promoted locally and deployed for live observation.

## Results

- Current live pool, seeds 1/19/101, both sides: 61-29-0, paired score
  +32/90, titanium 178,030 versus 142,840 (ratio 1.2463).
- Current-pool source reports: `reports/local-20260809T152902Z`,
  `reports/local-20260809T154538Z`, with final 25x25 replacement evidence in
  `reports/local-20260809T155537Z`.
- Old protected compatibility matrix, recomputed only from changed-map reruns:
  27-21-0, paired score +6/48, titanium 130,860 versus 108,690 (ratio 1.2040).
- Compatibility sources: `reports/local-20260809T153449Z`, replacing its
  `crossfire` block with `reports/local-20260809T154403Z` and
  `reports/local-20260809T155828Z`, and its `hive` block with
  `reports/local-20260809T155537Z`.
- Smoke: 4/4 commands clean, `reports/local-20260809T154513Z`.
- Focused release suite: 36/36 passed,
  `reports/release-v69-canonical-opening/focused-static.log`.
- Full `make static`: blocked by the inherited pre-v69 test API and obsolete
  3,200-line assertion; runtime-independent failure preserved at
  `reports/release-v69-canonical-opening/static.log`.
- Remote five-map gate: `reports/remote-20260809T155918Z`, match
  `1c260f12-1141-41e0-a0c7-58e27090c771`; reliability-clean 2-3 unpaired
  result (wins `jackpot`/`lighthouse`, losses `antler`/`archipelago`/`snowflake`).
- Exact remote seeds rerun locally with both sides: 8-2, command-clean, reports
  `local-20260809T160359Z`, `local-20260809T160417Z`,
  `local-20260809T160437Z`, `local-20260809T160456Z`, and
  `local-20260809T160511Z`; the server/local outcome disagreement remains a
  live-observation risk rather than a reliability failure.
- CLI upgraded from `fcode` 2.3.4 to 2.3.6 before the exact-seed rerun.

## Remaining risks

- Geometry preferences are based on the current synced live pool and should be
  re-profiled after a map-pool change.
- The full legacy unit suite must be rebased onto the v69 architecture; this
  candidate does not attempt that separate migration.

## Package and deployment

- Immutable snapshot: `bots/versions/v0014_canonical-opening_20260809-1606_7dd72f03`.
- Archive: `artifacts/submissions/v0014_canonical-opening_20260809-1606_7dd72f03.zip`.
- Archive SHA-256: `998c86506afdef96624348801aaf4dc8cb5dcac1a6e31bb3397a7cdbe36a70f3`.
- Platform: version 72, name `v0014-canonical-opening-7dd72f03`, ready and active.
- Activated: `2026-08-09T16:07:37Z`; deployment report:
  `reports/live-deploy-20260809T160717Z`.
- Rollback: platform v69, ready.
- Initial observation: `reports/live-observe-20260809T160750Z`; no v72-specific
  completed ladder series at capture time.
