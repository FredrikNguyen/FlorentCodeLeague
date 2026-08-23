# v306 — coordinated phase/role-lease architecture rewrite

## Objective

Replace the v0044 candidate's independent lifelong-role dispatch with a
deterministic map-context phase/lease boundary and add the missing Launcher
lifecycle.  The rewrite is motivated by fresh v107 losses and the 15-game
top-team opening audit in
`reports/iter-v306-architecture-audit/top-team-opening-analysis.json`:
control-first winners use early Launchers/Barriers while economy-first winners
run parallel route owners and deliver quickly.  v305's crisis handoff was
rejected, so this iteration changes coordination rather than another threshold.

## Allowed scope

- `bots/candidate/main.py`: phase/lease dispatch and `EntityType.LAUNCHER`
  handler dispatch;
- `bots/candidate/bot/strategy.py`: pure opening-profile and lease policy;
- `bots/candidate/bot/constants.py`: named lease/profile identifiers and
  documented Launcher radius;
- `bots/candidate/bot/attacker.py`: bounded Launcher construction and legal
  strict-progress Launcher actions;
- `tests/test_candidate_architecture_rewrite.py` and durable docs/reports.

The immutable v0044 comparator, `bots/baseline/`, live state, package, upload,
and activation are not modified.

## Non-goals

No Store-slot/schema change, Core spawn/ammo change, route geometry/FSM change,
Harvester selector rewrite, dynamic task-priority rewrite, turret-cap change,
or map-specific branch.  The Launcher must not throw a friendly route owner
before the first route, and every pickup/destination must pass `can_launch` and
strict progress checks.

## Validation record

Results are recorded below after the focused suite, compileall, static, smoke,
and the 15-map screen.  The inherited static failures remain separately
identified and are not attributed to v306.

## Decision

Rejected after the initial screen and one bounded route-protection repair.
The initial implementation passed **42/42** focused tests, compileall, smoke
**4/4**, and a command-clean 15-map screen, but lost **3–12** to immutable
v0044 (`reports/local-20260819T212347Z`).  Replay evidence showed the new
control/lease interaction produced a large pressure deficit and no reliable
Launcher lifecycle.

The bounded repair required three completed routes before dynamic assault
leases and one completed route before a control Launcher.  It passed **44/44**
focused tests, compileall, smoke **4/4** at
`reports/local-20260819T213041Z`, and a command-clean 15-map screen, but only
reached **6–9** with **67,830 vs 85,270 Ti** and two candidate no-delivery maps
(GlacierKeep and Royale); replay analysis is at
`reports/iter-v306-architecture-audit-repair/replay-analysis.json` and the
screen is `reports/local-20260819T213109Z`.  The accepted v0044/v305 rollback
reference was **7–8**, so there is no positive edge or release justification.

The temporary dispatcher, Launcher lifecycle, identifiers, and focused test
were removed.  Recursive production parity with immutable v0044 is zero at
`reports/iter-v306-architecture-audit-repair/rollback-source-parity.diff`.
Rollback focused coverage was **34/34**, compileall passed, static retained
the inherited 15 obsolete imports and two navigation assertions, and rollback
smoke was **4/4** at `reports/local-20260819T213523Z`.  No long gate, package,
upload, activation, or live transition occurred.  v105 remains the
operational rollback target and live v107 remains `active_observing`.
