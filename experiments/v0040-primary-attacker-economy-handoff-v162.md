# v162 primary-attacker opening economy handoff

## Objective

Recover the route-conversion losses where the candidate reaches the middle of
the game with fewer Harvesters and less delivered titanium than the baseline.
When no route has completed by a bounded round, let only the primary fixed
attacker join the existing Defender economy loop. It returns to its direct
Sentinel/Core lane as soon as the first route is recorded.

## Comparator and allowed files

- Comparator: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Allowed source: `bots/candidate/bot/attacker.py` and
  `bots/candidate/bot/constants.py`.
- Focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, reports, `UPDATES.md`, and durable project state.

## Non-goals

No changes to route construction or facing, Dynamic task priorities, Builder
spawning, ammo conversion, home turrets, forward Sentinel thresholds, barriers,
Launchers, Store layout, baseline/archive snapshots, package, upload,
activation, or live state.

## Hypothesis and bounded behavior

- Before round 28 the primary attacker keeps the v0040 direct opening.
- From round 28 through the bounded handoff window, zero completed routes lets
  only the primary attacker call the existing Defender SCOUT/CHAIN loop.
- A confirmed first route immediately ends the handoff; after the deadline the
  attacker resumes direct pressure even if the economy is still unhealthy.
- The existing Sentinel attempt runs before the handoff, so a legal forward
  damage source is never delayed by the economy fallback.

## Done criteria

- Focused tests cover the round, route-count, primary-ID, and deadline gates.
- Compileall passes; static is checked and inherited failures are recorded;
  smoke is command-clean.
- The 24-game all-map screen has a material paired win-rate edge over v0040,
  no command/TLE/suspicious-output failures, and no severe delivery collapse.
- Only a qualifying screen advances to the 60-game release matrix. A failed
  screen or release gate requires exact v0040 rollback and no platform action.

## Attempt 1 and repair 1

- Attempt 1 passed focused **21/21**, compileall, and smoke **4/4**; static
  retained the inherited failures. The 24-game all-map screen was **12-12**
  versus v0040 (candidate Ti **95,540** vs **100,530**, zero no-delivery rows,
  zero command/TLE/suspicious-output failures). Royale and Drakkarfjord
  delivery improved, but Auroraveil slipped to first delivery 126 versus 27
  turns and Nordkap remained 0-2. Report: `reports/local-20260818T003927Z`.
- Repair 1 keeps the handoff only while enemy-Core intel is unconfirmed. A
  confirmed Core now preserves the direct attacker lane. Focused coverage is
  rerun before the second screen; no release gate or platform operation is
  justified by the tied initial screen.

Repair 1 passed focused **27/27**, compileall, and smoke **4/4** after fixing
the minimal probe's absent `enemy_core_known` state. Static again retained the
inherited failures. The second 24-game screen fell to **11-13**, candidate Ti
**118,000** versus **124,210**, with zero no-delivery rows and zero command,
TLE, or suspicious-output failures (`reports/local-20260818T004409Z`). The
confirmed-Core guard improved Nordkap to 1-1 and Archipelago to 2-0, but
Icefloe and Auroraveil remained losses and Drumlin fell 0-2.

## Decision and rollback

v162 is **rejected after the tied initial screen and one unsuccessful repair**;
the 60-game release gate was not justified. The handoff constants, branch, and
focused fixture were removed with `apply_patch`. Candidate Python is
byte-identical to immutable v0040 (`reports/iter-v162-primary-attacker-handoff/rollback-source-diff.txt`).
Rollback focused tests were **20/20**, compileall passed, and smoke was **4/4**
(`reports/local-20260818T004839Z`). No package, upload, activation, or live
baseline transition occurred.

## Remaining risk

The first-route deficit is not safely fixed by diverting a fixed attacker based
only on a round and Core-intel state. The next hypothesis should change a
different conversion mechanism and begin again from exact v0040 parity.
