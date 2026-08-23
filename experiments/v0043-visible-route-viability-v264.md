# v264 visible-route viability guard — rejected

Date: 2026-08-19

## Hypothesis

On wall/chokepoint maps, an opening Harvester can be committed to a fully
visible disconnected component.  A conservative BFS before the first three
routes should reject only a proven dead source, while leaving unknown terrain
permissive, improving route conversion without changing mature economy or
combat.

## Scope

Changed only `bots/candidate/bot/defender.py` and focused tests.  The guard ran
before the existing belt-safety check, blacklisted rejected sources for the
existing expiry, and was inactive once three completed routes existed.  No
route FSM, ranking, workforce, combat, infiltration, or purchase policy was
changed.

## Validation

- Focused: 31/31 (`focused.log`); candidate compileall passed.
- `make static`: inherited failure only (15 obsolete module imports and two
  navigation fast-path assertions), `static.log`.
- Smoke: 4/4, `reports/local-20260819T084502Z`.
- Initial exact-v0043 rotated 15-map screen: candidate **6-9**, 85,110 vs
  82,620 titanium, 118 vs 133 Harvesters, all 15 sides delivered, zero TLE or
  suspicious rows; `reports/local-20260819T084526Z` and `replay-analysis.json`.
- Independent 15-map rotation: candidate **7-8**, 66,600 vs 70,900 titanium,
  119 vs 117 Harvesters, all 15 sides delivered, zero TLE or suspicious rows;
  `reports/local-20260819T084820Z` and `repeat-replay-analysis.json`.

The mechanism removed the observed no-delivery shape and was process-clean,
but its collection edge did not repeat and aggregate wins remained below the
baseline.  No protected-map collapse or replay-confirmed defect justified a
repair or longer gate.

## Decision and rollback

Reject v264; do not promote, package, upload, activate, or alter live state.
The temporary guard and tests were removed with `apply_patch`.  Exact recursive
candidate parity with immutable v0043 is recorded in
`reports/iter-v264-visible-route-viability/rollback-source.diff` (empty).
Rollback focused coverage was 26/26, compileall passed, static retained the
same inherited failures, and rollback smoke was 4/4 at
`reports/local-20260819T085326Z`.

## Follow-up

The next experiment must target a causal conversion or pressure failure rather
than another opening-source filter.  Keep the paired 15-map screen as a cheap
first gate; require a repeatable win edge before any longer gate or release.
