# v315 verified route-first lifecycle — rejected after one bounded repair

Date: 2026-08-20

## Objective and replay basis

Top-team openings convert several Builders into paying routes early, while
fresh v107 losses showed the local bot leaving long conveyor trails with one
or no paying Harvester.  v315 tested a structural lifecycle change rather
than another combat or spending knob: on a first route of a long board, an
ore-adjacent non-attacker reserved the source, laid the existing Core-facing
chain, returned to the reservation, and built the Harvester only after the
route reached a verified Core sink.

## Scope and non-goals

Temporary production scope was `bots/candidate/main.py`,
`bots/candidate/bot/constants.py`, and `bots/candidate/bot/defender.py`, with
focused coverage in `tests/test_candidate_route_first.py`.  The branch was
limited to perimeter >= 40, first-route Store state, and a dynamic reserve for
the estimated chain plus source; failed routes fell back to source-first.
Short boards, established routes, Store schema, role/task priorities,
Launcher/Sentinel/Barrier policy, package/upload/activation, and live state
were non-goals.

## Validation

- Initial focused route/seed/economy/defense subset: **38/38**;
  compileall passed; `make smoke` was **4/4** at
  `reports/local-20260820T004941Z`; static retained the inherited 15 stale
  imports and two navigation assertions.
- Initial rotated 15-map screen was command-clean, **7-8**, with collection
  **63,600/59,690 Ti** and zero no-delivery, TLE, or suspicious rows.  Max
  p99/peak callback was **1,196/5,542 us**.  Report:
  `reports/local-20260820T005003Z`; replay diagnostics:
  `reports/iter-v315-route-first-screen-analysis.json`.
- One permitted lifecycle-only repair restricted route-first to an early
  source (distance <= `EARLY_HARVEST_RANGE`) so a remote source could not pay
  the route latency twice.  Focused remained **38/38**, compileall passed,
  smoke was **4/4** at `reports/local-20260820T005245Z`; static retained the
  same inherited profile.
- Repair screen was command-clean but only **8-7**, collection
  **69,210/72,620 Ti**, with one candidate no-delivery row versus none for the
  comparator; max p99/peak was **1,285/5,774 us**.  Report:
  `reports/local-20260820T005310Z`; replay diagnostics:
  `reports/iter-v315-route-first-repair-screen-analysis.json`.

## Decision and rollback

The repair produced only a one-game screen edge and lower aggregate
conversion, while the first screen tied the prior v0044 result.  Reject v315;
do not run the long gate or release.  The temporary state machine, constant,
and focused test were removed.  Recursive candidate parity with immutable
v0044 is zero in
`reports/iter-v315-route-first-rollback-source-parity.diff` and
`reports/iter-v315-route-first-rollback-main-parity.diff`.

Rollback focused coverage was **34/34**, compileall passed, static retained
the inherited exit-2 profile, and rollback smoke was **4/4** at
`reports/local-20260820T005545Z`.  No package, upload, activation, or live
transition occurred; v0044 remains the local comparator and live v107/v105
state is unchanged.

## Next risk

Prebuilding from the source still adds a round-trip and is not a robust route
planner.  The next structural experiment should change how a Builder shares
or repairs a verified route (or use a genuinely Core-outward plan), not repeat
this source-reservation handoff or a global role/lease/Launcher rewrite.
