# v0068 — remote soft-threat lease

## Objective

Stop a dynamic builder from treating a remembered, non-turret home threat as
an unconditional 40-round commitment after the moving target leaves vision.
Record whether the task was assigned to a confirmed turret; after a bounded
soft-threat lease, release only non-turret assignments so the builder can
re-evaluate harvesting, repair, raids, or advance. Confirmed turret tasks stay
sticky because a ranged threat must not be abandoned merely because it crossed
the local vision edge.

## Allowed files

- `bots/candidate/main.py`
- `bots/candidate/bot/constants.py`
- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to task priority, nearest-owner arbitration, turret combat,
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

- Focused gate: 9/9 passed; compileall passed; smoke was 4/4 command-clean;
  `make static` exited 2 from the inherited obsolete-import suite. Logs:
  `reports/iter-remote-soft-threat-lease-v0068/`.
- The 54-game screen was **24/54 (44.4%)** candidate wins versus 30
  comparator wins, with collection **231,330 versus 255,610 (0.9050x)**.
  Both sides had zero no-delivery rows; command failures, TLEs, and suspicious
  output were zero. Max p99 was 1,332 us and peak callback 2,575 us. Report:
  `reports/local-20260814T225021Z`; analysis:
  `reports/iter-remote-soft-threat-lease-v0068/screen-analysis.json`.
- Status: **rejected at the screen gate**. Releasing unseen soft threats on a
  lease damaged economy and paired wins, so no full matrix or package was
  warranted. Source files were restored byte-identically to v0031; proof:
  `reports/iter-remote-soft-threat-lease-v0068/revert-source-diff.txt`.
  Rollback logs are in the same directory; no upload, activation, or baseline
  transition occurred.
