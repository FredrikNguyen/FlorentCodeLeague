from __future__ import annotations

from project_context import refresh_start_here


def main() -> int:
    path = refresh_start_here()
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
