from __future__ import annotations

import argparse
import json

from project_context import PROJECT_STATE_PATH, load_json, refresh_start_here, update_project_state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update durable development focus and refresh docs/START_HERE.md")
    parser.add_argument("--milestone")
    parser.add_argument("--hypothesis")
    parser.add_argument("--experiment")
    parser.add_argument("--next-task")
    parser.add_argument("--candidate-path")
    parser.add_argument("--baseline-path")
    parser.add_argument("--last-codex-task")
    parser.add_argument("--last-codex-outcome")
    parser.add_argument("--last-codex-report")
    parser.add_argument("--last-local-report")
    parser.add_argument("--clear-hypothesis", action="store_true")
    parser.add_argument("--clear-experiment", action="store_true")
    parser.add_argument("--show", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    changes = {}
    mapping = {
        "milestone": "current_milestone",
        "hypothesis": "current_hypothesis",
        "experiment": "current_experiment",
        "next_task": "next_recommended_task",
        "candidate_path": "candidate_path",
        "baseline_path": "baseline_path",
        "last_codex_task": "last_codex_task",
        "last_codex_outcome": "last_codex_outcome",
        "last_codex_report": "last_codex_report",
        "last_local_report": "last_local_report",
    }
    for argument, field in mapping.items():
        value = getattr(args, argument)
        if value is not None:
            changes[field] = value
    if args.clear_hypothesis:
        changes["current_hypothesis"] = None
    if args.clear_experiment:
        changes["current_experiment"] = None

    state = update_project_state(**changes) if changes else load_json(PROJECT_STATE_PATH)
    refresh_start_here()
    if args.show or not changes:
        print(json.dumps(state, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
