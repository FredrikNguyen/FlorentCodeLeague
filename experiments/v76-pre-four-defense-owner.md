# v76 pre-four-route defense owner

## Scope

- Parent: `bots/versions/v0018_nordkap-route-owner_20260809-2231_eeafad8f`.
- Hypothesis: before four maintained routes, repeated defensive construction
  should belong to one free home defender so route owners and workers continue
  expanding the economy instead of each placing structures on their own cooldown.
- Runtime change: `bots/candidate/bot/builder.py`.
- Focused tests: `tests/test_candidate_bootstrap_defense.py`.
- Protected layouts retain the parent policy: 14x18, 20x26, and the inset-core
  16x16 arena, which regressed under the broad first pass.

## Validation

- Focused unit tests: 5/5 passed.
- Static: only inherited obsolete API, navigation, and source-line-budget
  failures; `reports/pre-four-defense-final-static.log`.
- Smoke: 4/4 command-clean; `reports/local-20260809T235723Z`.
- Current 15-map live pool: 90/90 command-clean, 59-31, 213,690 versus
  128,370 titanium; `reports/local-20260809T233906Z`.
- Replay audit: 1,601,652 calls, zero TLE or suspicious output, p99 at most
  4.357 ms, peak callback 7.627 ms;
  `reports/pre-four-defense-final-release-analysis.json`.
- Gain maps: drumlin, hive, jackpot, moonrise, and saga each finished 6-0.
  Protected antler, lighthouse, and nordkap each remained seat-balanced 3-3.
- Snowflake confirmation: 7-3 and 47,200 versus 32,940 titanium across five
  seeds; `reports/local-20260809T235438Z`.
- Remote server gate: 3-2 versus v0018; match
  `c2cf4cd4-6eea-460f-89e3-949791febba2`, report
  `reports/remote-20260809T235805Z`.

## Decision

Release gates passed. Freeze and upload only after platform v75 completes its
12-series observation and the deterministic rollback to v72 is recorded.
Retain v72 as the rollback target during the next live observation.
