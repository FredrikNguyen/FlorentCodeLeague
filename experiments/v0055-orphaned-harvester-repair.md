# v0055 — orphaned-Harvester reconnect

## Objective

Restore production when an enemy destroys the complete outbound belt from an
owned Harvester. The existing repair detector can fix a surviving conveyor's
gap, but it cannot discover a Harvester whose first conveyor was also removed.

## Allowed files

- `bots/candidate/main.py`
- `bots/candidate/bot/defender.py`
- `tests/test_candidate_nearest_defense.py`
- this record, `UPDATES.md`, and `state/project_state.json`

## Non-goals

- no changes to attack/sentinel priorities, workforce caps, navigation, or map
  branches;
- do not interrupt a builder already in `MODE_CHAIN`;
- do not treat a fresh Harvester still being connected as orphaned;
- no platform upload or activation before a local promotion gate passes.

## Implementation

In SCOUT mode, after ordinary belt repair and before fresh Harvester purchase,
scan visible owned Harvesters that have no adjacent friendly conveyor/splitter.
Only consider them after the first route milestone or the bounded mid-game
round, and skip a target with a nearby friendly Builder. Navigate to a legal
adjacent seed tile, build one conveyor with a core-directed facing, then reuse
the existing seeded-route chain until it joins the Core ring. The detector is
local and deterministic; it does not add store slots.

## Promotion gate

Focused tests, `make static`, `make smoke`, then the six-map weak screen against
the moving best v0030. If the screen is a strict win-rate improvement and
reliability-clean, run the full 21-map/5-seed/side-swapped matrix, archive the
candidate, and repoint the moving baseline. Otherwise revert all bot edits and
retain v0030.
