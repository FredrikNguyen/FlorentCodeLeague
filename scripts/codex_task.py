from __future__ import annotations

import argparse
from pathlib import Path
import json
import subprocess
import tomllib

from common import ROOT, require_executable, save_json, utc_run_id
from project_context import refresh_start_here, update_project_state
from update_log import append_update

CONFIG = ROOT / "configs/codex_harness.toml"
PROJECT_STATE = ROOT / "state/project_state.json"


def compact(text: str, *, max_chars: int = 1400) -> str:
    rendered = " ".join(text.strip().split())
    return rendered if len(rendered) <= max_chars else rendered[: max_chars - 1] + "…"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one Luna implementation/test/self-review session")
    parser.add_argument("task", nargs="*")
    parser.add_argument("--plan", default=None, help="Plan file to implement")
    args = parser.parse_args()

    require_executable("codex")
    cfg = tomllib.loads(CONFIG.read_text(encoding="utf-8"))
    if cfg.get("allow_subagents", False):
        raise SystemExit("This cost-efficient workflow requires allow_subagents=false")

    models = cfg["models"]
    model = models["implementer"]
    reasoning_effort = models.get("implementer_effort", "max")
    if not PROJECT_STATE.is_file():
        raise SystemExit("state/project_state.json is required")

    refresh_start_here()
    if args.plan:
        plan_path = ROOT / args.plan
        if not plan_path.is_file():
            raise SystemExit(f"Plan not found: {plan_path}")
        plan_text = plan_path.read_text(encoding="utf-8").strip()
        if "No external plan has been approved" in plan_text:
            raise SystemExit("docs/CURRENT_PLAN.md still contains the empty template")
        task = f"Implement the approved plan in {args.plan}."
    else:
        task = " ".join(args.task).strip()
        if not task:
            raise SystemExit('Provide a task or use --plan docs/CURRENT_PLAN.md')
        plan_path = None

    report_dir = ROOT / "reports" / utc_run_id("luna")
    report_dir.mkdir(parents=True, exist_ok=True)
    events = report_dir / "events.jsonl"
    stderr_path = report_dir / "events.jsonl.stderr"
    final = report_dir / "final.md"

    plan_instruction = (
        f"Read and implement {plan_path.relative_to(ROOT)} exactly. " if plan_path else ""
    )
    prompt = f"""You are the repository's single implementation agent.
Your explicit model is {model} with reasoning effort {reasoning_effort}.
Do not spawn subagents or invoke Sol.

Task:
{task}

{plan_instruction}Read docs/START_HERE.md, the nearest applicable AGENTS.md files, and only the source
files/document sections required by the task. State a compact hypothesis and scope, implement
the smallest complete change, run focused tests (and smoke games only when behavior changed),
inspect the actual git diff, fix defects in this same session, and return at most
{cfg.get('max_final_summary_lines', 16)} lines covering changes, tests, result, risks, and next step.
Do not run the full evaluation matrix unless this is explicitly a release candidate.
Do not paste full logs; save them under {report_dir.relative_to(ROOT)}.
Do not perform platform upload/activation unless the task explicitly says this is a gated release.
"""

    argv = [
        "codex", "exec",
        "--model", model,
        "--sandbox", "workspace-write",
        "--config", f'model_reasoning_effort="{reasoning_effort}"',
        "--json",
        "--output-last-message", str(final),
        prompt,
    ]
    proc = subprocess.run(
        argv,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    events.write_text(proc.stdout, encoding="utf-8")
    stderr_path.write_text(proc.stderr, encoding="utf-8")
    final_text = final.read_text(encoding="utf-8") if final.exists() else ""

    manifest = {
        "backend": "single-process",
        "model": model,
        "reasoning_effort": reasoning_effort,
        "subagents": False,
        "task": task,
        "plan": str(plan_path.relative_to(ROOT)) if plan_path else None,
        "returncode": proc.returncode,
        "events": str(events.relative_to(ROOT)),
        "stderr": str(stderr_path.relative_to(ROOT)),
        "final": str(final.relative_to(ROOT)),
    }
    save_json(report_dir / "manifest.json", manifest)

    outcome = "completed" if proc.returncode == 0 else "failed"
    update_project_state(
        last_codex_task=task,
        last_codex_outcome=outcome,
        last_codex_report=str(report_dir.relative_to(ROOT)),
    )
    append_update(
        "Luna XHigh implementation run",
        [
            f"Task: {compact(task, max_chars=400)}",
            f"Model: `{cfg['model']}` with `{cfg['reasoning_effort']}` reasoning; subagents disabled.",
            f"Outcome: `{outcome}`; report: `{report_dir.relative_to(ROOT)}`.",
            f"Summary: {compact(final_text) if final_text else 'No final message produced.'}",
        ],
    )
    print(final_text or proc.stderr)
    print(f"Report: {report_dir}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
