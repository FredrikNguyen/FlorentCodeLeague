# v302 — four-route fixed-attacker economy gate

Date: 2026-08-19

## Objective and hypothesis

Fresh v107 losses showed the fixed attacker leaving the opening route loop
while the team still had only one-to-three paying Harvesters.  v302 routed
both fixed attackers through the existing Defender economy/chain loop until
four completed routes, then restored the unchanged attacker dispatch.  An
attacker already in `MODE_CHAIN` was specified to finish its route before the
phase gate could open.  No Store slot, route planner, combat policy, or live
state was changed.  Immutable comparator: v0044.

## Scope

Temporary changes were limited to `bots/candidate/main.py`,
`bots/candidate/bot/attacker.py`, `bots/candidate/bot/constants.py`, and
focused coverage in `tests/test_candidate_nearest_defense.py`.  The temporary
production and test edits were removed after the first screen.

## Validation

- Focused nearest-defense/seeded-route/economy tests: **35/35**.
- Candidate compileall: **pass**.
- `make static`: inherited exit 2 from 15 obsolete removed-module imports and
  two navigation fast-path assertions; no v302-specific failure.
- `make smoke`: four command-clean games at
  `reports/local-20260819T201111Z`.
- 15-map screen against v0044: **4–11** for candidate-A, all 15 commands
  clean.  Candidate/comparator collection was **57,920/62,450 Ti**; first
  delivery was **15/15 vs 14/15**.  Replay analysis found zero TLE and zero
  suspicious output, max p99/peak callback time **1,391/2,469 us**.
- Canonical screen evidence: `reports/local-20260819T201143Z`,
  `reports/iter-v302-four-route/replay-analysis.json`, and
  `reports/iter-v302-four-route/metrics.txt`.

## Decision and rollback

The first screen was decisively negative, so the plan's no-repair rule
applied.  No 60-game gate, package, upload, activation, or live operation was
performed.  The temporary edits and focused test were removed; recursive
production-source parity with immutable v0044 is zero at
`reports/iter-v302-four-route/rollback-source-parity.diff`.  Rollback focused
coverage is **34/34**, compileall passes, and rollback smoke is four
command-clean games at `reports/local-20260819T201446Z`.

Live v107 remains `active_observing`; v105 remains the operational rollback
target.  The next experiment must use a distinct mechanic/phase hypothesis,
not retry the four-route fixed-attacker gate unchanged.
