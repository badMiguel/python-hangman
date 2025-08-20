import unittest
from src.game import Game


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game(["big", "small"], ["big small"])

    def test_menu_select_basic(self) -> None:
        self.assertEqual(self.game._game_menu_helper("1"), "basic")

    def test_menu_select_intermediate(self) -> None:
        self.assertEqual(self.game._game_menu_helper("2"), "intermediate")

    def test_menu_select_none(self) -> None:
        self.assertEqual(self.game._game_menu_helper(""), None)

    def test_get_question_basic(self) -> None:
        self.game._get_question("basic")
        self.assertIn(self.game.answer, self.game.word_list)
        if self.game.answer == "big":
            self.assertEqual(self.game.hidden, ["_", "_", "_"])
        else:
            self.assertEqual(self.game.hidden, ["_", "_", "_", "_", "_"])

    def test_get_question_intermediate(self) -> None:
        self.game._get_question("intermediate")
        self.assertIn(self.game.answer, self.game.phrase_list)
        self.assertEqual(
            self.game.hidden, ["_", "_", "_", " ", "_", "_", "_", "_", "_"]
        )

    def test_letter_in_question_true(self) -> None:
        self.game.answer = "big"
        self.game.hidden = ["_", "_", "_"]
        self.game._letter_in_question("i")
        self.assertEqual(self.game.hidden, ["_", "i", "_"])

    def test_letter_in_question_false(self) -> None:
        self.game.answer = "big"
        initial_life = self.game.life
        self.game._letter_in_question("a")
        self.assertEqual(self.game.life, initial_life - 1)

    def test_letter_in_question_false_empty(self) -> None:
        self.game.answer = "big"
        initial_life = self.game.life
        self.game._letter_in_question("")
        self.assertEqual(self.game.life, initial_life - 1)

    def test_reset_game(self) -> None:
        self.game.life = 2
        self.game.hidden = ["_"]
        self.game.answer = "hello"
        self.game._reset_game()
        self.assertEqual(self.game.life, 5)
        self.assertEqual(self.game.hidden, [])
        self.assertEqual(self.game.answer, "")

if __name__ == "__main__":
    unittest.main()
