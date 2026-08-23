# v277 large-board income-backed workforce relay — rejected

Date: 2026-08-19

## Objective and scope

The fresh live Drakkarfjord loss showed the active v105 bot stopping at eight
Builders and three Harvesters while the winner reached twelve Builders and
twelve Harvesters.  The v276 local losses showed the same long-board staffing
shape.  v277 tested a map- and income-gated relay: after the first completed
Harvester milestone and a recent positive Core income heartbeat, large boards
could raise the staged living-Builder target from eight to ten.  The initial
perimeter threshold was 48; the one allowed repair narrowed it to 60.  Only
`bots/candidate/bot/core_role.py`, `bots/candidate/bot/constants.py`, and
focused workforce tests were in the implementation scope.  No route, combat,
baseline, package, upload, activation, or live-state change was allowed.

## Evidence

- Initial focused coverage was **33/33**, compileall passed, `make static`
  retained the inherited exit-2 failures, and smoke was **4/4**.  The screen
  logs and focused artifacts are under
  `reports/iter-v277-large-board-workforce/`.
- Initial seed-172 screen report `reports/local-20260819T131826Z` was **9-6**;
  collection was **96,140/93,380 Ti** and first delivery existed in all
  15/15 games for both sides.  The candidate had zero TLE or suspicious rows.
- Initial seed-175 report `reports/local-20260819T132059Z` was **7-8**;
  collection was **62,740/64,580 Ti**, with delivery **15/15 vs 15/15** and
  zero TLE or suspicious rows.  The paired result was **16-14** and
  collection **158,880/157,960 Ti**: the edge did not repeat strongly enough
  for a release gate.
- The bounded repair changed only the perimeter threshold to 60 and added a
  medium-board preservation case.  Repair focused coverage was **33/33**;
  compileall passed, static retained exit 2, and smoke was **4/4**.
- Repair seed-172 report `reports/local-20260819T132318Z` was **10-5** with
  collection **71,850/61,710 Ti**, delivery **15/15 vs 15/15**, and zero
  TLE/suspicious rows.  Repair seed-175 report
  `reports/local-20260819T132455Z` was **4-11** with collection
  **41,440/55,870 Ti**, delivery **15/15 vs 15/15**, and zero TLE/suspicious
  rows.  The repaired pair was **14-16**, collection **113,290/117,580 Ti**.
  The repair therefore failed to produce a repeatable edge.

## Rollback and risks

The candidate production tree was restored recursively byte-identically to
immutable `bots/versions/v0044_income-heartbeat-handoff_20260819-1110_eeafad8f`;
`reports/iter-v277-large-board-workforce/post-rollback-parity.diff` is zero
bytes.  Rollback focused coverage was **31/31**, compileall passed, smoke was
**4/4**, and static retained exit 2.  No release gate, promotion, package,
upload, activation, or live transition occurred.  The v277 hypothesis is
rejected; inspect long-board replay conversion failures before choosing v278.
v0044 remains the local baseline.  v105 is retained as the user's requested
historical rollback reference only; v101 remains the guarded operational
fallback because v105's recorded live result is 142/275 (51.64%).
