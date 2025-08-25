"""Core game logic for the Hangman game.

This module implements the `Game` class which controls the game state, question
selection, input processing, timer management, and screen rendering (terminal).

"""

import random
import shutil
import os
import threading
import time
import string


class Data:
    """Holds word/phrase data and provides accessors."""

    def __init__(self, word_list: list[str], phrase_list: list[str]) -> None:
        self.word_list = word_list
        self.phrase_list = phrase_list

    def get_random_word(self) -> str:
        """Return a random word from the list."""
        return random.choice(self.word_list)

    def get_random_phrase(self) -> str:
        """Return a random phrase from the list."""
        return random.choice(self.phrase_list)


class LetterTracker:
    """Tracks letter typed and letter list"""

    def __init__(self) -> None:
        self.letter_was_typed: dict[str, bool] = {}
        self.letter_list: list[str] = []
        self._initialise()

    def _initialise(self) -> None:
        for letter in string.ascii_lowercase:
            self.letter_list.append(letter)
            self.letter_was_typed[letter] = False

    def mark_typed(self, letter: str) -> None:
        """Mark a letter as typed"""
        self.letter_was_typed[letter] = True

    def is_typed(self, letter: str) -> bool:
        """Returns `True` if `letter` was typed before"""
        return self.letter_was_typed[letter]

    def reset_is_typed(self) -> None:
        """Resets `letter_was_typed` to all `False`"""
        for letter in self.letter_was_typed:
            self.letter_was_typed[letter] = False


class Game:
    """Main game controller for Hangman

    The class encapsulates various game state including word/phrase lists,
    current answer and hidden representation, life count, timer threads, and
    UI assets. Uses `game_menu` and `start_game` to for the game loop.
    """

    def __init__(
        self,
        settings: dict[str, str],
        assets,
        word_list: list[str],
        phrase_list: list[str],
    ) -> None:
        self.data = Data(word_list, phrase_list)
        self.settings = settings
        self.assets = assets
        self.state = {
            "life": int(self.settings["start_life"]),
            "hidden": [],
            "answer": "",
            "correct_counter": 0,
            "won": False,
        }
        self.tracker = LetterTracker()
        self.timer = {
            "start_timer_thread": None,
            "stop_event_thread": threading.Event(),
            "time_counter": int(self.settings["max_time"]),
            "timer_is_stopped": {},
            "thread_counter": 0,
            "skip_create_timer": False,
            "lock": threading.Lock(),
        }

    def _center_text_helper(self, width: int, text: str) -> str:
        return text.center(width)

    def _get_terminal_width(self) -> int:
        return shutil.get_terminal_size().columns

    def _get_terminal_height(self) -> int:
        return shutil.get_terminal_size().lines

    def _clear_screen(self) -> None:
        os.system("clear" if os.name == "posix" else "cls")

    def game_menu(self) -> None:
        """Displays the main menu and handle menu selection.

        This method prints informational notice, waits for user to continue,
        render out the menu options, and handles user input/action. Loop
        continues until user exits.
        """
        self._clear_screen()
        print(
            "Important:\n"
            "The game uses ANSI escape codes. Please ensure your device\n"
            "supports and maximise your terminal window for best\n"
            "experience. Modern Windows or VS Code's terminal should\n"
            "support ANSE escape sequence.\n\nThank you!\n"
        )
        _ = input("Press enter to continue.")

        self._clear_screen()
        self._display_menu()
        choice = input(" " * (self._get_terminal_width() // 2 - int(
            self.settings["menu_width"]) // 2) + "-> ")

        while choice != "3":
            self._clear_screen()

            action = self.game_menu_helper(choice)
            if action is None:
                pass
            else:
                self.start_game(action)

            self._display_menu()
            choice = input(
                " "
                * (
                    self._get_terminal_width() // 2
                    - int(self.settings["menu_width"]) // 2
                )
                + "-> "
            )

        self._clear_screen()

    def _display_menu(self) -> None:
        menu_text = [
            "",
            "*-----------------------------------*",
            "|                                   |",
            "|      Welcome to Hangman Game      |",
            "|                                   |",
            "*-----------------------------------*",
            "",
            "Select the number on the menu:",
            "------------------------------",
            "1. Basic",
            "2. Intermediate",
            "3. Quit",
            "",
        ]

        # move the curson to center the menu
        print(
            f"\033[{
                self._get_terminal_height() // 2 - len(menu_text) // 2
            };1H",
            end="",
        )
        for line in menu_text:
            print(self._center_text_helper(self._get_terminal_width(), line))

    def game_menu_helper(self, choice: str) -> str | None:
        """
        Helper function that returns either `basic` or `intermediate`
        depending on user input.
        """
        if choice == "1":
            return "basic"

        if choice == "2":
            return "intermediate"

        return None

    def start_game(self, level: str) -> None:
        """Run the main game loop for a single session

        Parameters:
            - level : str
                Difficulty level, selects word or phrase list
        """
        self.get_question(level)

        while (
            not self.timer["stop_event_thread"].is_set()
            and self.state["life"] > 0
            and self.state["correct_counter"] < len(self.state["answer"])
        ):
            self._clear_screen()
            self._print_question()

            if not self.timer["skip_create_timer"]:
                self._create_timer()
                with self.timer["lock"]:
                    self.timer["skip_create_timer"] = True

            len_list = len(self.tracker.letter_list)
            portion = len_list // 3
            # *2-1 because of the additional space added when printing
            width = len(
                self.tracker.letter_list[portion:len_list - portion]
            ) * 2 - 1
            letter_input = input(
                "\n" + " " * (
                    self._get_terminal_width() // 2 - width // 2
                ) + "-> "
            ).lower()

            self.letter_in_question(letter_input)
            if letter_input == "":
                with self.timer["lock"]:
                    self.timer["skip_create_timer"] = True
                continue

            if not self.timer["skip_create_timer"]:
                self._reset_timer(self.timer["thread_counter"] - 1)

        if not self.timer["stop_event_thread"].is_set():
            if self.timer["start_timer_thread"]:
                self.timer["start_timer_thread"].cancel()
            self._game_end_menu()
            _ = input("")

        self.reset_game()
        self._clear_screen()

    def _print_question(self) -> None:
        gallows = self.assets.get_gallows(self.state["life"])

        print(
            f"\033[{self._get_terminal_height()//2 - (len(gallows)+6)//2};1H",
            end="",
        )

        for line in gallows:
            print(self._center_text_helper(self._get_terminal_width(), line))

        print()
        print(
            self._center_text_helper(
                self._get_terminal_width(), " ".join(self.state["hidden"])
            )
        )

        len_letter_list = len(self.tracker.letter_list)
        portion = len_letter_list // 3
        list_of_letter_list = [
            # a-h
            self.tracker.letter_list[:portion],
            # i-r
            self.tracker.letter_list[portion:len_letter_list-portion],
            # s-z
            self.tracker.letter_list[len_letter_list-portion:len_letter_list],
        ]

        for letter_list in list_of_letter_list:
            print(
                f"\n\033[{
                    self._get_terminal_width()//2-len(letter_list)+1
                }C", end=""
            )
            for char in letter_list:
                if self.tracker.is_typed(char):
                    if char in self.state["answer"]:
                        print("\033[32m", end="")
                        print(char, end=" ")
                    else:
                        print("\033[31m", end="")
                        print(char, end=" ")

                    print("\033[39m", end="")
                    continue
                print(char, end=" ")

        print()

    def reset_game(self) -> None:
        """Resets game state, tracker, and timer to their initial values"""
        self.state["life"] = int(self.settings["start_life"])
        self.state["hidden"] = []
        self.state["answer"] = ""
        self.state["correct_counter"] = 0
        self.tracker.reset_is_typed()
        self.state["won"] = False
        self.timer["thread_counter"] = 0
        self.timer["time_counter"] = int(self.settings["max_time"])
        self.timer["skip_create_timer"] = False
        self.timer["stop_event_thread"].clear()

    def get_question(self, level: str) -> None:
        """Fetch a random word or phrase and set up the hidden puzzle

        Parameters:
            - level : str
                Difficulty level based on what user selects from menu
        """
        if level == "basic":
            self.state["answer"] = self.data.get_random_word()
        else:
            self.state["answer"] = self.data.get_random_phrase()

        for letter in self.state["answer"]:
            if letter == " ":
                self.state["hidden"].append(" ")
                self.state["correct_counter"] += 1
            else:
                self.state["hidden"].append("_")

    def letter_in_question(self, letter_input: str) -> None:
        """Process a guessed letter and update state, life, and counters

        Parameters:
            - letter_input : str
                Guessed user input
        """
        if (
            letter_input in self.tracker.letter_was_typed
            and self.tracker.is_typed(letter_input)
        ):
            return

        self.tracker.mark_typed(letter_input)
        if letter_input not in self.state["answer"]:
            self.state["life"] -= 1
            with self.timer["lock"]:
                self.timer["skip_create_timer"] = False
            return

        if letter_input in self.state["hidden"]:
            return

        with self.timer["lock"]:
            self.timer["skip_create_timer"] = False
        for idx, char in enumerate(self.state["answer"]):
            if self.state["answer"][idx] == letter_input:
                self.state["hidden"][idx] = char
                self.state["correct_counter"] += 1

            if self.state["correct_counter"] >= len(self.state["answer"]):
                self.state["won"] = True

    def _reset_timer(self, idx: int) -> None:
        if self.timer["start_timer_thread"]:
            self.timer["start_timer_thread"].cancel()
        self.timer["time_counter"] = int(self.settings["max_time"])
        with self.timer["lock"]:
            self.timer["timer_is_stopped"][idx] = True

    def _create_timer(self) -> None:
        # creates new thread for timer to avoid blocking whole program
        self.timer["start_timer_thread"] = threading.Timer(
            int(self.settings["max_time"]),
            self.timer_finished_thread,
            args=(self.timer["thread_counter"],),
        )
        timer_display_thread = threading.Thread(
            target=self._timer_display, args=(self.timer["thread_counter"],)
        )
        timer_countdown_thread = threading.Thread(
            target=self._timer_countdown, args=(self.timer["thread_counter"],)
        )

        thread_counter = self.timer["thread_counter"]
        with self.timer["lock"]:
            self.timer["timer_is_stopped"][thread_counter] = False

        self.timer["start_timer_thread"].start()
        timer_display_thread.start()
        timer_countdown_thread.start()

        self.timer["thread_counter"] += 1

    def timer_finished_thread(self, idx: int) -> None:
        """Handle end of timer - lose life, restart, or end game

        Parameter:
            - idx : int
                Identifier for `timer_is_stopped`
        """
        with self.timer["lock"]:
            self.timer["timer_is_stopped"][idx] = True
        with self.timer["lock"]:
            self.timer["skip_create_timer"] = False
        self.state["life"] -= 1
        if self.state["life"] <= 0:
            self._game_end_menu()
            self.timer["stop_event_thread"].set()
            return

        print("\033[s", end="")
        self._print_question()
        print("\033[u", end="", flush=True)
        self._reset_timer(self.timer["thread_counter"] - 1)
        self._create_timer()

    def _timer_countdown(self, idx: int) -> None:
        time.sleep(1)
        while (
            self.timer["time_counter"] > 0
            and not self.timer["timer_is_stopped"][idx]
        ):
            with self.timer["lock"]:
                self.timer["time_counter"] -= 1
            time.sleep(1)

    def _timer_display(self, idx: int) -> None:
        # Note:
        # The timer is re-rendered whether the time has changed or not from
        # the previous time because whole screen clears on any user input.
        # However, the timer does not reset when:
        #     1. User input == ""
        #     2. User input was already typed
        # Thus, in these two cases, the timer will not render immediately. A
        # better logic can be made, but with time limitation, this solution is
        # kept for now.
        time.sleep(0.01)
        while (
            self.timer["time_counter"] > 0
            and not self.timer["timer_is_stopped"][idx]
        ):
            print("\033[s", end="")
            print("\033[1;1H", end="")
            print("\033[K", end="")
            print("Time left: ", end="")
            if self.timer["time_counter"] <= 5:
                print("\033[31m", end="")
            print(self.timer["time_counter"])
            print("\033[39m", end="")
            print("\033[u", end="", flush=True)
            time.sleep(0.05)

    def _game_end_menu(self) -> None:
        self._clear_screen()

        print(
            f"\033[{
                self._get_terminal_height() // 2 -
                len(self.assets.get_gallows(0)) // 2
            };1H",
            end="",
        )

        if self.state["won"]:
            text = "Congratulations!"
            print("\033[32m\033[1m", end="")
            print(
                f"\n\033[{
                    self._get_terminal_width() // 2 - len(text) // 2
                }C",
                end="",
            )
            print(text)
            print("\033[39m\033[0m", end="")
            end_text: list[str] = [
                "",
                self.assets.get_emoticon(self.state["won"]),
                "",
                "Answer: " + self.state["answer"],
                "",
                "That was good! Feel free to play again",
                "",
            ]
        else:
            text = "Game Over!"
            print("\033[31m\033[1m", end="")
            print(
                f"\n\033[{self._get_terminal_width() // 2 - len(text) // 2}C",
                end="",
            )
            print(text)
            print("\033[39m\033[0m", end="")
            end_text: list[str] = [
                "",
                self.assets.get_emoticon(self.state["won"]),
                "",
                "Answer: " + self.state["answer"],
                "",
                "It's ok! You can try again.",
                "",
            ]

        for line in end_text:
            print(self._center_text_helper(self._get_terminal_width(), line))

        text = "Press 'enter' to exit."
        print(
            f"\n\033[{
                self._get_terminal_width() // 2 - len(text) // 2
            }C",
            end="",
        )
        print("\033[3m\033[2m", end="")
        print(text, end="")
        print("\033[0m\033[0m", end="")
        print(f"\n\033[{self._get_terminal_width()//2}C", end="")
