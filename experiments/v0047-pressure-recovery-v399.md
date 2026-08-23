# v399 pressure-capacity recovery lease — rejected

Date: 2026-08-21

## Objective and scope

Starting from immutable
`bots/versions/v0047_pressure-economy-steward_20260821-0200_eeafad8f`, v399
tested a live-capacity recovery hypothesis from the Royale/Drakkarfjord/
Glacierkeep release losses.  After the historical route counter and Core phase
had reached healthy `PRESSURE`, at most two nearest non-fixed Builders inside
the home radius could remain on the existing SCOUT/CHAIN economy loop when
the visible home Harvester count was depleted and the bank could not fund one
replacement route plus the fixed attack reserve.  The bounded repair narrowed
the trigger from one-to-two visible Harvesters to zero visible Harvesters.

Production scope was `bots/candidate/bot/dynamic.py`, with focused coverage in
`tests/test_candidate_economy_phase.py`.  Route geometry, source selection,
Store schema, Core spawning, fixed roles, combat targeting, unit prices,
package, upload, activation, and live state were non-goals.

## Done criteria

- Focused economy/defense/seeded-route tests, candidate compileall, static, and
  smoke must pass with only the inherited static profile.
- The 30-game all-map paired screen against immutable v0047 must reach at least
  19–11, remain delivery/reliability clean, and avoid a protected-map collapse.
- A screen-negative candidate receives one bounded repair at most; if that also
  misses the floor, remove temporary source/test/config edits and restore exact
  recursive parity with v0047.  No release gate or platform operation is
  justified by a failing short screen.

## Validation

- Initial focused coverage: **37/37**; candidate compileall passed; static
  retained the inherited exit-2 profile (15 obsolete imports and two
  navigation assertions); smoke was **4/4** at
  `reports/local-20260821T043923Z`.
- Initial rotated all-map screen (`screen_seed=1361`) was command-clean and
  delivery-clean (**30/30** on both sides), but candidate wins were **9–21**
  and collection was **128,030 vs 165,800 Ti**.  Max p99/peak was
  **1,385/5,381 us**, with zero TLE or suspicious rows.  Raw games and
  manifest are under `reports/local-20260821T044004Z`; parsed diagnostics are
  `reports/iter-v399-pressure-recovery/replay-analysis.json`.
- Repair focused coverage remained **37/37**; compileall passed; static kept
  the same inherited profile; smoke was **4/4** at
  `reports/local-20260821T044849Z`.
- Repair screen (`screen_seed=1373`) improved to **13–17**, but introduced
  one candidate no-delivery row (**29/30** candidate deliveries vs **30/30**)
  and still collected less (**124,370 vs 137,680 Ti**).  Reliability stayed
  clean: max p99/peak **1,335/5,437 us**, zero TLE/suspicious rows.  Raw games
  are under `reports/local-20260821T044446Z`; diagnostics are in
  `reports/iter-v399-pressure-recovery/repair-replay-analysis.json`.

## Decision and rollback

Reject v399 after the bounded repair.  The extra recovery lease consumed too
much productive pressure capacity and did not clear the 19–11 screen floor.
Temporary source/test/config edits were removed; recursive candidate parity
with immutable v0047 is exact.  Rollback focused coverage was **36/36**,
compileall passed, rollback smoke was **4/4** at
`reports/local-20260821T044849Z`, and rollback static retained the inherited
exit-2 profile (`reports/iter-v399-pressure-recovery/rollback-static.log`).
No release, package, remote, upload, activation, or baseline transition was
performed.  Immutable v0047 remains the strongest baseline.

Evidence is under `reports/iter-v399-pressure-recovery/`.
