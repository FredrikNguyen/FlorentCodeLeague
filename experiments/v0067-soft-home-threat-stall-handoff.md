# v0067 — soft home-threat stall handoff

## Objective

Convert a measured dynamic-builder dead end into useful work. When a Builder
holds a visible non-turret `TASK_HOME_THREAT` and both danger-aware and normal
navigation fail to produce a move, clear only that soft task so the next task
selection can return it to harvesting, repair, raid, or advance. Turret threats
remain sticky because abandoning a ranged threat would be unsafe.

## Allowed files

- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to turret response, task priorities, commitment constants,
  spending, roles, routing, exploration, raids, map branches, or Store layout;
- no edits to `bots/baseline/` or immutable snapshots;
- no upload, activation, or baseline transition before the local gate.

## Promotion gate

Run focused tests, compileall, `make static`, and `make smoke`, then the
54-game regression screen against immutable v0031. Run the 210-game matrix
only for a strict clean screen edge. Promote only if paired win rate improves
without delivery, collection, protected-map, or reliability regressions;
otherwise revert and retain v0031.

## Result

- Focused gate: 9/9 passed after fixing the test's missing `patch` import;
  compileall passed; smoke was 4/4 command-clean. `make static` exited 2 from
  the inherited obsolete-import suite. Logs: `reports/iter-soft-home-threat-stall-v0067/`.
- The 54-game screen was **26/54 (48.1%)** candidate wins versus 28
  comparator wins, with collection **229,270 versus 232,810 (0.9848x)**.
  Candidate and comparator both had zero no-delivery rows, TLEs, suspicious
  output, and command failures; max p99 was 1,287 us and peak callback 2,633
  us. Report: `reports/local-20260814T223822Z`; analysis:
  `reports/iter-soft-home-threat-stall-v0067/screen-analysis.json`.
- Status: **rejected at the screen gate**. The soft-task handoff reduced both
  paired win rate and collection, so no full matrix or package was warranted.
  The candidate was restored byte-identically to v0031; the empty proof is
  `reports/iter-soft-home-threat-stall-v0067/revert-diff.txt`. Rollback logs
  are in the same directory; no upload, activation, or baseline transition
  occurred.
