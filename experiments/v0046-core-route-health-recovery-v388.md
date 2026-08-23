# v388 Core route-health recovery lease — rejected

Date: 2026-08-21

## Objective and scope

Starting from immutable v0046, v388 tested a Core-authoritative route-health
signal.  After the existing strong-chain milestone, the Core published a
recovery phase when too few home Harvesters were visible; one nearest dynamic
Builder resumed the normal SCOUT/CHAIN economy loop while fixed attackers and
the rest of the pressure pool stayed offensive.  The signal reused the high
bits of the existing economy-phase Store channel.  Production scope was
limited to `bots/candidate/bot/constants.py`, `core_role.py`, and `dynamic.py`,
with focused coverage in `tests/test_candidate_economy_phase.py`.

## Validation and bounded repair

- Focused route/phase coverage was **32/32**; compileall passed; the candidate
  smoke was **4/4** at `reports/local-20260821T001738Z`.
- `make static` retained the inherited profile: 15 obsolete-module import
  errors and two navigation fast-path assertions; no v388-specific failure
  appeared (`reports/iter-v388-route-health/static.log`).
- Initial rotated all-map 30-game screen (`screen_seed=691`) was command- and
  reliability-clean but only **16–14** against v0046.  Candidate/baseline
  collection was **181,180/195,850 Ti**, first deliveries **30/29**, and
  max p99/peak **1,529/5,923 us**.  Sparse Glacierkeep games exposed delayed
  deliveries (candidate 142/194 versus baseline 54/46 rounds).
- One bounded repair narrowed recovery from fewer than three visible home
  Harvesters to an empty visible home end.  Repair focused coverage remained
  **32/32**, compileall passed, and smoke was **4/4** at
  `reports/local-20260821T002321Z`.
- The fresh rotated 30-game screen (`screen_seed=709`) improved to **17–13**
  and fixed Glacierkeep (2–0), but still missed the **19–11** promotion floor.
  It was command-clean with **29/30 vs 30/30** deliveries,
  **139,430/112,660 Ti** collection, max p99/peak **1,369/3,651 us**, and
  zero TLE/suspicious rows.  Summaries are
  `reports/iter-v388-route-health/screen-summary.json` and
  `screen-summary-repair.json`; replay details are in the paired analysis
  JSON files.

## Decision and rollback

Reject v388 without a second screen or long gate.  The recovery phase and
focused additions were removed; candidate production is recursively identical
to immutable v0046 (excluding generated caches).  Rollback focused coverage
was **31/31** at `reports/iter-v388-route-health/rollback-focused.log`,
compileall passed, and no package, upload, activation, baseline promotion, or
live transition occurred.  The two screen reports and raw matrices remain
under `reports/local-20260821T001804Z` and `reports/local-20260821T002346Z`.

## Remaining risk

The Core can detect a visibly empty home end, but a one-owner lease did not
clear the win-rate floor and the broader threshold briefly starved sparse-map
pressure.  Keep immutable v0046 as the best baseline and choose a distinct
pressure-conversion hypothesis next; do not revive this phase unchanged.
