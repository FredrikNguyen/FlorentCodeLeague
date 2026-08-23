# v0040 opening workforce floor — v165

Date: 2026-08-18

## Objective

Repair the opening workforce deficit exposed by the v164 remote gate. On the
five server maps, v164 placed only **1/4/6/4/5** Harvesters against v0040's
**5/7/9/4/7**, and lost four of five matches while remaining
reliability-clean. Keep newly spawned non-attacker Builders in the economy
role until three completed Harvester routes exist, so the scalable opening
workforce cannot switch to dynamic pressure before the first route base is
established.

## Comparator and allowed files

- Comparator: `bots/versions/v0040_shared-route-progress_20260817-1853_eeafad8f`.
- Source: `bots/candidate/main.py`.
- Focused coverage: `tests/test_candidate_nearest_defense.py`.
- Bookkeeping: this record, reports, `UPDATES.md`, and durable project state.

## Non-goals

No route geometry, chain construction, costs, combat, fixed attacker or
defender designations, Dynamic task ordering, Store layout, map-specific
branch, baseline/archive, package, upload, activation, or live-state change.

## Hypothesis and implementation

Change the fallback in `_assign_role` from an exact zero-route check to the
existing `OFFENSE_MIN_HARVESTERS` threshold. Permanent attacker/defender
assignments remain unchanged. Dynamic Builders therefore become economy
Defenders while the shared completed-route count is 0, 1, or 2, and only
return to the existing dynamic pool at three completed routes.

## Done criteria

- Focused coverage proves non-designated Builders are `ROLE_DEFENDER` below
  three completed routes and `ROLE_DYNAMIC` at the threshold; fixed role
  designations remain unchanged.
- Candidate compileall passes; `make static` is checked and inherited failures
  are recorded; smoke is command-clean.
- The shortened 24-game all-map screen materially improves aggregate paired
  win rate over v0040, with no command/TLE/suspicious-output failure or severe
  delivery collapse. Only a qualifying screen advances to the 60-game release
  matrix.
- A failed screen or release gate requires exact v0040 rollback and no
  platform operation. Remote comparison is attempted only after a qualifying
  local release result.

## Validation and decision

The initial three-route floor passed focused checks, compileall, and smoke. The
24-game screen was command-clean and scored **13-11** versus v0040. Replay
review found two candidate-side zero-delivery losses (Royale and
Drakkarfjord), while the candidate's route counts still did not establish a
clear opening floor advantage. A 13-11 edge is not a material improvement, so
the candidate did not advance to the release matrix.

### Bounded repair 1

Narrow the economy floor to the first **two** completed routes, leaving the
third-route transition to the existing Dynamic policy. This tests whether the
three-route Defender lock was too restrictive while preserving a meaningful
opening workforce floor. No other behavior changes. The repair will be
rejected and rolled back with the iteration if its 24-game result is not a
material aggregate improvement.

Repair 1 passed focused checks **27/27**, compileall, and command-clean smoke
(`reports/local-20260818T014310Z`). Its 24-game screen scored **14-10** versus
v0040, with all 15 maps represented, zero command/TLE/suspicious-output rows,
and no candidate-side zero-delivery games
(`reports/local-20260818T014335Z` and
`reports/iter-v165-opening-workforce-floor-repair1-screen-replay-analysis.json`).
This clears the short-screen threshold for the reduced 60-game release gate;
the candidate still must pass that gate before any remote comparison.

The reduced 60-game release gate then reversed to **26-34** against v0040,
with zero command failures, zero TLEs, zero suspicious-output rows, maximum
replay p99/peak execution of **1,418/5,459 us**, and no candidate-side
zero-delivery games (`reports/local-20260818T014615Z` and
`reports/iter-v165-opening-workforce-floor-repair1-release-replay-analysis.json`).
Repair 1 is rejected at the release gate; no remote comparison, package,
upload, activation, or baseline transition was attempted.

The source was restored to exact recursive v0040 parity (zero diff lines).
Rollback focused checks passed **26/26**, compileall passed, and rollback smoke
was **4/4** command-clean (`reports/local-20260818T015305Z`). The moving
baseline remains v0040 and the next iteration must target a different failure
mode than role-floor timing.
