# v160 — turret-line-safe forward Sentinel placement

## Objective

Test whether refusing to plant a forward Sentinel on a tile currently covered
by a visible enemy Gunner or Sentinel line prevents the short-lived Sentinel
replacement loop seen in v159 weak-map losses. The existing economy milestone,
pool limits, confirmed-Core requirement, site blacklist, and offensive cage
remain unchanged. If no safe legal site exists, the attacker keeps its normal
movement/raid fallback instead of buying a predictable casualty.

## Allowed files

- `bots/candidate/bot/attacker.py`
- `bots/candidate/bot/dynamic.py`
- `bots/candidate/main.py`
- `tests/test_candidate_nearest_defense.py`
- this experiment record, `UPDATES.md`, and durable state
- generated `docs/START_HERE.md` only through the state updater

## Non-goals

- no edits to `bots/baseline/` or immutable version snapshots;
- no Sentinel pool, route, harvester, workforce, ammo, barrier-cage,
  home-defense, Launcher, Store, or navigation threshold changes;
- no map-name or coordinate-specific branches;
- no package, upload, activation, or live-state change before a passing
  release gate.

## Done criteria

- Focused tests prove a legal safe site remains buildable, a site in the
  observed danger set is skipped, and callers pass the same danger set without
  changing the existing pool/economy gates.
- Candidate compileall passes; `make static` records only the inherited
  repository failures; `make smoke` is 4/4 command-clean; scoped
  `git diff --check` passes.
- The 30-game paired screen is command-clean, covers all 15 maps, stays below
  the local CPU budget, and has a material aggregate win-rate edge over
  immutable v0040 without a delivery/reliability collapse.
- If the screen is non-material or negative, allow at most two bounded repairs,
  then restore exact v0040 source parity. Do not run the 60-game gate after a
  non-material screen.

## Result

Rejected after the initial **10-20** screen and one bounded repair (**11-19**).
The repair improved collection but not paired wins, so the Sentinel danger veto
was removed and candidate Python was restored to exact v0040 parity. Rollback
focused tests were 20/20, compileall passed, smoke was 4/4, and static retained
only inherited failures. Full metrics are in
`reports/evaluation-v160-turret-line-safe-sentinel.md`.
