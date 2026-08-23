from __future__ import annotations

import argparse
import json
import subprocess

from common import ROOT, require_executable


def main() -> int:
    parser = argparse.ArgumentParser(description="One resumable live observation/decision cycle")
    parser.add_argument("--force-observe", action="store_true")
    args = parser.parse_args()
    require_executable("codex")
    require_executable("fcode")

    state_path = ROOT / "state/live_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("phase") == "uploaded_processing":
        rc = subprocess.run(["python", "scripts/live_operator.py", "resume"], cwd=ROOT, check=False).returncode
        if rc != 0:
            return rc
        state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("phase") != "active_observing" and not args.force_observe:
        print(f"No active observation to evaluate (phase={state.get('phase')}).")
        return 0

    rc = subprocess.run(["python", "scripts/live_operator.py", "observe"], cwd=ROOT, check=False).returncode
    if rc != 0:
        return rc
    state = json.loads(state_path.read_text(encoding="utf-8"))
    report_dir = ROOT / state["last_report_dir"]
    decision_path = report_dir / "live-decision.json"
    final_path = report_dir / "sol-live-review.md"
    jsonl_path = report_dir / "sol-live-review.jsonl"
    schema = ROOT / "schemas/live_decision.schema.json"

    prompt = f"""Act as the Sol medium live performance reviewer for Florent Code League.
Read AGENTS.md, UPDATES.md, configs/live_policy.toml, state/live_state.json, and all raw
JSON command records in {report_dir.relative_to(ROOT)}, including prefetched match-info files.
Do not call `fcode` and do not perform platform writes. Analyze ladder series for the currently
active version after its activation time; when activation time is unknown during baseline
bootstrap, use only matches you can confidently attribute to the active version and state the
uncertainty. Compute fractional series
score (our wins / 5), rating movement, opponent-Elo expected score and residual where fields
permit. Count crashes, submission errors, obvious TLE/exception/reliability failures from
available evidence. Return schema-valid JSON. Use keep_observing/insufficient_data before the
minimum series, promote only with adequate evidence, and rollback for a clear regression or
reliability defect. Never edit bot code and never activate directly; live_operator enforces policy.
"""
    argv = [
        "codex", "exec",
        "--model", "gpt-5.6-sol",
        "--sandbox", "read-only",
        "--config", 'model_reasoning_effort="medium"',
        "--json",
        "--output-schema", str(schema),
        "--output-last-message", str(decision_path),
        prompt,
    ]
    proc = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, check=False)
    jsonl_path.write_text(proc.stdout, encoding="utf-8")
    (jsonl_path.with_suffix(".jsonl.stderr")).write_text(proc.stderr, encoding="utf-8")
    if proc.returncode != 0 or not decision_path.is_file():
        print(proc.stderr)
        return proc.returncode or 1
    final_path.write_text(decision_path.read_text(encoding="utf-8"), encoding="utf-8")
    return subprocess.run([
        "python", "scripts/live_operator.py", "evaluate", "--decision", str(decision_path)
    ], cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
