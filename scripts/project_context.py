from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from common import ROOT, save_json

PROJECT_STATE_PATH = ROOT / "state/project_state.json"
LIVE_STATE_PATH = ROOT / "state/live_state.json"
START_HERE_PATH = ROOT / "docs/START_HERE.md"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def display(value: Any) -> str:
    if value is None or value == "":
        return "unknown"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value).replace("\n", " ").replace("|", "\\|")


def render_start_here(project: dict[str, Any], live: dict[str, Any]) -> str:
    return f"""# Start here

> Generated cross-session handoff. Do not hand-edit dynamic fields. Update
> `state/project_state.json` with `scripts/set_project_state.py` and deployment state
> through the live operator, then run `make refresh-start`.

## Current development focus

| Field | Value |
|---|---|
| Milestone | {display(project.get('current_milestone'))} |
| Current hypothesis | {display(project.get('current_hypothesis'))} |
| Current experiment | {display(project.get('current_experiment'))} |
| Next recommended task | {display(project.get('next_recommended_task'))} |
| Candidate | `{display(project.get('candidate_path'))}` |
| Frozen baseline | `{display(project.get('baseline_path'))}` |
| Last Codex task | {display(project.get('last_codex_task'))} |
| Last Codex outcome | {display(project.get('last_codex_outcome'))} |
| Last Codex report | {display(project.get('last_codex_report'))} |
| Last local report | {display(project.get('last_local_report'))} |

## Live deployment snapshot

| Field | Value |
|---|---|
| Phase | `{display(live.get('phase'))}` |
| Active platform version | {display(live.get('active_version'))} |
| Pending version | {display(live.get('pending_version'))} |
| Previous active version | {display(live.get('previous_active_version'))} |
| Last known-good version | {display(live.get('last_known_good_version'))} |
| Last known-good live score | {display(live.get('last_known_good_live_score'))} |
| Current candidate live score | {display(live.get('current_live_score'))} |
| Last observation | {display(live.get('last_observation_at'))} |
| Last decision | {display(live.get('last_decision'))} |

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

Generated at `{now_utc()}` from project state updated `{display(project.get('updated_at'))}` and live state updated `{display(live.get('updated_at'))}`.
"""


def refresh_start_here() -> Path:
    project = load_json(PROJECT_STATE_PATH)
    live = load_json(LIVE_STATE_PATH)
    START_HERE_PATH.parent.mkdir(parents=True, exist_ok=True)
    START_HERE_PATH.write_text(render_start_here(project, live), encoding="utf-8")
    return START_HERE_PATH


def update_project_state(**changes: Any) -> dict[str, Any]:
    state = load_json(PROJECT_STATE_PATH)
    unknown = sorted(set(changes) - set(state))
    if unknown:
        raise KeyError(f"Unknown project-state fields: {', '.join(unknown)}")
    state.update(changes)
    state["updated_at"] = now_utc()
    save_json(PROJECT_STATE_PATH, state)
    refresh_start_here()
    return state
