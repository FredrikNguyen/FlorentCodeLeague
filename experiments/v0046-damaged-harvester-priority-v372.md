# v372 Damaged-Harvester repair priority — rejected

Date: 2026-08-20

## Objective and scope

Starting from immutable v0046, v372 added a focused Dynamic task detector for
damaged friendly Harvesters in the home area.  The detector ran after belt-gap
repair but before opportunistic enemy-Harvester hijack, so a threatened local
income source could be healed before a Builder diverted to infiltration.  The
generic damaged-building repair path and all existing action/vision guards
were unchanged.

Production scope was `bots/candidate/bot/dynamic.py`; focused coverage used
`tests/test_candidate_nearest_defense.py`.  Bookkeeping and evidence are this
record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, `state/project_state.json`, and
the v372 report files.  No route FSM, Store schema, spawning, ammo, turret,
Sentinel, Launcher, Barrier, baseline, package, upload, activation, or live
state changed.

## Validation

- Focused nearest-defense coverage passed **27/27** and candidate compileall
  passed (`reports/iter-v372-damaged-harvester-priority/focused.log`,
  `compileall.log`).
- `make static` retained the inherited exit **2** from 15 obsolete-module
  imports and two navigation assertions; no v372-specific static defect was
  found (`static.log`).
- `make smoke` was **4/4** command-clean at
  `reports/local-20260820T202624Z` (`smoke.log`).
- Rotated screen 1 (seed 443) was **18–12**, 30/30 command-clean and
  delivery/reliability-clean, with **145,690/123,680 Ti** collected;
  `reports/local-20260820T202658Z` and `analysis.json`.
- Rotated screen 2 (seed 449) was **15–15**, 30/30 command-clean and
  delivery/reliability-clean, with **143,940/149,220 Ti** collected;
  `reports/local-20260820T203037Z` and `analysis-2.json`.  The combined
  short-screen result was **33–27**.
- The v0046-pinned 60-game release gate was command-clean with zero TLE or
  suspicious-output rows, but finished **25–35**; collection was
  **279,900/327,020 Ti**, mean first delivery **34.05/26.52** rounds, and
  every side delivered (`reports/local-20260820T203356Z` and
  `release-analysis.json`).

## Decision and rollback

Reject v372: its short-screen edge did not transfer to the release matrix and
the candidate lost 12, over 47,000 collected titanium.  The temporary source
and focused test edits were removed; candidate production is recursively
byte-identical to immutable v0046, with parity proof recorded in the next
rollback report.  No baseline promotion, package, upload, activation, or
live transition occurred.  Continue comparisons against v0046 with a
distinct hypothesis.
