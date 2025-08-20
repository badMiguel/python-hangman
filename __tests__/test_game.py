import unittest
from src.game import Game


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game(["big", "small"], ["big small"])

    def test_menu_select_basic(self) -> None:
        self.assertEqual(self.game._game_menu_helper("1"), "Basic level")

    def test_menu_select_intermediate(self) -> None:
        self.assertEqual(self.game._game_menu_helper("2"), "Intermediate level")

    def test_menu_select_quit(self) -> None:
        self.assertEqual(self.game._game_menu_helper("3"), "Quit")

    def test_menu_select_error(self) -> None:
        self.assertEqual(self.game._game_menu_helper("4"), "Try again")


if __name__ == "__main__":
    unittest.main()
