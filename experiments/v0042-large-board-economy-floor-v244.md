# v244 large-board economy floor

Date: 2026-08-19

## Hypothesis

The live v105 rollback and selected large-board losses suggested that the
scalable workforce was opening pressure while the economy was still fragile.
On boards with width plus height at least 48, dynamic Builders and the second
permanent attacker would wait for four completed Harvester chains; compact
boards would retain the three-route floor. The first fixed attacker remained
the early scouting/pressure lane.

## Scope

Changed only the candidate route-floor helper and its dynamic/core consumers,
plus focused nearest-defense coverage. No infiltration, route FSM, fixed-first
attacker lane, Store schema, package, upload, or live operation changed.

## Validation

- Focused tests: **28/28** (`reports/iter-v244-large-board-economy/focused.log`).
- Candidate compileall: pass (`reports/iter-v244-large-board-economy/compileall.log`).
- `make static`: inherited exit 2; 15 obsolete deleted-module imports and two
  navigation fast-path assertions (`reports/iter-v244-large-board-economy/static.log`).
- Smoke: **4/4**, report `reports/local-20260819T021221Z`.
- Rotated 15-map screen: **7-8**, command-clean, zero TLE/suspicious rows;
  candidate collected **72,010 vs 74,240 Ti**, and had one no-delivery row
  versus baseline delivery on all 15. Raw report:
  `reports/local-20260819T021241Z`; parsed replay diagnostics:
  `reports/iter-v244-large-board-economy/replay-analysis.json`.

## Decision

Reject without a repair or long gate. Glacierkeep was **210 vs 1,120 Ti**
with first delivery **226 vs 70**; Archipelago was **7,880 vs 18,800 Ti**.
The extra route gate delayed conversion rather than protecting the economy.
Temporary edits were removed and candidate source parity with immutable v0042
is zero-line (`reports/iter-v244-large-board-economy/rollback-source.diff`).
Rollback focused tests were **27/27**, compileall passed, static retained the
inherited failures, and rollback smoke was **4/4** at
`reports/local-20260819T021545Z`.
