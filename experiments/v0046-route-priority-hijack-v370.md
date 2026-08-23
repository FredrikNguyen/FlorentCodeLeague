# v370 Route-priority hijack gating — rejected

Date: 2026-08-20

## Objective and scope

Starting from immutable v0046, v370 moved dynamic enemy-Harvester hijacking
below the normal economy task.  During opening, converting, or crisis phase a
dynamic Builder therefore stayed on its own route loop even when an enemy
Harvester was visible; after pressure was published and no local ore was
available, the existing hijack path remained eligible.  The hypothesis was
that early infiltration was stealing route/workforce turns from the four
opening Harvesters and conveyor paths seen in the top-team replays.

Production scope was `bots/candidate/bot/dynamic.py`; focused coverage was the
temporary opening/pressure task-priority tests in
`tests/test_candidate_nearest_defense.py`.  No route FSM, Store schema, unit
cap, map literal, combat policy, baseline, or live files were changed.

## Validation and decision

- Focused coverage passed **37/37**; compileall passed.
- The all-map paired screen (`screen_seed=419`, 15 maps, 30 games) was
  **14-16**, with zero command failures and no delivery, TLE, or
  suspicious-output failures.  The first-screen 9-6 floor failed, so no
  second screen or release gate was justified.
- Replay diagnostics are in `reports/local-20260820T200558Z/analysis.json`.
  Losses showed route priority could leave the candidate with 3–7 Harvesters
  and low collected Ti on several maps; the broad gate was negative.
- Rollback focused coverage passed **35/35**, compileall passed, smoke was
  **4/4** at `reports/local-20260820T200958Z`, and recursive source parity with
  v0046 is empty at
  `reports/local-20260820T200558Z/rollback-source-parity.diff`.
- `make static` retained the inherited 15 obsolete-module import errors and
  two navigation fast-path assertions; no v370-specific static defect was
  introduced.

Reject v370 and keep exact v0046 as the comparator.  No release matrix,
package, upload, activation, or live baseline transition ran.

Reports: `reports/local-20260820T200558Z/`,
`reports/local-20260820T200958Z`, and this experiment record.
