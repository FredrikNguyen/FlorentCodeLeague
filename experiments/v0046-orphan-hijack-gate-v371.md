# v371 Orphan-only opening hijack — rejected

Date: 2026-08-20

## Objective and scope

Starting from immutable v0046, v371 tested a narrower infiltration contract
after v370's blanket route-first gate failed.  A dynamic Builder could still
hijack a visible enemy Harvester during the opening only when no friendly
Conveyor/Splitter outlet touched that source; connected enemy sources waited
for the existing pressure phase.  The intent was to steal otherwise wasted
output without interrupting a live route shell.

Production scope was `bots/candidate/bot/dynamic.py`; focused coverage was two
temporary orphan/connected-source task tests in
`tests/test_candidate_nearest_defense.py`.  No route FSM, Store schema, unit
cap, map literal, Sentinel/Launcher/Gunner policy, baseline, or live files
were changed.

## Validation and decision

- Focused coverage passed **37/37** after one import repair; compileall passed.
- The all-map paired screen (`screen_seed=431`, 15 maps, 30 games) was
  **12-18**, with zero command failures and no delivery, TLE, or
  suspicious-output failures.  The first-screen 9-6 floor failed, so no
  second screen or release gate was justified.
- Replay diagnostics are in `reports/local-20260820T201314Z/analysis.json`.
  The candidate frequently ended with 4–7 Harvesters and near-zero Ti on
  losses; orphan-only targeting did not make the opening robust.
- Rollback focused coverage passed **35/35**, compileall passed, smoke was
  **4/4** at `reports/local-20260820T201857Z`, and recursive source parity with
  v0046 is empty at
  `reports/local-20260820T201314Z/rollback-source-parity.diff`.
- `make static` retained the inherited 15 obsolete-module import errors and
  two navigation fast-path assertions; no v371-specific static defect was
  introduced.

Reject v371 and keep exact v0046 as the comparator.  No release matrix,
package, upload, activation, or live baseline transition ran.

Reports: `reports/local-20260820T201314Z/`,
`reports/local-20260820T201857Z`, and this experiment record.
