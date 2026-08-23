# v75 nordkap route-owner continuity

## Hypothesis and scope

- Parent: `bots/versions/v0016_meander-route-owner_20260809-2058_eeafad8f`.
- Hypothesis: on the sole 20x26 geometry (`nordkap`), a pre-income primary
  route owner must ignore non-adjacent Builder-rush alerts while free workers
  respond, preserving the first funded route.
- Runtime file: `bots/candidate/bot/builder.py`.
- Focused test: `tests/test_candidate_bootstrap_defense.py`.
- Non-goals: no behavior change after first income, during immediate contact,
  for free workers, or on any geometry except the already guarded 25x15 maps
  and the new 20x26 target.

## Evidence before change

- Platform v73 lost both observed `nordkap` games by Core destruction. In both
  downloaded replays it built 5-6 Conveyors, no Harvester, and delivered zero;
  opponents first delivered on turns 28-29. Replays:
  `replays/live-v73-diagnosis/nordkap-vs-klarum.replay26` and
  `replays/live-v73-diagnosis/nordkap-vs-oresund.replay26`.
- Immutable v0016 reproduced the side-sensitive failure on the two exact live
  seeds: one side delivered on turn 11 while the other built five Conveyors,
  no Harvester, and delivered zero in all four games. Report:
  `reports/local-20260809T220410Z`.
- Active platform v75 then lost `nordkap` in its first otherwise 4-1 series,
  confirming the geometry remained live-relevant.

## Implementation and gates

- Renamed the internal helper to describe bootstrap-owner continuity and added
  20x26 to its exact geometry allowlist. Immediate contact, post-income owners,
  free workers, and non-target 24x24/26x26 geometries retain prior behavior.
- Focused tests: 3/3 passed. Compileall and `git diff --check` passed.
- `make static` retains only inherited pre-v69 API/obsolete line-cap failures;
  log: `reports/v75-nordkap-route-owner/static.log`.
- Smoke: 4/4 command-clean; report `reports/local-20260809T220655Z`.
- Exact live-seed target: 4-0, 7,100 versus 1,200 titanium; the formerly
  starved side built a Harvester on turn 9 and delivered on turn 12.
- Five-seed target: 10-0, 17,750 versus 3,000 titanium, delivery on turns
  11-12 in every game, zero TLEs, p99 at most 2.900 ms; report
  `reports/local-20260809T221120Z`.
- Remote side-B target passed: candidate won `nordkap` by Core destruction in
  match `b7a4dbe1-022e-4319-bb8b-62a347d10b7f`; the four source-inactive maps
  followed their side-A advantage, so the aggregate remote score was 1-4.

## Release gate and package

- Current 15-map live pool: 90/90 command-clean, 48-42 overall. The sole
  source-active map was 6-0 with 10,650 versus 1,800 titanium; source-inactive
  maps totaled 42-42. Report: `reports/local-20260809T221649Z`.
- Aggregate titanium was 172,540 versus 179,880 because source-inactive
  `snowflake` repeated the known 2-4 immutable self-mirror side variance from
  `reports/local-20260809T203800Z`; it is not attributable to this branch.
- Across 1,521,490 bot calls there were zero TLE/suspicious-output signals,
  maximum per-replay p99 3.795 ms, and maximum callback 7.157 ms.
- Frozen package: `artifacts/submissions/v0018_nordkap-route-owner_20260809-2231_eeafad8f.zip`.
  SHA-256: `8cafb5ce16682f2ba1e9f7bcb5fbf5488b6f8d2c443d42f3848e55e6eb84f9b7`.

## Status

Release gates passed and v0018 is packaged. It must not be deployed while
platform v75 is still observing below its 12-series minimum. v72 remains the
known-good rollback.
