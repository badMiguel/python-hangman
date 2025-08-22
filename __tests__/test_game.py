import unittest
from src.game import Game
from src.read_json import ReadJson
from src.assets import Assets


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        settings = ReadJson().get_settings("settings.json")
        if not settings:
            self.fail("ReadJson().get_settings() returned none")

        self.game = Game(settings, Assets(), ["big", "small"], ["big small"])

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
        self.game.letter_was_typed = {
            "b": False,
            "i": False,
            "g": False,
        }
        self.game.hidden = ["_", "_", "_"]
        self.game._letter_in_question("i")
        self.assertTrue(self.game.letter_was_typed["i"])
        self.assertEqual(self.game.hidden, ["_", "i", "_"])

    def test_letter_in_question_false(self) -> None:
        self.game.answer = "big"
        self.game.letter_was_typed = {
            "b": False,
            "i": False,
            "g": False,
        }
        initial_life = self.game.life
        self.game._letter_in_question("a")
        self.assertTrue(self.game.letter_was_typed["a"])
        self.assertEqual(self.game.life, initial_life - 1)

    def test_letter_in_question_false_empty(self) -> None:
        self.game.answer = "big"
        self.game._letter_in_question("")
        self.assertEqual(self.game.life, self.game.life)

    def test_game_over(self) -> None:
        self.game.answer = "big"
        self.game.letter_was_typed = {
            "b": False,
            "i": False,
            "g": False,
        }
        initial_life = self.game.life

        self.game._letter_in_question("d")
        self.assertTrue(self.game.letter_was_typed["d"])
        self.assertEqual(self.game.life, initial_life - 1)

        self.game._letter_in_question("")
        self.assertEqual(self.game.life, initial_life - 1)

        self.game._letter_in_question("l")
        self.assertEqual(self.game.life, initial_life - 2)

    def test_game_won_words(self) -> None:
        self.game.answer = "big"
        self.game.letter_was_typed = {
            "b": False,
            "i": False,
            "g": False,
        }
        self.game.hidden = ["_", "_", "_"]
        self.game.correct_counter = 0

        self.game._letter_in_question("i")
        self.assertTrue(self.game.letter_was_typed["i"])
        self.assertEqual(self.game.correct_counter, 1)
        self.assertEqual(self.game.hidden, ["_", "i", "_"])

        self.game._letter_in_question("g")
        self.assertTrue(self.game.letter_was_typed["g"])
        self.assertEqual(self.game.correct_counter, 2)
        self.assertEqual(self.game.hidden, ["_", "i", "g"])

        self.game._letter_in_question("b")
        self.assertTrue(self.game.letter_was_typed["b"])
        self.assertEqual(self.game.correct_counter, 3)
        self.assertEqual(self.game.hidden, ["b", "i", "g"])
        self.assertTrue(self.game.won)

    def test_game_won_phrases(self) -> None:
        self.game.answer = "big big"
        self.game.letter_was_typed = {
            "b": False,
            "i": False,
            "g": False,
        }
        self.game.hidden = ["_", "_", "_", "_", "_", "_", "_"]
        self.game.correct_counter = 1

        self.game._letter_in_question("i")
        self.assertTrue(self.game.letter_was_typed["i"])
        self.assertEqual(self.game.correct_counter, 3)
        self.assertEqual(self.game.hidden, ["_", "i", "_", "_", "_", "i", "_"])

        self.game._letter_in_question("g")
        self.assertTrue(self.game.letter_was_typed["g"])
        self.assertEqual(self.game.correct_counter, 5)
        self.assertEqual(self.game.hidden, ["_", "i", "g", "_", "_", "i", "g"])

        self.game._letter_in_question("b")
        self.assertTrue(self.game.letter_was_typed["b"])
        self.assertEqual(self.game.correct_counter, 7)
        self.assertEqual(self.game.hidden, ["b", "i", "g", "_", "b", "i", "g"])
        self.assertTrue(self.game.won)

    def test_reset_game(self) -> None:
        self.game.life = 2
        self.game.hidden = ["_"]
        self.game.answer = "hello"
        self.game.correct_counter = 2
        self.game.letter_was_typed["a"] = True
        self.game.won = True
        self.game.thread_counter = 9
        self.game.time_counter = 9
        self.game.skip_create_timer = True
        self.game.stop_event_thread.set()

        self.game._reset_game()
        self.assertEqual(self.game.life, 7)
        self.assertEqual(self.game.hidden, [])
        self.assertEqual(self.game.answer, "")
        self.assertEqual(self.game.correct_counter, 0)
        self.assertFalse(self.game.letter_was_typed["a"])
        self.assertFalse(self.game.won)
        self.assertEqual(self.game.thread_counter, 0)
        self.assertEqual(self.game.time_counter, int(self.game.settings["max_time"]))
        self.assertEqual(self.game.skip_create_timer, False)
        self.assertFalse(self.game.stop_event_thread.is_set())

    def test_count_repeated_letter(self) -> None:
        self.game.answer = "big"
        self.game.letter_was_typed = {
            "b": False,
            "i": False,
            "g": False,
        }
        self.game.hidden = ["_", "_", "_"]
        self.game._letter_in_question("i")
        self.game._letter_in_question("i")
        self.game._letter_in_question("i")
        self.assertTrue(self.game.letter_was_typed["i"])
        self.assertEqual(self.game.correct_counter, 1)

        self.game._reset_game()
        self.game.answer = "small"
        self.game.letter_was_typed = {
            "s": False,
            "m": False,
            "a": False,
            "l": False,
            "l": False,
        }
        self.game.hidden = ["_", "_", "_", "_", "_"]
        self.game._letter_in_question("l")
        self.game._letter_in_question("l")
        self.game._letter_in_question("l")
        self.game._letter_in_question("l")
        self.assertTrue(self.game.letter_was_typed["l"])
        self.assertEqual(self.game.correct_counter, 2)


if __name__ == "__main__":
    unittest.main()
