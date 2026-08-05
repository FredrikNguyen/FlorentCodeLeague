from __future__ import annotations

import argparse
from pathlib import Path

from common import ROOT, require_executable, run_command, save_json, utc_run_id


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload only; never activates.")
    parser.add_argument("path")
    parser.add_argument("--name", required=True)
    parser.add_argument("--confirm", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.confirm:
        raise SystemExit("Refusing upload without --confirm.")
    require_executable("fcode")
    path = Path(args.path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        raise SystemExit(f"Not found: {path}")

    result = run_command([
        "fcode", "submission", "upload", str(path),
        "--name", args.name, "--json"
    ])
    report = ROOT / "reports" / utc_run_id("upload") / "upload.json"
    save_json(report, result.to_dict())
    print(result.stdout or result.stderr)
    print("Upload complete. This script did NOT activate the submission.")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
