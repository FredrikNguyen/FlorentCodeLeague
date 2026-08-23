# v0072 — nearest home-threat task claim

## Objective

Remove a measured source of dynamic-builder idling. A visible home turret or
enemy Builder is currently returned by every nearby dynamic builder's greedy
task picker; each non-owner then reaches `_execute_strike`, discovers it is not
the nearest responder, clears the task, and loses the rest of that round. Make
the nearest-responder ownership decision at task selection time. The selected
owner keeps the existing strike, flee, and siege behavior; all other builders
continue to the next productive task in the same round.

## Allowed files

- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to strike execution, threat ranking, turret construction, siege
  recall, economy, route FSM, workforce, navigation, raid/hijack behavior, or
  Store layout;
- no new map branches, timing thresholds, or unit types;
- no edits to `bots/baseline/` or immutable snapshots;
- no upload, activation, or baseline transition before the local gate.

## Promotion gate

Run focused tests, compileall, `make static`, `make smoke`, and `git diff
--check`, then the 54-game regression screen against immutable v0031. Run the
210-game matrix only for a strict, reliability-clean screen edge. Promote only
if paired win rate improves without delivery, collection, protected-map, or
reliability regressions; otherwise revert and retain v0031.

## Result

- Focused tests passed 8/8; candidate compileall passed; `make smoke` was 4/4
  command-clean; `git diff --check` passed. `make static` retained the
  inherited exit-2 obsolete-import result. Logs: `reports/iter-nearest-threat-task-claim-v0072/`.
- The 54-game screen was 42/54 candidate wins versus 12 comparator wins,
  287,380 versus 194,600 collected titanium (1.4768x), zero no-delivery rows,
  zero command failures/TLE/suspicious output, max p99 1,482 us, and peak
  callback 2,766 us (`reports/local-20260814T234501Z`).
- The full 210-game matrix was 121/210 candidate wins versus 89 comparator
  wins (57.6% versus 42.4%), 1,062,460 versus 923,170 collected titanium
  (1.1509x), zero command failures/TLE/suspicious output, max p99 1,490 us,
  and peak callback 3,386 us. Candidate no-delivery rows were 4 versus 3 for
  the comparator. Full evidence is under
  `reports/local-20260814T235305Z/` and
  `reports/iter-nearest-threat-task-claim-v0072/full-analysis.json`.
- Map-conditioned wins were strongest on Duel (9-1), Hive (8-2), Pinch (8-2),
  Quarry (8-2), Sweden (8-2), and Vault (7-3). Aurora, Bridge, Longship,
  Runestone, and String remained weaker; the aggregate edge is large enough
  under the current moving-win-rate policy to accept despite those localized
  regressions.
- Status: **promotion 2 accepted locally**. The candidate is archived as the
  next immutable moving baseline; no upload or activation was performed.
