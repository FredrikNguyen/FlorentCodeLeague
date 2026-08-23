# v0069 — loaded attacker sabotage pulse

## Objective

Convert a visible enemy logistics opportunity into immediate pressure. The
fixed attacker currently calls `_try_sabotage_with_attacker`, but that hook is
a permanent no-op, so it walks directly to the enemy core even when a loaded
conveyor or splitter is already in its vision. Let it claim and destroy only a
currently loaded enemy conveyor/splitter, then return to the direct siege lane
once the target is gone. This preserves the attacker role and avoids remote,
empty-logistics detours.

## Allowed files

- `bots/candidate/bot/attacker.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to dynamic-builder priorities, hijack routing, sentinel counts,
  spending, core defense, map branches, or Store layout;
- no chasing an unseen or empty target, no harvester takeover change, and no
  fixed-attacker role reassignment;
- no edits to `bots/baseline/` or immutable snapshots;
- no upload, activation, or baseline transition before the local gate.

## Promotion gate

Run focused tests, compileall, `make static`, and `make smoke`, then the
54-game regression screen against immutable v0031. Run the 210-game matrix
only for a strict clean screen edge. Promote only if paired win rate improves
without delivery, collection, protected-map, or reliability regressions;
otherwise revert and retain v0031.

## Result

- Focused gate: 9/9 passed; compileall passed; smoke was 4/4 command-clean;
  `make static` exited 2 from the inherited obsolete-import suite. Logs:
  `reports/iter-loaded-attacker-sabotage-v0069/`.
- The 54-game screen was **23/54 (42.6%)** candidate wins versus 31
  comparator wins, with collection **228,660 versus 235,770 (0.9698x)**.
  The candidate had one no-delivery row versus zero for the comparator;
  command failures, TLEs, and suspicious output were zero. Max p99 was 1,403
  us and peak callback 2,758 us. Report: `reports/local-20260814T230109Z`;
  analysis: `reports/iter-loaded-attacker-sabotage-v0069/screen-analysis.json`.
- Status: **rejected at the screen gate**. Enabling the fixed-attacker loaded
  logistics pulse hurt paired wins, collection, and delivery. The attacker
  source was restored byte-identically to v0031; proof:
  `reports/iter-loaded-attacker-sabotage-v0069/revert-source-diff.txt`.
  Rollback logs are in the same directory; no full matrix, package, upload,
  activation, or baseline transition occurred.
