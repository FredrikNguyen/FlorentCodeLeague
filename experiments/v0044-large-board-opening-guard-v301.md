# v301 — large-board opening Gunner guard

Date: 2026-08-19

## Hypothesis and scope

Fresh v107 losses on 30x30 boards ended at turns 73–99 with no candidate home
Gunner, while the opponents had one or two Gunners by turns 35–60 and forward
Sentinels.  v301 tested one map-contextual defense phase: after round 36 and
before the first completed route, a long-board Core could authorize exactly one
designated Defender to build a home Gunner only when the dynamic bank still
covered that Gunner, one Harvester, two Conveyors, and the standing economy
reserve.  Compact maps, post-route turret policy, routes, workforce, offense,
and other units were unchanged.  Scope was limited to `constants.py`,
`core_role.py`, `defender.py`, and focused nearest-defense coverage.

## Validation and evidence

- Focused nearest-defense/seeded-route/economy coverage passed **38/38**;
  candidate compileall passed.  `make static` retained the inherited exit-2
  profile: 15 obsolete removed-module imports and two navigation assertions.
- `make smoke` was **4/4** command-clean at
  `reports/local-20260819T195749Z`.
- The 15-map screen against immutable v0044 was command- and delivery-clean
  but negative: candidate-A finished **7-8**, collected
  **75,760 vs 81,020 Ti**, and first delivery averaged **34.73 vs 27.47**
  turns.  Every row delivered; there were zero TLE/suspicious rows and max
  p99/peak callback time was **1,492/2,465 us**.  Candidate placed 31 Gunners
  versus the comparator's 38 without a long-board survival or win-rate edge.
  Evidence is `reports/local-20260819T195814Z` and
  `reports/iter-v301-opening-guard/replay-analysis.log`.

## Decision and rollback

Reject v301 without repair or release.  The temporary constants, phase gate,
and tests were removed; `constants.py`, `core_role.py`, and `defender.py` are
each byte-identical to immutable v0044, proven by the empty
`reports/iter-v301-opening-guard/rollback-source-parity.diff`.
Rollback focused coverage was **34/34**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260819T200115Z`.  No 60-game gate, package,
upload, activation, or live transition occurred.  v105 remains the
operational rollback target and live v107 remains `active_observing`.
