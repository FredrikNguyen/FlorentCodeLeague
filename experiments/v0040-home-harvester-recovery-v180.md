# v180 home-local Harvester recovery

## Objective

Test whether a home-local dynamic Builder should re-enter the harvest loop when
the lifetime `SLOT_HARVESTER_COUNT` has reached the offense threshold but fewer
than two friendly Harvesters remain visible. The bounded idea targets the
failure mode where lifetime route accounting outlives the actual workforce.

## Allowed files and non-goals

- Allowed: `bots/candidate/bot/dynamic.py`,
  `tests/test_candidate_nearest_defense.py`, this record, `UPDATES.md`, and
  durable state.
- Non-goals: no route geometry, Core-ring, attacker, Launcher, Barrier,
  workforce-spawn, Store-policy, baseline, package, or live-operation changes.

## Iteration evidence

- Initial: focused **21/21**, compileall passed, smoke **4/4**;
  screen **11-10**, collection **86,710 vs 87,920** (0.9862x), no-delivery
  **0/0**, placed Harvesters **146 vs 186**
  (`reports/local-20260818T060909Z`).
- Repair 1 widened the visible home floor from one to two Harvesters and added
  a two-Harvester unit test. Focused **21/21**, compileall passed, smoke
  **4/4**; screen **11-10**, collection **132,130 vs 128,210** (1.0306x),
  no-delivery **0/1**, Harvesters **184 vs 150**
  (`reports/local-20260818T061232Z`). Its required release gate reversed to
  **28-32**, collection **266,200 vs 294,540** (0.9038x), no-delivery **0/1**,
  max p99/peak **1,596/5,060 us**
  (`reports/local-20260818T061518Z`).
- Repair 2 additionally required resources below two Harvester costs before
  forcing recovery. Focused **21/21**, compileall passed, smoke **4/4**;
  screen **10-11**, collection **95,280 vs 95,260** (1.0002x), no-delivery
  **0/0**, Harvesters **162 vs 159**
  (`reports/local-20260818T062254Z`). This is a tie, not a material edge.

## Decision

Reject v180. Both repairs failed to transfer their short-screen result to the
release gate or produce a material paired win edge. The temporary source and
test changes were removed; recursive candidate parity with immutable v0040 is
**0 diff lines**. Rollback focused tests passed **20/20**, compileall passed,
and rollback smoke was **4/4** (`reports/iter-v180-rollback-*`,
`reports/local-20260818T062740Z`). No remote gate, package, upload, activation,
or baseline transition occurred.
