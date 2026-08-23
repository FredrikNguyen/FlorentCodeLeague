# v157 siege-only Gunner escalation

## Objective

Keep the normal minimum home-defense shell, but reserve the maximum Gunner cap
for a visible enemy siege turret (Gunner, Sentinel, or Launcher). A nearby
enemy conveyor, Harvester, or Builder remains a threat for emergency timing
and siege reporting, but no longer authorises the same five-Gunner spending
spike.

## Comparator and scope

- Comparator: immutable `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Allowed files: `bots/candidate/bot/core_role.py` and
  `tests/test_candidate_nearest_defense.py`.
- Non-goals: minimum Gunner shell, reserve/round gates, route construction,
  Store layout, attacker/Launcher behavior, baseline/archive files, and
  platform state.

## Done criteria

- Focused tests prove non-siege threats do not trigger the maximum cap and
  actual siege turrets still do.
- Compileall and smoke are clean; `make static` has no new failures.
- The 36-game all-map screen beats v0040 on aggregate paired win rate without
  a delivery or reliability collapse.
- Only a material screen edge advances to the 90-game release matrix.
- If the screen fails, restore candidate source and tests byte-identically to
  v0040 and preserve all reports.

## Validation and decision

- Focused defense/cage tests: **26/26** before the screen
  (`reports/v157-focused.log`).
- Candidate and baseline compileall: passed (`reports/v157-compileall.log`).
- `make static`: retained the inherited **15 obsolete-import errors and two
  navigation fast-path assertions**; no new failure
  (`reports/v157-static.log`).
- Smoke: **4/4** before and after rollback
  (`reports/v157-smoke.log`, `reports/local-20260817T225859Z`).
- Reduced all-map screen: **14-22** versus v0040, zero command failures/TLEs/
  suspicious output, zero no-delivery rows for either side, candidate
  collection **120,220** versus **159,930**, max p99 **1,423 us**, and peak
  callback **3,333 us** (`reports/local-20260817T225452Z`,
  `reports/v157-screen36-analysis.json`, `reports/v157-screen36-summary.json`).
- The losses show that non-turret enemies reaching the Core still require the
  existing spending response; narrowing the escalation is not safe.

Decision: **rejected at the 36-game screen**. The candidate Core policy and
focused test were restored to v0040, recursive Python-source comparison found
no candidate-versus-v0040 difference, rollback focused tests were **25/25**,
compileall passed, and rollback smoke was **4/4** (`reports/local-20260817T225859Z`).
No 90-game gate, archive, package, upload, activation, or baseline transition
occurred.
