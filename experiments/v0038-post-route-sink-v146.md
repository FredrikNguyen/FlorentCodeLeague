# v146 post-route Harvester sink repair — locally promoted

## Parent and objective

Parent: immutable local baseline
`bots/versions/v0038_orphan-local-seed_20260817-1223_eeafad8f`.

Replay review found that `_try_reconnect_orphaned_harvester` treated any
adjacent friendly Conveyor/Splitter as an accepting outlet. A Conveyor facing
into the Harvester is on its output side and cannot accept; a Splitter accepts
only at its back. The objective was to validate the sink direction and permit
the existing local orphan repair after the first completed route.

## Exact scope

- `bots/candidate/bot/defender.py`
- `tests/test_candidate_nearest_defense.py`
- this record, reports, `UPDATES.md`, configs, and durable state

Non-goals were navigation, arbitrary conveyor merging, combat/workforce/Store
redesign, baseline edits during the experiment, and platform upload/activation.

## Implementation

Added `_harvester_has_accepting_neighbor`: Conveyors accept on their three
non-output sides; Splitters accept only on the side opposite their facing.
`_try_reconnect_orphaned_harvester` now uses that check and is eligible for a
visible post-route orphan while retaining nearest-responder and adjacency
guards. Added tests for an inward belt repair and an already accepting belt.

## Evidence

- Focused tests: 18/18; compileall passed; `make static` retained the inherited
  exit 2 (15 obsolete imports plus two navigation fast-path assertions).
- Smoke: 4/4 command-clean, report `reports/local-20260817T172343Z`.
- 54-game screen: **30-24**, 223,490 vs 209,840 collected Ti, zero candidate
  no-delivery vs one comparator; zero command/TLE/suspicious-output failures;
  max p99/peak 1,490/5,590 us. Report:
  `reports/local-20260817T172407Z`; replay diagnostics:
  `reports/iter-v146-post-route-sink/screen-replay-analysis.json`.
- 210-game gate: **121-89** (57.6%), 1,027,120 vs 852,170 collected Ti;
  map splits: antler 6-8, archipelago 8-6, auroraveil 9-5, drakkarfjord
  8-6, drumlin 11-3, fjordgate 8-6, frostgate 7-7, glacierkeep 7-7,
  icefloe 8-6, midgard 9-5, nordkap 7-7, ragnarok 9-5, royale 7-7,
  valkyrie 9-5, yulerune 8-6. Replay diagnostics were zero TLE/suspicious
  output, max p99/peak 1,476/5,651 us, three no-delivery games per side,
  and mean first delivery 32.3 vs 38.0 turns. Reports:
  `reports/local-20260817T172948Z` and
  `reports/iter-v146-post-route-sink/long-replay-analysis.json`.

## Decision

Promote v146 as the new local immutable baseline. Preserve the exact candidate
under `bots/versions/` and point local matrix configs at it. No platform upload,
activation, or live-state transition is performed in this checkpoint.

## Remaining risks

The candidate still has three no-delivery games in the full matrix, and
delivery starts later on average despite the win-rate gain. Live rating and
remote-server behavior remain unverified; keep v0038 available for rollback.
