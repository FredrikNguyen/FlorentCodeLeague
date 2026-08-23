# v204 — failed-chain cleanup and retry

## Objective

When the first conveyor chain stalled before any completed delivery, the
Builder that owned the chain recorded its private tiles, legally removed them,
and seeded one alternate accepting Conveyor beside the same Harvester. Shared
tiles and all post-delivery routes remained untouched.

## Scope and non-goals

- Temporary source: `bots/candidate/main.py` and
  `bots/candidate/bot/defender.py`.
- Temporary focused coverage: `tests/test_candidate_route_recovery.py`.
- Regression schedule: `configs/eval_regression.toml`, rotated seed 169.
- No primary-attacker, Barrier, Launcher, Sentinel, Gunner, ammo, ore,
  route-geometry, hijack/sabotage, Store, baseline, package, upload,
  activation, or live-state change.

## Validation and replay evidence

- Initial focused coverage was **26/26**, compileall passed, `make static`
  retained the inherited failures, and smoke was **4/4**. The seed-169
  15-map screen was **6-9**, command-clean with zero TLE/suspicious output,
  but had one candidate no-delivery Fjordgate row. Candidate mean first
  delivery was **26.29** versus **31.60** for v0042; collection was
  **86,520 vs 87,480 Ti**. Reports: `reports/local-20260818T140305Z` and
  `reports/iter-v204-route-recovery-replay-analysis.json`.
- The one permitted repair made the retry explicitly one-shot, preventing a
  failed retry from re-entering cleanup forever. Focused coverage remained
  **26/26**, compileall passed, static retained the inherited exit 2, and
  smoke was **4/4**. The same screen stayed **6-9**; it removed the
  no-delivery row, but candidate mean first delivery became **33.00** versus
  **32.47**, collection fell to **72,600 vs 72,370 Ti**, and replay inspection
  showed significant Conveyor removal/rebuild churn. Max p99/peak were
  **1,480/5,140 us**. Reports: `reports/local-20260818T140626Z` and
  `reports/iter-v204-route-recovery-repair-replay-analysis.json`.

## Decision and rollback

Reject v204: the repair improved the reliability symptom on this seed but did
not create a paired win-rate edge, and its cleanup cost delayed delivery and
reduced conversion. The temporary source and focused test were removed;
candidate production files are recursively byte-identical to immutable v0042.
Rollback nearest-defense was **23/23**, compileall passed, static retained the
same inherited exit 2, and smoke was **4/4** at
`reports/local-20260818T140957Z`. Rollback logs are under
`reports/iter-v204-route-recovery-rollback-*`. No release gate, package,
upload, activation, or live transition was justified.

## Replay follow-up

The repaired candidate's no-delivery fix was not enough because successful
high-ranking teams preserve an uninterrupted route shell while converting
surplus into early Barriers and Launchers. In the 15-game top-team sample,
winners averaged 5.0 Harvesters, 13.7 Barriers, 3.3 Launchers, and 0.7
Gunners; v0042's comparator side in the same screen averaged 8.0 Harvesters,
4.3 Barriers, no Launchers, and 2.5 Gunners. The next hypothesis must change
post-delivery workforce conversion/role assignment rather than add another
chain-repair loop or a one-off Launcher selector.
