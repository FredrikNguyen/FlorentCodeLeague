# v364 Spawn-side opening lanes — rejected

Date: 2026-08-20

## Objective

Address topology-specific late-ore/no-delivery openings seen in the v363 loss
screen while preserving exact immutable v0046 as the comparator.  If no
visible or advertised ore exists, only the first bounded prospecting calls use
the Builder's actual spawn-side relative to the Core as a cardinal lane.  The
existing row-major/grid-stride exploration remains the fallback and all normal
blacklist, danger, range, and navigation checks remain in force.

## Scope and non-goals

Candidate implementation is limited to `bots/candidate/bot/defender.py` and
`bots/candidate/bot/constants.py`, with temporary focused tests and the durable
plan/state/report files.  No route FSM, economy phase, Store slot, combat
policy, map literal, baseline snapshot, package, upload, activation, or live
state transition is part of this experiment.

## Evidence basis

The v363 outer-board ray scored 7-8 and 9-6 across rotated 15-map screens,
ending 16-14 with one no-delivery row.  Its loss set included Royale,
Frostgate, Valkyrie, Icefloe, Ragnarok, Archipelago, Midgard, Fjordgate, and
Antler, which is consistent with a single Core-facing direction not matching
each spawn topology.  v364 tests whether the already-observed local spawn side
is a safer early prior without changing later exploration.

## Gate and rollback

Focused tests, compileall, static, and smoke must pass before two rotated
15-map screens.  Screen 1 must be at least 9-6 and delivery/reliability-clean;
the paired screens must be at least 19-11.  At most one bounded repair is
allowed.  Any failed gate restores exact recursive v0046 parity, preserves the
reports, removes temporary source/tests/configs, and records the rejection.

## Result

Focused coverage was **39/39** before and after the one repair; compileall
passed, smoke was **4/4** on both passes, and static retained only the
inherited failures.  The initial screen (`screen_seed=281`) scored **8-7**;
the repaired screen (`screen_seed=293`) shortened the lane budget from four
to two calls and scored **7-8**.  Both screens were command/TLE/suspicious-
clean and had **15/15** candidate deliveries, but the pair was **15-15** and
missed the **19-11** gate.

The hypothesis is rejected.  Candidate source is recursively byte-identical
to immutable v0046; the empty parity proof is
`reports/iter-v364-spawn-side-opening-lanes/rollback-source-parity.diff`.
Rollback focused tests were **35/35**, compileall passed, rollback smoke was
**4/4**, and no release or live operation ran.  Screen loss evidence remains
under `screen1-analysis.json` and `screen2-analysis.json` for the next
topology/conversion hypothesis.
