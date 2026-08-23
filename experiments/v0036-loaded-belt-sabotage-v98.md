# v0036 loaded-belt sabotage (v98 parent)

## Objective

Improve conversion of an attacker reaching visible enemy economy.  A loaded
conveyor or splitter is titanium already in flight; destroying it should deny
that delivery immediately instead of walking past it to chip a harvester.

## Scope

- Parent comparator: immutable platform v98 snapshot
  `bots/versions/v0027_early-two-sentinel-shell_20260813-1831_eeafad8f`.
- Candidate change: `bots/candidate/bot/attacker.py`,
  `_find_enemy_economy_target` only.
- Harvester, builder, route, defense, and package interfaces are unchanged.

The target score is now 300/250/200 for harvester/splitter/conveyor, with a
200-point bonus when a conveyor or splitter visibly stores titanium.  This
keeps a harvester as the best empty persistent target while preferring a
loaded logistics tile.

## Evidence

- Prefilter: `reports/local-20260814T030907Z` — 36–18 (66.7%), 0 command
  failures across 54 games.
- Release matrix: `reports/local-20260814T031536Z` — 116–94 (55.24%), 0 ties,
  0 command failures across 210 games; map minimum 3–7.
- Replay diagnostics:
  `reports/iter-v99-loaded-sabotage-replay-analysis.json`.
  Candidate wins averaged 7.16 placed harvesters and 8.45 sentinels;
  candidate losses averaged 5.68 harvesters and 4.22 sentinels.
- Static syntax: `python -m py_compile bots/candidate/main.py bots/candidate/bot/*.py`
  passed.  `make static` remains blocked by 15 inherited obsolete test-import
  errors; see `reports/iter-v99-loaded-sabotage-static.log`.
- Smoke: `make smoke` passed 4/4 in
  `reports/local-20260814T031517Z`.

## Decision and risks

This is a release candidate because it is above the 55% full-matrix win-rate
gate with clean reliability.  Keep v98 as the fixed local comparator and v72
as the live rollback target.  The 3–7 floors on bridge, sprint, and vault and
the persistent side asymmetry remain risks; the next experiment must address
route-first economy without undoing the loaded-line raid priority.
