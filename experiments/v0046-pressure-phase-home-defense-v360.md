# v360 — pressure-phase home-defense shell

## Objective and replay basis

Keep immutable v0046 as the comparator.  Fresh v108 loss/top-team samples in
`reports/live-v108-followup-20260820T164909Z/` show underbuilt defensive shells:
the candidate often has one or two Gunners while opponents maintain several
Gunners and Sentinels.  v359's dynamic pressure handoff was rejected, so this
experiment changes only the Core's defense investment trigger.

## Hypothesis and scope

When the Core publishes healthy `PRESSURE`—five completed routes plus a recent
positive-income heartbeat—it has earned a quiet defensive investment window.
Raise the existing home-Gunner target to `MAX_GUNNERS_CAP` (five) in that phase
even if no enemy is visible, but keep the current dynamic price/reserve,
one-builder designation, lifetime placement guard, and route-tile exclusions.
Opening/converting/crisis and visible-threat behavior must remain unchanged.

Allowed production/test scope is `bots/candidate/bot/core_role.py` and
`tests/test_candidate_economy_phase.py`.  Store layout, spawn policy, route
geometry, dynamic/attacker tasks, immutable snapshots, and platform state are
non-goals.

## Validation

- Focused coverage was **32/32**, compileall passed, and smoke was **4/4**;
  `make static` retained the inherited 15 obsolete imports and two navigation
  assertions.
- The initial v0046-pinned rotated screen at
  `reports/local-20260820T170539Z` was **7-8** candidate-A, with zero command,
  TLE, suspicious, or delivery failures.
- The one repair relaxed only the quiet-pressure reserve to one dynamically
  priced Harvester plus two conveyor links.  Focused coverage remained
  **32/32**, but the repaired rotated screen at
  `reports/local-20260820T170802Z` was **6-9**, also reliability-clean.
- Post-rollback focused coverage was **31/31**, compileall passed, rollback
  smoke was **4/4** at `reports/local-20260820T171057Z`, and static retained
  only the inherited profile (`reports/iter-v360-pressure-phase-home-defense/rollback-static.log`).

## Decision and rollback

Reject v360 after the single bounded repair.  A quiet-pressure home shell did
not produce a repeatable edge and the reserve relaxation regressed the second
screen.  No 60-game release matrix, remote gate, package, upload, activation,
or baseline update ran.

Candidate production source was restored exactly to immutable v0046; the
recursive source parity proof is the empty
`reports/iter-v360-pressure-phase-home-defense/rollback-source-parity.diff`.
