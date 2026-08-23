# v402 Map-aware opening Launcher gate (rejected)

Date: 2026-08-21

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward_20260821-0200_eeafad8f`,
v402 tested a map-aware opening control contract.  The primary attacker's
existing one-home-Launcher relay stayed immediate on cramped maps, but on
longer maps it waited until the Core observed one completed Harvester chain.
The intent was to avoid competing with the first route where the control
corridor is not immediately contested.

Production scope was `bots/candidate/bot/attacker.py`; temporary focused
coverage was added to `tests/test_candidate_nearest_defense.py`.  Route FSM,
Store schema, spawning, dynamic task selection, Sentinel/Gunner policy,
Launcher lifecycle after the first build, package, upload, activation, and
live state were non-goals.

## Validation

- Candidate focused coverage passed **34/34** after correcting the fixture;
  compileall passed.  The first static invocation included the two temporary
  fixture failures plus the inherited 15 obsolete imports and two navigation
  assertions; after the fixture correction and rollback, static retained only
  the inherited profile.  Smoke was **4/4**.
- The rotated all-map 30-game screen (`screen_seed=1523`) scored **11-19**
  against v0047.  Candidate deliveries were **30/30** versus **29/30** for
  the comparator; command failures, TLEs, and suspicious rows were zero.
  Maximum p99/peak callback time was **1,352/5,032 us** and collection was
  **117,970 vs 156,310 Ti**.  Per-map candidate wins were Nordkap 1-1,
  Frostgate 0-2, Fjordgate 2-0, Icefloe 1-1, Archipelago 1-1, Glacierkeep
  1-1, Auroraveil 2-0, Midgard 0-2, Yulerune 0-2, Royale 1-1, Ragnarok 1-1,
  Drumlin 0-2, Antler 0-2, Valkyrie 0-2, and Drakkarfjord 1-1.
  Raw games are under `reports/local-20260821T053005Z`; diagnostics are in
  `reports/iter-v402-map-launcher-gate/replay-analysis.json`.

## Decision and rollback

Reject v402 without repair: the 11-19 screen and 38,340 Ti collection deficit
show that deferring the relay removed useful control without reliably
improving route conversion.  Temporary production, focused-test, and matrix
config edits were removed.  Recursive candidate production parity with
immutable v0047 is exact at
`reports/iter-v402-map-launcher-gate/rollback-source-parity.diff`.
Rollback focused coverage was **32/32**, compileall passed, smoke was **4/4**
at `reports/local-20260821T053407Z`, and static retained only the known
inherited failures.  No release, package, remote gate, upload, activation, or
baseline transition occurred.

## Remaining risk

The opening Launcher should not be gated by map size alone.  Resource-to-
pressure conversion remains the dominant v0047 weakness on protected maps;
the next candidate must use a distinct causal signal and preserve the exact
opening relay unless replay evidence supports a narrower change.
