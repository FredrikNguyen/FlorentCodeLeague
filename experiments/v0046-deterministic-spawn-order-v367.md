# v367 — Deterministic Core spawn ordering

## Hypothesis

The candidate's Core spawn ring is already legal and stable, but
`random.shuffle` uses process-global state that the competition seed does not
control.  A deterministic round-robin cursor should remove roster/opening-lane
variance without changing the legal tiles or the role contract.

## Scope

Temporary change is limited to `bots/candidate/bot/core_role.py` plus focused
tests.  v0046 is frozen at
`bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`.
No release, upload, activation, or live-state change is allowed before both
screen gates pass.

## Gate

- Focused tests, compileall, inherited static profile, and 4-game smoke pass.
- Rotated 15-map screen 1: at least 9-6, 15/15 deliveries, zero TLE/suspicious.
- After screen 1 passes, rotated screen 2; pair at least 19-11 with the same
  reliability floors.
- Only a passing pair may proceed to the pinned 60-game release gate.

## Result

Focused deterministic/economy/seeded/defense coverage was **37/37**,
compileall passed, initial smoke was **4/4**, and `make static` retained only
the inherited failures.  Screen 1 (`screen_seed=347`) scored **5-10** with
15/15 candidate deliveries, zero TLE/suspicious rows, max p99 1195 us, and
max peak 4250 us.  The 9-6 first-screen floor failed, so no repair or second
screen ran.

v367 is rejected.  Candidate source was restored to exact recursive v0046
parity (empty proof at
`reports/iter-v367-deterministic-spawn-order/rollback-source-parity.diff`),
the temporary test/config were removed, rollback focused tests were **35/35**,
compileall passed, and rollback smoke was **4/4**.  No release matrix,
remote gate, package, upload, activation, or baseline update ran.

For variance context, immutable v0046 played itself on the same one-sided
screen schedule and scored **6-9**, with 15/15 deliveries and aggregate
collection **77,190 vs 86,160 Ti**.  That control is diagnostic only; it does
not promote v367 or alter the comparator.  Evidence is preserved at
`reports/local-20260820T192137Z` and
`reports/iter-v367-deterministic-spawn-order/control-screen347-analysis.json`.
