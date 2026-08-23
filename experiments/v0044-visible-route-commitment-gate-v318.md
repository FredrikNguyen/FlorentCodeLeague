# v318 visible route-commitment gate — rejected after one repair

Date: 2026-08-20

## Objective and replay basis

The top-team audit and live v107 Yulerune/AuroraVeil losses show a recurring
conversion failure: the candidate can lay many conveyors after committing one
source, while the opponent builds a short paying route and spends the balance
on control.  v318 tested one structural contract before the first Harvester:
when the Core ring and corridor are fully visible, reject a source commitment
if a bounded cardinal walk through passable tiles cannot reach a Core-adjacent
sink within the existing chain slack.  Unknown vision preserves the old
optimistic behavior and the existing CHAIN walker remains unchanged.

## Scope and non-goals

Allowed production scope was `bots/candidate/bot/defender.py`; focused coverage
was a temporary `tests/test_candidate_route_commitment.py`.  Bookkeeping,
reports, `UPDATES.md`, `docs/CURRENT_PLAN.md`, and durable state were also
updated.  No Store schema, route executor, workforce, role/task, combat,
Launcher/Sentinel/Barrier policy, baseline, package, upload, activation, or
live state changed.

## Validation

- Initial focused coverage was **37/37**, compileall passed, static retained
  the inherited 15 obsolete-module imports and two navigation assertions, and
  smoke was 4/4 (`reports/local-20260820T013431Z`).
- The initial 15-map screen was command/delivery-clean at **9-6** candidate
  wins, candidate collection **56,580 vs 48,250 Ti**, all 15 candidate rows
  delivered, zero TLE/suspicious output, and max p99/peak **1,378/2,076 us**.
  Matrix: `reports/local-20260820T013500Z`; replay analysis:
  `reports/iter-v318-route-commitment/screen-analysis.json`.
- The 60-game gate was command-clean but only **32-28** candidate wins,
  collection **313,260 vs 315,860 Ti**, one no-delivery row for each side,
  zero TLE/suspicious output, and max p99/peak **1,478/5,158 us**.
  Matrix: `reports/local-20260820T013718Z`; replay analysis:
  `reports/iter-v318-route-commitment/release60-analysis.json`.  Map floors
  were weak on Yulerune (**0-4**) and Frostgate (**1-3**), so the edge was not
  promotion-grade.
- The one permitted repair limited the probe to the very first route, allowing
  later workforce expansion to use the prior commitment behavior.  Focused
  coverage was **38/38**, compileall passed, static retained the same
  inherited profile, and smoke was 4/4 (`reports/local-20260820T014542Z`).
  The rotated screen regressed to **6-9**, collection **73,820 vs 85,940 Ti**,
  with all 15 rows delivered and zero TLE/suspicious output.  Matrix:
  `reports/local-20260820T014615Z`; replay analysis:
  `reports/iter-v318-route-commitment/screen-repair-analysis.json`.

## Decision and rollback

Reject v318 after the allowed repair.  The visible viability probe was too
conservative on the long-gate map mix and did not produce a repeatable win or
conversion edge.  The temporary probe and focused test were removed; the
candidate Defender is byte-identical to immutable v0044, with parity confirmed
by `cmp` after rollback.  Rollback focused coverage was **34/34**, compileall
passed, static retained the inherited exit-2 profile, and rollback smoke was
4/4 (`reports/local-20260820T014853Z`).  No promotion, package, upload,
activation, or live operation occurred.  Preserve the live v107 observation
and v105 rollback; the next experiment must be a different structural route
or control hypothesis, not a stricter pre-commit filter.
