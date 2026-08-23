from __future__ import annotations

import argparse
import json
import subprocess
import sys

from common import ROOT


def main() -> int:
    parser = argparse.ArgumentParser(description="Package and autonomously deploy an approved candidate")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--experiment")
    args = parser.parse_args()

    before = set((ROOT / "artifacts/submissions").glob("*.manifest.json"))
    command = [sys.executable, "scripts/package_candidate.py", "--slug", args.slug]
    if args.experiment:
        command += ["--experiment", args.experiment]
    rc = subprocess.run(command, cwd=ROOT, check=False).returncode
    if rc != 0:
        return rc

    after = set((ROOT / "artifacts/submissions").glob("*.manifest.json"))
    created = sorted(after - before, key=lambda path: path.stat().st_mtime)
    if not created:
        raise SystemExit("Packaging succeeded but no new submission manifest was found.")
    manifest_path = created[-1]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    archive = ROOT / manifest["archive"]
    name = manifest["version"].replace("_", "-")
    return subprocess.run([
        sys.executable,
        "scripts/live_operator.py",
        "deploy",
        "--archive", str(archive),
        "--name", name,
    ], cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
