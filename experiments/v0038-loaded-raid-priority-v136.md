# v136 loaded-raid task priority rejection

## Objective and scope

Test whether a concrete enemy logistics raid should be selected before the
dynamic Builder falls back to visible ore after the three-route economy gate.
The existing raid finder already assigns one nearest responder and requires a
forward shell; this experiment changed only task ordering, then repaired it to
preempt harvesting only for a visibly loaded conveyor or splitter. The opening
economy, adjacent-only orphan seed, fixed attacker, Store schema, navigation,
map rules, baseline snapshot, and platform state were out of scope.

Allowed source/test files were `bots/candidate/bot/dynamic.py` and
`tests/test_candidate_nearest_defense.py`; this record, reports, `UPDATES.md`,
and `state/project_state.json` are checkpoint metadata.

## Evidence

- Initial focused tests passed 17/17, compileall passed, smoke was 4/4
  command-clean, and `make static` retained the inherited exit-2 result (15
  obsolete imports plus two navigation fast-path assertions).
- Initial 54-game screen: **29-25**, candidate 194,620 versus comparator
  175,570 collected Ti (1.1085x), zero command failures, and map results of
  fjordgate 3-3, antler 5-1, icefloe 3-3, archipelago 1-5, nordkap 2-4,
  drakkarfjord 4-2, glacierkeep 4-2, auroraveil 3-3, and ragnarok 4-2.
  Report: `reports/local-20260817T125258Z`.
- Repair 1 focused tests passed 17/17, compileall passed, smoke was 4/4, and
  static retained the inherited failures. Restricting pre-harvest pressure to
  loaded conveyor/splitter targets regressed the screen to **23-31** and
  203,530 versus 239,790 Ti (0.8488x); map floors included nordkap 1-5,
  drakkarfjord 1-5, and auroraveil 2-4. Report:
  `reports/local-20260817T125839Z`.
- Both screens were 54/54 command-clean with zero TLE or suspicious-output
  records. No 210-game gate was warranted.
- Rollback focused tests passed 16/16, compileall passed, and rollback smoke
  was 4/4 command-clean (`reports/local-20260817T130652Z`). Rollback static
  retained the same inherited failures. Dynamic source parity against v0038
  is exact, and no production Python source differs from the v0038 snapshot.
  No package, upload, activation, or live-state change was made.

## Decision

Reject v136 after its initial screen and one bounded repair. The raid-priority
reordering did not produce a clear aggregate edge and its repair materially
reduced collection. Restore and retain
`bots/versions/v0038_orphan-local-seed_20260817-1223_eeafad8f` as the moving
local baseline. The next hypothesis must diagnose the v0038 Ragnarok loss
cluster without globally reordering the economy loop.
