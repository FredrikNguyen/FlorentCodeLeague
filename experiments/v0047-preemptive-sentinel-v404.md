# v404 Preemptive Sentinel beacon response (rejected)

Date: 2026-08-21

## Objective and scope

Starting from immutable `v0047_pressure-economy-steward_20260821-0200_eeafad8f`,
v404 tested whether a Core-visible enemy Sentinel could be assigned to the
nearest home responder before the Sentinel had damaged the Core.  The
candidate decoded the existing zero-missing-HP `SLOT_CORE_SIEGE` beacon only
when the position was current, in vision, in bounds, and occupied by an enemy
Sentinel.  Ordinary siege thresholds, home-threat detection, route work, and
fixed attackers were unchanged.

Production scope was `bots/candidate/bot/dynamic.py`; temporary focused
coverage was added to `tests/test_candidate_nearest_defense.py`; the matrix
configuration was `experiments/.tmp-v404-preemptive-sentinel.toml`.  The Store
writer, spawning, route FSM, Launcher/Barrier policy, packaging, upload,
activation, and live state were non-goals.

## Validation

- Candidate focused coverage was **33/33**, compileall passed, and smoke was
  **4/4**.  `make static` retained the inherited exit-2 profile (15 obsolete
  imports and two navigation assertions); no v404 production static error was
  introduced.  Logs are under `reports/iter-v404-preemptive-sentinel/`.
- The first rotated 30-game all-map screen (`screen_seed=1621`) scored
  **17-13** for the candidate.  Candidate/comparator deliveries were
  **30/30**, collection was **145,240 vs 107,000 Ti**, and command failures,
  TLEs, and suspicious rows were zero.  Maximum p99/peak callback time was
  **1,365/3,672 us**.  Per-map losses included Valkyrie 0-2; the raw games
  are under `reports/local-20260821T054731Z`, with diagnostics in
  `replay-analysis.json`.
- The independent rotated repeat with the same source (`screen_seed=1621`)
  scored **13-17**.  Candidate/comparator deliveries were **30/29**,
  collection was **110,100 vs 125,370 Ti**, and command failures, TLEs, and
  suspicious rows were zero.  Maximum p99/peak was **1,449/6,165 us**.
  Drakkarfjord, Drumlin, Icefloe, and Yulerune were candidate 0-2 losses;
  raw games are under `reports/local-20260821T055101Z`, with diagnostics in
  `replay-analysis-2.json`.

## Decision and rollback

Reject v404 without repair: the independent repeat reversed the first-screen
edge and fell below the 19-11 promotion floor.  Temporary production,
focused-test, and matrix-config edits were removed.  Recursive candidate
production parity with immutable v0047 is exact at
`reports/iter-v404-preemptive-sentinel/rollback-source-parity.diff`.
Rollback focused coverage was **26/26**, compileall passed, rollback smoke was
**4/4** at `reports/local-20260821T055645Z`, and static retained only the
known inherited failures.  No release, package, remote gate, upload,
activation, or baseline transition occurred.

## Remaining risk

The zero-damage Core beacon is not a stable predictor of a winning Sentinel
intercept: the repeat lost collection and four protected maps.  Keep the
existing v0047 siege threshold and task ordering.  The next candidate must
use a distinct replay-backed conversion or defensive-topology signal and must
clear the same baseline gate before promotion.
