# v272 two-responder active logistics infiltrator intercept — rejected

## Objective and replay basis

The v271 release replay audit showed more hostile Builder attacks on friendly
home logistics in losses than wins, especially on Antler, Drumlin, Fjordgate,
Midgard, and Yulerune. The candidate already has hijack/raid behavior, so this
candidate isolated defense: a visible enemy Builder adjacent to a friendly
Harvester, Conveyor, or Splitter could admit the two nearest non-attacker
Builders to the existing home-threat strike task.

## Implementation and bounded repair

The initial implementation used route adjacency as the active signal. Focused
tests passed **32/32** (the v271 phase suite plus new infiltrator cases),
compileall passed, smoke was **4/4**, and `make static` retained only the
inherited deleted-module imports and navigation assertions. Its configured
15-map screen was command-clean but lost **3-12**, with candidate collection
**44,390 vs 95,150 Ti** and one candidate no-delivery row
(`reports/local-20260819T113347Z`).

The one allowed repair required the adjacent friendly logistics asset to be
visibly damaged before admitting the second responder. Focused tests passed
**33/33**, compileall passed, smoke was **4/4**, and static retained the same
inherited failures. The repaired screens were:

| screen | wins | collection Ti | first delivery | reliability |
| --- | ---: | ---: | --- | --- |
| seed 175 | 8-7 | 74,850 vs 59,920 | 15/15 vs 14/15 | zero TLE/suspicious |
| seed 172 | 7-8 | 58,810 vs 57,280 | 14/15 vs 15/15 | zero TLE/suspicious |

The paired screens therefore combined to **15-15**, equal **29/30** first
deliveries, and did not show a repeatable win-rate or delivery edge. Maximum
p99/peak execution was **1,522/3,009 us**. Full logs and replay diagnostics
are under `reports/iter-v272-two-responder-infiltrator/` and the two
`reports/local-20260819T113706Z` / `reports/local-20260819T113914Z` folders.

## Decision and rollback

Reject v272. The adjacency-only trigger was harmful; the damaged-asset repair
removed the obvious overreaction but still tied the baseline rather than
beating it. No 60-game gate, package, upload, activation, or live-state
transition was justified. Candidate source was restored byte-identically to
immutable v0044 at
`reports/iter-v272-two-responder-infiltrator/rollback-source.diff` (zero
lines). Rollback focused tests passed **30/30**, compileall passed, smoke was
**4/4**, and static retained the inherited failures.

The replay evidence supports active logistics damage as a real phenomenon, but
two Builder-fire responders are not a reliable conversion. A future
infiltration hypothesis needs a cheaper signal or a route-preserving response;
do not widen this responder count or radius. Historical platform v105 remains
a requested but known-bad reference (51.64% over 275 games); v101 stays the
guarded operational rollback until revalidated.
