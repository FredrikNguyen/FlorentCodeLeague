# v335 post-delivery siege phase

## Objective

Convert the existing enemy-Core cage from a fixed six-Barrier cap into a
phase-gated siege shell after the Core has published at least five healthy
Harvester chains and `PRESSURE`.  The candidate must preserve the opening
Launcher relay, route construction, and crisis recovery while giving the
existing attacker a finite late control objective.

## Scope

Production scope was limited to `bots/candidate/bot/constants.py` and
`bots/candidate/bot/attacker.py`.  The temporary Defender-side suppression
predicate was removed during review because it had no production caller.  No
Store schema, route FSM, baseline snapshot, platform state, or live operation
changed.

## Evidence

- Initial focused run: 39/39; compileall passed; smoke 4/4; static retained
  the inherited 15 stale-module import errors and two navigation assertions.
- Initial 15-map screen: 7-8, so the candidate received one bounded repair.
- Repair 1 removed the unused Harvester suppression path while retaining the
  phase-gated cage.  Focused coverage passed 39/39 and smoke 4/4.
- Repair 1 15-map screen: 10-5, 90,010/72,070 collected Ti, all 15 commands
  clean, and no reliability failures (`reports/local-20260820T051749Z`).
- Full 60-game gate: 33-27, 307,900/306,930 collected Ti, all commands clean,
  zero TLE/suspicious rows, max p99/peak 1,436/5,241 us
  (`reports/local-20260820T052022Z`).
- Cleanup removed the dead Defender predicate; focused tests passed, compileall
  passed, and smoke 4/4 (`reports/local-20260820T052916Z`).

## Decision

Promote this candidate as the new local immutable baseline `v0046` because it
clears the paired 60-game threshold without a reliability or protected-map
collapse.  The margin is modest and economy is essentially tied, so this is a
development baseline rather than evidence of live superiority.  Keep v0045 as
the rollback snapshot; no upload, activation, or live-state transition is part
of this checkpoint.

## Risks and next hypothesis

The deeper cage is still a single-attacker mechanism and loses on several
resource-dominant maps.  The next experiment should fundamentally reassign
post-delivery workforce into finite route-repair, defense, and siege utility
states with explicit expiry, rather than increasing another unit cap.
