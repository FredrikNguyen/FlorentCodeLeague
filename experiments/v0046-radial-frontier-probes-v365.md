# v365 Radial frontier probes — rejected

Date: 2026-08-20

## Objective

Address the remaining topology-dependent late-ore/resource-conversion losses
seen in the v363/v364 screens while preserving exact immutable v0046.  When no
visible or advertised ore exists, the first bounded prospecting calls probe
several deterministic cardinal/diagonal waypoints around the Builder's
captured initial position.  The normal grid-stride explorer remains the
fallback, with the existing range, danger, blacklist, and navigation checks.

## Scope and non-goals

Candidate implementation is limited to `bots/candidate/bot/defender.py` and
`bots/candidate/bot/constants.py`, with temporary focused tests and the durable
plan/state/report files.  No route FSM, economy phase, Store slot, combat
policy, map literal, baseline snapshot, package, upload, activation, or live
state transition is part of this experiment.

## Evidence basis

v363's single Core-facing ray ended 16-14 across its paired screens; v364's
spawn-side lane ended 15-15 after its one repair.  Both were delivery-clean
but retained losses with later/fewer profitable chains on Royale, Ragnarok,
Fjordgate, Icefloe, Nordkap, and related maps.  v365 tests whether a short
multi-direction frontier ring discovers nearby ore without committing every
Builder to one side.

## Gate and rollback

Focused tests, compileall, static, and smoke must pass before two rotated
15-map screens.  Screen 1 must be at least 9-6 and delivery/reliability-clean;
the paired screens must be at least 19-11.  At most one bounded repair is
allowed.  Any failed gate restores exact recursive v0046 parity, preserves the
reports, removes temporary source/tests/configs, and records the rejection.

## Result

Focused coverage was **38/38** before and after the one repair; compileall
passed, smoke was **4/4** on both passes, and static retained only the
inherited failures.  The initial screen (`screen_seed=307`) scored **5-10**;
the repaired one-probe ring (`screen_seed=317`) scored **6-9**.  Both screens
were command/TLE/suspicious-clean and had **15/15** candidate deliveries, but
the pair was **11-19** and missed the **19-11** gate.

The hypothesis is rejected.  Candidate source is recursively byte-identical
to immutable v0046; the empty parity proof is
`reports/iter-v365-radial-frontier-probes/rollback-source-parity.diff`.
Rollback focused tests were **35/35**, compileall passed, rollback smoke was
**4/4**, and no release or live operation ran.  Screen loss evidence remains
under `screen1-analysis.json` and `screen2-analysis.json` for the next
conversion/topology hypothesis.
