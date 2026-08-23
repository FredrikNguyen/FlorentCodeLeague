# v0040 idle Harvester chain handoff — v164

Date: 2026-08-18

## Objective

Convert an adjacent ore opportunity found by the last-resort idle fallback
into a real paying route. The baseline fallback can build a Harvester when a
Builder has no selected task, but it returns without entering `MODE_CHAIN`, so
the new source can remain disconnected and consume the same opening resource
that should create a conveyor path.

## Comparator and allowed files

- Comparator: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Source: `bots/candidate/main.py` and the existing Harvester/chain helper in
  `bots/candidate/bot/defender.py` (no defender source edit is planned).
- Focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, reports, `UPDATES.md`, and durable project state.

## Non-goals

No route geometry/facing, Dynamic task ordering, Builder spawning, fixed
attacker/defender behavior, ammo, turret/Sentinel/Barrier/Launcher policy,
Store layout, map-specific branch, baseline/archive, package, upload,
activation, or live-state change.

## Hypothesis and implementation

Replace the fallback's duplicated bare-ore build with the existing
`_try_build_harvester` helper. That helper already gates the live cost and
legality checks and initializes `MODE_CHAIN`, `chain_limit`, and the route
state. The fallback still runs only after the role produced no action or move,
so this changes an otherwise wasted turn into a connected route attempt.

## Done criteria

- Focused coverage proves an idle adjacent-ore conversion enters `MODE_CHAIN`
  and initializes its route state; existing nearest-defense/route tests remain
  green.
- Candidate compileall passes; `make static` is checked and inherited failures
  are recorded; smoke is command-clean.
- The shortened 24-game all-map screen materially beats v0040 on aggregate
  paired win rate, with no command/TLE/suspicious-output failure or severe
  delivery collapse. Only a qualifying screen advances to the 60-game release
  matrix.
- A failed screen or release gate requires exact v0040 rollback and no
  platform operation.

## Validation and decision

- Focused checks passed **27/27**, candidate compileall passed, `make static`
  retained the inherited 15 obsolete-import errors and two navigation
  assertions, and smoke was **4/4** command-clean
  (`reports/iter-v164-idle-harvester-chain-*`).
- The shortened 24-game all-map screen scored **15-9** versus v0040, with
  candidate Ti **73,780** versus **50,260**, zero no-delivery rows on either
  side, and replay max p99/peak **1,364/2,917 us**
  (`reports/local-20260818T011701Z` and
  `reports/iter-v164-idle-harvester-chain-screen-replay-analysis.json`).
- The 60-game release matrix scored **39-21**, candidate Ti **167,950** versus
  **152,700**, one no-delivery row per side, zero command failures/TLEs/
  suspicious output, and max p99/peak **1,517/5,024 us**
  (`reports/local-20260818T011957Z` and
  `reports/iter-v164-idle-harvester-chain-release-replay-analysis.json`).
- Complete source review found only the intended fallback handoff; all other
  candidate bot modules remain byte-identical to v0040. v164 qualifies as a
  new local best by paired win rate and is ready for immutable archiving and
  the guarded remote/live release workflow. The active platform version is
  unchanged until those steps complete.

## Remote gate decision

The guarded server match `fc3d1bcf-38a3-4bd4-994d-ab9b98860b8a` ran v164 as
Team A against v0040 on sprint, bridge, crossfire, vault, and aurora. It
finished **1-4** for v0040. The candidate was reliability-clean, but remote
replays showed a repeatable workforce deficit: v164 placed **1/4/6/4/5**
Harvesters on the five maps while v0040 placed **5/7/9/4/7**. The downloaded
replays and analysis are under
`reports/iter-v164-idle-harvester-chain-remote-replays/` and
`reports/iter-v164-idle-harvester-chain-remote-replay-analysis.json`.

The local edge is therefore not portable to the server map instances. v164 is
**rejected at the remote gate** despite the 39-21 local release result. The
v0041 archive is retained as an immutable rejected artifact, but no upload,
activation, or live-state change occurred; the mutable candidate must return
to v0040 before the next workforce hypothesis.
