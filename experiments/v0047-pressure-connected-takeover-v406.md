# v406 Pressure connected-source takeover priority (rejected)

Date: 2026-08-21

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward_20260821-0200_eeafad8f`,
v406 tested whether a healthy pressure-phase dynamic Builder should take over
one visible enemy Harvester that already had a hostile Conveyor/Splitter
outlet before repairing a local belt gap.  The branch required five completed
routes, the Core's `PRESSURE` phase, nearest non-fixed ownership, and enough
titanium for a replacement Harvester, two Conveyors, and the fixed attack
reserve.  Opening, converting, and crisis task order remained unchanged.

Production scope was `bots/candidate/bot/dynamic.py`; temporary focused
coverage was added to `tests/test_candidate_nearest_defense.py`; the rotated
screen configuration was `experiments/.tmp-v406-pressure-takeover.toml`.
Route FSM, Store schema, spawning, Sentinel/Launcher/Barrier/Gunner policy,
map branches, packaging, upload, activation, and live state were non-goals.

## Validation

- Candidate focused coverage passed **28/28**, compileall passed, and smoke was
  **4/4**.  `make static` retained the inherited exit-2 profile (15 obsolete
  imports and two navigation assertions); no v406-specific production static
  error appeared.  Logs are under `reports/iter-v406-pressure-takeover/`.
- The rotated all-map 30-game screen (`screen_seed=1693`) scored **14-16** for
  the candidate.  Candidate/comparator deliveries were **30/29**; collection
  was **119,440 vs 127,250 Ti**; placed Harvesters/Conveyors were **249/2,790
  vs 243/2,665**; and command failures, TLEs, and suspicious rows were zero.
  Maximum p99/peak callback time was **1,294/5,636 us**.  Candidate losses
  were 0-2 on Antler, Drakkarfjord, Fjordgate, Nordkap, Ragnarok, and
  Yulerune.  Raw games are under `reports/local-20260821T062203Z`, with
  diagnostics in `reports/iter-v406-pressure-takeover/replay-analysis.json`.

## Decision and rollback

Reject v406 without repair: the connected-source priority increased route
placements but did not improve win rate or collection and missed the 19-11
floor.  Temporary production, focused-test, and matrix-config edits were
removed.  Recursive candidate production parity with immutable v0047 is exact
at `reports/iter-v406-pressure-takeover/rollback-source-parity.diff`.
Rollback focused coverage was **26/26**, compileall passed, rollback smoke was
**4/4** at `reports/local-20260821T062556Z`, and static retained only the
known inherited failures.  No release, package, remote gate, upload,
activation, or baseline transition occurred.

## Remaining risk

Pressure-only source takeover is still too expensive or too late to convert
the extra route placements into wins.  Preserve v0047's belt-repair-first
ordering and ordinary hijack selector; choose a different causal mechanism
next.
