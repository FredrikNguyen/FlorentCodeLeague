# v0078 — enemy-Core barrier cage

## Objective

Use the top ladder's offensive topology pattern without changing v100's
economy, navigation, workforce, Store protocol, or Sentinel policy.

## Hypothesis

After a forward-Sentinel opportunity, fixed attackers can ring a verified
enemy Core with cheap Barriers. Enemy Builders lose repair/movement access,
while Sentinel shots pass through the cage.

## Implementation

- Added per-attacker cage-site memory and a six-site bound.
- Requires a verified enemy Core and one historically completed route.
- Preserves the current dynamic cost of one replacement Harvester before
  buying a Barrier; this repair prevents stale route history from starving
  delivery after route destruction.
- Uses only cardinal legal build sites within radius-squared 13.
- Refuses to consume the attacker's sole legal exit.

## Evidence

- Top-team replay sample: Jython 8-2 with 151 Barriers and O(1) 7-3 with 119
  Barriers across ten games each. Placement coordinates show offensive Core
  cages. Reports: `reports/top-teams-20260815-analysis.json` and
  `reports/top-teams-20260815-summary.json`.
- Focused tests: 5/5 pass. Compileall passes.
- `make static`: inherited failure in obsolete removed-module tests; no new
  production error. `make smoke`: command-clean.
- Strengthened 54-game screen including auroraveil: 31-23 versus v100.
- Full 210-game matrix: **124-86 (59.0%)** versus v100, zero command failures.
  Auroraveil remains weak at 4-10; archipelago and valkyrie are 12-2.
- Full replay audit: zero TLEs/suspicious output, max p99 1.477 ms, peak
  6.439 ms. Report: `reports/iter-enemy-core-cage-v0078-repair1-full210-analysis.json`.
- Corrected remote gate against exact v100 on current maps: **4-1**, match
  `84cb4c94-7a02-4631-a6c7-c4f2b21e6905`.

## Decision

Promoted as immutable local version
`bots/versions/v0035_enemy-core-cage_20260815-2116_eeafad8f`, archive
`artifacts/submissions/v0035_enemy-core-cage_20260815-2116_eeafad8f.zip`,
SHA-256 `2c20aa8860d4c9528f613067ad650d20c0ed4156d3202453f51bbcb6ab9d76c7`.
Guarded deployment activated platform v101 under
`v0035-enemy-core-cage-eeafad8f`; platform v100 is preserved as previous active.
