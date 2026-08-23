# v226 vector-gated infiltrator intercept — rejected

## Replay basis

The v224 position audit found that route-radius Builder entries before first
delivery were uncommon, but the saved v0042 loss sample had a route-response
median of **22 rounds** versus **6 rounds** for side A in the top-team sample.
The rejected v143 route-sentry fired on proximity alone (even after repairs
at squared distance 2 and orthogonal adjacency) and never exceeded its
30-24 control. v225's protected-midline lease also failed its release gate
(29-31) and was removed. The causal gap is therefore response selectivity and
latency, not a permanent escort or an opening movement restriction.

## Objective

Give a nearby Dynamic Builder a short, local response to a likely infiltrator
without stealing the route workforce. An enemy Builder must be observed on a
strictly inward trajectory toward our Core for multiple observations and be
within squared distance 2 of a friendly Harvester/Conveyor/Splitter. The
response starts only after one completed route, excludes active chains and
fixed attackers, is owned by the deterministic nearest responder, and expires
quickly when the target leaves sight or stops advancing.

## Allowed files

- `bots/candidate/main.py` for per-unit enemy-Builder motion memory;
- `bots/candidate/bot/constants.py` for the task and bounded expiry/geometry;
- `bots/candidate/bot/dynamic.py` for detection, ownership, and the existing
  legal strike/movement execution;
- one focused infiltrator-intercept test module;
- this experiment record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable
  report/state metadata.

## Non-goals

No proximity-only route sentry, cross-map recall, Barrier/Launcher/Sentinel/
Gunner policy, route rewrite, Store slot/schema change, hijack/sabotage
primitive, map-name branch, baseline/archive/package, upload, activation, or
live-state change. Active `MODE_CHAIN`, urgent home threat, and permanent
attacker work remain ahead of this task.

## Done criteria

Focused tests cover delayed motion confirmation, strict inward progress,
route-radius filtering, first-route/economy guard, nearest ownership,
expiry/stale target handoff, and legal adjacent fire/cardinal movement.
Compileall, `make static`, and `make smoke` retain the inherited profile. A
rotated 15-map screen against exact v0042 must be command-clean, introduce no
new no-delivery row, and show a clear paired win-rate or route-response edge
without a protected-map collapse. Run the 60-game gate only if that screen is
clearly positive; otherwise allow at most two bounded repairs and restore exact
v0042 parity.

## Initial checkpoint

Focused coverage was **33/33**, candidate compileall passed, `make smoke` was
**4/4** command-clean, and `make static` retained only the inherited 15
obsolete-module imports plus two navigation fast-path assertions. The
configured 15-map screen was command- and delivery-clean with zero TLE or
suspicious rows, but finished **7-8** candidate-side and collected
**66,100 vs 77,270 Ti**; mean first delivery was **29.93 vs 26.73**. It did
not establish a paired edge. Replay evidence is in
`reports/local-20260818T203054Z` and
`reports/iter-v226-infiltrator-intercept/screen-replay-analysis.json`.

## Bounded repair and decision

Add an explicit live-economy reserve (one Harvester plus one Conveyor) to the
intercept detector. A likely infiltrator should not pull a responder into a
combat detour while the balance cannot replace the route it is defending. No
other selector, geometry, or execution behavior changes.

The repair passed **34/34** focused tests, compileall, and smoke **4/4**;
static retained the same inherited exit 2. Its rotated 15-map screen remained
**7-8**, with collection **54,070 vs 68,580 Ti**, mean first delivery
**27.80 vs 34.53**, and zero no-delivery/TLE/suspicious rows. Because neither
the initial vector contract nor its single reserve repair beat v0042, the
candidate was rolled back rather than sent to the 60-game gate.

The second bounded repair moved interception below ordinary harvesting in the
selector and narrowed the local response radius from squared 2 to squared 9.
It passed **32/32** focused tests, compileall, and smoke **4/4**; static
retained the inherited exit 2. Its rotated screen was still **7-8**, with
collection **74,980 vs 83,750 Ti**, mean first delivery **36.87 vs 35.07**,
and zero no-delivery/TLE/suspicious rows
(`reports/local-20260818T204230Z`). It supplied no release evidence.

After the two unsuccessful bounded repairs, the candidate was fully rolled
back. Final rollback focused coverage was **27/27**, compileall passed, static
retained the inherited failures, and smoke was **4/4** at
`reports/local-20260818T204703Z`. Every candidate Python file is byte-
identical to immutable v0042; v0042 remains the local baseline. No promotion,
package, upload, activation, or live-state transition occurred.

Evidence: `reports/local-20260818T203054Z`,
`reports/local-20260818T203358Z`, `reports/local-20260818T204230Z`,
`reports/local-20260818T204703Z`,
`reports/iter-v226-infiltrator-intercept/`, and the v224 audit. The response
latency proxy is useful for review, but this local intercept does not convert
enough games to justify production complexity; the next hypothesis must be a
different phase/mechanic rather than widening this detector.
