# v174 blocked-attack economy rejoin

## Objective

Use replay evidence from the v0040 loss cluster to keep a fixed attacker from
idling forever on an unconfirmed, wall-separated enemy-Core lane. After a
short grace period and repeated no-step navigation, the attacker may rejoin
the existing Defender economy loop once, then return to direct pressure. This
was tested as a structural handoff, not a general workforce increase.

## Allowed files

- `bots/candidate/main.py`
- `bots/candidate/bot/attacker.py`
- `bots/candidate/bot/constants.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and durable state

## Non-goals

No route geometry, Dynamic task priorities, Sentinel/cage policy, home-defense
policy, Launcher/Barrier behavior, Store schema, immutable baseline, package,
upload, activation, or live-state changes.

## Evidence

- Initial implementation passed focused **23/23**, compileall, and command-clean
  smoke **4/4**. The 21-game all-map screen was **12-9** versus v0040 with
  zero no-delivery rows and zero runtime failures. Yulerune improved to 12
  versus 10 Harvesters, but the aggregate edge was not yet decisive
  (`reports/local-20260818T040707Z`,
  `reports/iter-v174-blocked-attack-rejoin-screen-replay-analysis.json`).
- Repair 1 allowed the same one-time handoff before the first completed route,
  retaining the round-80, eight-stall, unconfirmed-Core gates. Focused checks
  remained **23/23**, compileall passed, static retained the inherited exit-2
  result, and smoke was **4/4**. The screen improved to **13-8**, with zero
  candidate no-delivery rows and max p99/peak **1,478/5,179 us**
  (`reports/local-20260818T041101Z`,
  `reports/iter-v174-blocked-attack-rejoin-repair1-screen-replay-analysis.json`).
- The 60-game all-map release gate was locally positive at **34-26** versus
  v0040 (56.7%), zero no-delivery rows on either side, zero TLE/suspicious
  output/command failures, and max p99/peak **1,534/2,608 us**
  (`reports/local-20260818T041313Z`,
  `reports/iter-v174-blocked-attack-rejoin-release60-replay-analysis.json`).
- The required five-map server gate completed **1-4** for the candidate,
  reliability-clean. Remote losses reproduced the workforce/resource deficit
  on sprint, bridge, vault, and aurora; crossfire was the only candidate win
  (`reports/remote-20260818T041945Z`, match
  `d766ba27-6560-4434-a9eb-15a74fe33279`,
  `reports/iter-v174-blocked-attack-rejoin-remote-replay-analysis.json`).

## Decision and rollback

The local release edge did not transfer to server maps, so v174 is **rejected**
and no promotion or platform upload/activation is allowed. Candidate source
was restored to exact recursive v0040 parity (**0 diff lines**);
rollback focused tests passed **20/20**, compileall passed, and rollback smoke
was **4/4**. Static remains the known inherited obsolete-import and navigation
fast-path failure. Full logs and remote replay downloads are preserved under
the report paths above and `reports/iter-v174-blocked-attack-rejoin-*`.
