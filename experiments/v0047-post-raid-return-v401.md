# v401 Post-raid return lease (rejected)

Date: 2026-08-21

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward_20260821-0200_eeafad8f`,
v401 tested a lifecycle correction for dynamic Builder raids.  After a
confirmed adjacent fire against an enemy logistics target, the raider would
finish the target and return to the Core radius before selecting another task.
The intent was to convert successful sabotage into a defensive/economic pulse
instead of allowing the same worker to remain stranded in the enemy lane.

Production scope was `bots/candidate/bot/dynamic.py`; focused coverage was
temporary additions to `tests/test_candidate_economy_phase.py`.  Route FSM,
target selection, Store schema, spawning, fixed attackers, Sentinel/Launcher
policy, package, upload, activation, and live state were non-goals.

## Validation

- Focused coverage was **35/35**, compileall passed, and `make smoke` was
  **4/4**.  `make static` retained the inherited exit-2 profile (15 obsolete
  imports and two navigation fast-path assertions); no v401-specific static
  error appeared.  Logs are under
  `reports/iter-v401-post-raid-return/`.
- The rotated all-map 30-game screen (`screen_seed=1471`) was **14-16** for
  the candidate, below the 19-11 promotion floor.  Candidate deliveries were
  **30/30** versus **29/30** for v0047; command failures, TLEs, and suspicious
  rows were zero.  Maximum p99/peak callback time was **1,451/6,672 us** and
  collection was **141,560 vs 134,870 Ti** (candidate vs comparator).
- Per-map wins were antler 1-1, archipelago 2-0, auroraveil 2-0, drakkarfjord
  1-1, drumlin 0-2, fjordgate 1-1, frostgate 0-2, glacierkeep 0-2, icefloe
  1-1, midgard 2-0, nordkap 1-1, ragnarok 0-2, royale 0-2, valkyrie 2-0,
  and yulerune 1-1.  Replay diagnostics are in
  `reports/iter-v401-post-raid-return/replay-analysis.json`; raw games are
  under `reports/local-20260821T051704Z`.

## Decision and rollback

Reject v401: the delivery edge did not offset a 14-16 win regression, with
protected losses concentrated on Drumlin, Frostgate, Glacierkeep, Ragnarok,
and Royale.  No bounded repair was attempted because the failure was a broad
conversion regression rather than an isolated lifecycle defect.  Temporary
source and focused-test edits were removed, the temporary matrix config was
deleted, and recursive candidate production parity with immutable v0047 is
exact.  Rollback focused coverage was **32/32**, compileall passed, smoke was
**4/4** at `reports/local-20260821T052232Z`, and static retained only the known
inherited failures.  No release, package, remote gate, upload, activation, or
baseline transition occurred.

## Remaining risk

The baseline still loses several protected maps while converting surplus into
offense.  A future candidate must target a distinct map-aware conversion
mechanism and retain the v0047 route/delivery floor; do not revive this
post-raid return lease unchanged.
