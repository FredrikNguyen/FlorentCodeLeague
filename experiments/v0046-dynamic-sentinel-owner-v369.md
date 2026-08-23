# v369 Dynamic Sentinel ownership — rejected

Date: 2026-08-20

## Objective and scope

Starting from immutable v0046, v369 tested a structural resource-to-pressure
change motivated by the v367/v368 and top-team replay audit: dynamic Builders
would no longer buy forward Sentinels.  The two fixed attacker roles already
own the confirmed enemy-Core lane and shared Sentinel pool; dynamic workers
instead remained available for route conversion, belt repair, hijacking, raids,
and Builder-fire harassment.  The goal was to prevent repeated local Sentinel
rebuild decisions from consuming route capital when losses showed 20+ placed
Sentinels beside weak income.

Production scope was `bots/candidate/bot/dynamic.py`; focused coverage was the
temporary dynamic-advance test in `tests/test_candidate_nearest_defense.py`.
No baseline/version snapshot, Store schema, route FSM, map literal, live state,
or platform files were changed.

## Validation and decision

- Focused coverage passed **36/36**; candidate compileall passed.
- The paired all-map screen used 15 maps, 30 games, side swaps, and
  `screen_seed=413`: **15-15**, with zero command failures.  Every game had
  a replay; no TLE/suspicious-output or delivery failure was observed.
- Replay diagnostics are in `reports/local-20260820T195648Z/analysis.json`.
  The ownership rule did not remove all Sentinel overbuild: fixed attackers
  could still replace short-lived structures (for example, 21 Sentinels in a
  losing candidate-side game), and the aggregate result was neutral.
- Rollback focused coverage passed **35/35**, compileall passed, smoke was
  **4/4** command-clean at `reports/local-20260820T200226Z`, and recursive
  source parity with v0046 is empty at
  `reports/local-20260820T195648Z/rollback-source-parity.diff`.
- `make static` retained the inherited 15 obsolete-module import errors and
  two navigation fast-path assertions; no v369-specific static defect was
  introduced.

Reject v369, restore exact v0046 candidate parity, and keep v0046 as the only
comparator.  No release matrix, package, upload, activation, or live baseline
transition was justified.

Reports: `reports/local-20260820T195648Z/`,
`reports/local-20260820T200226Z`, and this experiment record.
