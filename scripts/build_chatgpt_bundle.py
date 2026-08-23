from __future__ import annotations

import json
import subprocess
import zipfile
from datetime import UTC, datetime
from pathlib import Path

from common import ROOT
from project_context import refresh_start_here

OUT = ROOT / "artifacts/chatgpt"


def read(path: Path, *, limit: int | None = None) -> str:
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    return text if limit is None or len(text) <= limit else text[:limit] + "\n…[truncated]\n"


def command(*argv: str) -> str:
    proc = subprocess.run(argv, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else "unavailable"


def latest_updates(max_chars: int = 5000) -> str:
    text = read(ROOT / "UPDATES.md")
    marker = "<!-- Automation appends newest entries immediately below this comment. -->"
    if marker in text:
        text = text.split(marker, 1)[1]
    return text[:max_chars].strip() or "No recorded updates."


def source_snapshot() -> str:
    chunks: list[str] = []
    for path in sorted((ROOT / "bots/candidate").rglob("*.py")):
        rel = path.relative_to(ROOT)
        chunks.append(f"### `{rel}`\n\n```python\n{read(path)}\n```")
    return "\n\n".join(chunks)


def latest_report_summary() -> str:
    state = json.loads(read(ROOT / "state/project_state.json"))
    rel = state.get("last_local_report") or state.get("last_codex_report")
    if not rel:
        return "No latest report recorded."
    path = ROOT / rel
    candidates = [path / "summary.md", path / "final.md", path / "manifest.json"]
    rendered = []
    for candidate in candidates:
        if candidate.is_file():
            rendered.append(f"### `{candidate.relative_to(ROOT)}`\n\n{read(candidate, limit=5000)}")
    return "\n\n".join(rendered) or f"Report path recorded as `{rel}`, with no compact summary file."


def packet(prompt_path: Path, title: str) -> str:
    refresh_start_here()
    branch = command("git", "branch", "--show-current")
    sha = command("git", "rev-parse", "--short=8", "HEAD")
    diff = command("git", "diff", "--", "bots/candidate", "tests", "scripts", "docs/CURRENT_PLAN.md")
    if not diff:
        diff = "No uncommitted relevant diff."
    return f"""# {title}

## Instructions

{read(prompt_path)}

## Current planning request

{read(ROOT / 'docs/PLANNING_REQUEST.md')}

## Current project handoff

{read(ROOT / 'docs/START_HERE.md')}

## Stable project brief

{read(ROOT / 'docs/PROJECT_BRIEF.md')}

## Current external plan

{read(ROOT / 'docs/CURRENT_PLAN.md')}

## Current machine state

### `state/project_state.json`

```json
{read(ROOT / 'state/project_state.json')}
```

### `state/live_state.json`

```json
{read(ROOT / 'state/live_state.json')}
```

## Git snapshot

- Branch: `{branch}`
- Commit: `{sha}`

```diff
{diff}
```

## Recent updates

{latest_updates()}

## Latest report summary

{latest_report_summary()}

## Current candidate source

{source_snapshot()}

## Additional detailed sources available in the repository

- `GAME_RULES.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/EVALUATION_PLAN.md`
- `docs/SUBMISSION_AND_VERSIONING.md`
- `docs/LIVE_AUTOPILOT.md`

Generated at {datetime.now(UTC).isoformat(timespec='seconds').replace('+00:00', 'Z')}.
"""


def ensure_bundle_inputs() -> None:
    defaults = {
        ROOT / "docs/PLANNING_REQUEST.md": (
            "# Current planning request\n\n"
            "Plan the next best improvement for the current bot. "
            "Keep it small enough for one Luna XHigh implementation session.\n"
        ),
        ROOT / "docs/CURRENT_PLAN.md": (
            "# Current external plan\n\nNo external plan has been supplied yet.\n"
        ),
    }
    for path, content in defaults.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")


def main() -> int:
    ensure_bundle_inputs()
    OUT.mkdir(parents=True, exist_ok=True)
    planning = packet(ROOT / "docs/CHATGPT_PLAN_PROMPT.md", "ChatGPT planning packet")
    review = packet(ROOT / "docs/CHATGPT_RELEASE_REVIEW_PROMPT.md", "ChatGPT release-review packet")
    planning_path = OUT / "PLANNING_PACKET.md"
    review_path = OUT / "RELEASE_REVIEW_PACKET.md"
    planning_path.write_text(planning, encoding="utf-8")
    review_path.write_text(review, encoding="utf-8")
    (ROOT / "docs/CHATGPT_CONTEXT.md").write_text(
        planning.split("## Instructions", 1)[1].split("## Current project handoff", 1)[1],
        encoding="utf-8",
    )

    bundle = OUT / "chatgpt-planning-bundle.zip"
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel in [
            "artifacts/chatgpt/PLANNING_PACKET.md",
            "docs/CHATGPT_PLAN_PROMPT.md",
            "docs/CHATGPT_CONTEXT.md",
            "docs/PLANNING_REQUEST.md",
            "docs/CURRENT_PLAN.md",
            "docs/PROJECT_BRIEF.md",
            "docs/START_HERE.md",
            "state/project_state.json",
            "state/live_state.json",
        ]:
            path = ROOT / rel
            if path.is_file():
                zf.write(path, rel)
        for path in sorted((ROOT / "bots/candidate").rglob("*.py")):
            zf.write(path, path.relative_to(ROOT))

    print(planning_path)
    print(review_path)
    print(bundle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
