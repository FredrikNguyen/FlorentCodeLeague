# v345 delivery-proof control handoff — rejected, v0046 retained

Date: 2026-08-20

## Objective and scope

Build on immutable local baseline
`bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`
with one top-team-informed control handoff: dynamic Builders may take a
nearest-owner enemy-Core Barrier turn only after the Core has proved a live
delivery route and a forward Sentinel exists.  The primary fixed attacker
kept its existing direct logistics/siege policy.  Production scope was
`bots/candidate/bot/attacker.py`, `bots/candidate/bot/dynamic.py`, and one
focused delivery-proof test.  No Store schema, Core spawn policy, fixed
identity, route geometry, baseline, package, platform, or live-state change
was allowed.

## Replay basis

The v344 Icefloe failure had two Harvesters and 46 conveyors but no titanium
delivery, while v0046 delivered 12 routes.  Top-team samples showed that
control shells are useful only after a paying route is live.  v345 therefore
added a Core-phase delivery proof, a nearest dynamic control owner, and a
bounded Barrier handoff.  The first implementation incorrectly applied the
proof to the existing fixed-attacker Barrier path and regressed seed 179;
that path was restored in repair 1.  Repair 2 tightened only the new dynamic
handoff to the stable `PRESSURE` phase so “converting” could not spend on
control while income was still settling.

## Evidence

- Initial focused delivery/economy/nearest coverage: **34/34**;
  compileall passed; inherited `make static` profile remained exit 2; smoke
  was **4/4**.  The first concurrent screen collided on its UTC report id and
  is retained only as a log (`reports/local-20260820T093045Z`), not scored.
- Initial valid screens were seed 173 **7-8**, **62,450 vs 74,800 Ti**, and
  seed 179 **3-12**, **41,600 vs 59,250 Ti**.  Both valid screens delivered;
  reports are `reports/iter-delivery-proof-v345-screen-seed173-analysis.json`
  and `reports/iter-delivery-proof-v345-screen-seed179-rerun-analysis.json`.
- Repair 1 focused coverage/compileall/smoke passed.  Seed 173 was **7-8**
  (**71,470 vs 75,100 Ti**) and seed 179 was **9-6** (**55,200 vs 50,570
  Ti**); all 30 candidate rows delivered.  Combined result: **16-14** and
  **126,670 vs 125,670 Ti** (+1,000 Ti).  Reports:
  `reports/iter-delivery-proof-v345-repair1-screen-seed173-analysis.json`,
  `reports/iter-delivery-proof-v345-repair1-screen-seed179-analysis.json`.
- Repair 2 focused coverage/compileall/smoke passed.  Seed 173 improved to
  **8-7** (**92,170 vs 75,570 Ti**, +16,600 Ti), but seed 179 fell to **6-9**
  (**75,210 vs 81,470 Ti**, -6,260 Ti).  Both were delivery-clean; combined
  result was **14-16** despite **167,380 vs 157,040 Ti** (+10,340 Ti).
  Reports:
  `reports/iter-delivery-proof-v345-repair2-screen-seed173-analysis.json`,
  `reports/iter-delivery-proof-v345-repair2-screen-seed179-analysis.json`.

## Decision and rollback

The two rotated screens did not provide a repeatable win-rate/conversion
edge, so the release gate was not run.  After the second bounded repair,
`attacker.py` and `dynamic.py` were restored byte-for-byte to immutable v0046;
the temporary focused test was removed.  Rollback coverage was **31/31**,
compileall passed, and rollback smoke was **4/4** at
`reports/local-20260820T094817Z`.  Source parity was verified with `diff -qr`
for the candidate and immutable `bot/` trees.  No promotion, package, upload,
activation, or live-state transition occurred; live v108 and the v0046 local
baseline remain unchanged.

## Remaining risk / next hypothesis

The result confirms that a delivery proof is necessary but not sufficient:
pressure-phase-only control improved one rotation and harmed another.  The
next experiment must be a genuinely different workforce architecture—an
explicit map-aware economy/pressure lease that keeps route owners productive
and assigns sabotage/defense to surplus builders—rather than another Barrier
or phase-threshold knob.  It must first explain the seed-179 long-board
Harvester/conveyor deficit against the top-team control/economy split before
any release gate or platform operation.
