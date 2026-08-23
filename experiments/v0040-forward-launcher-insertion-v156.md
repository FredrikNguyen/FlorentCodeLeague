# v156 forward Launcher insertion

## Objective

Use the Launcher mobility mechanic once, in a bounded offensive window: after
three completed Harvester routes and confirmed enemy-Core intel, the primary
fixed attacker may build one legal forward Launcher and the Launcher may throw
only a designated fixed attacker onto a verified passable tile beside the enemy
Core. This tests the mobility pattern visible in winning replay samples
without adding an open-ended Launcher fleet.

## Comparator and scope

- Comparator: immutable `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Allowed files: `bots/candidate/main.py`,
  `bots/candidate/bot/attacker.py`, `bots/candidate/bot/constants.py`, and
  `tests/test_candidate_forward_launcher.py`.
- Non-goals: home Launcher/ejection, route geometry, Store layout, Sentinel or
  barrier gates, home-defense spending, baseline/archive files, and platform
  state.

## Done criteria

- Focused tests prove the economy/intel/primary-attacker gates, legal build
  site, passable destination filtering, designated-attacker pickup, and
  `can_launch` gating.
- Compileall and smoke are clean; `make static` has no new failures.
- The 36-game all-map screen beats v0040 on aggregate paired win rate without
  a delivery or reliability collapse.
- Only a material screen edge advances to the 90-game release matrix.
- If the screen fails, restore candidate source and focused tests
  byte-identically to v0040 and preserve all reports.

## Validation and decision

- Focused Launcher, cage, and nearest-defense tests: **29/29** before the
  screen (`reports/v156-focused.log`).
- Candidate and baseline compileall: passed (`reports/v156-compileall.log`).
- `make static`: retained the inherited **15 obsolete-import errors and two
  navigation fast-path assertions**; no new failure
  (`reports/v156-static.log`).
- Smoke: **4/4** before and after rollback
  (`reports/v156-smoke.log`, `reports/local-20260817T225056Z`).
- Reduced all-map screen: **16-20** versus v0040, zero command failures/TLEs/
  suspicious output, candidate no-delivery **0** versus comparator **1**,
  candidate collection **150,880** versus **165,170**, max p99 **1,503 us**,
  peak callback **4,948 us**, and one Launcher placement across the screen
  (`reports/local-20260817T224558Z`, `reports/v156-screen36-analysis.json`,
  `reports/v156-screen36-summary.json`).
- The mobility pulse did not convert into paired wins and reduced collection,
  so no release matrix was justified.

Decision: **rejected at the 36-game screen**. Candidate `main.py`, attacker,
constants, and the focused Launcher test were removed/restored; recursive
Python-source comparison found no candidate-versus-v0040 difference. Rollback
focused tests were **25/25**, compileall passed, and rollback smoke was **4/4**
(`reports/local-20260817T225056Z`). No 90-game gate, archive, package, upload,
activation, or baseline transition occurred.
