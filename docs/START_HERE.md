# Start here

> Generated cross-session handoff. Do not hand-edit dynamic fields. Update
> `state/project_state.json` with `scripts/set_project_state.py` and deployment state
> through the live operator, then run `make refresh-start`.

## Current development focus

| Field | Value |
|---|---|
| Milestone | v0015 close-contact bootstrap defense packaged; v72 active and observing before deployment unlock |
| Current hypothesis | On close-contact non-balanced geometries, limiting redundant pre-income emergency structures to one designated free Defender preserves first-route funding without weakening distant or post-income defense. |
| Current experiment | experiments/v72-close-contact-bootstrap-defense.md |
| Next recommended task | Continue deterministic observation of platform v72 to 24 series; promote it as known-good if evidence remains positive, then deploy packaged v0015 with v72 as rollback. |
| Candidate | `bots/candidate` |
| Frozen baseline | `bots/versions/v0015_close-contact-bootstrap-defense_20260809-1903_7dd72f03` |
| Last Codex task | Continue evidence-based iterations toward 2000 Elo while retaining the strongest reliable live rollback. |
| Last Codex outcome | v0015 passed a recomputed 51-39 current-pool gate, 4-1 remote gate, smoke/package/focused checks, and is frozen pending v72 live promotion at 24 series. |
| Last Codex report | experiments/v72-close-contact-bootstrap-defense.md |
| Last local report | reports/local-20260809T185644Z |

## Live deployment snapshot

| Field | Value |
|---|---|
| Phase | `active_observing` |
| Active platform version | 73 |
| Pending version | unknown |
| Previous active version | 72 |
| Last known-good version | 72 |
| Last known-good live score | 0.6417 |
| Current candidate live score | unknown |
| Last observation | 2026-08-09T20:13:19Z |
| Last decision | observation captured |

## Working tree snapshot

| Field | Value |
|---|---|
| Branch | `agent/publish-v10` |
| Commit | `7dd72f03` |
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

Generated at `2026-08-09T20:13:19Z` from project state updated `2026-08-09T19:03:58Z` and live state updated `2026-08-09T20:13:19Z`.
