# v385 stale forward-Sentinel retirement — rejected

## Objective and scope

Starting from immutable local baseline
`bots/versions/v0046_post-delivery-siege-phase-v335_20260820-0530_eeafad8f`,
v385 tested the requested unit-reuse behavior: when the owning attacker had a
forward Sentinel that survived the early-death window but fell to 10 HP or
less, it could destroy that obsolete structure for free, blacklist the old
tile, and immediately seek a different legal Core-facing site.  A replacement
site was fully preflighted before the destroy, so no Sentinel was removed when
there was no alternate firing geometry.

Allowed production files were `bots/candidate/bot/attacker.py`,
`bots/candidate/bot/constants.py`, and `bots/candidate/main.py`, with temporary
coverage in `tests/test_candidate_nearest_defense.py`.  A temporary rotated
screen config, this record, reports, `UPDATES.md`, `docs/CURRENT_PLAN.md`, and
durable state were bookkeeping.  Routes, workforce, Store layout, opening
Launcher, Barrier cage, ammo policy, baseline snapshots, package, upload,
activation, and live state were non-goals.

## Validation

- Focused coverage passed **33/33**; candidate compileall passed.  `make
  static` retained the inherited 15 obsolete-module imports and two navigation
  fast-path assertions; no v385-specific static error appeared.
- `make smoke` was **4/4** command-clean at
  `reports/local-20260820T233258Z`.
- The explicit immutable-v0046 rotated all-map screen (15 maps, both sides,
  `screen_seed=647`) was command-, delivery-, and reliability-clean but only
  **15–15**.  Candidate and baseline both delivered in **30/30** rows;
  collection was **138,160 vs 173,590 Ti**.  Candidate ended with **203 vs
  208** Harvesters and **45 vs 34** Sentinels.  Max p99/peak callback time was
  **1,350/2,508 us**, with zero TLE or suspicious rows.  Raw games are
  `reports/local-20260820T233341Z`; replay diagnostics are
  `reports/iter-v385-sentinel-retirement/replay-analysis.json`.

## Decision and rollback

Reject v385 without a long gate.  The retirement policy increased surviving
Sentinel count but converted 35,430 fewer titanium into the economy and did not
improve wins.  Threshold-only repairs would be ungrounded, so the temporary
state, thresholds, logic, focused tests, and config were removed.  Recursive
candidate parity with immutable v0046 is empty at
`reports/iter-v385-sentinel-retirement/rollback-source-parity.diff`.

Rollback focused coverage was **31/31**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260820T233832Z`.  No promotion, release gate,
package, upload, activation, or live transition occurred; immutable v0046
remains the comparator and local baseline.

## Follow-up

Do not retry Sentinel teardown by changing only the age or HP threshold.  The
next candidate must address the remaining map-dependent Harvester/Conveyor
resource-conversion losses while preserving first-delivery, runtime, and
protected-map floors.
