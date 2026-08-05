from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import tomllib
from typing import Any

from common import ROOT, require_executable, run_command, save_json, utc_run_id
from update_log import append_update, refresh_current_state

STATE_PATH = ROOT / "state/live_state.json"
POLICY_PATH = ROOT / "configs/live_policy.toml"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_state() -> dict:
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def load_policy() -> dict:
    return tomllib.loads(POLICY_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    state["updated_at"] = now()
    save_json(STATE_PATH, state)
    refresh_current_state({
        "phase": state.get("phase"),
        "active_version": state.get("active_version"),
        "last_known_good_version": state.get("last_known_good_version"),
        "previous_active_version": state.get("previous_active_version"),
        "last_known_good_live_score": state.get("last_known_good_live_score"),
        "current_live_score": state.get("current_live_score"),
        "activated_at": state.get("activated_at"),
        "last_observation": state.get("last_observation_at"),
        "last_decision": state.get("last_decision"),
    })


def parse_json(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)



def extract_match_ids(data: Any) -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for item in walk(data):
        if not isinstance(item, dict):
            continue
        value = item.get("match_id")
        if value is None and "id" in item:
            markers = {"score", "games", "match_type", "type", "status", "rating_change", "team_a"}
            if markers.intersection(item):
                value = item.get("id")
        if value is None:
            continue
        rendered = str(value)
        if rendered not in seen:
            seen.add(rendered)
            ids.append(rendered)
    return ids

def first_value(data: Any, keys: tuple[str, ...]):
    for item in walk(data):
        for key in keys:
            if key in item and item[key] not in (None, ""):
                return item[key]
    return None


def version_rows(data: Any) -> list[dict]:
    rows = []
    for item in walk(data):
        if not isinstance(item, dict):
            continue
        version = item.get("version") or item.get("submission_version") or item.get("id")
        status = item.get("status") or item.get("state")
        if version is not None and status is not None:
            rows.append(item)
    return rows


def active_version(*payloads: Any):
    for data in payloads:
        for item in walk(data):
            if not isinstance(item, dict):
                continue
            active = item.get("active") is True or item.get("is_active") is True
            if active:
                return item.get("version") or item.get("submission_version") or item.get("id")
            for key in ("active_version", "active_submission_version", "submission_version"):
                if key in item and item[key] not in (None, ""):
                    return item[key]
    return None


def call_json(argv: list[str], report_dir: Path, name: str) -> tuple[int, Any, dict]:
    result = run_command(argv)
    payload = parse_json(result.stdout)
    record = result.to_dict()
    save_json(report_dir / f"{name}.json", record)
    return result.returncode, payload, record


def snapshot(label: str) -> tuple[Path, dict]:
    report_dir = ROOT / "reports" / utc_run_id(label)
    report_dir.mkdir(parents=True, exist_ok=True)
    payloads = {}
    commands = {
        "status": ["fcode", "status", "--json"],
        "submissions": ["fcode", "submission", "list", "--json"],
        "ladder": ["fcode", "ladder", "--around", "--json"],
        "matches": ["fcode", "match", "list", "--mine", "--type", "ladder", "--limit", "100", "--json"],
    }
    for name, argv in commands.items():
        _, payload, _ = call_json(argv, report_dir, name)
        payloads[name] = payload

    # Prefetch match details outside Codex. The reviewer can stay in a read-only sandbox
    # and never receives platform-write authority or network responsibility.
    match_ids = extract_match_ids(payloads.get("matches"))[:100]
    payloads["match_ids"] = match_ids
    for index, match_id in enumerate(match_ids, start=1):
        call_json(
            ["fcode", "match", "info", match_id, "--json"],
            report_dir,
            f"match-info-{index:03d}-{match_id}",
        )
    return report_dir, payloads


def require_authorized(policy: dict) -> None:
    if not policy.get("autonomous_live_ops"):
        raise SystemExit("Autonomous live operations are disabled in configs/live_policy.toml")


def wait_ready(version: str, policy: dict, report_dir: Path) -> bool:
    deadline = time.monotonic() + int(policy.get("submission_ready_timeout_seconds", 300))
    poll = int(policy.get("poll_interval_seconds", 15))
    attempt = 0
    while time.monotonic() < deadline:
        attempt += 1
        rc, payload, _ = call_json(
            ["fcode", "submission", "list", "--json"], report_dir, f"submissions-{attempt:03d}"
        )
        if rc == 0:
            for row in version_rows(payload):
                row_version = row.get("version") or row.get("submission_version") or row.get("id")
                if str(row_version) != str(version):
                    continue
                status = str(row.get("status") or row.get("state")).lower()
                if status == "ready":
                    return True
                if status in {"flagged", "rejected", "error", "failed"}:
                    return False
        time.sleep(max(1, poll))
    return False


def choose_uploaded_version(upload_payload: Any, before: Any, after: Any):
    direct = first_value(upload_payload, ("version", "submission_version", "id"))
    if direct is not None:
        return direct
    before_versions = {
        str(row.get("version") or row.get("submission_version") or row.get("id"))
        for row in version_rows(before)
    }
    for row in version_rows(after):
        value = row.get("version") or row.get("submission_version") or row.get("id")
        if str(value) not in before_versions:
            return value
    return None


def do_activate(version: str, report_dir: Path) -> None:
    rc, _, record = call_json(
        ["fcode", "submission", "activate", str(version), "--json"], report_dir, "activate"
    )
    if rc != 0:
        raise RuntimeError(record["stderr"] or "activation failed")


def bootstrap() -> int:
    state = load_state()
    report_dir, payloads = snapshot("live-bootstrap")
    current = active_version(payloads.get("status"), payloads.get("submissions"))
    state["active_version"] = current
    if state.get("last_known_good_version") is None:
        state["last_known_good_version"] = current
    state["phase"] = "idle"
    state["last_report_dir"] = str(report_dir.relative_to(ROOT))
    state["last_observation_at"] = now()
    state["last_decision"] = "bootstrap"
    save_state(state)
    append_update("Live state bootstrapped", [f"Active version: {current}", f"Report: {report_dir.relative_to(ROOT)}"])
    return 0


def deploy(archive: str, name: str) -> int:
    policy = load_policy()
    require_authorized(policy)
    state = load_state()
    if state.get("phase") == "active_observing" and not policy.get("allow_deploy_while_observing", False):
        raise SystemExit("A deployment is already being observed; resolve it before deploying another.")

    report_dir, payloads = snapshot("live-deploy")
    current = active_version(payloads.get("status"), payloads.get("submissions"))
    rollback_target = state.get("last_known_good_version") or current
    if rollback_target is None:
        raise SystemExit("No rollback target is known. Run `live_operator.py bootstrap` first.")

    archive_path = Path(archive)
    if not archive_path.is_absolute():
        archive_path = ROOT / archive_path
    if not archive_path.is_file():
        raise SystemExit(f"Archive not found: {archive_path}")

    rc, upload_payload, record = call_json(
        ["fcode", "submission", "upload", str(archive_path), "--name", name, "--json"],
        report_dir,
        "upload",
    )
    if rc != 0:
        append_update("Live upload failed", [f"Name: {name}", f"Report: {report_dir.relative_to(ROOT)}"])
        return rc
    _, after, _ = call_json(["fcode", "submission", "list", "--json"], report_dir, "submissions-after-upload")
    version = choose_uploaded_version(upload_payload, payloads.get("submissions"), after)
    if version is None:
        raise RuntimeError("Could not identify uploaded submission version; inspect report before retrying.")

    state.update({
        "phase": "uploaded_processing",
        "candidate": name,
        "active_version": current,
        "previous_active_version": current,
        "last_known_good_version": rollback_target,
        "pending_version": version,
        "current_live_score": None,
        "current_adjusted_score": None,
        "baseline_match_ids": [],
        "observed_match_ids": [],
        "last_report_dir": str(report_dir.relative_to(ROOT)),
        "last_decision": "uploaded",
    })
    save_state(state)
    append_update("Candidate uploaded", [f"Candidate: {name}", f"Version: {version}", f"Rollback target: {rollback_target}", f"Report: {report_dir.relative_to(ROOT)}"])

    if not policy.get("auto_activate", True):
        return 0
    ready = wait_ready(str(version), policy, report_dir)
    if not ready:
        state["phase"] = "submission_error"
        state["last_decision"] = "submission not ready"
        save_state(state)
        append_update("Candidate not activated", [f"Version: {version}", "Submission did not reach ready state.", f"Report: {report_dir.relative_to(ROOT)}"])
        return 1

    do_activate(str(version), report_dir)
    state.update({
        "phase": "active_observing",
        "active_version": version,
        "pending_version": None,
        "activated_at": now(),
        "last_observation_at": None,
        "last_decision": "activated for observation",
    })
    save_state(state)
    append_update("Candidate activated", [f"Version: {version}", f"Previous/rollback: {rollback_target}", f"Observation state persisted in state/live_state.json", f"Report: {report_dir.relative_to(ROOT)}"])
    return 0


def resume() -> int:
    state = load_state()
    policy = load_policy()
    require_authorized(policy)
    if state.get("phase") == "uploaded_processing" and state.get("pending_version") is not None:
        report_dir = ROOT / "reports" / utc_run_id("live-resume")
        report_dir.mkdir(parents=True, exist_ok=True)
        version = str(state["pending_version"])
        if not wait_ready(version, policy, report_dir):
            state["phase"] = "submission_error"
            state["last_decision"] = "resume: submission not ready"
            state["last_report_dir"] = str(report_dir.relative_to(ROOT))
            save_state(state)
            return 1
        do_activate(version, report_dir)
        state.update({"phase": "active_observing", "active_version": version, "pending_version": None, "activated_at": now(), "last_decision": "resumed and activated", "last_report_dir": str(report_dir.relative_to(ROOT))})
        save_state(state)
        append_update("Deployment resumed", [f"Activated version: {version}", f"Report: {report_dir.relative_to(ROOT)}"])
        return 0
    return observe()


def observe() -> int:
    state = load_state()
    report_dir, payloads = snapshot("live-observe")
    current = active_version(payloads.get("status"), payloads.get("submissions"))
    if current is not None:
        state["active_version"] = current
    state["last_report_dir"] = str(report_dir.relative_to(ROOT))
    state["last_observation_at"] = now()
    state["last_decision"] = "observation captured"
    save_state(state)
    append_update("Live observation captured", [f"Active version: {state.get('active_version')}", f"Report: {report_dir.relative_to(ROOT)}"])
    print(report_dir)
    return 0


def rollback(reason: str) -> int:
    policy = load_policy()
    require_authorized(policy)
    state = load_state()
    target = state.get("last_known_good_version") or state.get("previous_active_version")
    if target is None:
        raise SystemExit("No rollback version recorded.")
    report_dir = ROOT / "reports" / utc_run_id("live-rollback")
    report_dir.mkdir(parents=True, exist_ok=True)
    failed_version = state.get("active_version")
    do_activate(str(target), report_dir)
    state.update({
        "phase": "rolled_back",
        "active_version": target,
        "pending_version": None,
        "current_live_score": None,
        "current_adjusted_score": None,
        "last_decision": f"rollback: {reason}",
        "last_report_dir": str(report_dir.relative_to(ROOT)),
        "last_observation_at": now(),
    })
    save_state(state)
    append_update("Automatic rollback", [f"Failed candidate version: {failed_version}", f"Reactivated: {target}", f"Reason: {reason}", f"Report: {report_dir.relative_to(ROOT)}"])
    return 0


def promote(score: float | None, adjusted: float | None, reason: str) -> int:
    state = load_state()
    active = state.get("active_version")
    if active is None:
        raise SystemExit("No active version to promote.")
    state.update({
        "phase": "idle",
        "last_known_good_version": active,
        "last_known_good_live_score": score,
        "last_known_good_adjusted_score": adjusted,
        "current_live_score": score,
        "current_adjusted_score": adjusted,
        "last_decision": f"promoted: {reason}",
    })
    save_state(state)
    append_update("Live candidate promoted", [f"Version: {active}", f"Live score: {score}", f"Adjusted score: {adjusted}", f"Reason: {reason}"])
    return 0


def evaluate(decision_path: str) -> int:
    policy = load_policy()
    require_authorized(policy)
    state = load_state()
    decision = json.loads(Path(decision_path).read_text(encoding="utf-8"))
    series = int(decision["series_count"])
    score = decision.get("live_score")
    adjusted = decision.get("adjusted_score")
    reliability = int(decision.get("reliability_failures", 0))
    state.update({
        "current_live_score": score,
        "current_adjusted_score": adjusted,
        "rating_after": decision.get("rating_after"),
        "rank_after": decision.get("rank_after"),
        "observed_match_ids": decision.get("match_ids", []),
        "last_observation_at": now(),
        "last_decision": decision.get("decision"),
    })
    save_state(state)
    append_update("Live score evaluated", [f"Version: {state.get('active_version')}", f"Series: {series}", f"Score: {score}", f"Adjusted score: {adjusted}", f"Reliability failures: {reliability}", f"Proposed decision: {decision.get('decision')}", f"Reason: {decision.get('reason')}"])

    if reliability > 0 and policy.get("rollback_on_reliability_failure", True):
        return rollback(f"{reliability} reliability failure(s): {decision.get('reason')}")
    if decision.get("decision") == "rollback":
        return rollback(str(decision.get("reason")))
    if series < int(policy.get("minimum_series", 12)):
        state = load_state()
        state["phase"] = "active_observing"
        state["last_decision"] = "insufficient live series"
        save_state(state)
        return 0

    baseline = state.get("last_known_good_live_score")
    baseline_adjusted = state.get("last_known_good_adjusted_score")
    raw_worse = baseline is not None and score is not None and score <= baseline - float(policy.get("raw_score_rollback_margin", 0.05))
    adjusted_comparable = baseline_adjusted is not None and adjusted is not None
    adjusted_worse = adjusted_comparable and adjusted <= baseline_adjusted - float(policy.get("adjusted_score_rollback_margin", 0.03))
    if raw_worse and (adjusted_worse if adjusted_comparable else True):
        return rollback(f"live score regression: candidate={score}, known_good={baseline}, adjusted={adjusted}, known_good_adjusted={baseline_adjusted}")

    if decision.get("decision") == "promote" and series >= int(policy.get("preferred_series", 24)):
        return promote(score, adjusted, str(decision.get("reason")))

    state = load_state()
    state["phase"] = "active_observing"
    state["last_decision"] = "keep observing"
    save_state(state)
    return 0


def show_status() -> int:
    print(json.dumps(load_state(), indent=2, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("bootstrap")
    deploy_p = sub.add_parser("deploy")
    deploy_p.add_argument("--archive", required=True)
    deploy_p.add_argument("--name", required=True)
    sub.add_parser("resume")
    sub.add_parser("observe")
    rollback_p = sub.add_parser("rollback")
    rollback_p.add_argument("--reason", required=True)
    promote_p = sub.add_parser("promote")
    promote_p.add_argument("--score", type=float)
    promote_p.add_argument("--adjusted", type=float)
    promote_p.add_argument("--reason", required=True)
    evaluate_p = sub.add_parser("evaluate")
    evaluate_p.add_argument("--decision", required=True)
    sub.add_parser("status")
    args = parser.parse_args()

    if args.command != "status":
        require_executable("fcode")
    return {
        "bootstrap": bootstrap,
        "deploy": lambda: deploy(args.archive, args.name),
        "resume": resume,
        "observe": observe,
        "rollback": lambda: rollback(args.reason),
        "promote": lambda: promote(args.score, args.adjusted, args.reason),
        "evaluate": lambda: evaluate(args.decision),
        "status": show_status,
    }[args.command]()


if __name__ == "__main__":
    raise SystemExit(main())
