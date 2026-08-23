# v361 — designated-defense action order

## Objective and replay basis

Keep immutable v0046 as the comparator.  The fresh v108/top-team replay sample
shows underbuilt home shells.  The Core already writes one designated Builder
for the next Gunner, but the Defender FSM currently attempts another Harvester
before using that designation, so a route opportunity can starve the defense
action.

## Hypothesis and scope

After the existing ring, belt-repair, and orphan-reconnect checks, let a
Core-designated Builder attempt its legal home Gunner before attempting a new
Harvester.  The `_try_build_gunner` guard still enforces the designation,
dynamic cost, position band, belt protection, and `can_build_gunner`; all other
Builders retain the old Harvester-first behavior.

Allowed production/test scope is `bots/candidate/bot/defender.py` and
`tests/test_candidate_economy_phase.py`.  No cap, reserve, Store schema,
route geometry, fixed role, attacker, or platform state changes.

## Validation

Focused coverage was **32/32**, compileall passed, and `make smoke` was **4/4**.
`make static` retained only the inherited 15 obsolete imports and two
navigation assertions (exit 2).  The initial rotated v0046-pinned screen at
`reports/local-20260820T171547Z` scored **5-10**, command/TLE/suspicious/
delivery-clean.  The one bounded repair added a dynamic-cost Harvester plus
two-conveyor reserve around the preemption; focused coverage stayed **32/32**,
and the repaired screen at `reports/local-20260820T172138Z` scored **8-7**.
It was also clean: 15/15 command-clean, zero TLEs, zero suspicious rows, all
candidate deliveries present, maximum p99/peak **1,333/3,174 us**.

## Decision

v361 is **rejected** after its single allowed repair because the first-screen
floor is **9-6**.  Candidate production source was restored to exact recursive
v0046 parity at
`reports/iter-v361-designated-defense-action-order/rollback-source-parity.diff`
(empty).  Rollback focused coverage was **31/31**, compileall passed, and
rollback smoke was **4/4** at
`reports/iter-v361-designated-defense-action-order/rollback-smoke-final.log`.
No second screen, release matrix, remote gate, package, upload, activation, or
baseline update ran; immutable v0046 remains the comparator.
