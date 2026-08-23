# v0070 — cramped-map early sentinel shell

## Objective

Adapt the opening combat shell to map geometry. The current economy-first
policy allows only one early forward Sentinel everywhere, even on compact
maps where the enemy Core is already within the early combat radius. After the
first route is complete, permit a second early Sentinel only on those cramped
maps; retain the one-Sentinel opening on long maps so route 0 remains funded.

## Allowed files

- `bots/candidate/bot/attacker.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to route construction, workforce counts, dynamic priorities,
  sabotage/hijack behavior, ammo, turret response, or Store layout;
- no map-name catalog or fixed-coordinate branch; compactness is derived from
  the existing core-distance geometry helper;
- no edits to `bots/baseline/` or immutable snapshots;
- no upload, activation, or baseline transition before the local gate.

## Promotion gate

Run focused tests, compileall, `make static`, and `make smoke`, then the
54-game regression screen against immutable v0031. Run the 210-game matrix
only for a strict clean screen edge. Promote only if paired win rate improves
without delivery, collection, protected-map, or reliability regressions;
otherwise revert and retain v0031.

## Result

- Focused gate: 9/9 passed before the screen; the restored candidate passed
  7/7 after rollback. Candidate compileall passed, smoke was 4/4
  command-clean, and `make static` retained the inherited exit-2
  obsolete-import result. Rollback logs are under
  `reports/iter-cramped-early-sentinel-shell-v0070/`.
- The 54-game screen was **21/54 (38.9%)** candidate wins versus 33
  comparator wins, with collection **210,430 versus 248,230 (0.8477x)**.
  The candidate had one no-delivery row versus zero for the comparator;
  command failures, TLEs, and suspicious output were zero. Max p99 was
  1,467 us and peak callback 3,026 us. Report:
  `reports/local-20260814T231336Z`; analysis:
  `reports/iter-cramped-early-sentinel-shell-v0070/screen-analysis.json`.
- Status: **rejected at the screen gate**. The geometry-aware second
  Sentinel shell sharply reduced both paired wins and collection, so no full
  matrix was run. The candidate source and focused tests were restored
  byte-identically to v0031; proof is
  `reports/iter-cramped-early-sentinel-shell-v0070/revert-source-diff.txt`.
  No package, upload, activation, or baseline transition occurred.
