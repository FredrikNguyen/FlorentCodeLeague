# v258 pre-route home infiltrator interception — rejected

## Replay basis and hypothesis

Fresh live v106 Glacierkeep replay `replays/live-v106-refresh/atlas-ad2b2c0a/game_5.replay26`
showed the opponent destroying early home conveyors and replacing the vacated
tiles with Barriers at `(13,3)`, `(15,4)`, `(16,3)`, and `(14,4)`. It later
placed 31 Barriers and 198 Conveyors while our side had only 4 Harvesters and
84 Conveyors, first delivering at round 592 before the 999-turn
`titanium_collected` loss. v258 tested whether the permanent Defender could
intercept the visible enemy Builder before three completed routes, but only
while a friendly home Harvester/Conveyor/Splitter was still present.

## Exact scope

- `bots/candidate/bot/defender.py`: SCOUT-only local detector/executor;
- `tests/test_candidate_nearest_defense.py`: gate, ownership, legality, and
  chain-preservation coverage;
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable state/report
  metadata.

No generic Barrier demolition, opening-order rewrite, active-chain interrupt,
hijack/raid selector, fixed-attacker pressure, Launcher/Sentinel/Gunner
purchase, Store, map branch, baseline/archive, package, upload, activation, or
live-state change was included.

## Validation

- Focused nearest-defense coverage: **30/30** after correcting one fixture
  that accidentally selected a non-adjacent Builder; report
  `reports/iter-v258-home-infiltrator/focused-initial.log`.
- Candidate compileall: pass at
  `reports/iter-v258-home-infiltrator/compileall.log`.
- `make static`: inherited exit 2 only (15 obsolete deleted-module imports and
  two navigation fast-path assertions),
  `reports/iter-v258-home-infiltrator/static.log`.
- `make smoke`: **4/4** command-clean,
  `reports/iter-v258-home-infiltrator/smoke.log`.
- Rotated 15-map screen against exact v0043: **7-8** candidate-A, all 15
  sides delivered, **62,270 vs 68,370 Ti**, zero TLE/suspicious rows, maximum
  p99/peak **1,508/3,059 us**. Raw report:
  `reports/local-20260819T070825Z`; parsed diagnostics:
  `reports/iter-v258-home-infiltrator/screen15-analysis.json`.

## Decision and rollback

The screen supplied no win-rate or collection edge, and none of its controlled
baseline pairings showed an actual enemy-Builder infiltration event that would
validate a repair. Reject v258 without a repair or longer gate. Temporary
source and test edits were removed; recursive candidate parity with immutable
v0043 is zero at `reports/iter-v258-home-infiltrator/rollback-source.diff`.
Rollback focused coverage was **26/26**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260819T071408Z`. No release gate, package,
upload, activation, or live-state transition occurred. Preserve the live
Glacierkeep causality as evidence, but do not widen the already-rejected
infiltrator family; the next candidate needs a distinct route-preservation or
conversion hypothesis.
