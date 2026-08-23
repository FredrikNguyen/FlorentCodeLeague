# v131 — second-attacker economy rejoin (rejected)

## Objective

Replay losses on Yulerune and related long maps showed fewer harvesters and
conveyors while the second fixed attacker had no confirmed Core or Sentinel
progress. The candidate reassigned only that second attacker to the existing
Defender economy/repair loop after three completed chains and a bounded
no-sighting epoch; the first attacker remained on the direct lane.

## Scope

- `bots/candidate/bot/attacker.py`
- `bots/candidate/bot/constants.py`
- `tests/test_candidate_nearest_defense.py`
- `reports/iter-attacker-economy-rejoin-v131-*`

No alternate-Core search, guessed Sentinel, route FSM, ammo, package, upload,
activation, or live state change was allowed.

## Evidence

- Focused checks: 24/24 initial and repair; rollback 23/23.
- Compileall passed for initial, repair, and rollback.
- `make static` retained the inherited exit 2 from obsolete imports and two
  navigation fast-path assertions.
- Initial 24-game screen: 9-15, 68,960 versus 91,640 collected titanium,
  zero no-delivery rows, first delivery 26.3 versus 24.8 turns, zero command
  failures/TLE/suspicious output, maximum p99 1,480 us.
- Repair 1 restricted the handoff off cramped maps. It scored 8-16,
  84,010 versus 117,540 collection, zero no-delivery rows, first delivery
  27.5 versus 23.3 turns, zero command failures/TLE/suspicious output, and
  maximum p99 1,441 us. Map floors included fjordgate 0/4 and ragnarok 1/4.

## Decision

Reject after two bounded attempts. The handoff constant, branch, and focused
test were removed with `apply_patch`; candidate source was restored
byte-for-byte to immutable v0037. Rollback focused/compile/smoke passed
(23/23, compile clean, 4/4; rollback smoke
`reports/local-20260817T102958Z`). No 54/210 gate, package, upload,
activation, or live baseline change was performed.

## Next hypothesis

Use a different replay-backed structural change; do not repeat this attacker
handoff without new evidence.
