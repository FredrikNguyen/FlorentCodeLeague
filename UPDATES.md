# Florent Code League development and live updates

This file is the durable handoff between Codex sessions. It is append-only except for the **Current state** table, which automation may refresh.

## Current state

| Field | Value |
|---|---|
| Workflow phase | `idle` |
| Working candidate | `bots/candidate` |
| Current active platform version | unknown |
| Last known-good platform version | unknown |
| Previous active platform version | unknown |
| Last known-good live score | unknown |
| Current candidate live score | unknown |
| Last deployment | never |
| Last observation | never |
| Last decision | none |

Machine-readable state: [`state/live_state.json`](state/live_state.json).

## Score definition

The primary live score is the mean fractional score over rated five-game series during a version's observation window:

```text
series score = our game wins / 5
live score   = mean(series score)
```

Also record rating delta and opponent-adjusted residual when available. Reliability failures override score and trigger immediate rollback.

## Append-only update log

<!-- Automation appends newest entries immediately below this comment. -->

### NEXT Iterations Plan Iteration 1 validation — 2026-08-05T21:11:47Z

- Objective: validate adjacent legal stances, active per-unit path reuse, bounded deterministic replanning, navigation/layout epoch separation, and non-consuming destroy semantics. No source edits were made; the existing CURRENT_PLAN implementation remains a separate v0004 checkpoint.
- Allowed surface reviewed: bots/candidate/bot/navigation.py, world.py, builder.py, actions.py, and focused navigation/action tests. Non-goals remained Store layout, economy thresholds, role assignment, combat priorities, and Core budget policy.
- Tests: focused Iteration 1 suite 34/34; make static 97/97 plus compileall; make smoke 4/4 command-clean; required regression subset 24/24 command-clean with no stderr.
- Reports: reports/iteration1-validation-20260805T2120/summary.md, focused.log, static.log, smoke.log, regression-summary.txt, complete v0003-to-candidate.diff, and v0004-to-candidate.diff; local regression report reports/local-20260805T210935Z and smoke report reports/local-20260805T210923Z.
- Metrics: active-path tests cover one BFS/replan followed by cache hits, epoch/goal invalidation, blocked-step retry, adjacent-target exclusion, CPU cutoff, and oscillation fallback; no exception, TLE, or command-failure indicators.
- Self-review: source comparison against v0004 is identical apart from generated __pycache__ bytecode; no defects were found and no repair was needed. Full 21-map matrix remains deferred to the release gate.
- Iteration status: PASSED; Iteration 2 is now the next implementation checkpoint.


### NEXT Iterations Plan Iteration 0 reconciliation — 2026-08-05T21:08:46Z

- Files changed: .codex/config.toml; .codex/agents/sol-planner.toml; .codex/agents/luna-implementer.toml; .codex/agents/sol-reviewer.toml; AGENTS.md; scripts/codex_task.py; Makefile; generated artifacts/chatgpt planning packets; report/state metadata. No candidate behavior changes were made in this iteration.
- Source/archive evidence: v0003 archive SHA-256 fd757d1c6ff72c8e5e45bad37b6201700c599f9aa83caeeadf7d22b21adb6608; immutable v0003 snapshot retained; intentional current-plan delta is separately packaged as v0004_navigation-iteration1 SHA-256 59e579333548bd8e41dfe1f13f78900138a09192476ca20cc67d057e85051c56.
- Tests: harness/startup focused tests 16/16; make static 97/97 plus compileall; make smoke 4/4; Iteration 0 regression 20/20 command-clean; make handoff passed.
- Reports and packets: reports/reconcile-iteration0-20260805T/summary.md, source-hashes.txt, static.log, smoke.log, regression artifacts under reports/local-20260805T210359Z, and artifacts/chatgpt/PLANNING_PACKET.md plus RELEASE_REVIEW_PACKET.md.
- Metrics: zero command failures, exceptions, or TLE indicators in smoke/regression; packet source matches the candidate; v0003 remains recoverable; no additional strategy/economy/navigation changes mixed into this checkpoint.
- Remaining risks: Iteration 1 in the external plan duplicates the already-completed current-plan navigation checkpoint, so it must be validated as a separate no-op checkpoint before Iteration 2; no full 21-map matrix was run.
- Iteration status: PASSED; proceed only to the separate Iteration 1 validation checkpoint.


### Current-plan navigation checkpoint — 2026-08-05T21:00:41Z

- Status: behavior checkpoint passed; next-plan iterations are paused because make static exits 2 on pre-existing harness/startup failures outside the approved scope.
- Files changed: bots/candidate/bot/navigation.py, world.py, builder.py, actions.py, tests/test_candidate_navigation.py, tests/test_candidate_actions.py, tests/test_candidate_builder_navigation.py.
- Focused tests: 34/34 passed; compileall passed. Full logs: reports/navigation-20260805T2110/focused.log and compileall.log.
- make static: exit 2; candidate/static-contract checks passed, with 4 harness failures and 3 missing-agent errors. Full log: reports/navigation-20260805T2110/make-static.log.
- make smoke: 4/4 games, zero command failures; report: reports/local-20260805T205901Z.
- Regression subset: 24/24 games, zero command failures/stderr; report: reports/local-20260805T205908Z.
- Metrics: active path one BFS and two cache hits over a three-step route; goal/epoch/blocked-step invalidations replan once; candidate production count is 1,800 lines.
- Behavior unchanged deliberately: Store/economy/budget/roles/defense/offense/opening policy. Remaining risk: static harness state must be repaired before NEXT_ITERATIONS_PLAN Iteration 0 can start.
- Report: reports/navigation-20260805T2110/summary.md


### Live battle observation — 2026-08-05T19:31:39Z

- Platform reports submission `v0003-entrypoint-class-2de8371f` as numeric version `1`, `ready`, and active for Kleos.
- Eight rated ladder series are complete: one win and seven losses. The newest series beat Git Glam 3–2 (+4.041 Elo), raising the rating to `1402.3331784619274` and placing Kleos at rank `39/102`.
- The newest series reached the 1000-turn titanium-collection limit on all five maps: wins on `crossfire`, `sweden`, and `skerry`; losses on `twins` and `runestone`. No match error or resignation was reported.
- Previous Powerpuff Girls 0–5 ended by `core_destroyed` on all five maps after 266–317 turns; no platform/runtime error was reported.
- Replay-level comparison: the Git Glam series first produced HP events at turns 325–766 and no core destruction; the Powerpuff series first produced HP events at turns 12–87 and destroyed the Kleos core in every game. The current weakness is collection/economy on `twins` and `runestone`, not a submission/runtime failure.
- Battle descriptions from the decoded replay streams:
  - Git Glam `crossfire`: Kleos stayed at 4 builders, 2 harvesters, and 4 conveyors while Git Glam expanded to 13 builders, 4 harvesters, 13 conveyors, and a full turret mix; no core damage, Kleos won the 1000-turn collection finish.
  - Git Glam `sweden`: first HP event at turn 458; Kleos reached 5 builders, 2 harvesters, and 13 conveyors, with sustained turret/resource activity and no core damage; Kleos won by collection.
  - Git Glam `twins`: first HP event at turn 454; Kleos stayed at 4 builders, 1 harvester, and 4 conveyors while Git Glam grew to 27 builders, 5 harvesters, 20 conveyors, and heavy defense; Git Glam won collection without destroying the core.
  - Git Glam `runestone`: first HP event at turn 622; Kleos recorded 85 conveyor placements and 70 later removals, indicating route churn or repair activity; Git Glam’s larger 28-builder/42-conveyor footprint won collection.
  - Git Glam `skerry`: first HP event at turn 766; Kleos finished with 4 builders, 3 harvesters, and 6 conveyors, survived without core damage, and won collection.
  - Powerpuff `duel`, `sweden`, `longship`, `hive`, and `quarry`: first HP events came at turns 12, 87, 29, 37, and 48 respectively; Powerpuff scaled substantial gunner/harvester/conveyor forces and destroyed the Kleos core at turns 273, 285, 271, 266, and 317.
- Full notes and per-map descriptions: `reports/live-battles-20260805T193139Z.md`; raw capture: `reports/live-latest-battles-20260805T193139Z/`; newest replays: `replays/live-c17b2501-20260805/`.

### Codex cap-replan fix — 2026-08-05T17:37:04Z

- Fixed blocked-route replanning for a Builder that already owns one of the three shared project reservations: admission now counts only other projects while preserving the owner's reservation, so it cannot deadlock at the cap or create a fourth project.
- Added Player.run coverage for reserved replanning at the shared cap and strengthened the unreserved fourth-project rejection test.
- Validation: independent Sol review `APPROVED`; focused unit suite 33/33; smoke 4/4; regression 54/54; full matrix 210/210 command-clean, 205/210 wins versus 165/210 prior, with bridge and string 10/10 and no non-target map regression; benchmark p99 6.246564 ms, max 6.830654 ms.
- Remote gate was attempted but DNS was unavailable; no platform upload or activation was performed. Luna harness compatibility remains unavailable (`native_luna_compatible: False`).
- Submission archive: `artifacts/submissions/v0002_cap-replan_20260805-1736_2de8371f.zip` (SHA-256 `5f3118ba1d25c98fc890f76b895ab6c68adc5a51b4a4feeffa9ea52c81edd9c2`).

### Codex implementation task — 2026-08-05T11:23:01Z

- Task: Implement only the final Sol review blocker in reports/codex-20260805T084146Z/review-2.md: derive a team-wide active-project count from authoritative live shared state using a delayed-Store-safe Core/Builder protocol; apply that count before route admission and every new_project discretionary spend; add a real Player.run test with three independently owned active projects, without directly assigning BuilderStateData.active_projects, proving a fourth route and Splitter/Barrier/Launcher/turret projects are rejected. Preserve baseline, configs, maps, README, unrelated files, and the existing successful remediation. Use the required Sol planner -> Luna implementer -> Sol reviewer workflow, run the exact focused retest plus make static, make smoke, make eval-regression, make eval-local, and the benchmark. Do not perform platform operations. Produce truthful process-fallback evidence with exact agent IDs/models/exit codes.
- Backend: process-fallback
- Luna evidence recorded: False
- Outcome: planner failed
- Report: reports/codex-20260805T112300Z


### Codex implementation task — 2026-08-05T11:22:46Z

- Task: Implement only the final Sol review blocker in reports/codex-20260805T084146Z/review-2.md: derive a team-wide active-project count from authoritative live shared state using a delayed-Store-safe Core/Builder protocol; apply that count before route admission and every new_project discretionary spend; add a real Player.run test with three independently owned active projects, without directly assigning BuilderStateData.active_projects, proving a fourth route and Splitter/Barrier/Launcher/turret projects are rejected. Preserve baseline, configs, maps, README, unrelated files, and the existing successful remediation. Use the required Sol planner -> Luna implementer -> Sol reviewer workflow, run the exact focused retest plus make static, make smoke, make eval-regression, make eval-local, and the benchmark. Do not perform platform operations. Produce truthful native-v1 evidence with exact agent IDs/models/exit codes and stop after the allowed review limit.
- Backend: native-v1
- Luna evidence recorded: False
- Outcome: native V1 did not provide complete Luna/approval evidence
- Report: reports/codex-20260805T112246Z


### Codex implementation task — 2026-08-05T11:13:58Z

- Task: Resume the existing integrated candidate remediation. Read reports/codex-20260805T010045Z/review-1.md and implement only its four concrete findings: (1) verify the single-map bounded route planner and blocked-step CPU path, (2) make delivery/repair/claim-heartbeat/reassignment transitions executable through real Builder/Core handlers, (3) wire payback/reserve, Splitter/Barrier/Launcher, threat/opening, and late-game policies into live handlers with legality and fresh-target guards, and (4) produce truthful native Sol-Luna-Sol evidence. The current tree already contains a Luna remediation attempt; do not broaden scope or revert it. Preserve baseline, versions, README, state/UPDATES/startup, configs, maps, and unrelated files. Run the exact reviewer retests, make static, make smoke, make eval-regression, make eval-local, and the expanded benchmark; use existing full-matrix reports only if hashes match, otherwise rerun. No platform operations. The final report must use backend native-v1, name exact agent IDs/models/exit codes, and have an independent sol_reviewer verdict.
- Backend: native-v1
- Luna evidence recorded: False
- Outcome: APPROVED
- Report: reports/codex-20260805T084146Z


### Verification-only Sol-Luna-Sol harness probe approved — 2026-08-05T00:54:23Z

- sol_planner produced a bounded read-only packet; luna_implementer reported `# Florent Code League bot workspace`; sol_reviewer returned `APPROVED`.
- Native multi-agent evidence records `gpt-5.6-sol` for planning/review and `gpt-5.6-luna` for implementation inspection.
- Before/after status, diff, protected hashes, and full repository fingerprints matched; no source, configuration, live-state, or platform changes occurred.
- Evidence: `reports/codex-20260805T004253Z`.


### Session startup and scoped document routing added — 2026-08-05T00:25:00Z

- Added generated `docs/START_HERE.md` plus machine-readable `state/project_state.json` for cross-session development focus.
- Root `AGENTS.md` now requires a startup bootstrap but routes agents to detailed documents conditionally instead of loading everything every time.
- Added nested instructions for `bots/candidate/`, `scripts/`, and `tests/`.
- Updated Sol planner, Luna implementer, and Sol reviewer instructions to read startup state and nearest nested guidance.
- Added project-state/update scripts, automatic startup-summary refresh, Make targets, and regression tests.
- Resolved the orchestration-skill conflict: Luna implementation tasks cannot deploy, while the approved primary Sol/operator live workflow remains authorized by policy.


### Codex harness and live operator audited — 2026-08-05

- Found that the original custom-agent TOML did not prove Luna execution under the current Sol/Terra V2 versus Luna V1 mismatch.
- Added a reversible native-V1 route and an explicit process-isolated Sol → Luna Max → Sol fallback with exact command evidence.
- Added autonomous resumable upload, activation, live scoring, promotion, and rollback using `state/live_state.json`.
- Separated V1 and V2 configuration modes to avoid a boolean/table key conflict.
- Kept Sol as the only live reviewer/operator; Luna implements code but cannot modify live state or perform platform writes.


### Repository initialized — 2026-08-05

- Created the rules reference, Codex harness, starter bot, local/remote evaluation scripts, and submission workflow.
- Initial live state is unknown because no authenticated `fcode` session was available when the repository was generated.
