# v0040 low-liquidity Gunner retirement — v183

## Objective

Test one bounded liquidity conversion: after four completed Harvester routes,
when the bank cannot fund the next Harvester and no enemy or siege beacon is
visible near the Core, retire one already-adjacent surplus home Gunner. Keep
the nearest-home-responder rule and a three-Gunner safety floor so this cannot
turn a live defense into economy spending.

## Parent and scope

- Parent/baseline: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`
- Candidate: `bots/candidate`
- Changed source: `bots/candidate/bot/constants.py`, `bots/candidate/bot/dynamic.py`
- Focused coverage: `tests/test_candidate_nearest_defense.py`
- Non-goals: no opening workforce, route geometry, Sentinel, raid, Launcher,
  Core-ring, or navigation changes; no edits to `bots/baseline/` or the parent
  snapshot.
- Git SHA: `eeafad8f6207fcccb135311659aa55ca6c690a64` (worktree dirty; unrelated
  pre-existing changes preserved).
- Engine: `fcode 2.3.4` (update notice 2.3.8 available; not installed).
- Map pool: all 15 configured maps; map hashes recorded in
  `reports/iter-v183-low-liquidity-gunner/maps.json`.

## Iteration evidence

The initial and first repair were rejected on the shortened all-map screen:

- Initial: 7–11, 63,020 vs 72,920 collected titanium; report
  `reports/local-20260818T071633Z`.
- Repair 1 (four routes, raw Harvester-cost liquidity gate, three-Gunner
  floor): 8–10, 94,700 vs 90,150; report `reports/local-20260818T071940Z`.
- Repair 2 added the already-adjacent target requirement: 10–8, 93,350 vs
  84,280, zero no-delivery rows; report `reports/local-20260818T072217Z`.

## Final validation

- Focused: 23/23 — `reports/iter-v183-low-liquidity-gunner/final-focused.log`.
- Compileall: pass — `reports/iter-v183-low-liquidity-gunner/final-compileall.log`.
- Static: exit 2 from the known inherited 15 obsolete imports and 2
  navigation fast-path assertions; no new v183 failure —
  `reports/iter-v183-low-liquidity-gunner/final-static.log`.
- Smoke: 4/4 command-clean — `reports/local-20260818T072653Z` and
  `reports/iter-v183-low-liquidity-gunner/final-smoke.log`.
- Post-promotion schedule validation: 6/6; post-promotion smoke against the
  v0042 baseline: 4/4 command-clean — `reports/iter-v183-low-liquidity-gunner/post-promotion-schedule.log`,
  `reports/local-20260818T074256Z`, and
  `reports/iter-v183-low-liquidity-gunner/post-promotion-smoke.log`.
- Release: 60/60 command-clean, candidate 35–25 (58.33%), no ties, one
  no-delivery per side, max p99/peak 1,500/5,361 µs —
  `reports/local-20260818T072713Z` and
  `reports/iter-v183-low-liquidity-gunner/release-analysis.json`.
- Release placed totals (candidate vs parent): 532 vs 478 Harvesters, 6,266
  vs 6,066 conveyors, 138 vs 121 Gunners, 217 vs 179 Sentinels; collected
  titanium 312,210 vs 323,460.

## Decision

Promote as the new local baseline candidate and submit through the guarded
remote/live release path. The decision is win-rate-led (35–25) with clean
execution and no delivery regression; the lower aggregate titanium and weak
fjordgate/midgard floors remain observation risks.

## Platform fields

- Remote test: match `a036c379-15c9-4c1a-ac5b-c25e5bb9881f` completed 4–1
  (candidate won sprint, bridge, crossfire and vault; lost aurora).
- Package: `artifacts/submissions/v0042_low-liquidity-gunner_20260818-0737_eeafad8f.zip`,
  SHA-256 `ed2a6bc1c801ef224921bde802f23e692e135bbf6cd507e373149e1289bb26c0`.
- Platform submission: version 105, ready and active; upload/activation report
  `reports/live-deploy-20260818T073828Z`.
- Live guard: v104 was rolled back after fresh 103/190 (0.542) evidence below
  v101's preserved 0.700 score; v101 remains the rollback target for v105.
- Ladder before activation: rank 38, rating 1564.04, 6–4 recent record;
  platform v105 is now `active_observing`, so live promotion is deferred until
  its observation window supplies evidence.
- Post-activation snapshot confirms v105 is active, but no v105-rated ladder
  series has started yet: `reports/live-post-v183-activation-20260818T074634Z`.
