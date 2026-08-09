from __future__ import annotations

import unittest

from fcode import Position, Team

from bots.candidate.bot.core import _opening_position_key


class _Controller:
    def __init__(
        self,
        width: int,
        height: int,
        team: Team,
        origin: Position = Position(1, 1),
    ) -> None:
        self.width = width
        self.height = height
        self.team = team
        self.origin = origin

    def get_map_width(self) -> int:
        return self.width

    def get_map_height(self) -> int:
        return self.height

    def get_team(self) -> Team:
        return self.team

    def get_position(self) -> Position:
        return self.origin


class OpeningOrientationTests(unittest.TestCase):
    def test_weaker_side_rotates_to_team_b_orientation(self) -> None:
        point = Position(2, 3)
        self.assertEqual((14, 11), _opening_position_key(_Controller(14, 18, Team.A), point))
        self.assertEqual((3, 2), _opening_position_key(_Controller(14, 18, Team.B), point))

    def test_weaker_side_rotates_to_team_a_orientation(self) -> None:
        point = Position(2, 3)
        self.assertEqual((3, 2), _opening_position_key(_Controller(26, 26, Team.A), point))
        self.assertEqual((22, 23), _opening_position_key(_Controller(26, 26, Team.B), point))

    def test_ambiguous_geometry_preserves_baseline_order(self) -> None:
        point = Position(2, 3)
        for team in Team:
            self.assertEqual((3, 2), _opening_position_key(_Controller(28, 20, team), point))

    def test_same_size_cross_diagonal_geometry_uses_team_a_orientation(self) -> None:
        point = Position(2, 3)
        cross_corner = Position(2, 11)
        self.assertEqual(
            (3, 2),
            _opening_position_key(_Controller(16, 16, Team.A, cross_corner), point),
        )
        self.assertEqual(
            (12, 13),
            _opening_position_key(_Controller(16, 16, Team.B, Position(13, 3)), point),
        )

    def test_same_size_same_quadrant_geometry_uses_team_b_orientation(self) -> None:
        point = Position(2, 3)
        self.assertEqual(
            (12, 13),
            _opening_position_key(_Controller(16, 16, Team.A, Position(3, 3)), point),
        )
        self.assertEqual(
            (3, 2),
            _opening_position_key(_Controller(16, 16, Team.B, Position(11, 11)), point),
        )

    def test_25_square_cross_diagonal_preserves_baseline_order(self) -> None:
        point = Position(2, 3)
        for team, origin in ((Team.A, Position(2, 20)), (Team.B, Position(21, 3))):
            self.assertEqual(
                (3, 2),
                _opening_position_key(_Controller(25, 25, team, origin), point),
            )

    def test_25_square_same_quadrant_uses_team_a_orientation(self) -> None:
        point = Position(2, 3)
        self.assertEqual(
            (3, 2),
            _opening_position_key(_Controller(25, 25, Team.A, Position(5, 5)), point),
        )
        self.assertEqual(
            (21, 22),
            _opening_position_key(_Controller(25, 25, Team.B, Position(19, 19)), point),
        )


if __name__ == "__main__":
    unittest.main()
