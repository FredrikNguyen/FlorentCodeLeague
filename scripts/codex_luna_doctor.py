from __future__ import annotations

import argparse
from pathlib import Path
import json
import os
import re
import shutil

from common import ROOT, run_command, save_json, utc_run_id

STATE = ROOT / "state/codex_runtime.json"


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def model_rows(data) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for item in walk(data):
        model = item.get("id") or item.get("slug") or item.get("model") or item.get("name")
        if isinstance(model, str) and model.startswith("gpt-"):
            rows.setdefault(model, item)
    return rows


def parse_json_blob(text: str):
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    starts = [i for i, c in enumerate(text) if c in "[{"]
    for start in starts:
        try:
            return json.loads(text[start:])
        except json.JSONDecodeError:
            continue
    return None


def inspect() -> dict:
    result = {
        "codex_found": shutil.which("codex") is not None,
        "codex_version": None,
        "debug_command": None,
        "catalog_readable": False,
        "sol_backend": None,
        "terra_backend": None,
        "luna_backend": None,
        "native_luna_compatible": False,
        "override_catalog": None,
        "override_exists": False,
        "notes": [],
    }
    if not result["codex_found"]:
        result["notes"].append("codex executable not found")
        return result

    version = run_command(["codex", "--version"])
    result["codex_version"] = (version.stdout or version.stderr).strip()

    data = None
    for argv in (["codex", "debug", "models", "--json"], ["codex", "debug", "models"]):
        output = run_command(argv)
        parsed = parse_json_blob(output.stdout)
        if output.returncode == 0 and parsed is not None:
            data = parsed
            result["debug_command"] = argv
            break
    if data is not None:
        result["catalog_readable"] = True
        rows = model_rows(data)
        for model, key in (
            ("gpt-5.6-sol", "sol_backend"),
            ("gpt-5.6-terra", "terra_backend"),
            ("gpt-5.6-luna", "luna_backend"),
        ):
            row = rows.get(model, {})
            result[key] = row.get("multi_agent_version") or row.get("multiAgentVersion")
        result["native_luna_compatible"] = (
            result["sol_backend"] == result["luna_backend"]
            and result["sol_backend"] in {"v1", "v2"}
        )
    else:
        result["notes"].append("could not parse `codex debug models`; update Codex or inspect manually")

    if STATE.exists():
        try:
            state = json.loads(STATE.read_text(encoding="utf-8"))
            path = Path(state.get("catalog_path", ""))
            result["override_catalog"] = str(path) if str(path) else None
            result["override_exists"] = path.is_file()
        except Exception as exc:
            result["notes"].append(f"invalid codex runtime state: {exc}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--require-native-v1", action="store_true")
    args = parser.parse_args()
    report = inspect()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for key, value in report.items():
            print(f"{key}: {value}")
        if report["sol_backend"] == "v2" and report["luna_backend"] == "v1":
            print("\nDetected current Sol-V2/Luna-V1 incompatibility.")
            print("Run: python scripts/setup_codex_v1_catalog.py")
    if args.require_native_v1:
        return 0 if report["override_exists"] else 1
    return 0 if report["codex_found"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
