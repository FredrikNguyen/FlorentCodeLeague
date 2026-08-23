# v0040 Harvester route verification — v150

Date: 2026-08-17

## Objective

Use the existing homeward repair ranking to correct a first-route conveyor
whose saved walking direction is a sideways/backward detour, while preserving
the v0040 route FSM for ordinary forward links. The hypothesis came from the
fresh live v102 losses (Atlas, TRRR, and Landers), where low or zero delivery
was associated with sparse or disconnected conveyor networks.

## Allowed scope and non-goals

The candidate scope was `bots/candidate/bot/defender.py` and one focused test
fixture in `tests/test_candidate_nearest_defense.py`. Economy thresholds,
navigation, combat, workforce, Store protocol, map selection, baseline
archives, and platform state were non-goals. Every screen used immutable
`bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f` as the
comparator.

## Done criteria

- Keep ordinary v0040 chain facing unchanged.
- Focused tests, compileall, and smoke pass; static must be checked and any
  inherited failures recorded.
- The 54-game screen must beat v0040 on paired wins without command/TLE or
  suspicious-output regressions; only then may the 210-game gate and release
  packaging be considered.

## Attempts

1. Applied the repair ranking whenever `_best_feed_direction` was absent.
   Focused **21/21**, compileall passed, smoke **4/4**, and static retained
   the inherited failures. The screen was **13-41** versus v0040, with zero
   command failures or stderr; replay evidence showed ordinary forward links
   were being rewritten, so the attempt was rejected.
2. Restricted the repair to non-monotonic saved directions relative to the
   Core. Focused **21/21**, compileall passed, smoke **4/4**, and static had
   the same inherited failures. The screen improved to **23-31**, still below
   v0040, with zero command failures/stderr; no long gate was run.
3. Restricted it further to the first pending link of a new chain. Focused
   **21/21**, compileall passed, smoke **4/4**, and static remained inherited
   red. The screen reached **25-29**, still below v0040, with zero command
   failures/stderr; this was the second and final permitted repair.

Reports: `reports/iter-v150-harvester-route-verification/`, including the
three screen runs `reports/local-20260817T192242Z`,
`reports/local-20260817T192903Z`, and `reports/local-20260817T193459Z`.

## Live replay evidence

The reviewed v102 losses remain under `reports/live-v102-replays/`, with the
compact analysis in `reports/iter-v149-route-seal/live-replay-analysis.json`.
They showed first delivery lag, 2–7 Harvesters and 25–102 conveyors in the
losses, and a Glacierkeep-style disconnected route. The evidence motivated
this bounded repair but did not justify changing ordinary chain facing.

## Decision

v150 is **rejected after two bounded repairs**. The v150 source and focused
fixture were restored byte-for-byte to v0040; rollback focused tests were
**20/20**, compileall passed, rollback smoke was **4/4**, and static retained
the known inherited failures. No 210-game gate, package, upload, activation,
or baseline transition was performed.

## Next risk

The remaining defect is route verification, not a safe global facing rewrite.
The next iteration should start from v0040 and test one Harvester-owned
progress/sink marker or a bounded post-build verification action, with no
changes to ordinary detour routing until replay evidence proves the marker is
wrong.
