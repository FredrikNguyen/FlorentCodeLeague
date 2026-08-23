# Start here

> Generated cross-session handoff. Do not hand-edit dynamic fields. Update
> `state/project_state.json` with `scripts/set_project_state.py` and deployment state
> through the live operator, then run `make refresh-start`.

## Current development focus

| Field | Value |
|---|---|
| Milestone | v0047 retained; repository cleanup and release documentation completed |
| Current hypothesis | A future candidate must improve verified route conversion or defensive response without weakening early belt repair |
| Current experiment | v411 rejected after 5-10 and 6-9 15-map screens; reports/local-20260821T085912Z |
| Next recommended task | Paused by user after cleanup; resume with a distinct replay-backed v0047 comparison |
| Candidate | `bots/candidate` |
| Frozen baseline | `bots/versions/v0047_pressure-economy-steward_20260821-0200_eeafad8f` |
| Last Codex task | Repository cleanup, release documentation, and v0047 retention |
| Last Codex outcome | Removed obsolete archives, v0001-v0046 snapshots, generated replay/cache/temp artifacts, starter bot, and pre-v0047 tests; retained v0047 as the only immutable snapshot; make static 67/67 and smoke 4/4 passed; no bot or live operation changed |
| Last Codex report | docs/REPOSITORY_CLEANUP.md |
| Last local report | reports/local-20260823T073457Z |

## Live deployment snapshot

| Field | Value |
|---|---|
| Phase | `active_observing` |
| Active platform version | 109 |
| Pending version | unknown |
| Previous active version | 107 |
| Last known-good version | 107 |
| Last known-good live score | 0.5128 |
| Current candidate live score | 0.6000 |
| Last observation | 2026-08-20T18:25:06Z |
| Last decision | observation captured |

## Working tree snapshot

| Field | Value |
|---|---|
| Branch | `agent/publish-v10` |
| Commit | `11a89464` |
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

Generated at `2026-08-23T07:42:34Z` from project state updated `2026-08-23T07:36:28Z` and live state updated `2026-08-20T18:25:06Z`.
