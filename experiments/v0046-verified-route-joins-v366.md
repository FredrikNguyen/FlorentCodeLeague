# v366 Verified route joins — rejected

Date: 2026-08-20

## Objective

Address the positive-delivery but low-throughput losses in the v364/v365
screens without changing opening or combat behavior.  Once the team has a
completed route, allow a new chain to join a visible friendly conveyor only
when a bounded cardinal orientation walk proves that the existing belt reaches
the Core.  Unknown tiles, splitters, cycles, wrong-team buildings, and a
pre-milestone economy all retain the old no-merge behavior.

## Scope and non-goals

Candidate implementation is limited to `bots/candidate/bot/defender.py` and
`bots/candidate/bot/constants.py`, with temporary focused tests and the durable
plan/state/report files.  No opening selector, economy phase, Store slot,
splitter policy, combat policy, map literal, baseline snapshot, package,
upload, activation, or live state transition is part of this experiment.

## Evidence basis

v364 ended 15-15 and v365 ended 11-19 despite 15/15 candidate deliveries on
both screens.  Several losses had equal or higher Harvester counts but much
less collected titanium, consistent with long independent chains and delayed
conversion.  v366 tests a verified sink join only after an earlier route has
already proven the Core path.

## Gate and rollback

Focused tests, compileall, static, and smoke must pass before two rotated
15-map screens.  Screen 1 must be at least 9-6 and delivery/reliability-clean;
the paired screens must be at least 19-11.  At most one bounded repair is
allowed.  Any failed gate restores exact recursive v0046 parity, preserves the
reports, removes temporary source/tests/configs, and records the rejection.

## Result

Focused route/economy/seeded/defense coverage was **39/39**, compileall passed,
smoke was **4/4**, and static retained only the inherited failures.  The first
screen (`screen_seed=331`) scored **2-13** with 15/15 candidate deliveries and
zero TLE/suspicious rows; it missed the 9-6 first-screen floor, so no repair or
second screen ran.

The hypothesis is rejected.  Candidate source is recursively byte-identical
to immutable v0046; the empty parity proof is
`reports/iter-v366-verified-route-joins/rollback-source-parity.diff`.
Rollback focused tests were **35/35**, compileall passed, rollback smoke was
**4/4**, and no release or live operation ran.  The route-join implementation
was removed after the severe conversion regression.
