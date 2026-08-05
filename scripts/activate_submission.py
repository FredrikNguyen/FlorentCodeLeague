from __future__ import annotations

import argparse

from common import ROOT, require_executable, run_command, save_json, utc_run_id


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("version")
    parser.add_argument("--confirm", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.confirm:
        raise SystemExit("Refusing activation without --confirm.")
    require_executable("fcode")

    listing = run_command(["fcode", "submission", "list", "--json"])
    if listing.returncode != 0:
        print(listing.stderr)
        return listing.returncode

    result = run_command([
        "fcode", "submission", "activate", str(args.version), "--json"
    ])
    report_dir = ROOT / "reports" / utc_run_id("activation")
    save_json(report_dir / "before-submissions.json", listing.to_dict())
    save_json(report_dir / "activation.json", result.to_dict())
    status = run_command(["fcode", "status", "--json"])
    save_json(report_dir / "after-status.json", status.to_dict())
    print(result.stdout or result.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
