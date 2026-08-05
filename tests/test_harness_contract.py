from __future__ import annotations

from pathlib import Path
import json
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HarnessContractTest(unittest.TestCase):
    def test_current_official_custom_agent_layout(self) -> None:
        config = tomllib.loads((ROOT / ".codex/config.toml").read_text(encoding="utf-8"))
        self.assertIn("agents", config)
        self.assertNotIn("sol_planner", config["agents"])
        self.assertNotIn("luna_implementer", config["agents"])
        for name in ("sol-planner.toml", "luna-implementer.toml", "sol-reviewer.toml"):
            self.assertTrue((ROOT / ".codex/agents" / name).is_file())

    def test_release_pipeline_packages_then_deploys(self) -> None:
        text = (ROOT / "scripts/release_candidate.py").read_text(encoding="utf-8")
        self.assertIn("package_candidate.py", text)
        self.assertIn("live_operator.py", text)
        self.assertIn('"deploy"', text)

    def test_custom_luna_agent_is_explicit(self) -> None:
        data = tomllib.loads((ROOT / ".codex/agents/luna-implementer.toml").read_text(encoding="utf-8"))
        self.assertEqual("gpt-5.6-luna", data["model"])
        self.assertEqual("max", data["model_reasoning_effort"])
        self.assertEqual("workspace-write", data["sandbox_mode"])

    def test_process_fallback_selects_luna_explicitly(self) -> None:
        text = (ROOT / "scripts/codex_task.py").read_text(encoding="utf-8")
        self.assertIn('models["implementer"]', text)
        self.assertIn('"--model", model', text)
        self.assertIn("gpt-5.6-luna", (ROOT / "configs/codex_harness.toml").read_text(encoding="utf-8"))

    def test_native_v1_route_is_invocation_scoped(self) -> None:
        setup = (ROOT / "scripts/setup_codex_v1_catalog.py").read_text(encoding="utf-8")
        wrapper = (ROOT / "scripts/codex_v1.sh").read_text(encoding="utf-8")
        self.assertIn("models-v1.json", setup)
        self.assertIn("models-original-", setup)
        self.assertIn("model_catalog_json", wrapper)
        self.assertNotIn("config.toml", wrapper)

    def test_v1_and_v2_modes_do_not_conflict_in_project_toml(self) -> None:
        project = (ROOT / ".codex/config.toml").read_text(encoding="utf-8")
        self.assertNotIn("[features.multi_agent_v2]", project)
        native = (ROOT / "scripts/codex_v1.sh").read_text(encoding="utf-8")
        self.assertIn("features.multi_agent_v2=false", native)
        diagnostic = (ROOT / "scripts/codex_v2_visible.sh").read_text(encoding="utf-8")
        self.assertIn("hide_spawn_agent_metadata=false", diagnostic)

    def test_live_reviewer_is_read_only(self) -> None:
        text = (ROOT / "scripts/live_autopilot.py").read_text(encoding="utf-8")
        self.assertIn('"--sandbox", "read-only"', text)
        self.assertIn("prefetched match-info", text)

    def test_live_policy_authorizes_autonomy(self) -> None:
        policy = tomllib.loads((ROOT / "configs/live_policy.toml").read_text(encoding="utf-8"))
        self.assertTrue(policy["autonomous_live_ops"])
        self.assertTrue(policy["auto_activate"])
        self.assertTrue(policy["auto_rollback"])

    def test_durable_live_state_and_updates_exist(self) -> None:
        state = json.loads((ROOT / "state/live_state.json").read_text(encoding="utf-8"))
        self.assertIn("last_known_good_version", state)
        self.assertIn("last_known_good_live_score", state)
        updates = (ROOT / "UPDATES.md").read_text(encoding="utf-8")
        self.assertIn("Append-only update log", updates)
        self.assertIn("Last known-good live score", updates)

    def test_luna_cannot_operate_live(self) -> None:
        luna = (ROOT / ".codex/agents/luna-implementer.toml").read_text(encoding="utf-8").lower()
        self.assertIn("never upload", luna)
        self.assertIn("live state", luna)


if __name__ == "__main__":
    unittest.main()
