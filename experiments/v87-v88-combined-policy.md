# v87-v88 combined policy checkpoint

## Objective

Use v87's empirically stronger income discipline as the strategy base, retain
v88's local ore-ownership guard, and beat the current v88 submission in a
side-swapped controlled comparison.

## Evidence

The exact downloaded artifact comparison put v87 over v88 at 117-93 and
1.139x titanium across 210 games (`reports/local-20260812T071910Z`,
`reports/v88-v87-full-replay-analysis.json`). Replay review found v88's
losses were primarily an economy-scale problem: it fielded 3-5 Builders in
four losses while its opponents fielded 9-15; top teams sustained multiple
connected routes and larger worker fleets. Evidence:
`reports/v88-loss-and-top-team-replay-analysis.json`.

## Retained candidate

The mutable candidate combines:

- v87's independent floor/buffer ammo accounting, observed-income lifetime
  ammo allowance, surplus-only idle fire, and income-gated mature workforce
  target of eight Builders;
- v88's local closest-Builder visible-ore ownership, excluding permanent
  attackers from economic ownership.

It passed the selected 54-game gate 33-21 with 1.1860x titanium, zero TLE or
suspicious replay output, p99 <= 1.218 ms, and peak <= 2.548 ms:
`reports/local-20260812T074500Z` and
`reports/v87-v88-combined-regression-analysis.json`.

The full fixed 21-map confirmation was 112-98, 750,460-694,890 titanium
(1.0800x), 210/210 command-clean, zero TLE/suspicious output, max p99 1.483
ms, and peak 2.836 ms: `reports/local-20260812T074937Z` and
`reports/v87-v88-combined-full-replay-analysis.json`.

## Rejected variants

- Removing v88 ore ownership: 23-31, 1.0225x titanium; it harms string,
  bridge, atoll, and aurora. `reports/local-20260812T080438Z`.
- Four-Builder opening: 30-24, 1.0752x titanium, weaker than the retained
  candidate's selected result. `reports/local-20260812T080918Z`.
- Seven-Builder mature cap: 26-28, 1.0177x titanium.
  `reports/local-20260812T081404Z`.

## Status and risks

The retained combination is the current local best versus v88, but the full
margin (112-98) is smaller than the selected gate and longship remains a 2-8
loss. It is not packaged or deployed. `make static` still has 15 obsolete
imports from the retired pre-v86 test architecture; compile, source-contract,
and smoke checks pass.
