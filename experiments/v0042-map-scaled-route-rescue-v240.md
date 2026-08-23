# v240 map-scaled late route rescue — rejected

## Replay basis and decision to avoid another infiltration branch

The saved infiltration audit and the v229/v233/v235/v236/v237 experiments do
not show a stable defensive or offensive infiltration conversion. Reactive
Builder interception, home Launcher ejection, body-blocking, Builder-target
priority, Sentinel-target priority, and loaded-source hijack each failed to
produce a repeatable paired edge. The recurring local loss signal is instead
late/no delivery after the fixed attacker has left the home route.

## Objective and scope

After a map-scaled Core-to-mirror deadline, if the primary fixed attacker still
observed zero completed routes and zero forward Sentinels, and the bank could
fund one Harvester plus two Conveyors, return only that attacker to the home
economy. It reused the existing orphan reconnect, Harvester build, and CHAIN
FSM; no enemy threat detector or infiltration selector was added.

Temporary files were `bots/candidate/main.py`,
`bots/candidate/bot/attacker.py`, `bots/candidate/bot/constants.py`, and
`tests/test_candidate_route_rescue.py`. A temporary seed-173 screen config was
used only for the paired run. The baseline remained immutable v0042.

## Validation

- New route-rescue tests: **6/6**; combined focused subset: **33/33**.
- Candidate compileall passed; smoke was **4/4** at
  `reports/local-20260819T010345Z`.
- `make static` retained the inherited **15** obsolete-module import errors
  and **2** navigation fast-path assertions.
- The rotated 15-map screen was command-clean with zero candidate
  no-delivery/TLE/suspicious rows and max p99/peak **1,341/2,499 us**.
  Candidate-A finished **7-8**, collection **64,280 vs 74,780 Ti**, and
  first-delivery mean **37.67 vs 89.47** (the baseline had one no-delivery
  row). Raw report: `reports/local-20260819T010427Z`; replay analysis:
  `reports/iter-v240-route-rescue/replay-analysis.json`.

The delivery mean was better but the candidate lost both aggregate collection
and paired win rate, so it is not promotion evidence. No bounded repair was
justified: the screen did not isolate a route-rescue conversion edge, and a
second rescue threshold would repeat the rejected v201/v202 handoff family.

## Rollback

The temporary source/test/config edits were removed. Recursive candidate versus
immutable-v0042 source parity is zero lines at
`reports/iter-v240-route-rescue/rollback-source.diff`. Rollback focused
coverage was **27/27**, compileall passed, static retained the inherited
failures, and rollback smoke was **4/4** at
`reports/local-20260819T010805Z`. Logs are in
`reports/iter-v240-route-rescue/`. No release gate, promotion, package,
upload, activation, or live-state transition occurred; v0042 remains the
local baseline.

## Next direction

Do not retry late primary-attacker economy handoffs or another generic
infiltration selector without new causal replay evidence. Prefer a high-
frequency pressure or resource-conversion mechanism that does not pull the
fixed attacker off its forward lane.
