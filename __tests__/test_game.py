import unittest
from src.game import Game
from src.read_json import ReadJson


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        settings = ReadJson().get_settings("settings.json")
        if not settings:
            self.fail("ReadJson().get_settings() returned none")

        self.game = Game(
            settings, ["big", "small"], ["big small"]
        )

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

    def test_game_over(self) -> None:
        self.game.answer = "big"
        initial_life = self.game.life

        self.game._letter_in_question("d")
        self.assertEqual(self.game.life, initial_life - 1)

        self.game._letter_in_question("")
        self.assertEqual(self.game.life, initial_life - 2)

        self.game._letter_in_question("")
        self.assertEqual(self.game.life, initial_life - 3)

    def test_game_won(self) -> None:
        self.game.answer = "big"
        self.game.hidden = ["_", "_", "_"]
        self.game.correct_counter = 0

        self.game._letter_in_question("i")
        self.assertEqual(self.game.correct_counter, 1)
        self.assertEqual(self.game.hidden, ["_", "i", "_"])

        self.game._letter_in_question("g")
        self.assertEqual(self.game.correct_counter, 2)
        self.assertEqual(self.game.hidden, ["_", "i", "g"])

        self.game._letter_in_question("b")
        self.assertEqual(self.game.correct_counter, 3)
        self.assertEqual(self.game.hidden, ["b", "i", "g"])

    def test_reset_game(self) -> None:
        self.game.life = 2
        self.game.hidden = ["_"]
        self.game.answer = "hello"
        self.game.correct_counter = 2

        self.game._reset_game()
        self.assertEqual(self.game.life, 5)
        self.assertEqual(self.game.hidden, [])
        self.assertEqual(self.game.answer, "")
        self.assertEqual(self.game.correct_counter, 0)


if __name__ == "__main__":
    unittest.main()
