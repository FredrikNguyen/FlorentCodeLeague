# v0037 first-delivery gate plus loaded-belt sabotage (v98 parent)

## Objective

Repair the server-transfer failure found in v99.  v99 could spend 30 Ti on a
forward Sentinel before its opening route had paid back, producing a sprint
delivery at turn 157 in the remote gate.  Require one completed harvester chain
before any forward Sentinel purchase, while retaining v99's loaded-line raid
priority.

## Scope

- Parent comparator: immutable platform v98 snapshot
  `bots/versions/v0027_early-two-sentinel-shell_20260813-1831_eeafad8f`.
- Changed file: `bots/candidate/bot/attacker.py` only.
- Added guard in `_try_build_sentinel`: return before Sentinel purchase when
  `SLOT_HARVESTER_COUNT == 0`.
- Retained v99's loaded conveyor/splitter scoring (300/250/200 base with a
  200 loaded bonus).

## Evidence

- Focused prefilter: `reports/local-20260814T034515Z` — 33–21 (61.11%),
  0 command failures across 54 games.
- Remote server gate: match `8e322c8b-4f2c-46d4-9ebd-3d45d326b401`, 3–2;
  evidence `reports/remote-v100-first-delivery-match.json` and replay analysis
  `reports/remote-v100-first-delivery-replay-analysis.json`.  First delivery
  was turn 14 on sprint and turn 40 on bridge.
- Full release matrix: `reports/local-20260814T035252Z` — 124–86 (59.05%),
  0 ties, 0 command failures across all 210 map/seed/side games.
- Full replay diagnostics:
  `reports/iter-v100-first-delivery-full-replay-analysis.json`.
  Wins averaged 6.95 harvesters and 8.34 sentinels; losses averaged 5.20
  harvesters and 4.00 sentinels.  Worst maps were skerry and vase at 3–7.
- Syntax/functional checks: Python compile passed; `make smoke` passed 4/4
  (`reports/local-20260814T041705Z`).  `make static` remains blocked by 15
  inherited obsolete test imports (`reports/iter-v100-first-delivery-static.log`).

## Decision and risks

This candidate is eligible for guarded promotion: it exceeds the 55% full
matrix gate, improves v99 by eight wins, and passes the remote gate with no
reliability error.  Preserve v72 as rollback and v98 as the fixed comparator.
Vase/skerry remain weak, and late/no-delivery losses still occur on vase; the
next iteration should target route recovery there without removing the gate.
