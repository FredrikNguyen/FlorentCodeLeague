# v274 route-preserving opening receiver — rejected after one repair

Date: 2026-08-19

## Hypothesis and scope

Fresh v107 GlacierKeep evidence and v273 diagnostics showed the Defender
building all eight Core-adjacent receiver Conveyors before the first
Harvester route. v274 deferred Dynamic Builder ring errands until the first
completed route and capped opportunistic pre-route receivers. The bounded
scope was `bots/candidate/bot/defender.py`, one constant, and focused ring
tests; workforce, route search, combat, Store, packaging, submission, and
live-state operations were excluded.

## Initial candidate

The initial cap was two receiver tiles. Focused coverage passed **34/34**,
compileall passed, smoke was **4/4**, and `make static` retained the inherited
deleted-module imports and two navigation assertions. The screen pair against
exact v0044 was command-clean with zero TLE/suspicious rows:

| screen | candidate wins | collection Ti | first delivery | max p99/peak us |
| --- | ---: | ---: | ---: | ---: |
| seed 172 | 6-9 | 74,940 vs 72,780 | 15/15 vs 14/15 | 1,291/6,041 |
| seed 175 | 7-8 | 60,140 vs 57,680 | 15/15 vs 15/15 | 1,315/2,413 |

The initial aggregate was **13-17**. Replay review showed the cap preserved
delivery coverage but made some long-board routes extremely late (for example
GlacierKeep/AuroraVeil), so it did not meet the paired win criterion.

## One bounded repair

The sole repair raised the receiver allowance to four tiles while retaining
the no-Dynamic-ring-walk opening gate. Focused coverage remained **34/34**,
compileall passed, smoke was **4/4**, and static retained the inherited
failures. Both repaired screens remained reliability-clean:

| screen | candidate wins | collection Ti | first delivery | max p99/peak us |
| --- | ---: | ---: | ---: | ---: |
| seed 172 | 9-6 | 63,960 vs 55,990 | 15/15 vs 15/15 | 1,228/5,389 |
| seed 175 | 6-9 | 63,280 vs 83,610 | 15/15 vs 15/15 | 1,487/2,541 |

The repaired aggregate was **15-15** with collection **127,240 vs 139,600
Ti**. It did not beat exact v0044, so no 60-game gate, remote gate, package,
submission, activation, or live transition was justified.

## Rollback

The candidate source was restored recursively to exact v0044 parity; the
rollback source diff has zero lines. Rollback focused coverage passed **31/31**,
compileall passed, smoke was **4/4**, and static retained the inherited exit
2. Reports are in:

- `reports/live-observe-20260819T114622Z/`
- `reports/live-v107-diagnosis/`
- `reports/iter-v274-opening-receiver/`
- `reports/local-20260819T121223Z`
- `reports/local-20260819T121425Z`
- `reports/local-20260819T121737Z`
- `reports/local-20260819T121923Z`
- `reports/local-20260819T122205Z`

v0044 remains the moving local baseline. v107 remains active-observing;
v101 remains the guarded operational rollback because the requested v105
historical reference is known bad at 142/275 (51.64%). The route-order idea
should not be widened without a new causal signal; the next experiment should
target the late-delivery/chain-recovery path directly.
