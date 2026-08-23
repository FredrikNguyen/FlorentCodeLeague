# v368 reactive home Barrier response — rejected

Date: 2026-08-20

## Objective and scope

The v367 loss/top-team replays showed a recurring control difference: winning
sides spend cheap Barriers when an infiltrator or turret reaches home, while
v0046 has an unused per-builder home-barrier memory and answers most early
threats with a more expensive Gunner path.  v368 gave only the permanent
Defender one reactive Barrier before three completed routes, after a visible
enemy Builder/turret entered the existing home-threat radius and only while a
dynamic Harvester plus two conveyor links remained affordable.  The allowed
repair narrowed the trigger to an enemy Builder because turret/siege response
already exists in v0046.

Production scope was `bots/candidate/bot/defender.py` and
`bots/candidate/bot/constants.py`; focused coverage was the temporary
`tests/test_candidate_reactive_home_barrier.py`.  Routes, spawning, Store
layout, hijack/raid, offensive units, baseline, and live state were unchanged.

## Validation and decision

- Initial focused coverage: **38/38**; compileall passed; `make smoke` was
  **4/4**; `make static` retained the inherited 15 obsolete-module imports and
  two navigation assertions.
- Initial rotated screen (`screen_seed=401`) was **9-6**, all 15 candidate
  rows delivered, zero TLE/suspicious rows, and max p99/peak **1,207/4,876 us**.
- The independent screen (`screen_seed=409`) was **7-8**, all rows delivered,
  zero TLE/suspicious rows, max p99/peak **1,374/2,773 us**; pair **16-14**.
- The one allowed Builder-only repair passed **39/39**, compileall and smoke
  **4/4**, and retained the inherited static profile, but the rerun was **6-9**
  (all rows delivered, zero TLE/suspicious rows, max p99/peak **1,197/2,181
  us**).  The repaired pair was **15-15**.

The reactive Barrier did not produce a repeatable win-rate edge.  Reject v368,
restore exact recursive v0046 candidate parity, and do not run a release gate,
package, upload, activation, or live transition.

Reports: `reports/iter-v368-reactive-home-barrier/`,
`reports/local-20260820T193344Z`, `reports/local-20260820T193600Z`,
`reports/local-20260820T193904Z`.
