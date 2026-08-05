from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import shutil

from codex_luna_doctor import model_rows, parse_json_blob, walk
from common import ROOT, run_command, save_json

TARGET_MODELS = {"gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"}
STATE = ROOT / "state/codex_runtime.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_versions(value) -> int:
    changed = 0
    if isinstance(value, dict):
        model = value.get("id") or value.get("slug") or value.get("model") or value.get("name")
        if model in TARGET_MODELS:
            key = "multi_agent_version" if "multi_agent_version" in value else "multiAgentVersion"
            if value.get(key) != "v1":
                value[key] = "v1"
                changed += 1
        for child in value.values():
            changed += replace_versions(child)
    elif isinstance(value, list):
        for child in value:
            changed += replace_versions(child)
    return changed


def main() -> int:
    if not shutil.which("codex"):
        raise SystemExit("codex executable not found")

    parsed = None
    command = None
    raw = ""
    for argv in (["codex", "debug", "models", "--json"], ["codex", "debug", "models"]):
        result = run_command(argv)
        candidate = parse_json_blob(result.stdout)
        if result.returncode == 0 and candidate is not None:
            parsed = candidate
            raw = result.stdout
            command = argv
            break
    if parsed is None:
        raise SystemExit(
            "Could not obtain a complete JSON model catalog from `codex debug models`. "
            "Update Codex and rerun; no files were changed."
        )

    rows = model_rows(parsed)
    missing = sorted(TARGET_MODELS - set(rows))
    if missing:
        raise SystemExit(f"Model catalog missing required models: {missing}")

    original = json.dumps(parsed, indent=2, sort_keys=True).encode()
    changed = replace_versions(parsed)
    after_rows = model_rows(parsed)
    incompatible = [
        model for model in TARGET_MODELS
        if (after_rows[model].get("multi_agent_version") or after_rows[model].get("multiAgentVersion")) != "v1"
    ]
    if incompatible:
        raise SystemExit(f"Failed to create V1 catalog for: {incompatible}")

    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser().resolve()
    target_dir = codex_home / "fcl-harness"
    target_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = target_dir / f"models-original-{stamp}.json"
    catalog = target_dir / "models-v1.json"
    backup.write_bytes(original)
    catalog.write_text(json.dumps(parsed, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    state = {
        "schema_version": 1,
        "created_at": stamp,
        "codex_home": str(codex_home),
        "catalog_path": str(catalog),
        "backup_path": str(backup),
        "source_command": command,
        "source_sha256": sha256_bytes(original),
        "catalog_sha256": sha256_bytes(catalog.read_bytes()),
        "changed_entries": changed,
        "models": {
            model: (after_rows[model].get("multi_agent_version") or after_rows[model].get("multiAgentVersion"))
            for model in sorted(TARGET_MODELS)
        },
        "usage": [
            "--config", f'model_catalog_json="{catalog}"',
            "--config", "features.multi_agent=true",
            "--config", "features.multi_agent_v2=false",
        ],
    }
    save_json(STATE, state)
    print(f"Created reversible V1 model catalog: {catalog}")
    print(f"Original catalog backup: {backup}")
    print("No global config.toml was modified.")
    print("Use scripts/codex_v1.sh or scripts/codex_task.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
