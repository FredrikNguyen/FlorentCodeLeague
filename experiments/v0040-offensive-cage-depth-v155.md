# v155 offensive cage depth

## Objective

Increase the confirmed enemy-Core barrier cage from six to ten tiles so a
forward attacker can deny more repair and approach paths, matching the
barrier-heavy winning replay pattern without changing the route, reserve, or
sentinel gates.

## Comparator and scope

- Comparator: immutable `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Allowed files: `bots/candidate/bot/constants.py` and
  `tests/test_candidate_enemy_core_cage.py`.
- Non-goals: Launcher support, home-defense spending, route geometry, Store
  protocol, sentinel timing, baseline/archive files, and platform state.

## Done criteria

- Focused cage tests cover the ten-tile visible cap and existing safety gates.
- Compileall and smoke are clean; `make static` has no new failures.
- The 36-game all-map screen beats v0040 on aggregate paired win rate without
  a delivery or reliability collapse.
- Only a material screen edge advances to the 90-game release matrix.
- If the release gate fails, restore candidate source byte-identically to v0040
  and preserve all reports.

## Validation and decision

- Focused cage plus nearest-defense tests: **25/25** before and after rollback
  (`reports/v155-focused.log`, `reports/v155-rollback-focused.log`).
- Candidate and baseline compileall: passed (`reports/v155-compileall.log`,
  `reports/v155-rollback-compileall.log`).
- `make static`: retained the inherited **15 obsolete-import errors and two
  navigation fast-path assertions**; no new failure (`reports/v155-static.log`).
- Smoke: **4/4** before and after rollback
  (`reports/v155-smoke.log`, `reports/local-20260817T223903Z`).
- Reduced all-map screen: **16-20** versus v0040, zero command failures/TLEs/
  suspicious output, zero no-delivery rows for either side, candidate
  collection **167,280** versus **179,160**, max p99 **1,381 us**, and peak
  callback **3,415 us** (`reports/local-20260817T223421Z`,
  `reports/v155-screen36-analysis.json`, `reports/v155-screen36-summary.json`).
- Map losses clustered on Antler, Auroraveil, Drakkarfjord, Fjordgate,
  Nordkap, Ragnarok, and Royale; the deeper cage did not improve the paired
  win rate.

Decision: **rejected at the 36-game screen**. The candidate cap and focused test
fixture were restored to v0040, and a recursive Python-source comparison found
no candidate-versus-v0040 difference. No 90-game gate, archive, package,
upload, activation, or baseline transition occurred.
