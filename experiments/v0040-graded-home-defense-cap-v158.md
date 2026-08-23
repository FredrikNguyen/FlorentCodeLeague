# v0040 graded home-defense cap — v158

Date: 2026-08-18

## Objective

Repair the defense/economy trade-off exposed by v157.  The v0040 Core policy
raises the home-Gunner cap to five for any visible enemy contact after the
opening economy; v157 narrowed that response to visible siege turrets and
fell to 14–22 against v0040.  This candidate keeps the five-Gunner shell for a
real Gunner, Sentinel, or Launcher, but limits ordinary Builder/logistics
contact to one extra slot (maximum four).

## Comparator and scope

- Comparator: immutable `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Allowed files: `bots/candidate/bot/core_role.py`,
  `tests/test_candidate_nearest_defense.py`, this record, `UPDATES.md`, and
  durable state.
- Non-goals: route construction, workforce spawning, attack/sentinel/Launcher
  behavior, Store layout, map selection, baseline archives, and platform state.

## Done criteria

- Focused coverage proves the graded cap: four for non-siege contact and five
  for a visible siege turret, while the existing economy-young and emergency
  gates remain unchanged.
- Candidate compileall and smoke are clean; `make static` has no new failures.
- The 36-game all-map screen materially beats v0040 on paired win rate with no
  reliability or delivery collapse. Only a material edge advances to the
  90-game release matrix.
- If the screen fails, restore candidate source and fixture byte-identically
  to v0040, preserve all reports, and do not perform platform operations.

## Validation and decision

Initial focused coverage was **21/21**, compileall passed, `make smoke` was
**4/4**, and `make static` retained only the inherited 15 obsolete-import
errors plus two navigation fast-path assertions (`reports/v158-*`).  The
initial 36-game all-map screen scored **19–17** against v0040, with candidate
collection **170,900** versus **158,100**, one candidate no-delivery row versus
zero, zero TLE/suspicious output, max p99 **1,447 us**, and peak callback
**5,021 us** (`reports/local-20260817T230801Z`,
`reports/v158-screen36-summary.json`).  The positive margin was not material
enough to justify a release gate and the delivery floor regressed.

Repair 1 added a close-contact emergency (squared distance <= 8) for
non-siege enemies while preserving the remote four-Gunner cap.  Focused tests
remained **21/21**, compileall passed, smoke was **4/4**, and static retained
the same inherited failures (`reports/v158-repair1-*`).  The second 36-game
screen again scored **19–17**, now with candidate collection **193,220** versus
**200,910**, one no-delivery row for each side, zero TLE/suspicious output,
max p99 **1,487 us**, and peak callback **5,267 us**
(`reports/local-20260817T231300Z`,
`reports/v158-repair1-screen36-summary.json`).

**Decision: rejected after two bounded screens.**  The candidate source and
focused fixture were restored to v0040; no 90-game gate, archive, package,
upload, activation, or baseline transition occurred.  Rollback parity and
validation will be recorded below.

## Rollback validation

The production source is byte-identical to v0040 (`reports/v158-rollback-source-diff.txt`).
Rollback focused coverage is **20/20**, candidate and baseline compileall pass,
and rollback smoke is **4/4** (`reports/v158-rollback-focused.log`,
`reports/v158-rollback-compileall.log`, and
`reports/local-20260817T231807Z`). No release gate or platform operation was
performed.
