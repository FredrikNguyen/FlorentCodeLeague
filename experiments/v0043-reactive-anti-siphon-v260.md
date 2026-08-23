# v260 reactive anti-siphon against hostile logistics — rejected after one repair

## Replay basis and objective

Fresh read-only live capture `reports/live-v259-followup-20260819T073600Z`
contained a concrete infiltration shape absent from the earlier enemy-Builder
audit. In Coreflood match `225ac574-3dc7-4997-ba23-37269182b627`, game 3,
enemy Conveyors appeared orthogonally beside our Harvesters on turns 26, 40,
123, 154, 248, 254, and 381. Their facings left our Harvester on an accepting
input side, so the opponent could siphon stacks without an enemy Builder
entering the route radius. The current dynamic policy ignored hostile belts
unless the post-shell raid was open.

v260 reused `TASK_HOME_THREAT` for only a visible enemy Conveyor/Splitter
adjacent to a friendly Harvester whose fixed output did not point into that
Harvester. The nearest non-fixed dynamic Builder used the existing legal
adjacent-fire path; active CHAIN owners, fixed attackers, ordinary belts, and
the Store/route FSM were unchanged.

## Validation

- Initial focused coverage was **30/30**, candidate/baseline compileall passed,
  `make static` retained the inherited 15 obsolete-module import errors plus
  two navigation fast-path assertions, and smoke was **4/4**. The exact-v0043
  15-map screen was command-clean at **6-9**, with candidate/baseline
  collection **65,930/87,030 Ti**, zero TLE/suspicious rows, and raw report
  `reports/local-20260819T074544Z`.
- The screen contained many geometric contacts, but most were empty belts and
  the 2-damage Builder attack required long chases. One bounded repair kept the
  same facing test but required `get_stored_resource()` to prove a currently
  loaded hostile outlet before committing a worker. Repair focused coverage
  was **31/31**, compileall passed, static retained the same inherited result,
  and smoke was **4/4**. The repair screen improved only to **7-8**, with
  collection **55,290/70,070 Ti**, zero TLE/suspicious rows, and no protected
  map or delivery edge; raw report `reports/local-20260819T074952Z`.

## Decision and rollback

Reject v260. The loaded-outlet repair removed low-confidence empty-belt
chases, but one 15-map win edge was not repeatable and collection regressed.
No release/long gate or platform operation was justified. Temporary detector
and focused tests were removed; recursive candidate parity with immutable
v0043 is exact (`reports/iter-v260-anti-siphon/rollback-source.diff`, empty).
Rollback focused coverage was **26/26**, compileall passed, and rollback smoke
was **4/4** at `reports/local-20260819T075233Z`. No package, upload, activation,
promotion, or live-state transition occurred.

## Remaining risk and next direction

Hostile accepting outlets are real in live replays, but spending a dynamic
Builder to grind a 20-HP belt did not convert into wins. Keep the evidence for
future high-confidence sabotage; next test the resource/defense trade directly
by delaying extra home Gunners until a stronger route economy exists, while
retaining the two-Gunner floor and immediate response to actual siege turrets.
