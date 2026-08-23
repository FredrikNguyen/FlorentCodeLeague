# v407 Source Harvester Barrier guard — rejected

## Objective and scope

Compare one bounded defensive-topology change against immutable
`v0047_pressure-economy-steward_20260821-0200_eeafad8f`: after the established
economy threshold, let the nearest non-fixed Builder place a Barrier beside a
connected friendly Harvester only when a visible enemy Builder is close to the
source.  Preserve the output side, Core ring, route reserve, task ordering,
Store schema, and all other production behavior.  Temporary edits were limited
to `bots/candidate/bot/defender.py`, focused tests, and temporary evaluation
configs.

## Evidence

- The initial broad screen (`screen_seed=1717`) was **14-16** for the candidate
  against v0047.  It delivered **30/30** on both sides, collected
  **146,170 vs 157,790 Ti**, and had zero command failures/TLEs/suspicious rows;
  max p99/peak was **1,324/5,338 us**.
- The bounded repair requiring a nearby visible enemy Builder reached **19-11**
  on the rotated 30-game screen, with **30/30** deliveries, collection
  **162,350 vs 164,450 Ti**, zero command failures/TLEs/suspicious rows, and
  max p99/peak **1,481/4,719 us**.  This met the short-screen floor but did not
  establish a release-quality improvement.
- The required 60-game release gate was **31-29**, with **60/60** deliveries,
  collection **289,390 vs 319,690 Ti**, zero command failures/TLEs/suspicious
  rows, and max p99/peak **1,473/2,117 us**.  The candidate was not
  significantly better and lost aggregate collection.

## Validation and decision

Focused candidate coverage was **29/29**, compileall passed, and smoke was
**4/4** (`reports/local-20260821T064438Z`).  `make static` retained the
inherited exit-2 profile (15 obsolete imports plus two navigation assertions),
with no v407-specific error.  Release and replay evidence is under
`reports/local-20260821T064925Z` and `reports/iter-v407-source-barrier/`.

Reject v407.  Temporary production, test, and config edits were removed;
recursive production parity with immutable v0047 is exact.  Rollback focused
coverage was **26/26**, compileall passed, and rollback smoke was **4/4**
(`reports/local-20260821T065733Z`).  No package, upload, activation, live
state change, or baseline transition occurred.  Keep v0047 as the baseline and
use a distinct replay-backed hypothesis next; do not widen the source Barrier
guard without stronger evidence.
