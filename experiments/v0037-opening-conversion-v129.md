# v129 — pre-delivery conversion reserve (rejected)

## Objective

Preserve capital for the first Harvester route by reserving one Harvester and
four conveyor costs while no completed route exists. A bounded repair also
suppressed discretionary floor/buffer conversion until a route or live threat
was visible.

## Scope

- `bots/candidate/bot/core_role.py`
- `tests/test_candidate_nearest_defense.py`
- `reports/iter-opening-conversion-v129/`

No route FSM, attacker, dynamic worker, package, upload, activation, or live
state change was allowed.

## Evidence

- Focused checks: 25/25 initial, 26/26 repair, 23/23 rollback.
- Compileall passed for initial, repair, and rollback.
- `make static` retained the inherited exit 2 from obsolete imports and two
  navigation fast-path assertions.
- Initial 24-game screen: 13-11, 73,400 versus 53,670 collected titanium;
  zero versus two no-delivery rows; first delivery 25.8 versus 19.2 turns;
  maximum p99 1,580 us.
- Initial 54-game checkpoint: 30-24, 181,240 versus 174,660 collected
  titanium; two versus four no-delivery rows; first delivery 33.7 versus
  28.5 turns; maximum p99 1,461 us.
- Repair 1 24-game screen: 12-12, 110,010 versus 100,920 collected titanium;
  zero versus one no-delivery row; first delivery 23.8 versus 24.0 turns;
  maximum p99 1,356 us. No 54-game repair was run because the short screen
  did not qualify.

## Decision

Reject after the bounded repair. The Core reserve and conversion gate and
focused tests were removed with `apply_patch`; candidate source was restored
byte-for-byte to immutable v0037. Rollback focused/compile/smoke passed
(23/23, compile clean, 4/4; see the rollback logs and local report in the
  report directory). No 210-game gate, package, upload, activation, or live
baseline change was performed.

## Next hypothesis

Inspect v0037 conversion losses and test one different threat-aware
ammo/defense policy without changing the route FSM.
