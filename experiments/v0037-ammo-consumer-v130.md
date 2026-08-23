# v130 — ammo consumer contract (rejected)

## Objective

Use replay evidence showing that most losses never retained a forward Sentinel
while still ending with excess ammo. The candidate gated Core conversion on a
known friendly Gunner/Sentinel consumer; repair 1 restored the established
prestock/threat buffer and allowed the floor during a visible threat.

## Scope

- `bots/candidate/bot/core_role.py`
- `tests/test_candidate_nearest_defense.py`
- `reports/iter-ammo-consumer-v130-*` logs and replay-analysis JSON files

No route FSM, attacker, dynamic worker, package, upload, activation, or live
state change was allowed.

## Evidence

- Focused checks: 26/26 initial and repair; rollback 23/23.
- Compileall passed for initial, repair, and rollback.
- `make static` retained the inherited exit 2 from 15 obsolete imports and two
  navigation fast-path assertions.
- Initial 24-game screen: 9-15, 84,400 versus 89,660 collected titanium,
  one versus zero no-delivery rows, first delivery 35.8 versus 26.1 turns,
  zero command failures/TLE/suspicious output, and maximum p99 1,584 us.
- Repair 1 24-game screen: 15-9, with zero no-delivery rows, zero command
  failures/TLE/suspicious output, 94,110 versus 88,790 collected titanium,
  first delivery 25.6 versus 41.0 turns, and maximum p99 1,415 us.
- Repair 1 54-game checkpoint: 25-29, 151,620 versus 167,020 collected
  titanium, zero versus two no-delivery rows, first delivery 41.6 versus 42.8
  turns, zero command failures/TLE/suspicious output, maximum p99 1,362 us,
  and map floors archipelago 2/6 and nordkap 1/6. The short edge did not
  persist.

## Decision

Reject after two bounded attempts. The consumer helper, conversion gates, and
focused tests were removed with `apply_patch`; candidate source was restored
byte-for-byte to immutable v0037. Rollback focused/compile/smoke passed
(23/23, compile clean, 4/4; rollback smoke report
`reports/local-20260817T101344Z`). No 210-game gate, package, upload,
activation, or live baseline change was performed.

## Next hypothesis

Use a different replay-backed structural change; do not retest ammo conversion
gates or route-opening deferrals without new evidence.
