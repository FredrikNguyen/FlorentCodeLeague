from __future__ import annotations

import ast
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "bots/candidate"
FORBIDDEN_SUFFIXES = {".so", ".dll", ".dylib", ".pyd"}


class StaticContractTest(unittest.TestCase):
    def test_entrypoint_exists_and_mentions_player(self) -> None:
        entry = CANDIDATE / "main.py"
        self.assertTrue(entry.is_file())
        tree = ast.parse(entry.read_text(encoding="utf-8"))
        names = {
            alias.asname or alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
        }
        classes = {
            node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        }
        # The platform's validator requires a literal entry-point class, not
        # only an imported alias.  Keep this stricter than the runtime export
        # check so packaging catches that failure locally.
        self.assertIn("Player", classes)
        self.assertIn("Player", names | classes)

    def test_all_python_parses(self) -> None:
        for path in CANDIDATE.rglob("*.py"):
            with self.subTest(path=path):
                ast.parse(path.read_text(encoding="utf-8"))

    def test_no_native_extensions(self) -> None:
        bad = [
            p for p in CANDIDATE.rglob("*")
            if p.is_file() and p.suffix.lower() in FORBIDDEN_SUFFIXES
        ]
        self.assertEqual([], bad)

    def test_submission_limits(self) -> None:
        entries = [p for p in CANDIDATE.rglob("*") if p.is_file()]
        self.assertLessEqual(len(entries), 500)
        self.assertLessEqual(sum(p.stat().st_size for p in entries), 50 * 1024 * 1024)

    def test_no_direction_to_in_candidate_movement_helper(self) -> None:
        # Prevent the known tutorial trap; cardinal_direction_to is allowed.
        offenders = []
        for path in CANDIDATE.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            stripped = text.replace("cardinal_direction_to", "")
            if ".direction_to(" in stripped:
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual([], offenders)

    def test_candidate_has_only_pure_python_and_allowed_imports(self) -> None:
        allowed_roots = {"__future__", "collections", "collections.abc", "dataclasses", "enum", "math", "statistics", "time", "typing", "fcode", "bot"}
        for path in CANDIDATE.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertIn(alias.name.split(".")[0], allowed_roots, path)
                if isinstance(node, ast.ImportFrom) and node.level == 0:
                    self.assertIn((node.module or "").split(".")[0], allowed_roots, path)

    def test_no_map_names_or_old_turret_literals_in_policy(self) -> None:
        map_names = ("atoll", "aurora", "bridge", "crossfire", "duel", "fjord", "hive", "jackpot", "longship", "pinch", "quarry", "runestone", "showdown", "skerry", "sprint", "strait", "string", "sweden", "twins", "vase", "vault")
        text = "\n".join(path.read_text(encoding="utf-8").lower() for path in (CANDIDATE / "bot").glob("*.py"))
        for name in map_names:
            self.assertNotIn(f'"{name}"', text)
            self.assertNotIn(f"'{name}'", text)
        self.assertNotIn("gunner_damage = 10", text)
        self.assertNotIn("sentinel_damage = 10", text)

    def test_store_indices_and_production_budget(self) -> None:
        text = "\n".join(path.read_text(encoding="utf-8") for path in (CANDIDATE / "bot").glob("*.py"))
        for match in __import__("re").finditer(r"(?:read_store|write_store)\(\s*(\d+)", text):
            self.assertLess(int(match.group(1)), 16)
        count = 0
        for path in (CANDIDATE / "bot").glob("*.py"):
            count += sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#"))
        self.assertLessEqual(count, 1800)


if __name__ == "__main__":
    unittest.main()
