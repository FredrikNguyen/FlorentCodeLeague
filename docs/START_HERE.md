# Start here

> Generated cross-session handoff. Do not hand-edit dynamic fields. Update
> `state/project_state.json` with `scripts/set_project_state.py` and deployment state
> through the live operator, then run `make refresh-start`.

## Current development focus

| Field | Value |
|---|---|
| Milestone | Reviewer-only workflow complete; v0008 retained as baseline and platform v10 is under live observation |
| Current hypothesis | The locally verified v0008 winner should outperform the prior v0006 snapshot; retain it as baseline while monitoring live reliability without implementing source changes. |
| Current experiment | reports/reviewer-workflow-20260806T1202Z |
| Next recommended task | Reviewer-only live observation of platform v10; do not change the baseline or bot source until live evidence is available. |
| Candidate | `bots/candidate` |
| Frozen baseline | `bots/versions/v0008_reviewer-current-best_20260806-1209_3f2505d7` |
| Last Codex task | Reviewer-only workflow: compare current candidate and unseen ready submissions, validate only the final winner, activate it, and capture live evidence. |
| Last Codex outcome | v0008 beat v0006 on 210 games (953940 vs 748370, ratio 1.2747, 110/210 wins); v4-v6 lost, v7 and v8 were harness-rejected for finally blocks, and v9 lost 168600 vs 174450 (0.9665). v0008 is platform v10 with v2 preserved for rollback; its first two rated series are 3-2 and 0-5. |
| Last Codex report | reports/reviewer-workflow-20260806T1202Z |
| Last local report | reports/local-20260806T122741Z |

## Live deployment snapshot

| Field | Value |
|---|---|
| Phase | `active_observing` |
| Active platform version | 10 |
| Pending version | unknown |
| Previous active version | 8 |
| Last known-good version | 2 |
| Last known-good live score | unknown |
| Current candidate live score | unknown |
| Last observation | 2026-08-06T13:14:35Z |
| Last decision | observation captured |

## Working tree snapshot

| Field | Value |
|---|---|
| Branch | `main` |
| Commit | `3f2505d7` |
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

Generated at `2026-08-06T13:15:48Z` from project state updated `2026-08-06T13:14:35Z` and live state updated `2026-08-06T13:14:35Z`.
