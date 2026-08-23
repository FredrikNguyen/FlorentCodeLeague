# v290 Teamwide Core Intel Relay — rejected

Date: 2026-08-19

## Objective

Test whether allowing any Builder that directly sees the enemy Core to relay
its packed position through the existing delayed Store slot would let the
fixed attacker confirm its Sentinel target sooner, without changing routes,
workforce, tasks, or spending.

## Scope

Only `bots/candidate/main.py`, `bots/candidate/bot/attacker.py`, focused relay
tests, this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, and durable report
metadata were in scope.  Launcher construction, route/workforce tuning,
Sentinel/Barrier/Gunner policy, Store schema, baseline/archive files, and live
operations were explicit non-goals.

## Validation and decision

- Focused tests: 37/37 pass; `reports/iter-v290-core-intel-relay/focused-final.log`.
- Compileall: pass; `reports/iter-v290-core-intel-relay/compileall-final.log`.
- Static: inherited exit 2 (15 obsolete-module import errors and two old
  navigation fast-path assertions); `reports/iter-v290-core-intel-relay/static.log`.
- Smoke: 4/4 command-clean; `reports/local-20260819T163827Z` and
  `reports/iter-v290-core-intel-relay/smoke.log`.
- Screen: 15/15 command-clean, no TLE or suspicious rows, but candidate-A
  won 7-8, collected 47,370/60,630 Ti, had 1/0 no-delivery rows, and max
  p99/peak 1,310/5,563 us; `reports/local-20260819T163848Z` and
  `reports/iter-v290-core-intel-relay/screen-analysis.json`.

The screen did not meet the required repeatable-edge and delivery criteria.
The relay was removed without repair.  Rollback focused tests were 34/34,
rollback compileall passed, rollback smoke was 4/4, static retained the
inherited exit 2, and `rollback-source-parity.diff` is zero.  v0044 remains
the comparator; no promotion, package, upload, activation, or live transition
was performed.  v105 remains the user-requested operational rollback target.
