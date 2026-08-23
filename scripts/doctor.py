from __future__ import annotations

import platform
import shutil
import sys

from common import ROOT, run_command


def main() -> int:
    problems: list[str] = []
    print(f"Python: {sys.version.split()[0]} ({platform.platform()})")
    if sys.version_info[:2] not in {(3, 12), (3, 13)}:
        problems.append("FCL documents require Python 3.12 or 3.13.")

    for exe in ("fcode", "codex", "git"):
        path = shutil.which(exe)
        print(f"{exe}: {path or 'NOT FOUND'}")
        if not path:
            problems.append(f"Missing executable: {exe}")

    if shutil.which("fcode"):
        result = run_command(["fcode", "--version"])
        print(f"fcode version: {result.stdout.strip() or result.stderr.strip()}")
    if shutil.which("codex"):
        result = run_command(["codex", "--version"])
        print(f"codex version: {result.stdout.strip() or result.stderr.strip()}")

    for required in (
        ROOT / "AGENTS.md",
        ROOT / "GAME_RULES.md",
        ROOT / "bots/candidate/main.py",
        ROOT / ".codex/config.toml",
    ):
        if not required.exists():
            problems.append(f"Missing: {required.relative_to(ROOT)}")

    maps = list((ROOT / "maps").glob("*.map26"))
    print(f"Synced maps: {len(maps)}")
    if len(maps) < 21:
        print("Hint: run `fcode maps sync`.")

    if problems:
        print("\nProblems:")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("\nDoctor checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
