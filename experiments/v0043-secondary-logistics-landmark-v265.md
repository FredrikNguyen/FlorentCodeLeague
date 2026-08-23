# v265 secondary logistics landmark — rejected

## Objective and replay basis

The attributable v106 losses in `reports/iter-v251-live-check/9c66c9bc/`
showed fixed attackers reaching the opposing half with two-to-four Harvesters
but no confirmed enemy Core or forward Sentinel. The candidate tested whether
the designated secondary attacker could follow the fixed output of a visible
enemy Conveyor as a local downstream landmark, while the primary attacker,
economy, Sentinel legality/liquidity gates, and all infiltration behavior
remained unchanged.

## Exact scope

- `bots/candidate/bot/attacker.py`: secondary-only landmark navigation;
- `tests/test_candidate_nearest_defense.py`: ownership, direction, filtering,
  bounds, and confirmed-Core tests;
- this record, plan/update/state metadata, and reports.

No enemy-belt raid, hijack/takeover, infiltrator defense, Store schema,
workforce/economy/route policy, purchase policy, baseline/archive, package,
upload, activation, or live-state operation was included.

## Validation

- Focused landmark and nearest-defense coverage: **30/30**;
  `reports/iter-v265-secondary-landmark/focused.log`.
- Candidate compileall: passed;
  `reports/iter-v265-secondary-landmark/compileall.log`.
- `make static`: inherited failure only — 15 obsolete-module imports and two
  navigation fast-path assertions;
  `reports/iter-v265-secondary-landmark/static.log`.
- `make smoke`: **4/4** command-clean;
  `reports/iter-v265-secondary-landmark/smoke.log`.
- Scoped `git diff --check`: passed. The unscoped worktree check retains
  unrelated existing whitespace in `artifacts/chatgpt/PLANNING_PACKET.md`.
- First rotated 15-map screen: command-clean, zero TLE/suspicious rows,
  candidate **8-7**, **69,730 vs 79,350 Ti**, and one candidate
  no-delivery row. Raw report `reports/local-20260819T091027Z`; parsed
  replay metrics `reports/iter-v265-secondary-landmark/screen-replay-analysis.json`.
- Independent screen rotation: command/delivery/reliability-clean, candidate
  **7-8**, **63,840 vs 60,190 Ti**. Raw report
  `reports/local-20260819T091300Z`; parsed metrics
  `reports/iter-v265-secondary-landmark/screen173-replay-analysis.json`.

## Decision and rollback

Across both screens the candidate was **15-15** and collected **133,570 vs
139,540 Ti**. The one initial win edge did not repeat and no reliability or
first-delivery improvement offset the collection loss. Reject v265 without a
repair or longer gate. The temporary attacker/tests were removed and the
candidate attacker is byte-identical to exact v0043; proof is
`reports/iter-v265-secondary-landmark/rollback-source.diff`. Remove the
temporary screen config before ending the iteration. No package, upload,
activation, promotion, or live-state operation occurred.

## Follow-up

This confirms that a visible enemy route is not, by itself, a reliable Core
landmark. Keep the infiltration branch closed: the direct live evidence still
supports route conversion and pressure timing as the next search area, but a
new candidate needs a distinct causal signal rather than another generic
infiltration or guessed-Core variation.
