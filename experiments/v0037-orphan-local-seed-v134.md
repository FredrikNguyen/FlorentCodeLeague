# v134 local orphan-seed repair

## Objective and scope

Test whether an opening Builder that is already nearest to a visible own
Harvester with no adjacent friendly Conveyor/Splitter can seed one legal local
outlet before the normal Harvester builder runs. The responder is restricted to
the pre-first-delivery phase (`SLOT_HARVESTER_COUNT == 0`), excludes designated
attackers, suppresses duplicate claims near an active chain owner, and must
already be adjacent to the selected seed tile. No owner backtracking, Store
schema, navigation, combat, Launcher/Sentinel, map branch, baseline source, or
platform operation was included.

Allowed source/test files were `bots/candidate/bot/defender.py` and
`tests/test_candidate_nearest_defense.py`; this experiment record and durable
state are the only checkpoint metadata.

## Evidence

- Focused tests: 25/25 pass after the initial implementation and after the
  bounded repair; compileall passes.
- `make static` remains the inherited repository failure: 15 obsolete import
  errors plus two navigation fast-path assertions; no new error was introduced.
- Smoke is 4/4 command-clean after both source states. Reports:
  `reports/local-20260817T114706Z` and `reports/local-20260817T115515Z`.
- Initial 54-game screen: candidate **25-29**, with one candidate
  no-delivery row. Report: `reports/local-20260817T114906Z`.
- Repair 1 changed only the responder from local navigation to adjacent-only
  seeding. The 54-game screen improved to **34-20**, with one candidate
  no-delivery row (in a loss), zero command failures/TLE/suspicious output,
  maximum p99 callback 1,487 us, and maximum peak callback 5,692 us. Report:
  `reports/local-20260817T115537Z`.
- Full 21-map, seven-seed, side-swapped gate: **125-85 (59.52%)** versus
  immutable v0037, 210/210 command-clean, zero TLE/suspicious output, three
  candidate no-delivery rows, maximum p99 callback 1,487 us, and maximum peak
  callback 5,692 us. Report: `reports/local-20260817T120039Z`.
- Full-gate map floors: antler 8-6, archipelago 8-6, auroraveil 7-7,
  drakkarfjord 10-4, drumlin 8-6, fjordgate 8-6, frostgate 10-4,
  glacierkeep 7-7, icefloe 9-5, midgard 7-7, nordkap 12-2, ragnarok 4-10,
  royale 8-6, valkyrie 11-3, and yulerune 8-6. Ragnarok is the remaining
  protected-map risk despite the aggregate win-rate gain.

## Decision

Repair 1 is accepted as the moving local baseline under the current paired
win-rate policy: it clears the 54-game edge and wins 125/210 against v0037
without reliability failures. The immutable snapshot is archived as v0038;
the live platform is not uploaded or activated in this checkpoint. Next work
must target the ragnarok loss cluster without weakening the opening economy or
the no-delivery guard.
