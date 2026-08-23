# v352 source-Sentinel interceptor — rejected in self-review

Date: 2026-08-20

## Replay basis and proposed mechanism

The fresh platform-v108 loss to Askar City was reliability-clean but repeatedly
lost active Harvesters to enemy Sentinels.  Examples include Nordkap source
`(6,11)` removed at turn 38 with an enemy Sentinel on the same lane, Icefloe
sources `(3,11)` and `(6,11)` removed at turns 58 and 62, and Yulerune sources
removed at turns 93, 170, and 203.  The raw live input is
`reports/live-v108-scheduler-audit-20260820T115830Z/23ac_game_*.replay26`.

The initial hypothesis was a one-shot, local counter: when an enemy Sentinel's
visible fixed ray had a live, routed friendly Harvester as its first friendly
target, a non-attacker adjacent to an empty tile before that source would build
one correctly faced Sentinel.  It retained two Conveyor costs, excluded fixed
attackers/core-ring/belt-sever sites/multi-Sentinel lanes, and used a
per-source one-shot guard.  The intention was to trade for the hostile turret
while preserving a source that had already begun converting.

Temporary scope was `bots/candidate/main.py`,
`bots/candidate/bot/defender.py`, and
`tests/test_candidate_nearest_defense.py`.  Source selection, ordinary chain
geometry, Store schema, Core spawning, fixed identities, baseline/archive,
package, platform, and live state were non-goals.

## Focused validation and self-review

The temporary focused nearest-defense suite passed **30/30** at
`reports/iter-v352-source-sentinel-interceptor/focused.log`.

The mechanism was rejected before any screen because it does not meet its own
causal guarantee:

1. `GAME_RULES.md` specifies that Sentinel fire is not blocked by walls or
   intervening units.  The opposing bot owns target choice, so an intervening
   friendly Sentinel cannot be assumed to stop a capable opponent from firing
   the Harvester directly.
2. The Core only guarantees the 10-ammo floor before its normal prestock path.
   A counter Sentinel needs three 10-ammo shots to remove a 40-HP Sentinel;
   the proposed defensive Sentinel is not recorded as a forward Sentinel, so
   it cannot safely rely on the existing forward-siege ammo buffer.
3. A direct source shot destroys a 30-HP Harvester in two 18-damage shots.
   Therefore a single counter turret neither survives nor kills reliably
   enough to protect source delivery under the engine's permitted targeting.

These are mechanics failures, not a parameter issue.  Do not repair this by
loosening cost/ammo thresholds, adding repeated counter turrets, or assuming a
nearest-target opponent policy.

## Rollback and durable result

All temporary production/test changes were removed.  Recursive candidate
source parity with immutable v0046 is empty at
`reports/iter-v352-source-sentinel-interceptor/rollback-source-parity.diff`.

- Rollback focused suite: **26/26** pass,
  `reports/iter-v352-source-sentinel-interceptor/rollback-focused.log`.
- Candidate compileall: pass,
  `reports/iter-v352-source-sentinel-interceptor/rollback-compileall.log`.
- `make static`: inherited failure profile only (15 stale deleted-module
  imports and two navigation fast-path assertions),
  `reports/iter-v352-source-sentinel-interceptor/rollback-static.log`.
- `make smoke`: **4/4 command-clean** at
  `reports/local-20260820T130712Z`; log:
  `reports/iter-v352-source-sentinel-interceptor/rollback-smoke.log`.

No 15-game screen, 60-game release matrix, remote gate, package, upload,
activation, promotion, or live-state transition occurred.  Immutable v0046
remains the local baseline and platform v108 remains `active_observing`.

## Next direction

Treat source Sentinel attrition as evidence to audit **preemption**, not to
ship an unproven reactive shield.  Before another implementation, compare the
v108 loss and top-team replays for the earliest actionable point at which a
source-killing Sentinel could be prevented, denied resources, or safely
outpaced.  Any new mechanism must remain useful when the enemy deliberately
targets the Harvester and when the team has only the 10-ammo floor; otherwise
it is not eligible for a candidate screen.
