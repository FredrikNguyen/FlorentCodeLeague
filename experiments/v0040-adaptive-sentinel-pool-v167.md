# v0040 adaptive Sentinel pool — v167

Date: 2026-08-18

## Objective

Address the recurring pressure losses on Royale, Auroraveil, Glacierkeep, and
Nordkap where the candidate often reaches the enemy side with fewer forward
Sentinels than v0040. The current economy ramp permits one early Sentinel and
then jumps directly to the full three-Sentinel pool only after five completed
chains. This experiment tests a guarded intermediate second Sentinel once the
team has both paying-route proof and confirmed enemy Core intel.

## Comparator and allowed files

- Comparator: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Source: `bots/candidate/bot/attacker.py` and `bots/candidate/bot/constants.py`.
- Focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, reports, `UPDATES.md`, and durable project state.

## Non-goals

No route navigation or chain geometry, Builder role/spawn policy, ore target
ranking, combat target selection, ammo conversion, barrier cage, Store layout,
map-specific branch, baseline/archive, package, upload, activation, or live
state change.

## Hypothesis and implementation

Keep the existing one-Sentinel opening and three-Sentinel five-chain target.
Between those thresholds, permit a second forward Sentinel only when at least
two completed chains are recorded, the enemy Core has been confirmed, and the
current bank can still fund one replacement Harvester plus one Sentinel. This
is a reversible resource-backed transition rather than a global Sentinel
increase; it should add pressure on maps where v0040 under-fields defense while
preserving the opening economy reserve.

## Done criteria

- Focused tests cover the one-, two-, and three-Sentinel pool transitions,
  including missing intel and insufficient-bank guards; existing role/route
  tests remain green.
- Candidate compileall passes; `make static` is checked and inherited failures
  are recorded; smoke is command-clean.
- The shortened 24-game all-map screen materially improves aggregate paired
  win rate over v0040 without systematic TLE/suspicious output or candidate
  delivery collapse. Only a qualifying screen advances to the 60-game gate.
- A failed screen or release requires exact v0040 rollback and no platform
  operation. Remote comparison is attempted only after a qualifying release.

## Validation and decision

The initial guarded two-route variant passed focused checks **28/28**,
compileall, and command-clean smoke (`reports/local-20260818T021303Z`);
`make static` remained at the inherited 15 obsolete-import errors plus two
navigation fast-path assertions (`reports/iter-v167-adaptive-sentinel-pool-static.log`).
Its 24-game screen was command-clean but tied v0040 **12-12**, with no
candidate no-delivery games. Replay analysis showed candidate first delivery
mean **45.1** versus **28.6** for v0040, while Sentinel placements averaged
**3.29** versus **3.04**; the extra Sentinels did not convert to wins
(`reports/local-20260818T021330Z` and
`reports/iter-v167-adaptive-sentinel-pool-screen-replay-analysis.json`).

Repair 1 lowered the intermediate route threshold from two completed chains to
one while preserving confirmed Core intel and the replacement reserve. Focused
checks remained **28/28**, compileall passed, smoke was command-clean
(`reports/local-20260818T021659Z`), and static had the same inherited failures
(`reports/iter-v167-adaptive-sentinel-pool-repair1-static.log`). The repair
screen again tied **12-12**, with zero candidate no-delivery games; candidate
first delivery mean was **28.5** versus **25.0**, and Sentinel placements
fell to **3.04** versus **3.88** (`reports/local-20260818T021713Z` and
`reports/iter-v167-adaptive-sentinel-pool-repair1-screen-replay-analysis.json`).
It did not qualify for the release gate.

Both variants were rejected without a 60-game release, remote comparison,
package, upload, activation, or baseline transition. The intermediate pool
and its tests were rolled back to exact recursive v0040 parity (**0 diff
lines**; `reports/iter-v167-adaptive-sentinel-pool-rollback-source-diff.txt`).
Rollback focused checks passed **25/25**, compileall passed, and rollback smoke
was command-clean (`reports/local-20260818T022030Z`). The pressure losses still
need an intervention that improves confirmed-Core timing or route workforce,
not another Sentinel-count ramp.
