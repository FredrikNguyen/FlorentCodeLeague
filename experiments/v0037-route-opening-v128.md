# v128 — defer long-distance core-ring maintenance (rejected)

## Objective

Address v0037's slow first delivery by preventing dynamic Builders from
walking to a Core-ring gap before the first completed Harvester chain. The
opening already assigns every non-attacker to economy; the ring is maintenance
and the first chain can feed the Core directly. A repair restored the adjacent
idle fallback while keeping only the long-distance dynamic task deferred.

## Scope

- `bots/candidate/main.py`
- `bots/candidate/bot/defender.py`
- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- `reports/iter-route-opening-v128/`

No attacker, ammo, Store, workforce, package, upload, activation, or live state
change was allowed.

## Evidence

- Focused checks: 24/24 initial and repair; rollback 23/23.
- Compileall: passed initial, repair, and rollback.
- `make static`: inherited exit 2 from obsolete imports and navigation
  assertions (`static.log`).
- Initial 24-game screen: 13-11, 94,670 versus 87,670 collected titanium,
  zero no-delivery rows, max p99 1,431 us.
- Initial 54-game checkpoint: 24-30, 168,460 versus 165,630 collection,
  first delivery 52.5 versus 37.6 turns, one no-delivery row per side,
  zero command failures/TLE/suspicious output, max p99 1,497 us.
- Repair 1 24-game screen: 14-10, 62,180 versus 69,250 collection, first
  delivery 23.1 versus 26.7 turns, zero no-delivery rows, max p99 1,393 us.
- Repair 1 54-game checkpoint: 20-34, 137,780 versus 186,410 collection,
  first delivery 63.7 versus 36.5 turns, one versus three no-delivery rows,
  zero command failures/TLE/suspicious output, max p99 1,395 us.

## Decision

Reject after one bounded repair. All route-opening edits and the focused test
were removed with `apply_patch`; candidate source compares byte-for-byte with
immutable v0037. Rollback focused/compile/smoke passed (23/23, compile clean,
4/4; `reports/local-20260817T093403Z`). No package, 210-game gate, upload,
activation, or baseline transition was performed.

## Next hypothesis

Use replay evidence to test one conversion-side change that preserves the
route FSM: keep the Core's pre-first-delivery ammo floor from consuming the
last route capital, while retaining the established reserve and siege buffer
after a completed route. Gate only the new behavior with focused Core tests and
the same short comparison.
