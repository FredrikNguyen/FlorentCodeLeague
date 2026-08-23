from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class StartupContextTest(unittest.TestCase):
    def test_root_bootstrap_routes_to_concise_and_conditional_docs(self) -> None:
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("docs/START_HERE.md", text)
        self.assertIn("state/project_state.json", text)
        self.assertIn("state/live_state.json", text)
        self.assertIn("Do **not** read every long document", text)
        self.assertIn("Task-specific required reading", text)

    def test_nested_agent_files_exist(self) -> None:
        for path in (
            ROOT / "bots/candidate/AGENTS.md",
            ROOT / "scripts/AGENTS.md",
            ROOT / "tests/AGENTS.md",
        ):
            self.assertTrue(path.is_file(), path)

    def test_project_state_and_start_here_exist(self) -> None:
        state = json.loads((ROOT / "state/project_state.json").read_text(encoding="utf-8"))
        self.assertIn("current_milestone", state)
        self.assertIn("next_recommended_task", state)
        start = (ROOT / "docs/START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("Current development focus", start)
        self.assertIn("Live deployment snapshot", start)
        self.assertIn("Task-specific document routing", start)

    def test_custom_agents_read_startup_context(self) -> None:
        for name in ("sol-planner.toml", "luna-implementer.toml", "sol-reviewer.toml"):
            text = (ROOT / ".codex/agents" / name).read_text(encoding="utf-8")
            self.assertIn("docs/START_HERE.md", text)
            self.assertIn("AGENTS.md", text)

    def test_update_log_refreshes_start_here(self) -> None:
        text = (ROOT / "scripts/update_log.py").read_text(encoding="utf-8")
        self.assertIn("from project_context import refresh_start_here", text)
        self.assertGreaterEqual(text.count("refresh_start_here()"), 2)

    def test_codex_task_records_project_handoff(self) -> None:
        text = (ROOT / "scripts/codex_task.py").read_text(encoding="utf-8")
        self.assertIn("update_project_state", text)
        self.assertIn("last_codex_report", text)
        self.assertIn("state/project_state.json", text)


if __name__ == "__main__":
    unittest.main()
