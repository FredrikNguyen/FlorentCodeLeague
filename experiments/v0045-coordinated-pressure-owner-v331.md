# v331 — coordinated pressure-owner assault lane (rejected)

## Objective and scope

Top-team openings sustain several control units while our dynamic workforce
often remains split between route conversion and opportunistic raids.  v331
tested a real coordination contract rather than another unit-count knob: the
Core reused the unused high bits of the existing `SLOT_GUNNER_CAP` channel to
publish one deterministic dynamic Builder as a pressure owner during the
published `PRESSURE` phase.  That owner could preempt ordinary harvesting only
when the historical harvester floor was met, attack a visible loaded enemy
logistics target when profitable, and otherwise advance toward the enemy Core.
Existing CHAIN work, fixed attackers, repair priority, turret cap, Store slot
count, spending rules, and map policy were unchanged.

Production scope was `bots/candidate/bot/constants.py`,
`bots/candidate/bot/core_role.py`, and `bots/candidate/bot/dynamic.py`, with
three focused contract tests in `tests/test_candidate_nearest_defense.py`.
No baseline snapshot, package, upload, activation, or live state was touched.

## Validation

- The focused suite passed **43/43** after fixing the missing `MODE_SCOUT`
  import; compileall passed.  The rollback suite later passed **40/40** at
  `reports/iter-v331-pressure-owner-rollback-focused.log`.
- `make static` retained the inherited repository profile: 15 obsolete-module
  import errors and two navigation fast-path assertions; no new v331 failure
  was reported (`reports/iter-v331-pressure-owner-static.log`).
- Smoke was command-clean **4/4** at `reports/local-20260820T042832Z`.
- The rotated 15-map screen was command-clean but only **4-11 candidate-A**
  versus immutable v0045.  Candidate collection was **42,460 Ti** versus
  **60,840 Ti** for the comparator; every row delivered and max p99/peak was
  **1,332/4,350 us**.  Reports are
  `reports/local-20260820T042906Z` and
  `reports/iter-v331-pressure-owner-replay-analysis.json`.

## Decision and rollback

Reject v331.  A single dynamic pressure owner did not produce sustained
multi-unit pressure; it pulled a route worker into long advances while the
comparator continued to expand and control the map.  The candidate was
restored to exact recursive parity with immutable v0045, verified with
`diff -rq` excluding `__pycache__`.  No 60-game gate, remote gate, package,
upload, promotion, activation, or live-state transition was justified.

## Remaining risk

The failure is architectural: one shared assault lease is too coarse for map
context and does not provide the multi-unit Launcher/Sentinel/Barrier waves
seen in stronger replays.  The next candidate should test a bounded squad or
relay lifecycle with explicit release/return conditions, while preserving
route throughput and not assigning a single worker to an unbounded march.
