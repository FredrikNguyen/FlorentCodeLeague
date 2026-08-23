# v161 — geometry-adaptive first-Sentinel economy gate

## Objective

Test whether the opening pressure transition should depend on map geometry.
Cramped maps have a short Core-to-Core path and benefit from the existing
one-route Sentinel pressure. On non-cramped maps, require two completed
Harvester routes before buying the first forward Sentinel so the opening can
fund a second income path before committing the 30-Ti siege asset. The normal
three-Sentinel pool, five-route expansion, confirmed-Core requirement, and all
attack/route behavior remain unchanged.

## Allowed files

- `bots/candidate/bot/attacker.py`
- `tests/test_candidate_nearest_defense.py`
- this experiment record, `UPDATES.md`, and durable state
- generated `docs/START_HERE.md` only through the state updater

## Non-goals

- no edits to `bots/baseline/` or immutable version snapshots;
- no danger-line veto, Sentinel pool, route geometry, workforce, ammo,
  barrier-cage, home-defense, Launcher, Store, or navigation changes;
- no map-name or coordinate-specific branches; compactness is derived from
  existing Core symmetry geometry;
- no package, upload, activation, or live-state change before a passing
  release gate.

## Done criteria

- Focused tests prove one-route permission on cramped geometry, two-route
  gating on non-cramped geometry, and preservation of the existing pool gates.
- Candidate compileall passes; `make static` records only inherited failures;
  `make smoke` is 4/4 command-clean; scoped `git diff --check` passes.
- The 30-game paired screen covers all 15 maps, is command-clean and below the
  CPU budget, and has a material aggregate win-rate edge over immutable v0040
  without a delivery/reliability collapse.
- If non-material or negative, allow at most two bounded repairs, then restore
  exact v0040 source parity. Do not run the 60-game gate after a non-material
  screen.

## Result

The screen scored **21-9**, but the 60-game release gate reversed to **27-33**
against v0040, with lower collection and a 0-4 Nordkap/Royale floor. v161 is
rejected at the release gate. The candidate was restored to exact v0040 parity;
rollback focused tests were 20/20, compileall passed, and rollback smoke was
4/4. Full metrics are in
`reports/evaluation-v161-geometry-adaptive-sentinel.md`. No package, upload,
activation, or baseline transition occurred.
