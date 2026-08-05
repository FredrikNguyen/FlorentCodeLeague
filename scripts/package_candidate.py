from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import shutil
import subprocess
import zipfile

from common import ROOT, save_json


FORBIDDEN_SUFFIXES = {".so", ".dll", ".dylib", ".pyd"}
MAX_ARCHIVE = 5 * 1024 * 1024
MAX_UNPACKED = 50 * 1024 * 1024
MAX_FILES = 500


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="bots/candidate")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--experiment")
    return parser.parse_args()


def git_value(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False
    )
    return proc.stdout.strip() or "nogit"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    args = parse_args()
    source = ROOT / args.source
    if not (source / "main.py").is_file():
        raise SystemExit(f"{source} must contain main.py")

    sha = git_value("rev-parse", "--short=8", "HEAD")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    existing = sorted((ROOT / "bots/versions").glob("v[0-9][0-9][0-9][0-9]_*"))
    number = len(existing) + 1
    version = f"v{number:04d}_{args.slug}_{stamp}_{sha}"

    snapshot = ROOT / "bots/versions" / version
    if snapshot.exists():
        raise SystemExit(f"Snapshot exists: {snapshot}")
    shutil.copytree(source, snapshot, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    entries = [p for p in snapshot.rglob("*") if p.is_file()]
    unpacked = sum(p.stat().st_size for p in entries)
    forbidden = [p for p in entries if p.suffix.lower() in FORBIDDEN_SUFFIXES]
    if len(entries) > MAX_FILES or unpacked > MAX_UNPACKED or forbidden:
        raise SystemExit(
            f"Package invalid: files={len(entries)}, bytes={unpacked}, forbidden={forbidden}"
        )

    output_dir = ROOT / "artifacts/submissions"
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{version}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in entries:
            zf.write(path, path.relative_to(snapshot))
    if archive.stat().st_size > MAX_ARCHIVE:
        archive.unlink(missing_ok=True)
        raise SystemExit("Archive exceeds 5 MB.")

    manifest = {
        "version": version,
        "source": str(source.relative_to(ROOT)),
        "snapshot": str(snapshot.relative_to(ROOT)),
        "archive": str(archive.relative_to(ROOT)),
        "archive_sha256": sha256(archive),
        "archive_bytes": archive.stat().st_size,
        "unpacked_bytes": unpacked,
        "files": len(entries),
        "git_sha": git_value("rev-parse", "HEAD"),
        "git_status": git_value("status", "--short"),
        "experiment": args.experiment,
    }
    save_json(archive.with_suffix(".manifest.json"), manifest)
    print(f"Created {archive}")
    print(f"SHA256 {manifest['archive_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
