from __future__ import annotations

import argparse

from common import ROOT, require_executable, run_command, save_json, utc_run_id


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="snapshot")
    parser.add_argument("--limit", type=int, default=100)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_executable("fcode")
    report_dir = ROOT / "reports" / utc_run_id(f"live-{args.label}")

    commands = {
        "status": ["fcode", "status", "--json"],
        "ladder-around": ["fcode", "ladder", "--around", "--json"],
        "matches": [
            "fcode", "match", "list", "--mine", "--type", "ladder",
            "--limit", str(args.limit), "--json",
        ],
        "submissions": ["fcode", "submission", "list", "--json"],
    }
    failed = False
    for name, argv in commands.items():
        result = run_command(argv)
        save_json(report_dir / f"{name}.json", result.to_dict())
        failed = failed or result.returncode != 0
        print(f"{name}: rc={result.returncode}")
    print(f"Saved: {report_dir}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
