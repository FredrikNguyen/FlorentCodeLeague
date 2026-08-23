# v303 emergency anti-Launcher home defense

Date: 2026-08-19

## Hypothesis

Fresh v107 losses showed enemy Launchers reaching the opening area before the
candidate had a completed route.  A Launcher can pick up a Builder from either
team, so the existing pre-route Gunner prohibition may leave the opening
workforce without a ranged response.  One bounded exception was tested: the
Core-designated home defender could use the existing Gunner placement path
before the first route only when a visible enemy Launcher was inside the
existing home radius.

## Scope

Temporary production changes were limited to `bots/candidate/bot/defender.py`
and focused tests in `tests/test_candidate_nearest_defense.py`.  The normal
Core designation, lifetime cap, reserve, placement, facing, and action legality
checks were unchanged.  No Store/schema, role, route, dynamic task, Launcher,
Barrier, Sentinel, map, package, upload, activation, or live-state changes
were made.

## Validation

- Initial focused nearest-defense/seeded-route/economy coverage: **36/36**.
- Initial compileall: pass.
- Initial `make static`: inherited failure profile (15 obsolete removed-module
  imports and two navigation fast-path assertions).
- Initial smoke: **4/4** command-clean at
  `reports/local-20260819T202610Z`.
- Initial 15-map screen (`reports/local-20260819T202638Z`): **5-10**,
  collection **51,970 vs 64,840 Ti**, all commands clean. Replay analysis
  recorded zero TLE/suspicious rows, max p99/peak **1,440/2,582 us**. No local
  comparator game placed a Launcher, so the new branch was not exercised.

## Bounded repair

The exception could have authorized a second early home Gunner under delayed
Store state.  The one allowed repair rejected the exception whenever a visible
friendly home Gunner already existed and added a regression test for the
single-turret bound.

- Repair focused coverage: **37/37**.
- Repair compileall: pass.
- Repair `make static`: same inherited failures only.
- Repair smoke: **4/4** command-clean at
  `reports/local-20260819T202953Z`.
- Repair screen (`reports/local-20260819T203012Z`): **8-7**, all 15 first
  deliveries, collection **69,010 vs 55,030 Ti**, zero TLE/suspicious rows,
  max p99/peak **1,440/2,582 us**.
- Independent screen (`reports/local-20260819T203157Z`): **6-9**,
  collection **55,430 vs 64,320 Ti**, 14/15 first deliveries for each side,
  zero TLE/suspicious rows, max p99/peak **1,280/2,203 us**.

The 8-7 result was not repeatable and the local schedule did not contain the
target threat.  No longer gate was justified.

## Decision and rollback

Reject v303.  The temporary helper, import, and tests were removed.  Recursive
production-source parity with immutable
`bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f` is zero in
`reports/iter-v303-anti-launcher/rollback-source-parity.diff`.

- Rollback focused coverage: **34/34**.
- Rollback compileall: pass.
- Rollback smoke: **4/4** command-clean at
  `reports/local-20260819T203405Z`.
- No package, upload, activation, or live transition occurred.
- Live v107 remains `active_observing`; v105 remains the operational rollback.

Full logs and replay analyses are under `reports/iter-v303-anti-launcher/`.
