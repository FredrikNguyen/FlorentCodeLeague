# v0040 quiet-defense retirement workforce reuse — v173

## Objective

Reuse one late-game unit-cap slot without weakening the opening. After a
non-cramped base has five completed routes, at least three intact home Gunners,
a rich bank, and 80 consecutive threat-free rounds, the Core may authorize the
nearest non-attacker Builder to destroy only the farthest intact home Gunner.
Once the delayed marker confirms the removal, the Core raises the late Builder
target by one. No turret is rebuilt automatically.

## Comparator and allowed files

- Comparator: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Source: `bots/candidate/main.py`, `bots/candidate/bot/constants.py`,
  `bots/candidate/bot/core_role.py`, and `bots/candidate/bot/dynamic.py`.
- Focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, `UPDATES.md`, and durable project state.

## Non-goals

No opening workforce, route FSM, ore selection, combat target, Sentinel,
Launcher, Barrier, ammo, navigation, Store layout, map branch, baseline,
archive, package, upload, activation, or live-state change.

## Hypothesis and implementation

Port the previously measured, one-shot retirement lifecycle while retaining
v0040's current defense cap and route behavior. Add a high-valued marker in
the existing Gunner-cap Store slot, Core-side quiet/maturity gates and delayed
completion detection, a single late Builder bonus, and a Dynamic task that
walks to and legally destroys the designated outer Gunner. The marker is
cleared only after the Core observes the live-Gunner count drop, preventing
duplicate retirement or accidental rebuilding.

## Done criteria

- Focused tests prove all retirement gates, nearest non-attacker ownership,
  farthest-Gunner selection, legal destroy, delayed completion, and no second
  retirement marker.
- Candidate compileall passes; `make static` is checked and inherited failures
  are recorded; smoke is command-clean.
- The 21-game all-map screen materially improves paired win rate over v0040 or
  shows a clear workforce/resource gain without delivery collapse, with no
  command, TLE, or suspicious-output regression.
- Only a materially positive screen advances to the 60-game release gate. A
  tie/regression or reliability/delivery failure requires exact v0040 rollback
  and no platform operation.

## Evidence and decision

- Initial implementation passed focused checks **23/23**, compileall, and
  command-clean smoke (**4/4**, `reports/local-20260818T033808Z`). Static
  retained the inherited 15 obsolete-import errors plus two navigation
  assertions. The 21-game all-map screen was a material **15-6** versus v0040,
  with mean resources **3,953 vs 2,685**, living Harvesters **7.29 vs 6.29**,
  first delivery **42.2 vs 35.2** among delivered games, and zero candidate
  no-delivery rows (`reports/local-20260818T033838Z` and
  `reports/iter-v173-quiet-defense-retirement-screen-replay-analysis.json`).
- The required 60-game release gate was command-clean but tied **30-30**.
  Candidate resources were **4,464 vs 4,435**, living Harvesters **6.97 vs
  6.25**, and Builders **8.35 vs 8.17**; each side had one no-delivery row.
  Max p99/peak was **1,394/5,636 us** (`reports/local-20260818T034101Z` and
  `reports/iter-v173-quiet-defense-retirement-release60-replay-analysis.json`).
- Bounded repair 1 canceled a pending retirement immediately when a new home
  threat appeared. Focused checks were **24/24**, compileall passed, smoke was
  **4/4**, and static was unchanged. The screen regressed to **9-12**, with
  resources **4,756 vs 5,787**, living Harvesters **5.95 vs 8.19**, and first
  delivery **24.8 vs 48.8** (`reports/local-20260818T034849Z` and
  `reports/iter-v173-quiet-defense-retirement-repair1-screen-replay-analysis.json`).
- v173 is rejected after the release tie and unsuccessful repair. All source
  and focused changes were removed; recursive v0040 parity is **0 diff lines**
  in `reports/iter-v173-quiet-defense-retirement-rollback-source-diff.txt`.
  Rollback focused checks passed **20/20**, compileall passed, and rollback
  smoke was **4/4**. No package, release, remote match, upload, activation, or
  baseline transition occurred.
