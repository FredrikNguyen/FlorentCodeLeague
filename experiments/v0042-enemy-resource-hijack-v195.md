# v195 — enemy-resource hijack

## Objective

Test a late, reserve-funded Builder transition that adds a legal Conveyor
outlet beside a visible enemy Harvester and routes that outlet to our Core.
The first version targeted only disconnected enemy sources; the bounded repair
allowed an enemy-connected source to receive a parallel accepting outlet, but
never duplicated an outlet we already owned.  No enemy building was destroyed.

## Scope

- `bots/candidate/bot/defender.py`
- `bots/candidate/bot/dynamic.py`
- `tests/test_candidate_hijack.py`
- `configs/eval_regression.toml` (screen seed 162, unchanged during v195)

## Validation

| checkpoint | result | report |
| --- | --- | --- |
| focused unittest (initial) | 27/27 pass | terminal log |
| focused unittest (repair) | 31/31 pass | terminal log |
| compileall | pass | terminal log |
| `make static` | exit 2; known deleted-module imports and two pre-existing navigation assertions | terminal log |
| `make smoke` (initial) | 4/4 command-clean | `reports/local-20260818T112528Z` |
| initial 15-game screen | 6–9, one A no-delivery, 0 TLE, 0 suspicious | `reports/local-20260818T112546Z` |
| `make smoke` (repair) | 4/4 command-clean | `reports/local-20260818T113036Z` |
| repaired 15-game screen | 7–8, zero A no-delivery, 0 TLE, 0 suspicious, max p99 1496 us | `reports/local-20260818T113100Z` |

## Decision

Reject.  The repair removed the no-delivery row and improved the screen by one
win, but v0042 still won the paired screen 8–7.  The candidate is restored
byte-for-byte to `bots/versions/v0042_low-liquidity-gunner_20260818-0737_eeafad8f`.

## Diagnosis and next direction

The legal parallel-outlet mechanic is safe enough to test, but it did not
convert enough games to establish an edge.  A follow-up should target a
connected enemy Conveyor only when its Harvester output and a replacement
route to our Core are both visible, then destroy that enemy Conveyor through a
separate adjacent legal action before seeding.  It must retain the same late
economy/defense/replacement reserves and must be measured as a separate
sabotage-then-takeover hypothesis; do not mix it into this rejected snapshot.
