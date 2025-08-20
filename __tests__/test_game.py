import unittest
from src.game import Game


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game(["big", "small"], ["big small"])

    def test_menu_select_basic(self) -> None:
        self.assertEqual(self.game._game_menu_helper("1"), "basic")

    def test_menu_select_intermediate(self) -> None:
        self.assertEqual(self.game._game_menu_helper("2"), "intermediate")


if __name__ == "__main__":
    unittest.main()
