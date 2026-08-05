from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Store the request embedded in the generated ChatGPT planning packet."
    )
    parser.add_argument("request", nargs="+")
    args = parser.parse_args()
    request = " ".join(args.request).strip()
    if not request:
        raise SystemExit("Planning request cannot be empty")

    path = ROOT / "docs" / "PLANNING_REQUEST.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# Current planning request\n\n{request}\n",
        encoding="utf-8",
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
