# v336 finite utility lease

## Objective

Replace the dynamic Builder pool's purely local greedy handoff with one
Core-designated, rotating utility owner.  The owner would run the verified
economy/repair loop for a 24-round epoch, then release and rotate; local home
threats, belt repairs, and damaged-building repairs remained higher priority.

## Scope

Temporary production scope was `bots/candidate/bot/constants.py`,
`bots/candidate/bot/core_role.py`, and `bots/candidate/bot/dynamic.py`, with
focused coverage in `tests/test_candidate_economy_phase.py`.  The lease used
the unused high bits of `SLOT_GUNNER_CAP` for an owner and epoch.  Opening
spend, route geometry, fixed attacker behavior, baseline snapshots, and live
platform state were out of scope.

## Evidence and repairs

- Initial implementation focused coverage passed **33/33**, compileall passed,
  `make static` retained the inherited 15 import errors and two navigation
  assertions, and smoke was **4/4**.
- The first screen was command-clean but functionally invalid: **0-15**, no
  candidate buildings or deliveries.  Replay analysis exposed a caught Core
  exception caused by an undefined `harvester_count` in `_update_defense`
  (`reports/iter-v336-utility-screen.log`).
- Repair 1 fixed that defect.  Focused coverage stayed **33/33**, smoke was
  **4/4**, and the screen became **2-13**, collection **66,240/125,170 Ti**,
  first delivery **36.1/25.4** turns
  (`reports/local-20260820T054013Z`).
- Repair 2 moved the lease from healthy `PRESSURE` to sub-five-chain
  `CONVERTING`, based on replay diagnosis.  Focused coverage passed **33/33**,
  static retained only the inherited failures, smoke was **4/4**, but the
  screen remained negative at **4-11**, collection **73,220/79,090 Ti**, and
  first delivery **32.7/96.8** turns
  (`reports/local-20260820T054434Z`).

## Decision

Reject v336 after the two bounded repair attempts.  The lease did not improve
paired wins and its healthy-phase version materially starved offensive/defense
conversion; the conversion-phase version still lacked an aggregate edge.
Restore recursive production parity with immutable v0046 and keep v0046 as the
moving baseline.  No package, upload, activation, or live-state transition
occurred.

## Remaining risks and next direction

The failure is not solved by one globally leased economy worker.  Loss replays
still show route throughput and defensive topology diverging by map, so the
next hypothesis should assign a utility only from verified local defects (a
broken route, damaged home shell, or reachable siege target) and release it
immediately when that defect is gone, rather than forcing a timed workforce
lease.
