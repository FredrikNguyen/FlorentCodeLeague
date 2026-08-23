# v247 low-liquidity recovery — rejected after one bounded repair

## Objective

Use the live v105 Drakkarfjord loss to test whether the historical completed
route counter leaves dynamic Builders in an unfunded pressure phase after an
infiltration or route cut. The candidate would re-enter the existing
SCOUT/CHAIN economy loop when the bank could not buy one Harvester and no
forward Sentinel had been observed. The opening, route FSM, fixed roles, and
infiltration selectors were otherwise unchanged.

## Scope and non-goals

- Temporary source: `bots/candidate/bot/dynamic.py`.
- Temporary focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, `UPDATES.md`, `docs/CURRENT_PLAN.md`, durable
  state, and reports under `reports/iter-v247-low-liquidity-recovery/`.
- No Store schema, opening timing, route geometry, home-threat selector,
  hijack/raid primitive, fixed-role, weapon, map, baseline, package, upload,
  activation, or live-state change.

## Validation

The initial recovery gate passed focused coverage **29/29**, compileall, and
smoke **4/4**. `make static` retained the inherited 15 obsolete-module import
errors and two navigation fast-path assertions. The rotated 15-map screen was
command-clean with zero TLE/suspicious rows but lost **6-9** and collected
**76,540 vs 84,860 Ti**. Drakkarfjord first delivery improved to **42 vs 66**,
but the aggregate result was not positive. Raw report:
`reports/local-20260819T025422Z`; replay diagnostics:
`reports/iter-v247-low-liquidity-recovery/initial-replay-analysis.json`.

The one bounded repair assigned the recovery lease to only the lowest-id
visible non-fixed Builder. Focused coverage passed **31/31**, compileall and
smoke **4/4** stayed clean, and static retained the same inherited failures.
The repair screen fell to **5-10**, collected **48,040 vs 60,730 Ti**, and
introduced a candidate no-delivery Royale row. Raw report:
`reports/local-20260819T025805Z`; diagnostics:
`reports/iter-v247-low-liquidity-recovery/repair-replay-analysis.json`.

## Decision and rollback

Reject v247 after the two unsuccessful screen attempts. Both temporary source
and test edits were removed; recursive candidate parity with immutable v0042
is zero-line at
`reports/iter-v247-low-liquidity-recovery/rollback-source.diff`. Rollback
focused coverage was **27/27**, compileall passed, and rollback smoke was
**4/4** at `reports/local-20260819T030033Z`; rollback static retained the
same inherited failures in
`reports/iter-v247-low-liquidity-recovery/rollback-static.log`. No release
gate, promotion, package, upload, activation, or live-state transition
occurred.

The infiltration hypothesis remains closed for now: the v224–v242 family
already covered direct interception, body-blocking, turret targeting,
Launcher ejection, and Harvester hijacking without a paired edge. The next
candidate must use new high-frequency replay evidence rather than widen those
branches or reintroduce a broad low-liquidity handoff.
