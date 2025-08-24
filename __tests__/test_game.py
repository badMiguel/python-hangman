import unittest
from src.game import Game, Data, LetterTracker
from src.read_json import ReadJson
from src.assets import Assets


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        settings = ReadJson().get_settings("settings.json")
        if not settings:
            self.fail("ReadJson().get_settings() returned none")

        word_list = ["big", "small"]
        phrase_list = ["big small"]
        self.game = Game(settings, Assets(), ["big", "small"], ["big small"])
        self.data = Data(word_list, phrase_list)
        self.tracker = LetterTracker()

    def test_menu_select_basic(self) -> None:
        self.assertEqual(self.game.game_menu_helper("1"), "basic")

    def test_menu_select_intermediate(self) -> None:
        self.assertEqual(self.game.game_menu_helper("2"), "intermediate")

    def test_menu_select_none(self) -> None:
        self.assertEqual(self.game.game_menu_helper(""), None)

    def test_get_question_basic(self) -> None:
        self.game.get_question("basic")
        self.assertIn(self.game.state["answer"], self.data.word_list)
        if self.game.state["answer"] == "big":
            self.assertEqual(self.game.state["hidden"], ["_", "_", "_"])
        else:
            self.assertEqual(self.game.state["hidden"], ["_", "_", "_", "_", "_"])

    def test_get_question_intermediate(self) -> None:
        self.game.get_question("intermediate")
        self.assertIn(self.game.state["answer"], self.data.phrase_list)
        self.assertEqual(
            self.game.state["hidden"], ["_", "_", "_", " ", "_", "_", "_", "_", "_"]
        )

    def test_letter_in_question_true(self) -> None:
        self.game.state["answer"] = "big"
        self.tracker.initialise()
        self.game.state["hidden"] = ["_", "_", "_"]
        self.game.letter_in_question("i")
        self.assertTrue(self.game.tracker.is_typed("i"))
        self.assertEqual(self.game.state["hidden"], ["_", "i", "_"])

    def test_letter_in_question_false(self) -> None:
        self.game.state["answer"] = "big"
        self.tracker.initialise()
        initial_life = self.game.state["life"]
        self.game.letter_in_question("a")
        self.assertTrue(self.game.tracker.is_typed("a"))
        self.assertEqual(self.game.state["life"], initial_life - 1)

    def test_letter_in_question_false_empty(self) -> None:
        self.game.state["answer"] = "big"
        self.game.letter_in_question("")
        self.assertEqual(self.game.state["life"], self.game.state["life"])

    def test_game_over(self) -> None:
        self.game.state["answer"] = "big"
        self.tracker.initialise()
        initial_life = self.game.state["life"]

        self.game.letter_in_question("d")
        self.assertTrue(self.game.tracker.is_typed("d"))
        self.assertEqual(self.game.state["life"], initial_life - 1)

        self.game.letter_in_question("")
        self.assertEqual(self.game.state["life"], initial_life - 1)

        self.game.letter_in_question("l")
        self.assertEqual(self.game.state["life"], initial_life - 2)

    def test_game_won_words(self) -> None:
        self.game.state["answer"] = "big"
        self.tracker.initialise()
        self.game.state["hidden"] = ["_", "_", "_"]
        self.game.state["correct_counter"] = 0

        self.game.letter_in_question("i")
        self.assertTrue(self.game.tracker.is_typed("i"))
        self.assertEqual(self.game.state["correct_counter"], 1)
        self.assertEqual(self.game.state["hidden"], ["_", "i", "_"])

        self.game.letter_in_question("g")
        self.assertTrue(self.game.tracker.is_typed("g"))
        self.assertEqual(self.game.state["correct_counter"], 2)
        self.assertEqual(self.game.state["hidden"], ["_", "i", "g"])

        self.game.letter_in_question("b")
        self.assertTrue(self.game.tracker.is_typed("b"))
        self.assertEqual(self.game.state["correct_counter"], 3)
        self.assertEqual(self.game.state["hidden"], ["b", "i", "g"])
        self.assertTrue(self.game.state["won"])

    def test_game_won_phrases(self) -> None:
        self.game.state["answer"] = "big big"
        self.tracker.initialise()
        self.game.state["hidden"] = ["_", "_", "_", "_", "_", "_", "_"]
        self.game.state["correct_counter"] = 1

        self.game.letter_in_question("i")
        self.assertTrue(self.game.tracker.is_typed("i"))
        self.assertEqual(self.game.state["correct_counter"], 3)
        self.assertEqual(self.game.state["hidden"], ["_", "i", "_", "_", "_", "i", "_"])

        self.game.letter_in_question("g")
        self.assertTrue(self.game.tracker.is_typed("g"))
        self.assertEqual(self.game.state["correct_counter"], 5)
        self.assertEqual(self.game.state["hidden"], ["_", "i", "g", "_", "_", "i", "g"])

        self.game.letter_in_question("b")
        self.assertTrue(self.game.tracker.is_typed("b"))
        self.assertEqual(self.game.state["correct_counter"], 7)
        self.assertEqual(self.game.state["hidden"], ["b", "i", "g", "_", "b", "i", "g"])
        self.assertTrue(self.game.state["won"])

    def test_reset_game(self) -> None:
        self.game.state["life"] = 2
        self.game.state["hidden"] = ["_"]
        self.game.state["answer"] = "hello"
        self.game.state["correct_counter"] = 2
        self.game.tracker.mark_typed("a")
        self.game.state["won"] = True
        self.game.thread_counter = 9
        self.game.time_counter = 9
        self.game.skip_create_timer = True
        self.game.stop_event_thread.set()

        self.game.reset_game()
        self.assertEqual(self.game.state["life"], 7)
        self.assertEqual(self.game.state["hidden"], [])
        self.assertEqual(self.game.state["answer"], "")
        self.assertEqual(self.game.state["correct_counter"], 0)
        self.assertFalse(self.game.tracker.is_typed("a"))
        self.assertFalse(self.game.state["won"])
        self.assertEqual(self.game.thread_counter, 0)
        self.assertEqual(self.game.time_counter, int(self.game.settings["max_time"]))
        self.assertEqual(self.game.skip_create_timer, False)
        self.assertFalse(self.game.stop_event_thread.is_set())

    def test_count_repeated_letter(self) -> None:
        self.game.state["answer"] = "big"
        self.tracker.initialise()
        self.game.state["hidden"] = ["_", "_", "_"]
        self.game.letter_in_question("i")
        self.game.letter_in_question("i")
        self.game.letter_in_question("i")
        self.assertTrue(self.game.tracker.is_typed("i"))
        self.assertEqual(self.game.state["correct_counter"], 1)

        self.game.reset_game()
        self.game.state["answer"] = "small"
        self.game.state["hidden"] = ["_", "_", "_", "_", "_"]
        self.game.letter_in_question("l")
        self.game.letter_in_question("l")
        self.game.letter_in_question("l")
        self.game.letter_in_question("l")
        self.assertTrue(self.game.tracker.is_typed("l"))
        self.assertEqual(self.game.state["correct_counter"], 2)

    def test_timer_finished(self) -> None:
        self.game.state["life"] = 1
        self.game.timer_finished_thread(0)
        self.assertEqual(self.game.state["life"], 0)
        self.assertTrue(self.game.stop_event_thread.is_set())


if __name__ == "__main__":
    unittest.main()
