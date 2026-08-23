# v0074 — four-route economy gate

## Objective

Keep dynamic Builders productive on economy until four completed Harvester
routes exist. Preserve the first fixed scouting attacker and urgent defensive,
repair, and hijack work, while delaying the second fixed attacker and surplus
pressure by one completed route.

## Scope

- Restore the mutable candidate to the v0032 strategy after the rejected v0033
  turret-retirement experiment.
- Change the shared offense-readiness threshold from three completed routes to
  four.
- Add focused coverage for dynamic task selection and fixed-attacker creation
  on both sides of that threshold.
- Do not change navigation, path shapes, Store layout, combat targeting, unit
  lifecycle, immutable baselines, or live platform state.

## Hypothesis

The third route is too early to divert scarce Builder capacity into a second
fixed attacker and dynamic pressure. Requiring a fourth completed route should
improve the opening economy and paired win rate while retaining the existing
pressure behavior once the economy is established.

## Validation

- Focused tests: **12/12 passed**
  (`reports/iter-four-route-gate-focused.log`). The tests cover route counts
  zero through three remaining economic, four routes enabling pressure, the
  second fixed attacker waiting for four routes, and absence of rejected
  turret-retirement behavior.
- Candidate compileall passed. `make static` retained the inherited exit-2
  result from 15 obsolete-module imports; no new static failure was identified.
- Smoke: **4/4 command-clean**, with zero TLE or suspicious output
  (`reports/local-20260815T151332Z`).
- 54-game screen versus v0032: **32-22 (59.3%)**, 249,640 versus 215,880
  collected titanium (1.1564x), zero candidate no-delivery rows versus one,
  zero command failures/TLE/suspicious output, max p99 1,342 us and peak
  callback 4,410 us (`reports/local-20260815T151644Z`; analysis
  `reports/iter-four-route-gate-v0074/screen-analysis.json`).
- Full 210-game matrix versus v0032: **112-98 (53.3%)**, 1,045,020 versus
  1,027,770 collected titanium (1.0168x), zero candidate no-delivery rows
  versus two, zero command failures/TLE/suspicious output, max p99 1,508 us and
  peak callback 5,542 us (`reports/local-20260815T152315Z`; analysis
  `reports/iter-four-route-gate-v0074/full-analysis.json`).

## Decision and risks

**Promote locally.** The full gate confirms the screen direction with a
14-game paired margin and cleaner delivery, satisfying the user's win-rate-led
moving-baseline rule. The gain is modest and collection is nearly flat.
Jackpot (1-9), Showdown (2-8), Fjord (3-7), Pinch (4-6), Twins (4-6), and Vault
(3-7) remain important weaknesses for route-continuity diagnosis. No upload or
activation is part of this promotion.
