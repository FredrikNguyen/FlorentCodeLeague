# v405 Post-delivery dynamic Core-cage lease (rejected)

Date: 2026-08-21

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward_20260821-0200_eeafad8f`,
v405 tested a late offensive-topology lease inspired by the top-team Barrier
counts.  After five completed routes, Core `PRESSURE`, confirmed enemy-Core
intel, and an observed forward Sentinel, the nearest non-fixed dynamic Builder
could claim one visible empty tile inside the enemy-Core cage radius.  The
existing Barrier executor, belt-sever guard, and v0047 fixed-attacker cage
remained unchanged.  A replacement-Harvester plus fixed-attack reserve had to
remain funded.

Production scope was `bots/candidate/bot/dynamic.py`; temporary focused
coverage was added to `tests/test_candidate_nearest_defense.py`; the rotated
screen configuration was `experiments/.tmp-v405-siege-cage.toml`.  Store
schema, route FSM, spawning, ammo, Sentinel/Launcher policy, home defense,
map-name branches, packaging, upload, activation, and live state were
non-goals.

## Validation

- Candidate focused coverage passed **28/28**, compileall passed, and smoke was
  **4/4**.  `make static` retained the inherited exit-2 profile (15 obsolete
  imports and two navigation assertions); no v405-specific production static
  error appeared.  Logs are under `reports/iter-v405-siege-cage/`.
- The rotated all-map 30-game screen (`screen_seed=1663`) scored **13-17** for
  the candidate.  Candidate and comparator deliveries were **30/30**;
  collection was **145,760 vs 154,720 Ti**; and command failures, TLEs, and
  suspicious rows were zero.  Maximum p99/peak callback time was
  **1,378/5,587 us**.  Candidate losses were 0-2 on Drakkarfjord, Drumlin,
  Midgard, and Nordkap.  Candidate placed 166 Barriers versus 185 for the
  comparator.  Raw games are under `reports/local-20260821T061249Z`, with
  diagnostics in `reports/iter-v405-siege-cage/replay-analysis.json`.

## Decision and rollback

Reject v405 without repair: the bounded cage lease did not improve aggregate
win rate or collection and did not clear the 19-11 floor.  Temporary
production, focused-test, and matrix-config edits were removed.  Recursive
candidate production parity with immutable v0047 is exact at
`reports/iter-v405-siege-cage/rollback-source-parity.diff`.
Rollback focused coverage was **26/26**, compileall passed, rollback smoke was
**4/4** at `reports/local-20260821T061733Z`, and static retained only the
known inherited failures.  No release, package, remote gate, upload,
activation, or baseline transition occurred.

## Remaining risk

The top-team Barrier count is not enough evidence that dynamic Builders should
leave route conversion for a second cage owner; the candidate actually placed
fewer Barriers and lost four protected maps.  Keep v0047's fixed-attacker cage
and economy ordering.  Choose a distinct replay-backed conversion or
defensive hypothesis next.
