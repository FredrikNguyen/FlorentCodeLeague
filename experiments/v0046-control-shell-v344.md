# v344 — map-aware reserve-backed control shell

Date: 2026-08-20

## Objective and scope

Top-team replays split their openings by map: control-first teams establish a
small Launcher/Barrier/Sentinel shell on compact boards, while economy-first
teams place Harvesters and conveyors immediately on larger boards.  v0046 had
only a one-off primary Launcher and delayed every Sentinel/Barrier until a
route milestone.  v344 tested a structural phase contract on immutable v0046:
the primary fixed attacker could spend on one confirmed-intel compact-map
Sentinel/Barrier pulse only with a complete next-builder/route/offense reserve;
fresh home threats, siege, stale intel, low liquidity, and non-compact maps
released it.  A pressure-phase dynamic Builder could then own one local
Barrier handoff before resuming logistics raids.

Allowed production scope was `bots/candidate/bot/attacker.py`,
`bots/candidate/bot/dynamic.py`, and one focused control-shell test file.  No
Core spawn, Store schema, route geometry, fixed identity, baseline snapshot,
package, platform, or live-state change was allowed to remain.

## Validation and bounded repairs

- Initial focused coverage passed **38/38**, compileall passed, and smoke was
  **4/4** at `reports/local-20260820T085245Z`.  The seed-179 15-map screen was
  **7-8 candidate-A**, delivery-clean, and collected **60,410 vs 52,310 Ti**
  (+8,100).  Analysis:
  `reports/iter-control-shell-v344-screen-analysis.json`.
- The rotated seed-173 screen exposed a failure: **4-11**, **47,720 vs
  78,360 Ti**, and two candidate no-delivery rows (Fjordgate and Icefloe).
  Analysis: `reports/iter-control-shell-v344-screen-seed173-analysis.json`.
- Repair 1 added a round-20 economy-settling window before a route-less shell.
  Focused coverage remained **38/38**, compileall passed, static retained the
  inherited profile, and smoke was **4/4** at
  `reports/local-20260820T085829Z`.  Seed-173 became delivery-clean at **7-8**
  with **67,690 vs 68,750 Ti**.  Analysis:
  `reports/iter-control-shell-v344-repair1-screen-seed173-analysis.json`.
- Repair 2 kept the early Sentinel reserve but moved Barrier spending behind a
  completed route.  Focused coverage remained **38/38**, compileall passed,
  static retained the inherited profile, and smoke was **4/4** at
  `reports/local-20260820T090144Z`.  Seed-173 was **8-7**, delivery-clean,
  **82,480 vs 70,930 Ti** (+11,550); seed-179 was **8-7**, delivery-clean,
  **70,690 vs 63,450 Ti** (+7,240).  Analyses:
  `reports/iter-control-shell-v344-repair2-screen-seed173-analysis.json` and
  `reports/iter-control-shell-v344-repair2-screen-seed179-analysis.json`.

## Release gate and decision

The specified 60-game endpoint/side gate was command-clean at **38-22
candidate wins**, **370,960 vs 329,100 Ti** (+41,860), max p99/peak
**1,368/5,938 us**, zero TLE/suspicious rows.  However, one candidate-side
Icefloe game had no titanium delivery while v0046 delivered.  This is a
protected-map reliability regression under the promotion guard, despite the
aggregate win and collection edge.  Full report and analysis:
`reports/local-20260820T090611Z` and
`reports/iter-control-shell-v344-release-analysis.json`.

Reject v344 after the two permitted repairs.  Restore exact recursive v0046
production parity; both source parity proofs are zero-byte:
`reports/iter-control-shell-v344-rollback-attacker.diff` and
`reports/iter-control-shell-v344-rollback-dynamic.diff`.  Rollback focused
coverage was **31/31**, compileall passed, static retained the inherited 15
obsolete-module imports plus two navigation assertions, and rollback smoke was
**4/4** at `reports/local-20260820T091439Z`.  No promotion, package, upload,
activation, or live-state transition occurred; live state remains v108
`active_observing` with v107 known-good.

## Follow-up

Do not retry the compact control pulse unchanged.  The aggregate signal is
promising, but Icefloe still exposes an opening sink failure.  The next
fundamental experiment should add a verified delivery/route-health proof to
the control-phase handoff, not another spend threshold; preserve v0046 as the
rollback baseline until that proof is delivery-clean at the release gate.
