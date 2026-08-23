# v137 economy workforce floor rejection

## Objective and scope

Test the replay-backed phase hypothesis that stage-2 non-attacker Builders
should remain in the Defender economy loop until three completed routes, rather
than becoming dynamic immediately after the first route. Ragnarok losses often
had only two-to-five Harvesters while the stronger side had seven or more. A
bounded repair released the floor early when the bank was already rich, so
resource-rich maps could pressure sooner.

Allowed source/test files were `bots/candidate/main.py` and
`tests/test_candidate_nearest_defense.py`; this record, reports, `UPDATES.md`,
and `state/project_state.json` are checkpoint metadata. No Store schema, route
FSM, task ordering, map branch, navigation, baseline snapshot, or platform
operation was allowed.

## Evidence

- Initial focused checks passed 17/17, compileall passed, smoke was 4/4
  command-clean, and static retained the inherited exit-2 result (15 obsolete
  imports plus two navigation fast-path assertions). The 54-game screen was
  **31-23 (57.41%)**, 240,960 versus 181,520 collected Ti (1.3275x), zero
  no-delivery rows, and zero command/TLE/suspicious-output failures. Map
  results included Archipelago 5-1, Auroraveil 5-1, Nordkap 4-2, and Ragnarok
  1-5. Report: `reports/local-20260817T131522Z`.
- The release-sized 210-game matrix was reliability-clean (210/210 command
  clean, zero TLE/suspicious output, max p99 1,484 us, peak 5,325 us) but only
  **107-103 (50.95%)**, 865,280 versus 887,780 Ti (0.9747x). Map floors were
  Midgard 3-11, Royale 3-11, while Ragnarok improved to 9-5. Report:
  `reports/local-20260817T132105Z`.
- Repair 1 kept the floor only below the rich-bank state. Focused checks passed
  17/17, compileall passed, smoke was 4/4, and static retained the inherited
  failures. The 54-game screen regressed to **25-29 (46.30%)**, 159,270
  versus 172,480 Ti (0.9234x), with Auroraveil 1-5 and Archipelago/Nordkap
  2-4; report `reports/local-20260817T134339Z`.
- Rollback focused checks passed 16/16, compileall passed, rollback smoke was
  4/4 (`reports/local-20260817T134854Z`), and rollback static retained the
  inherited failures. All nine candidate Python sources are byte-identical to
  v0038 after rollback. No package, upload, activation, or live-state change
  was made.

## Decision

Reject v137 after the long-gate regression and one bounded repair. The next
hypothesis must address the Ragnarok chain/route conversion failure without a
global workforce phase change; retain
`bots/versions/v0038_orphan-local-seed_20260817-1223_eeafad8f` as the moving
local baseline.
