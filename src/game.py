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


class Game:
    def __init__(
        self,
        settings: dict[str, str],
        assets,
        word_list: list[str],
        phrase_list: list[str],
    ) -> None:
        self.data = Data(word_list, phrase_list)
        self.settings = settings
        self.life = int(self.settings["start_life"])

        self.hidden: list[str] = []
        self.answer = ""
        self.correct_counter = 0
        self.won = False
        self.letter_was_typed: dict[str, bool] = {}
        self.letter_list: list[str] = []

        self.start_timer_thread: threading.Timer | None = None
        self.stop_event_thread: threading.Event = threading.Event()
        self.time_counter = int(self.settings["max_time"])
        self.timer_is_stopped: dict[int, bool] = {}
        self.thread_counter = 0
        self.skip_create_timer = False
        self.lock = threading.Lock()

        self.assets = assets

    def _center_text_helper(self, width: int, text: str) -> str:
        return text.center(width)

    def _get_terminal_width(self) -> int:
        return self.terminal.columns

    def _get_terminal_height(self) -> int:
        return self.terminal.lines

    def _clear_screen(self) -> None:
        os.system("clear" if os.name == "posix" else "cls")

    def game_menu(self) -> None:
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
        choice = input(
            " "
            * (self._get_terminal_width() // 2 - int(self.settings["menu_width"]) // 2)
            + "-> "
        )

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
        self._get_terminal_size()
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
        print(f"\033[{self._get_terminal_height()//2 - len(menu_text) //2};1H", end="")
        for line in menu_text:
            print(self._center_text_helper(self._get_terminal_width(), line))

    def _get_terminal_size(self) -> None:
        self.terminal = shutil.get_terminal_size()

    def game_menu_helper(self, choice: str) -> str | None:
        if choice == "1":
            return "basic"

        if choice == "2":
            return "intermediate"

        return None

    def start_game(self, level: str) -> None:
        self.get_question(level)
        self._create_letter_was_typed()

        while (
            not self.stop_event_thread.is_set()
            and self.life > 0
            and self.correct_counter < len(self.answer)
        ):
            self._print_question()

            if not self.skip_create_timer:
                self.create_timer()
                with self.lock:
                    self.skip_create_timer = True

            len_letter_list = len(self.letter_list)
            portion = len_letter_list // 3
            # *2-1 because of the additional space added when printing
            width = len(self.letter_list[portion : len_letter_list - portion]) * 2 - 1

            letter_input = input(
                "\n" + " " * (self._get_terminal_width() // 2 - width // 2) + "-> "
            ).lower()

            self.letter_in_question(letter_input)
            if letter_input == "":
                with self.lock:
                    self.skip_create_timer = True
                continue

            if not self.skip_create_timer:
                self.reset_timer(self.thread_counter - 1)

            self._clear_screen()

        if not self.stop_event_thread.is_set():
            if self.start_timer_thread:
                self.start_timer_thread.cancel()
            self.game_end_menu()
            _ = input("")

        self.reset_game()
        self._clear_screen()

    def _create_letter_was_typed(self) -> None:
        letter_list: list[str] = []

        letters = string.ascii_lowercase
        for letter in letters:
            letter_list.append(letter)
            self.letter_was_typed[letter] = False

        self.letter_list = letter_list

    def _print_question(self) -> None:
        self._get_terminal_size()

        gallows = self.assets.get_gallows(self.life)

        print(
            f"\033[{self._get_terminal_height()//2 - (len(gallows)+6)//2};1H",
            end="",
        )

        for line in gallows:
            print(self._center_text_helper(self._get_terminal_width(), line))

        print()
        print(
            self._center_text_helper(self._get_terminal_width(), " ".join(self.hidden))
        )

        len_letter_list = len(self.letter_list)
        portion = len_letter_list // 3
        list_of_letter_list = [
            # a-h
            self.letter_list[:portion],
            # i-r
            self.letter_list[portion : len_letter_list - portion],
            # s-z
            self.letter_list[len_letter_list - portion : len_letter_list],
        ]

        for letter_list in list_of_letter_list:
            print(f"\n\033[{self._get_terminal_width()//2-len(letter_list)+1}C", end="")
            for char in letter_list:
                if self.letter_was_typed[char]:
                    if char in self.answer:
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
        self.life = int(self.settings["start_life"])
        self.hidden = []
        self.answer = ""
        self.correct_counter = 0
        self._create_letter_was_typed()
        self.won = False
        self.thread_counter = 0
        self.time_counter = int(self.settings["max_time"])
        self.skip_create_timer = False
        self.stop_event_thread.clear()

    def get_question(self, level: str) -> None:
        if level == "basic":
            self.answer = self.data.get_random_word()
        else:
            self.answer = self.data.get_random_phrase()

        for letter in self.answer:
            if letter == " ":
                self.hidden.append(" ")
                self.correct_counter += 1
            else:
                self.hidden.append("_")

    def letter_in_question(self, letter_input: str) -> None:
        if (
            letter_input in list(self.letter_was_typed.keys())
            and self.letter_was_typed[letter_input]
        ):
            return

        self.letter_was_typed[letter_input] = True
        if letter_input not in self.answer:
            self.life -= 1
            with self.lock:
                self.skip_create_timer = False
            return

        if letter_input in self.hidden:
            return

        with self.lock:
            self.skip_create_timer = False
        for idx, char in enumerate(self.answer):
            if self.answer[idx] == letter_input:
                self.hidden[idx] = char
                self.correct_counter += 1

            if self.correct_counter >= len(self.answer):
                self.won = True

    def reset_timer(self, idx: int) -> None:
        if self.start_timer_thread:
            self.start_timer_thread.cancel()
        self.time_counter = int(self.settings["max_time"])
        with self.lock:
            self.timer_is_stopped[idx] = True

    def create_timer(self) -> None:
        # creates new thread for timer to avoid blocking whole program
        self.start_timer_thread = threading.Timer(
            int(self.settings["max_time"]),
            self.timer_finished_thread,
            args=(self.thread_counter,),
        )
        timer_display_thread = threading.Thread(
            target=self._timer_display, args=(self.thread_counter,)
        )
        timer_countdown_thread = threading.Thread(
            target=self._timer_countdown, args=(self.thread_counter,)
        )

        with self.lock:
            self.timer_is_stopped[self.thread_counter] = False

        self.start_timer_thread.start()
        timer_display_thread.start()
        timer_countdown_thread.start()

        self.thread_counter += 1

    def timer_finished_thread(self, idx: int) -> None:
        with self.lock:
            self.timer_is_stopped[idx] = True
        with self.lock:
            self.skip_create_timer = False
        self.life -= 1
        if self.life <= 0:
            self.game_end_menu()
            self.stop_event_thread.set()
            return

        print("\033[s", end="")
        self._print_question()
        print("\033[u", end="", flush=True)
        self.reset_timer(self.thread_counter - 1)
        self.create_timer()

    def _timer_countdown(self, idx: int) -> None:
        time.sleep(1)
        while self.time_counter > 0 and not self.timer_is_stopped[idx]:
            with self.lock:
                self.time_counter -= 1
            time.sleep(1)

    def _timer_display(self, idx: int) -> None:
        time.sleep(0.01)
        previous_time = -1
        while self.time_counter > 0 and not self.timer_is_stopped[idx]:
            if previous_time == self.time_counter:
                time.sleep(0.05)
                continue

            previous_time = self.time_counter
            print("\033[s", end="")
            print("\033[1;1H", end="")
            print("\033[K", end="")
            print("Time left: ", end="")
            if self.time_counter <= 5:
                print("\033[31m", end="")
            print(self.time_counter)
            print("\033[39m", end="")
            print("\033[u", end="", flush=True)
            time.sleep(0.05)

    def game_end_menu(self) -> None:
        self._clear_screen()

        self._get_terminal_size()

        print(
            f"\033[{
                self._get_terminal_height()//2 - len(self.assets.get_gallows(0))//2
            };1H",
            end="",
        )

        if self.won:
            text = "Congratulations!"
            print("\033[32m\033[1m", end="")
            print(f"\n\033[{self._get_terminal_width()//2 - len(text)//2}C", end="")
            print(text)
            print("\033[39m\033[0m", end="")
            end_text: list[str] = [
                "",
                self.assets.get_emoticon(self.won),
                "",
                "Answer: " + self.answer,
                "",
                "That was good! Feel free to play again",
                "",
            ]
        else:
            text = "Game Over!"
            print("\033[31m\033[1m", end="")
            print(f"\n\033[{self._get_terminal_width()//2 - len(text)//2}C", end="")
            print(text)
            print("\033[39m\033[0m", end="")
            end_text: list[str] = [
                "",
                self.assets.get_emoticon(self.won),
                "",
                "Answer: " + self.answer,
                "",
                "It's ok! You can try again.",
                "",
            ]

        for line in end_text:
            print(self._center_text_helper(self._get_terminal_width(), line))

        text = "Press 'enter' to exit."
        print(f"\n\033[{self._get_terminal_width()//2 - len(text)//2}C", end="")
        print("\033[3m\033[2m", end="")
        print(text, end="")
        print("\033[0m\033[0m", end="")
        print(f"\n\033[{self._get_terminal_width()//2}C", end="")
