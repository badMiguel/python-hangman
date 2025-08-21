import random
import shutil
import os
import platform


class Game:
    def __init__(
        self, settings: dict[str, str], word_list: list[str], phrase_list: list[str]
    ) -> None:
        self.word_list = word_list
        self.phrase_list = phrase_list
        self.settings = settings
        self.life = int(self.settings["start_life"])
        self.clear_type: str = "clear" if platform.system() == "Linux" else "cls"

        self.hidden = []
        self.answer = ""
        self.correct_counter = 0

    def _center_text_helper(self, width: int, text: str) -> str:
        return text.center(width)

    def game_menu(self) -> None:
        os.system(self.clear_type)

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
        width = shutil.get_terminal_size().columns
        for line in menu_text:
            print(self._center_text_helper(width, line))
        choice = input(
            " " * (width // 2 - int(self.settings["menu_width"]) // 2) + "-> "
        )

        while choice != "3":
            os.system(self.clear_type)

            action = self._game_menu_helper(choice)
            if action is None:
                pass
            else:
                self.start_game(action)

            width = shutil.get_terminal_size().columns
            for line in menu_text:
                print(self._center_text_helper(width, line))
            choice = input(
                " " * (width // 2 - int(self.settings["menu_width"]) // 2) + "-> "
            )

    def _game_menu_helper(self, choice: str) -> str | None:
        if choice == "1":
            return "basic"

        if choice == "2":
            return "intermediate"

        return None

    def start_game(self, level: str) -> None:
        self._get_question(level)

        while self.life > 0 and self.correct_counter < len(self.answer):
            print(
                self.hidden,
                " - ",
                self.answer,
                " - ",
                f"life:  {self.life}",
                " - ",
                f"score: {self.correct_counter}",
            )
            letter_input = input("> ")
            self._letter_in_question(letter_input)

        self._reset_game()

    def _reset_game(self) -> None:
        os.system(self.clear_type)
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

        for idx, char in enumerate(self.answer):
            if self.answer[idx] == letter_input:
                self.hidden[idx] = char
                self.correct_counter += 1

    def _start_timer(self) -> None:
        pass
