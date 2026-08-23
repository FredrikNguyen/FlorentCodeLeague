# v0024 — bootstrap economy plus deterministic frontier exploration

## Objective

Beat the immutable v0023 workforce-first snapshot on the protected paired
checkpoint, then validate the retained candidate on the full 21-map, five-seed
matrix.

## Hypothesis and scope

The v0023 opening can spend a non-attacker dynamic Builder on core-ring repair
or advance work before any Harvester route has delivered. Assign every
non-attacker spawned during that zero-chain bootstrap to the economy floor, and
replace process-global random exploration with a bounded per-Builder frontier
sequence. Later spawns remain dynamic. The only source files in scope were `bots/candidate/main.py`
and `bots/candidate/bot/defender.py`.

Non-goals: combat/turret/ammo policy, route-chain mechanics, Store schema,
navigation rewrite, baseline/snapshot edits, submission, activation, or live
state changes.

## Iteration and evidence

- A ring-gating-only probe was rejected: 15–21 on the 36-game protected
  subset; report `reports/local-20260812T165240Z`.
- A temporary bootstrap defender released after first delivery was rejected:
  16–20 on the same 36-game subset; report `reports/local-20260812T170820Z`.
- The retained combined candidate (opening bootstrap economy floor plus
  deterministic frontier exploration) won 29–19 on the
  first 48-game protected checkpoint (`reports/local-20260812T171311Z`) and
  31–17 on the independent repeat (`reports/local-20260812T171648Z`). Pooled:
  60–36, 62.5% wins, with no command failures.
- Full gate against exact v0023: 122–88 over 210 games, candidate titanium
  876,380 versus 797,940 (1.0983x), zero command failures, zero TLE markers,
  zero suspicious output, maximum replay p99 1,462 us and peak callback
  2,956 us. Report:
  `reports/local-20260812T172029Z/bootstrap-deterministic-explore-v0023-210-summary.json`.

## Validation and status

Focused tests: 18/18 passed. `compileall` and `git diff --check` passed.
`make smoke` passed 4/4 (`reports/local-20260812T173907Z`). `make static`
remains blocked by the inherited 15 obsolete pre-v86 test imports; the full
log is `reports/bootstrap-deterministic-explore-v0023-static.log`.

Status: **PASSED — new local best over v0023; not submitted or activated**.
Remaining risks are map-specific collection losses on atoll/fjord/quarry and
four missing candidate first-delivery observations on vase plus one on sprint.
