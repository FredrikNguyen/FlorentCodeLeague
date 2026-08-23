# v159 — bounded home barrier shell

## Objective

Test whether a small, geometry-derived defensive shell prevents the early
route and builder losses visible in v158 and in the live/top-team replay audit.
After the first completed route proves that the economy exists, one nearest
dynamic worker may build up to four barriers on empty tiles outside the Core's
conveyor ring. The worker returns to normal harvesting/repair/pressure work
after each site.

## Allowed files

- `bots/candidate/bot/constants.py`
- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_nearest_defense.py`
- this experiment record, `UPDATES.md`, and `state/project_state.json`
- generated `docs/START_HERE.md` only through the state updater

## Non-goals

- no edits to `bots/baseline/` or immutable version snapshots;
- no Sentinel, Launcher, Gunner, ammo, route-FSM, hijack, raid, navigation, or
  enemy-core target changes;
- no barrier on the immediate Core conveyor ring, no barrier that severs a
  visible friendly belt, and no hard-coded map coordinates;
- no package, upload, activation, or live-state change before a passing local
  gate.

## Done criteria

- Focused tests prove the route/resource gate, nearest-worker ownership,
  four-site cap, and legal adjacent build path; existing nearest-defense and
  route tests remain green.
- Candidate compileall passes; `make static` records only the inherited
  repository failures; `make smoke` is 4/4 command-clean; `git diff --check`
  passes for the scoped files.
- The 30-game all-map paired screen against immutable v0040 is command-clean,
  below the local CPU budget, and has a material aggregate win-rate edge or a
  clear delivery/reliability improvement without a delivery collapse.
- If the screen does not meet that bar, allow at most two bounded repairs,
  then restore exact v0040 source parity and validate the rollback. Do not run
  the 60-game gate after a non-material screen.

## Result

Rejected after the initial **13-17** screen, repair 1 (**15-15**), and repair 2
(**9-21**). The implementation and its focused fixture were removed; recursive
candidate/source parity with v0040 is exact. Focused rollback tests were 20/20,
compileall passed, and rollback smoke was 4/4. Full metrics and report paths are
in `reports/evaluation-v159-home-barrier.md`. No release gate, package, upload,
activation, or baseline transition occurred.
