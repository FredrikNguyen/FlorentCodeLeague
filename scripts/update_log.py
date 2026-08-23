from __future__ import annotations

import re
from datetime import UTC, datetime

from common import ROOT
from project_context import refresh_start_here

UPDATES = ROOT / "UPDATES.md"
MARKER = "<!-- Automation appends newest entries immediately below this comment. -->"


def now_utc() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def append_update(title: str, bullets: list[str]) -> None:
    text = UPDATES.read_text(encoding="utf-8")
    if MARKER not in text:
        raise RuntimeError("UPDATES.md marker missing")
    entry = "\n\n### " + title + " — " + now_utc() + "\n\n"
    entry += "\n".join(f"- {bullet}" for bullet in bullets) + "\n"
    UPDATES.write_text(text.replace(MARKER, MARKER + entry, 1), encoding="utf-8")
    refresh_start_here()


def refresh_current_state(values: dict[str, object]) -> None:
    text = UPDATES.read_text(encoding="utf-8")
    labels = {
        "phase": "Workflow phase",
        "active_version": "Current active platform version",
        "last_known_good_version": "Last known-good platform version",
        "previous_active_version": "Previous active platform version",
        "last_known_good_live_score": "Last known-good live score",
        "current_live_score": "Current candidate live score",
        "activated_at": "Last deployment",
        "last_observation": "Last observation",
        "last_decision": "Last decision",
    }
    for key, label in labels.items():
        if key not in values:
            continue
        value = values[key]
        rendered = "unknown" if value is None else str(value)
        pattern = rf"(^\| {re.escape(label)} \| ).*?( \|$)"
        text, count = re.subn(pattern, rf"\g<1>{rendered}\g<2>", text, flags=re.MULTILINE)
        if count != 1:
            raise RuntimeError(f"Could not update UPDATES.md field: {label}")
    UPDATES.write_text(text, encoding="utf-8")
    refresh_start_here()
