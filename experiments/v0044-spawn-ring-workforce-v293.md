# v293 — spawn-ring workforce reservation (rejected)

## Objective

Test whether the optional core Conveyor ring was filling the same legal spawn
tiles needed for the stage-2 Builder wave. Fresh v107 Auroraveil evidence had
five candidate Builders by turn 4, no later Builder placements, and ring
Conveyors appearing from turns 18–30 while the opponent reached 9–13 Builders.

## Scope

The candidate temporarily packed the workforce target/living count into the
unused high bits of `SLOT_GUNNER_CAP`, gated core-ring construction and repair
while the target was pending, and added focused pack/gate tests. No target,
route, combat, or live-state policy changed. One bounded repair retained two
verified ring conveyors to preserve a delivery sink.

## Evidence

- Initial focused coverage: 33/33; compileall passed; smoke command-clean.
- Initial 15-map screen: `reports/local-20260819T173239Z`, 5–10 vs v0044;
  candidate delivery 13/15, with zero-delivery Drakkarfjord and Auroraveil.
- Repair focused coverage: 33/33.
- Repair screen: `reports/local-20260819T173557Z`, 8–7 and 15/15 delivery,
  but collection 42,080 vs 61,670 Ti.
- Independent all-map seed screen:
  `reports/local-20260819T173801Z`, 5–10 and collection 49,810 vs 80,070 Ti.
- No TLE, suspicious output, or command failure in either screen.

## Decision and rollback

The one-game first-screen edge was not repeatable and collection regressed, so
v293 was rejected. The signal, gates, and tests were removed. Recursive source
parity with immutable v0044 is zero diff at
`reports/iter-v293-spawn-ring/parity-after-revert.diff`.

Rollback focused coverage was 30/30, compileall passed, rollback smoke was
command-clean at `reports/local-20260819T174055Z`, and `make static` retained
the inherited deleted-module imports plus two navigation fast-path failures.
No promotion, package, upload, activation, or live transition occurred.
v105 remains the operational rollback target; live v107 was untouched.
