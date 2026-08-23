# v238 — deterministic action tie-breakers (rejected)

## Objective and scope

The baseline self-control screen was 5–10 on the same 15-map schedule, which
made recent small candidate edges untrustworthy. This bounded experiment
replaced only the three process-global random calls in the candidate: spawn
ring ordering, the attacker's far exploration fallback, and the exact-center
home-Gunner facing. A local hash retained round/unit variation without shared
random state. Production scope was `bot/util.py`, `bot/core_role.py`,
`bot/attacker.py`, and `bot/defender.py`, plus one focused helper test.

## Validation

- Focused helper/role tests: **30/30**.
- `python -m compileall -q bots/candidate bots/baseline`: **pass**.
- `make static`: inherited **exit 2** (15 missing legacy-module imports and two
  navigation fast-path assertions; no v238-specific failure).
- `make smoke`: **4/4**, zero command failures
  (`reports/iter-v238-deterministic-action-tiebreakers/smoke.log`).
- Rotated 15-map screen against exact v0042: **4–11** candidate-A, command
  clean, candidate Ti **41,110** vs baseline **79,350**, no TLE or suspicious
  rows; first delivery mean **32.13** vs **28.07**
  (`reports/local-20260819T003515Z`, replay analysis at
  `reports/iter-v238-deterministic-action-tiebreakers/replay-analysis.json`).

## Decision

Reject. Deterministic spawn ordering caused a large systematic loss, matching
the earlier v193 result; the exploration/facing changes did not recover it.
The source was restored recursively byte-identical to immutable v0042, with
rollback focused coverage **27/27**, compileall passing, and no release gate,
promotion, package, upload, activation, or live-state transition. The edited
and rollback source comparisons are retained at
`reports/iter-v238-deterministic-action-tiebreakers/edited-source.diff` and
`rollback-source.diff`.

## Follow-up

Do not retry global determinism or rare infiltrator overlap. Select the next
hypothesis from a repeated, high-frequency loss signature—prefer route
last-mile/resource conversion or a map-context decision—and require a paired
edge beyond the self-control variance before any long gate.
