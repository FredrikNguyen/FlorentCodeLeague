# v248 offense progress watchdog — rejected

## Objective

Test one structural continuous-offence mechanism against the exact moving
baseline v0042: when a fixed attacker has held an explicit remembered enemy
logistics target without closing distance or removing hit points for a bounded
window, clear that stale target and replan through the existing legal pressure
ladder. The experiment must not interrupt normal Core travel, Sentinel
construction, or economy conversion.

## Allowed files

- `bots/candidate/bot/attacker.py`;
- `tests/test_candidate_nearest_defense.py`;
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, durable state metadata,
  and report files.

## Non-goals

No economy, route FSM/geometry, Harvester or workforce target, infiltration or
hijack selector, Sentinel/Barrier/Launcher/Gunner policy, Store schema,
map-specific branch, baseline/archive, package, upload, activation, or live
state operation.

## Done criteria

Focused tests, candidate compileall, static, and smoke must retain the
inherited profile. The rotated 15-map screen must be command/delivery-clean
with no new TLE or suspicious rows and show a repeatable paired edge. Only a
screen-positive candidate may advance to the 60-game release gate. A failed
release gate requires exact v0042 source parity and no promotion.

## Results

The initial watchdog armed from the guessed Core lane and was rejected after a
**4-11** screen with **45,350 vs 85,840 Ti**. Focused coverage was **26/26**,
compileall passed, smoke was **4/4**, and static retained the inherited
profile (15 obsolete-module import errors and two navigation fast-path
assertions). Raw report: `reports/local-20260819T031952Z`; replay analysis:
`reports/iter-v248-offense-watchdog/screen-replay-analysis.json`.

Repair 1 watched only an explicit remembered logistics target. It passed
**26/26** focused tests, compileall, and smoke **4/4**, but the screen improved
only to **6-9**, with **73,700 vs 81,180 Ti**. Raw report:
`reports/local-20260819T032259Z`; replay analysis:
`reports/iter-v248-offense-watchdog/repair-replay-analysis.json`.

Repair 2 cleared the stale target and fell through the existing priority ladder
instead of forcing an early fallback. It passed **26/26**, compileall, and
smoke **4/4**. Its screen was **12-3**, **88,900 vs 54,970 Ti**, with zero TLE
or suspicious rows, so it advanced to the release gate. Raw report:
`reports/local-20260819T032555Z`; replay analysis:
`reports/iter-v248-offense-watchdog/repair2-replay-analysis.json`.

The configured 60-game release gate was command-clean but failed the paired
promotion criterion: the candidate won **24-36 (40%)**, collected
**246,020 vs 273,550 Ti**, and had no wins on either endpoint run of Fjordgate
or Valkyrie. Reliability was clean (zero TLE/suspicious rows; maximum p99
**1,526 us**, peak **4,618 us**). Raw report:
`reports/local-20260819T032755Z`; replay analysis:
`reports/iter-v248-offense-watchdog/release-replay-analysis.json`.

Reject v248 after the two bounded repairs. Removed only the temporary watchdog
source/test hunks; `bots/candidate/bot/attacker.py` is byte-identical to the
immutable v0042 copy, with zero lines in
`reports/iter-v248-offense-watchdog/rollback-source.diff`. Rollback focused
coverage was **23/23**, compileall passed, and rollback smoke was **4/4** at
`reports/local-20260819T033635Z`. Baseline remains v0042; no package, upload,
activation, or live-state transition occurred.

## Blocker and next direction

The screen-positive result was seed/side-sensitive and did not transfer to the
release gate. Do not promote or reopen this watchdog unchanged. Revisit
continuous offence only with fresh replay causality and a mechanism that is
aware of map topology and both side orders before spending another long gate.
