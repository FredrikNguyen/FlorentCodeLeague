# v141 chain-pending recovery

## Objective

Preserve a pending conveyor when a danger flee or local displacement moves a
Builder away from the vacated tile. The repair navigates back under the current
danger map and uses the existing blocked limit; a bounded-distance repair keeps
only local recoveries.

## Allowed files

- `bots/candidate/bot/defender.py`
- `tests/test_candidate_seeded_route.py`
- this experiment record, reports, `UPDATES.md`, and durable state

## Non-goals

- No route merging, workforce/role/task changes, exploration, combat, ammo,
  Store, map branch, baseline, package, upload, or activation changes.

## Results

- Initial pending recovery: focused 21/21, compileall passed, smoke 4/4,
  static inherited exit 2; 54-game screen **26-28**, candidate/comparator Ti
  **220,810/200,280**, no-delivery **1/1**. Report:
  `reports/local-20260817T144253Z`.
- Repair 1 limited recovery to pending tiles within squared distance 16.
  Focused 21/21, compileall passed, smoke 4/4, static inherited exit 2; screen
  **29-25**, candidate/comparator Ti **198,520/204,950**, no-delivery **0/0**.
  Ragnarok was 6-0, but the aggregate edge was only four games and collection
  regressed. Report: `reports/local-20260817T144837Z`.
- Both runs were command-clean with zero TLE/suspicious-output failures. The
  repair did not produce a significant aggregate gain.

## Decision

Reject after the initial screen and one bounded repair. Restore production
candidate files and focused tests byte-for-byte to v0038. Rollback focused
tests were 21/21, compileall passed, smoke 4/4, and static retained inherited
failures. No 210-game gate, package, upload, activation, or live baseline
change was performed.

## Next hypothesis

Use the Ragnarok signal without retaining a global pending recovery: inspect
map-local chain route selection and only alter a deterministic local path choice
where it avoids a visible hostile-fire corridor.
