import unittest
from src.game import Game


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game(["big", "small"], ["big small"])

    def test_menu_select_basic(self) -> None:
        self.assertEqual(self.game._game_menu_helper("1"), "basic")

    def test_menu_select_intermediate(self) -> None:
        self.assertEqual(self.game._game_menu_helper("2"), "intermediate")

    def test_get_question_basic(self) -> None:
        self.assertIn(self.game._get_question("basic"), self.game.word_list)

    def test_get_question_intermediate(self) -> None:
        self.assertIn(self.game._get_question("intermediate"), self.game.phrase_list)

    def test_letter_in_question_true(self) -> None:
        self.game.hidden = ["_", "_", "_"]
        self.game._letter_in_question("big", "i")
        self.assertEqual(self.game.hidden, ["_", "i", "_"])

    def test_letter_in_question_false(self) -> None:
        initial_life = self.game.life
        self.game._letter_in_question("big", "a")
        self.assertEqual(self.game.life, initial_life - 1)


if __name__ == "__main__":
    unittest.main()
