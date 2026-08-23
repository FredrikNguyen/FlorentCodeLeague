from __future__ import annotations

import argparse

from common import ROOT, require_executable, run_command, save_json, utc_run_id

DEFAULT_MAPS = ["sprint", "bridge", "crossfire", "vault", "aurora"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", default="bots/candidate")
    parser.add_argument("--baseline", default="bots/baseline")
    parser.add_argument("--maps", nargs="*", default=DEFAULT_MAPS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_executable("fcode")
    run_id = utc_run_id("remote")
    report_dir = ROOT / "reports" / run_id

    argv = [
        "fcode", "match", "test",
        args.candidate, args.baseline, *args.maps, "--json"
    ]
    result = run_command(argv)
    save_json(report_dir / "remote-test.json", result.to_dict())
    print(result.stdout or result.stderr)
    print(f"Saved: {report_dir}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
