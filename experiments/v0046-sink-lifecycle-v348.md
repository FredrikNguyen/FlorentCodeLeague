# v348 sink/path lifecycle — rejected, v0046 retained

Date: 2026-08-20

## Objective and scope

Build on immutable local baseline
`bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`
with a route-sink lifecycle change.  A normal chain received a bounded
move/build-round budget, recorded its Harvester origin on failure, and opened
a short recovery window before that Builder could purchase another source.
The first bounded repair traced the failed source's visible fixed-output belt
frontier and seeded the first verified gap; the second repair made that repair
strictly local so a distant frontier could not pull a worker off the economy.

Allowed production scope was `bots/candidate/bot/defender.py`; focused coverage
was in the temporary `tests/test_candidate_sink_lifecycle.py`.  Store schema,
Core spawn policy, fixed identities, route geometry, attacker policy,
immutable snapshots, package, platform, and live state were non-goals.

## Replay basis and implementation

The v347 replay audit (`reports/iter-sink-lifecycle-v348-replay-audit.json`)
showed late first delivery on Royale/Auroraveil and chains that spent many
rounds skipping unbuildable tiles while placing conveyors.  The initial
candidate bounded chain travel and delayed replacement-source spending. Repair
1 added a local route-origin marker and a bounded visible frontier walk that
could seed a gap after a failed chain.  That repair regressed because the
recovering Builder navigated across the map. Repair 2 retained frontier
seeding only when the gap was already adjacent, restoring workforce mobility.

## Validation

- Initial focused coverage was **34/34**; repair 1 and repair 2 were **35/35**.
  Compileall passed for every candidate.  Inherited `make static` remained
  exit 2 with the obsolete candidate-module imports and two navigation
  fast-path assertions; no new production-budget failure appeared.
- Smoke was **4/4 command-clean** for the initial candidate, both repairs, and
  rollback.  Rollback focused coverage was **31/31**, compileall passed, and
  source parity is empty at
  `reports/iter-sink-lifecycle-v348-rollback-source-parity.diff`.
- Initial rotated screens were seed-173 **10-5** / **83,570 vs 79,780 Ti** and
  seed-179 **7-8** / **57,430 vs 61,710 Ti** (combined **17-13** but
  **141,000 vs 141,490 Ti**).  Both were delivery-clean, with zero TLE or
  suspicious rows; max p99/peak callback time was **1,371/5,692 us**.
- Repair 1 screens were seed-173 **6-9** / **77,160 vs 62,810 Ti** and
  seed-179 **5-10** / **67,600 vs 83,140 Ti** (combined **11-19** and
  **144,760 vs 145,950 Ti**).  Repair 2 screens were seed-173 **9-6** /
  **90,550 vs 74,230 Ti** and seed-179 **6-9** / **109,330 vs 109,970 Ti**
  (combined **15-15** and **199,880 vs 184,200 Ti**).  Both repair rotations
  were delivery-clean with zero TLE/suspicious rows; repair-2 max p99/peak
  was **1,364/4,959 us**.  Analyses are under
  `reports/iter-sink-lifecycle-v348-*-analysis.json`.

## Decision and rollback

Reject v348: the collection surplus in repair 2 did not become a repeatable
win-rate edge, and the initial 17-13 edge disappeared on the rotated screen.
After the two permitted repairs, restore `bots/candidate/bot/defender.py`
byte-for-byte to immutable v0046 and delete the temporary focused test.  No
release gate, promotion, package, upload, activation, or live transition
occurred; live v108 remains `active_observing` and immutable v0046 remains the
local baseline.

## Remaining risk and next direction

The chain timer and local frontier marker are safe but not sufficient: losses
still come from low Harvester/workforce conversion on long or contested maps,
not only from a visible sink gap.  Do not retry the timer/frontier design
unchanged.  The next fundamental rewrite should inspect top-team route
throughput and resource-to-pressure timing, then change a complete role/task
contract while preserving the no-idle and protected-map gates.
