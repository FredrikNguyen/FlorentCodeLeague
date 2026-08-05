# Start here

> Generated cross-session handoff. Do not hand-edit dynamic fields. Update
> `state/project_state.json` with `scripts/set_project_state.py` and deployment state
> through the live operator, then run `make refresh-start`.

## Current development focus

| Field | Value |
|---|---|
| Milestone | NEXT Iteration 1: navigation/action criteria validated as separate checkpoint |
| Current hypothesis | Active per-unit paths, legal adjacent stances, and layout-only route epochs reduce replans without changing Store or strategy policy. |
| Current experiment | reports/iteration1-validation-20260805T2120 |
| Next recommended task | Read and inspect NEXT_ITERATIONS_PLAN Iteration 2, then implement only the Store protocol checkpoint if its pre-edit criteria are satisfied. |
| Candidate | `bots/candidate` |
| Frozen baseline | `bots/baseline` |
| Last Codex task | Validate NEXT_ITERATIONS_PLAN Iteration 1 navigation/action criteria already delivered by the CURRENT_PLAN checkpoint; no duplicate source edits. |
| Last Codex outcome | PASSED: focused 34/34, make static 97/97 plus compileall, smoke 4/4, and required regression 24/24 command-clean. |
| Last Codex report | reports/iteration1-validation-20260805T2120 |
| Last local report | reports/local-20260805T210935Z |

## Live deployment snapshot

| Field | Value |
|---|---|
| Phase | `idle` |
| Active platform version | unknown |
| Pending version | unknown |
| Previous active version | unknown |
| Last known-good version | unknown |
| Last known-good live score | unknown |
| Current candidate live score | unknown |
| Last observation | unknown |
| Last decision | unknown |

## Working tree snapshot

| Field | Value |
|---|---|
| Branch | `main` |
| Commit | `2de8371f` |
| Status | working tree has changes |

Always run `git status --short` yourself; this generated snapshot may be older than the working tree.

## Startup checklist

Before doing any work:

1. Read this file.
2. Read the current-state table and newest relevant entries in `UPDATES.md`.
3. Read `state/project_state.json` and `state/live_state.json`.
4. Run `git status --short` and inspect relevant diffs.
5. Read the nearest applicable `AGENTS.md` for files you will touch.
6. Load only the task-specific detailed documents below.

## Task-specific document routing

| Task | Required detailed reading |
|---|---|
| Bot mechanics or strategy | `bots/candidate/AGENTS.md`, `GAME_RULES.md`, relevant `docs/IMPLEMENTATION_PLAN.md` milestone |
| Non-trivial implementation | `docs/CODEX_HARNESS.md`, experiment record, relevant nested `AGENTS.md` |
| Evaluation or promotion | `docs/EVALUATION_PLAN.md`, experiment record, baseline/live comparison |
| Packaging or live operations | `scripts/AGENTS.md`, `docs/SUBMISSION_AND_VERSIONING.md`, `docs/LIVE_AUTOPILOT.md`, fresh `state/live_state.json` |
| Repository/tooling architecture | `docs/REPOSITORY_STRUCTURE.md`, `docs/PROJECT_CONSIDERATIONS.md` |

## Durable handoff rules

- `state/project_state.json`: authoritative current development focus.
- `state/live_state.json`: authoritative deployment and rollback state.
- `UPDATES.md`: human-readable append-only history.
- `docs/START_HERE.md`: generated concise view of those sources.
- Approved implementation tasks must record their report/outcome and regenerate this file.
- Platform actions may continue across sessions; never infer their state from chat history.

## Useful commands

```bash
make refresh-start
make codex TASK="<bounded task>"
make static
make smoke
make live-status
make live-autopilot
```

Generated at `2026-08-05T21:11:47Z` from project state updated `2026-08-05T21:11:38Z` and live state updated `2026-08-05T00:00:00Z`.
