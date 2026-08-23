# v310 — shared siege-cage pressure lease

## Objective and evidence

Top-team winners convert forward pressure into Barrier topology (mean 13.7
Barriers in the v306 audit), while v0044 dynamic pressure builders proceed to
harass once the Sentinel shell exists.  The existing fixed-Attacker cage
primitive is reserve-backed and legality-gated but is not available to dynamic
pressure workers.

## Allowed files and non-goals

- `bots/candidate/bot/dynamic.py`
- focused additions to `tests/test_candidate_nearest_defense.py`
- this record, `docs/CURRENT_PLAN.md`, `UPDATES.md`, durable state, and reports

No baseline/archive, Store schema, route FSM, spawn target, Launcher behavior,
Sentinel/Gunner/ammo policy, home defense, map policy, package, upload,
activation, or live-state change.  Barrier construction must remain bounded by
the existing reserve/cap/legality primitive.

## Validation plan

Run focused pressure/defense/economy/seeded-route tests, compileall,
`make static`, `make smoke`, then the rotated 15-map screen against immutable
v0044.  Only if the screen is clean and shows a repeatable edge should the
60-game endpoint gate run.  A negative screen permits one cage-only repair,
then exact v0044 source parity is restored.

## Status

Rejected after one bounded cage-only repair; source rolled back to exact
immutable v0044 parity and no release/live operation performed.

## Validation and decision

- Focused pressure/economy/route tests: **36/36** initial and **37/37** after
  the repair; rollback focused subset **34/34**.  Reports are under
  `reports/iter-v310-shared-siege-cage/`.
- Compileall passed; smoke was **4/4** for the initial and repaired candidates,
  with rollback smoke **4/4** at `reports/local-20260819T230601Z`.
- `make static` retained the inherited 15 obsolete removed-module imports and
  two navigation fast-path assertions; no v310-specific static failure.
- Initial screen: **8–7**, 15/15 command-clean, no TLE/suspicious output,
  candidate Barrier mean 4.43 versus comparator 4.40;
  `reports/local-20260819T225438Z` and
  `reports/iter-v310-shared-siege-cage/replay-analysis.json`.
- Endpoint gate: **31–29 (51.7%)**, 60/60 command-clean;
  `reports/local-20260819T225630Z` and
  `reports/iter-v310-shared-siege-cage/long-replay-analysis.json`.
- Repair screen: **5–10**, 15/15 command-clean;
  `reports/local-20260819T230356Z`.
- Decision: reject.  The branch changed topology but not aggregate outcomes,
  and the bounded repair introduced a protected-map regression.  Dynamic cage
  code/tests were removed; recursive production-source parity with immutable
  v0044 is zero.  v105 remains the live rollback and v107 is unchanged.
