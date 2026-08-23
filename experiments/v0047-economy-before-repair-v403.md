# v403 Economy-before-generic-repair priority (rejected)

Date: 2026-08-21

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward_20260821-0200_eeafad8f`,
v403 tested a phase-scoped task-order change.  While the route count or Core
phase was still opening, converting, or crisis, a dynamic Builder with an
economy claim chose Harvester/route work before a generic damaged-building
repair.  Home threats, belt gaps, and enemy-Harvester hijacks remained ahead;
once pressure was established, the existing repair priority stayed intact.

Production scope was `bots/candidate/bot/dynamic.py`; temporary focused
coverage was added to `tests/test_candidate_nearest_defense.py`.  Route FSM,
Store schema, spawning, fixed attacker/Launcher/Sentinel policy, package,
upload, activation, and live state were non-goals.

## Validation

- Candidate focused coverage was **34/34**, compileall passed, and smoke was
  **4/4**.  `make static` retained the inherited exit-2 profile: 15 obsolete
  imports and two navigation assertions; no production-specific static error
  appeared after the fixture import correction.  Logs are under
  `reports/iter-v403-economy-repair-priority/`.
- The rotated all-map 30-game screen (`screen_seed=1571`) was **12-18**, below
  the 19-11 promotion floor.  Candidate and comparator deliveries were both
  **30/30**; command failures, TLEs, and suspicious rows were zero.  Maximum
  p99/peak callback time was **1,372/3,021 us**, and collection was effectively
  tied at **158,770 vs 158,750 Ti**.  Candidate wins by map were Nordkap 1-1,
  Antler 1-1, Drumlin 1-1, Valkyrie 2-0, Archipelago 1-1, Auroraveil 1-1,
  Drakkarfjord 1-1, Icefloe 1-1, Frostgate 1-1, Royale 0-2, Fjordgate 0-2,
  Ragnarok 0-2, Glacierkeep 1-1, Yulerune 1-1, and Midgard 0-2.  Raw games
  are under `reports/local-20260821T053841Z`; diagnostics are in
  `reports/iter-v403-economy-repair-priority/replay-analysis.json`.

## Decision and rollback

Reject v403 without repair: moving generic repair below early economy did not
produce a win-rate edge and left four protected maps at 0-2.  Temporary
production, focused-test, and matrix config edits were removed.  Recursive
candidate production parity with immutable v0047 is exact at
`reports/iter-v403-economy-repair-priority/rollback-source-parity.diff`.
Rollback focused coverage was **32/32**, compileall passed, smoke was **4/4**,
and static retained only the known inherited failures.  No release, package,
remote gate, upload, activation, or baseline transition occurred.

## Remaining risk

Generic repair remains ahead of opening economy for a reason: the task reorder
did not turn resource parity into wins.  The next candidate should target a
different pressure/conversion mechanism and preserve v0047 task ordering.
