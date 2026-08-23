from __future__ import annotations

from pathlib import Path
import tomllib
import unittest

from scripts.common import stratified_map_seed_pairs, stratified_screen_side_swaps


class StratifiedScheduleTests(unittest.TestCase):
    def test_release_matrix_covers_all_configured_maps_and_sides(self) -> None:
        config_root = Path(__file__).parents[1] / "configs"
        config = tomllib.loads(
            (config_root / "eval_matrix.toml").read_text(encoding="utf-8")
        )

        self.assertEqual(15, len(config["maps"]))
        self.assertEqual([1, 101], config["seeds"])
        self.assertTrue(config["side_swap"])
        self.assertEqual(
            60,
            len(config["maps"])
            * len(config["seeds"])
            * (2 if config["side_swap"] else 1),
        )

    def test_fast_screen_covers_all_maps_with_small_stratified_schedule(self) -> None:
        config_root = Path(__file__).parents[1] / "configs"
        config = tomllib.loads(
            (config_root / "eval_regression.toml").read_text(encoding="utf-8")
        )

        self.assertEqual(15, config["screen_pairs"])
        self.assertEqual(15, config["screen_games"])
        self.assertTrue(config["side_swap"])
        self.assertGreaterEqual(config["screen_pairs"], len(config["maps"]))
        pairs = stratified_map_seed_pairs(
            config["maps"], config["seeds"], config["screen_pairs"], config["screen_seed"]
        )
        self.assertEqual(set(config["maps"]), {map_name for map_name, _ in pairs})
        side_swaps = stratified_screen_side_swaps(
            len(pairs), config["screen_games"], config["screen_seed"],
            side_swap=config["side_swap"],
        )
        self.assertEqual(0, len(side_swaps))
        self.assertEqual(15, len(pairs) + len(side_swaps))

    def test_schedule_covers_every_map_and_has_requested_pair_count(self) -> None:
        pairs = stratified_map_seed_pairs(
            ["antler", "midgard", "yulerune"], [1, 7, 19], 5, 153
        )

        self.assertEqual(5, len(pairs))
        self.assertEqual({"antler", "midgard", "yulerune"}, {m for m, _ in pairs})

    def test_seed_makes_schedule_reproducible_and_rotatable(self) -> None:
        maps = ["antler", "midgard", "yulerune"]
        seeds = [1, 7, 19]

        self.assertEqual(
            stratified_map_seed_pairs(maps, seeds, 5, 153),
            stratified_map_seed_pairs(maps, seeds, 5, 153),
        )
        self.assertNotEqual(
            stratified_map_seed_pairs(maps, seeds, 5, 153),
            stratified_map_seed_pairs(maps, seeds, 5, 154),
        )

    def test_pair_count_cannot_drop_map_coverage(self) -> None:
        with self.assertRaises(ValueError):
            stratified_map_seed_pairs(["antler", "midgard"], [1], 1, 153)
        with self.assertRaises(ValueError):
            stratified_map_seed_pairs(["antler"], [1], 2, 153)

    def test_screen_side_swap_count_is_seeded_and_bounded(self) -> None:
        first = stratified_screen_side_swaps(15, 16, 153, side_swap=True)
        self.assertEqual(first, stratified_screen_side_swaps(15, 16, 153, side_swap=True))
        self.assertNotEqual(first, stratified_screen_side_swaps(15, 16, 154, side_swap=True))
        with self.assertRaises(ValueError):
            stratified_screen_side_swaps(15, 14, 153, side_swap=True)
        with self.assertRaises(ValueError):
            stratified_screen_side_swaps(15, 18, 153, side_swap=False)


if __name__ == "__main__":
    unittest.main()
