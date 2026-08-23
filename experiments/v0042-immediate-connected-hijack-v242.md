# v242 immediate connected-source hijack — rejected

## Objective and evidence

Test the user's own-infiltration hypothesis without reopening the rejected
long-route hijack and sabotage variants. A dynamic Builder could prefer one
visible enemy Harvester only when its hostile logistics outlet was visible, an
empty adjacent seed tile was immediately buildable, the Builder was the
nearest non-fixed responder, and dynamic prices left a Harvester-plus-two-
Conveyor reserve. The branch never walked toward a source and did not change
the fixed attacker's forward lane.

## Allowed files

- `bots/candidate/bot/dynamic.py`;
- `tests/test_candidate_nearest_defense.py`;
- this record, `UPDATES.md`, and durable report/state metadata.

## Non-goals

No opening workforce, normal route FSM, fixed-attacker sabotage, Launcher,
Barrier, Sentinel/Gunner/ammo policy, Store schema, map branch, baseline or
archive change, package, upload, activation, or live-state operation. The
temporary task was limited to an already-adjacent action and retained dynamic
cost queries and nearest ownership.

## Validation

- New legality/ownership checks plus nearest-defense/seeded-route coverage:
  **30/30**; candidate compileall passed.
- `make static` retained the inherited exit 2: 15 obsolete deleted-module
  imports and two navigation fast-path assertions. No v242-specific static
  error appeared (`reports/iter-v242-immediate-hijack/rollback-static.log`).
- `make smoke` was **4/4** command-clean at
  `reports/local-20260819T013816Z`; the rollback smoke was also **4/4** at
  `reports/local-20260819T014208Z`.
- The rotated 15-map screen was command/delivery-clean with zero TLE or
  suspicious rows, but candidate-A lost **5-10**, collected **85,780 vs
  88,400 Ti**, and placed fewer Harvesters (**116 vs 123**), Conveyors
  (**1,510 vs 1,855**), Sentinels (**55 vs 68**), and Barriers (**60 vs 91**).
  Both sides delivered on all 15 rows. Raw report:
  `reports/local-20260819T013838Z`; parsed diagnostics:
  `reports/iter-v242-immediate-hijack/replay-analysis.json`.

## Decision and rollback

Reject v242 without a repair or long gate. The immediate steal preempted
productive logistics without a paired win or collection edge. The temporary
source and test edits were removed; candidate source is recursively
byte-identical to immutable v0042 (`reports/iter-v242-immediate-hijack/rollback-source.diff`).
Rollback focused coverage was **27/27**, compileall passed, and static kept the
inherited failures. No promotion, package, upload, activation, or live-state
transition occurred.

## Follow-up

The two directions now have the same result: route-radius infiltrations are
rare, and both broad and immediate enemy-source hijack variants spend more
logistics than they return. Do not retry this target-quality branch without a
new causal replay signal. Choose the next high-frequency resource-to-pressure
hypothesis while keeping the fixed attacker on its direct lane.
