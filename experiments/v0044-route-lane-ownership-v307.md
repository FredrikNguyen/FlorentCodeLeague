# v307 map-relative route-lane ownership — rejected after one bounded repair

Date: 2026-08-19

## Objective and replay basis

The v306 architecture audit found a repeated opening failure: on the saved
GlacierKeep/Royale losses, v0044 laid a long conveyor trail but committed only
one paying Harvester, while the top-team winners converted several Builders in
parallel.  v307 tested a structural economy change rather than another combat
threshold: non-attacker Builders received a deterministic cardinal sector from
their Core-relative position and preferred ore in that sector, with nearest-ore
fallback when the sector was empty.

## Scope and non-goals

Temporary production changes were limited to `bots/candidate/main.py` and
`bots/candidate/bot/defender.py`; focused coverage was
`tests/test_candidate_route_lanes.py`.  No Store slot, route geometry,
spending, combat, Launcher/Sentinel/Barrier policy, baseline snapshot, package,
upload, activation, or live state changed.  The immutable comparator was
`bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`.

## Validation

- Initial lane variant: focused **37/37**, compileall passed, `make static`
  retained the inherited 15 stale-module import errors and two navigation
  fast-path assertions, and smoke was **4/4** at
  `reports/local-20260819T214931Z`.
- Initial 15-map screen was command-clean at
  `reports/local-20260819T215002Z`: candidate **7-8**, collection
  **51,620/56,520 Ti**, first delivery **15/15 vs 15/15**, and no candidate
  no-delivery row.  Replay diagnostics are in
  `reports/iter-route-lane-screen-analysis.json`; the lane rule removed the
  old zero-delivery shape but lowered Harvester stock and delayed GlacierKeep
  delivery to turn 206 versus 34 for the comparator.
- One bounded repair applied lane preference only during the opening routes
  and only within a four-tile Manhattan detour of the nearest ore.  Focused
  coverage was **38/38**, compileall passed, static retained the same inherited
  profile, and smoke was **4/4** at
  `reports/local-20260819T215242Z`.
- Repair screen was command-clean at `reports/local-20260819T215304Z` but
  regressed to **4-11**, collection **35,210/57,340 Ti**, with first delivery
  **15/15 vs 15/15**.  Replay diagnostics are in
  `reports/iter-route-lane-repair-screen-analysis.json`.

## Decision and rollback

Reject v307 after the initial screen and its one allowed bounded repair.  The
map-relative sector ownership is not robust to asymmetric/rotated maps: the
repair preserved delivery but starved the opening workforce and lost the
aggregate comparison.  The lane state, picker helpers, and focused test were
removed.  Candidate production source is recursively byte-identical to the
immutable v0044 comparator at
`reports/iter-route-lane-rollback-source.diff` (zero lines).

Rollback focused coverage was **34/34** at
`reports/iter-route-lane-rollback-focused.log`, compileall passed, rollback
smoke was **4/4** at `reports/local-20260819T215601Z`, and the rollback static
profile remains the inherited **15 import errors plus two navigation
assertions** (`reports/iter-route-lane-rollback-static.log`).  No longer gate,
promotion, package, upload, activation, or live transition occurred.  Live
v107 remains `active_observing`; v105 remains the operational rollback.

## Remaining risk

Top-team parallel route conversion remains a credible gap, but a purely local
sector partition is not a safe implementation.  The next architecture must
coordinate route ownership without forcing a geometric detour, and must prove
delivery/Harvester conversion before adding control spending.
