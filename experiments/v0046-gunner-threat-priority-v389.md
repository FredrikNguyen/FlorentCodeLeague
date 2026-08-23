# v389 Gunner threat-class rotation priority — rejected

Date: 2026-08-21

## Objective and scope

Starting from immutable v0046, v389 tested whether home Gunners should rotate
toward enemy Sentinels, Launchers, and Gunners before nearer harmless logistics
when choosing a new firing line.  The candidate retained all existing turret
count, ammo, placement, and economy policies; only target ranking in
`bots/candidate/main.py` changed, with one focused behavioral test in
`tests/test_candidate_nearest_defense.py`.

## Validation

- Focused target/economy coverage passed **32/32**, compileall passed, and the
  static target retained the inherited 15 obsolete-module imports and two
  navigation fast-path assertions (`reports/iter-v389-gunner-priority-static.log`).
- Smoke was **4/4** command-clean at `reports/local-20260821T003440Z`.
- The rotated all-map 30-game screen (`screen_seed=727`) was command- and
  reliability-clean but tied v0046 at **15–15**.  Candidate/baseline
  collection was **114,480/102,230 Ti**, first deliveries were **30/29**, and
  max p99/peak was **1,400/4,930 us**, with zero TLE/suspicious rows.
  Raw games are under `reports/local-20260821T003514Z`; parsed evidence is
  `reports/iter-v389-gunner-priority/replay-analysis.json` and
  `screen-summary.json`.

## Decision and rollback

Reject v389 without a second screen or long gate: a collection edge without a
win-rate edge is not a promotion.  The temporary target priority, focused test,
and screen config were removed; candidate production is recursively identical
to immutable v0046 (the main-file proof is
`reports/iter-v389-gunner-priority/rollback-main.diff`, empty).  Rollback
focused coverage was **31/31**, compileall passed, rollback smoke was **4/4**
at `reports/local-20260821T003917Z`, and static retained the same inherited
exit-2 profile.  No promotion, package, upload, activation, or live transition
occurred.

## Remaining risk

Threat-class rotation is plausible for live infiltrations but did not produce a
local win-rate edge.  Keep v0046 as the best baseline and choose a distinct
resource-to-pressure mechanism next; do not retain this ranking change without
new replay evidence.
