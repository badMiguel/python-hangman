import random
import shutil
import os, platform
import threading, time


class Game:
    def __init__(
        self,
        settings: dict[str, str],
        asset_list,
        word_list: list[str],
        phrase_list: list[str],
    ) -> None:
        self.word_list = word_list
        self.phrase_list = phrase_list
        self.settings = settings
        self.life = int(self.settings["start_life"])
        self.clear_type: str = "clear" if platform.system() == "Linux" else "cls"

        self.terminal_width = shutil.get_terminal_size().columns
        self.terminal_height = shutil.get_terminal_size().lines

        self.hidden: list[str] = []
        self.answer = ""
        self.correct_counter = 0
        self.letter_was_typed: dict[str, bool] = {}

        self._start_timer_thread: threading.Timer | None = None
        self._timer_display_thread: threading.Thread | None = None

        self.assets = asset_list

    def _center_text_helper(self, width: int, text: str) -> str:
        return text.center(width)

    def game_menu(self) -> None:
        os.system(self.clear_type)

        self._display_menu()
        choice = input(
            " " * (self.terminal_width // 2 - int(self.settings["menu_width"]) // 2)
            + "-> "
        )

        while choice != "3":
            os.system(self.clear_type)

            action = self._game_menu_helper(choice)
            if action is None:
                pass
            else:
                self.start_game(action)

            self._display_menu()
            choice = input(
                " " * (self.terminal_width // 2 - int(self.settings["menu_width"]) // 2)
                + "-> "
            )

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
        print(f"\033[{self.terminal_height//2 - len(menu_text) //2};1H", end="")
        for line in menu_text:
            print(self._center_text_helper(self.terminal_width, line))

    def _get_terminal_size(self) -> None:
        self.terminal_width = shutil.get_terminal_size().columns
        self.terminal_height = shutil.get_terminal_size().lines

    def _game_menu_helper(self, choice: str) -> str | None:
        if choice == "1":
            return "basic"

        if choice == "2":
            return "intermediate"

        return None

    def start_game(self, level: str) -> None:
        self._get_question(level)
        self.create_timer()

        while self.life > 0 and self.correct_counter < len(self.answer):
            self._print_question()
            letter_input = input("> ")
            self._letter_in_question(letter_input)

        self._reset_game()
        os.system(self.clear_type)

    def _print_question(self) -> None:
        os.system(self.clear_type)

        if self.life == 1:
            gallows = self.assets.gallows_6
        elif self.life == 2:
            gallows = self.assets.gallows_5
        elif self.life == 3:
            gallows = self.assets.gallows_4
        elif self.life == 4:
            gallows = self.assets.gallows_3
        elif self.life == 5:
            gallows = self.assets.gallows_2
        elif self.life == 6:
            gallows = self.assets.gallows_1
        else:
            gallows = self.assets.gallows_0

        for line in gallows:
            print(line)

        print()
        print(" ".join(self.hidden))

    def _reset_game(self) -> None:
        self.life = int(self.settings["start_life"])
        self.hidden = []
        self.answer = ""
        self.correct_counter = 0

    def _get_question(self, level: str) -> None:
        if level == "basic":
            self.answer = random.choice(self.word_list)
        else:
            self.answer = random.choice(self.phrase_list)

        for letter in self.answer:
            if letter == " ":
                self.hidden.append(" ")
                self.correct_counter += 1
            else:
                self.hidden.append("_")

    def _letter_in_question(self, letter_input: str) -> None:
        if not letter_input or letter_input not in self.answer:
            self.life -= 1
            return

        if letter_input in self.hidden:
            return

        for idx, char in enumerate(self.answer):
            if self.answer[idx] == letter_input:
                self.hidden[idx] = char
                self.correct_counter += 1

    def _start_timer(self) -> None:
        pass
