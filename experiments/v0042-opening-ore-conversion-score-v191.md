# v191 opening ore conversion score — rejected

Date: 2026-08-18

## Objective

Improve first-route conversion on wall/chokepoint maps without changing the
chain FSM. During the opening three completed routes, rank visible and
advertised ore by a bounded Builder-approach plus Core-distance estimate and a
small visible-access penalty; after the milestone, retain the nearest-source
policy.

## Allowed files and non-goals

Allowed source was `bots/candidate/bot/defender.py` with focused coverage in
`tests/test_candidate_nearest_defense.py`, plus this record, reports,
`UPDATES.md`, `docs/CURRENT_PLAN.md`, and durable state. The quick screen
remained the 15-game all-map schedule; the release matrix remained 60 games.

Non-goals were workforce/role thresholds, chain FSM or navigation, combat,
turrets, Launchers, barriers, Store layout, baseline/archive, package,
upload, activation, and live-state changes.

## Validation and evidence

- Focused related suites passed **35/35** for the initial and repaired
  variants; compileall passed. `make static` retained the inherited exit 2
  from the missing legacy modules and two navigation fast-path assertions.
- Smoke was **4/4** command-clean for both variants. Rollback logs are under
  `reports/iter-v191-opening-ore-score/rollback-*`.
- Initial implementation (opening route weight 2, boxed penalty 24) scored
  **7-8** on the seed-159 15-game screen, with candidate/comparator Ti
  **75,380/80,290** (0.9388x), one candidate no-delivery game, and zero
  command/TLE/suspicious-output failures. Report:
  `reports/local-20260818T101340Z`.
- Repair 1 halved the route weight and access penalties. It remained **7-8**,
  although collection improved to **79,190/69,720** (1.1358x); all 15 games
  were command-clean. Report: `reports/local-20260818T101626Z`.

## Decision and rollback

The paired win rate did not improve over v0042, so v191 is rejected without a
60-game gate. The temporary scoring helper and three focused tests were
removed. Candidate source is recursively identical to immutable
`bots/versions/v0042_low-liquidity-gunner_20260818-0737_eeafad8f`; no release,
package, remote gate, upload, activation, or baseline transition occurred.

## Remaining risk

The screen's collection improvement did not convert into wins, and the
opening score can still under-sample high-throughput deposits. A future
conversion hypothesis needs fresh replay causality rather than another global
ore-ranking weight adjustment.
