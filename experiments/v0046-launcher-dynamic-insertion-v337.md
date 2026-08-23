# v337 Launcher dynamic insertion

## Objective

Test one structural pressure conversion on immutable v0046: after the fixed
Launcher attacker has been dispatched, let that existing relay insert one
forward-moving non-floor Builder only after the economy has three completed
chains and a real titanium reserve.  Opening production, route geometry,
Store schema, fixed attacker roles, and platform state were out of scope.

## Allowed files and done criteria

The production change was limited to `bots/candidate/main.py`, with focused
Launcher coverage in `tests/test_candidate_v319_launcher.py`; this experiment
record, `UPDATES.md`, `state/project_state.json`, and `docs/CURRENT_PLAN.md`
were the durable files.  The candidate had to compile, pass focused tests,
remain command-clean in smoke and the 15-map screen, and show a repeatable
paired edge without protected-map collapse before any promotion.

## Evidence and bounded repairs

- Initial implementation added a reserve- and three-chain-gated fallback.
  Focused coverage passed **12/12**, compileall passed, `make static` retained
  the inherited 15 obsolete-import errors and two navigation assertions, and
  smoke was **4/4** (`reports/iter-v337-launcher-insert-smoke.log`).  The
  screen was command-clean but **6-9 candidate-A** across all 15 maps
  (`reports/local-20260820T055522Z`); replay analysis reported zero TLE or
  suspicious rows and exposed late-economy deficits on several losses
  (`reports/iter-v337-launcher-insert-replay-analysis.json`).
- Repair 1 excluded the Core-designated permanent defender from dynamic
  Launcher pickup, preserving the economy floor.  Focused coverage passed
  **13/13**, compileall passed, smoke was **20/20** command-clean, and the
  fresh screen was **5-10** (`reports/local-20260820T060351Z`).
- Repair 2 additionally required five completed chains and a recorded forward
  Sentinel before insertion, making the relay phase-proven rather than merely
  reserve-gated.  Focused coverage passed **13/13**, compileall passed, smoke
  was **20/20** command-clean, and the screen was **6-9**
  (`reports/local-20260820T060808Z`).  Replay analysis again found zero TLE or
  suspicious rows; max p99 was **1,298 us**
  (`reports/iter-v337-launcher-insert-repair2-replay-analysis.json`).

The same-baseline control screen was **7-8**, so the one-game swings are noisy
and neither repair established a positive aggregate edge.  No 60-game gate
was justified.

## Decision and rollback

Reject v337 after its two bounded repairs.  Restore candidate production to
exact recursive parity with immutable v0046 (zero diff excluding generated
`__pycache__`; `reports/iter-v337-launcher-insert-rollback-source-parity.diff`).
Rollback focused/static/compile checks and smoke were clean within the known
repository static baseline: focused contract checks passed, compileall
passed, `make static` retained the inherited failure profile, and rollback
smoke was **20/20** command-clean (`reports/local-20260820T061148Z`).  No
package, upload, activation, baseline promotion, or live-state transition
occurred.

## Remaining risks and next direction

Top-team replay composition still suggests more mobile pressure, but a home
Launcher cannot safely identify a route worker by proximity alone.  The next
experiment should verify a local defect or explicit task signal before taking
any Builder, and must preserve the permanent defender and early route floor.
