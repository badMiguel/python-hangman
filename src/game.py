import random
import shutil
import os
import platform


class Game:
    def __init__(self, word_list: list[str], phrase_list: list[str]) -> None:
        self.word_list = word_list
        self.phrase_list = phrase_list
        self.life = 5
        self.hidden = []

        self.clear_type: str = "cls"
        if platform.system() == "Linux":
            self.clear_type = "clear"

    def _center_text_helper(self, width: int, text: str) -> str:
        return text.center(width)

    def game_menu(self) -> None:
        os.system(self.clear_type)
        width = shutil.get_terminal_size().columns

        MENU_TEXT_WIDTH = 37
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
        for line in menu_text:
            print(self._center_text_helper(width, line))
        choice = input(" " * (width // 2 - MENU_TEXT_WIDTH // 2) + "-> ")

        while choice != "3":
            os.system(self.clear_type)

            self.start_game(self._game_menu_helper(choice))

            for line in menu_text:
                print(self._center_text_helper(width, line))
            choice = input(" " * (width // 2 - MENU_TEXT_WIDTH // 2) + "-> ")

    def _game_menu_helper(self, choice: str) -> str:
        if choice == "1":
            return "basic"

        if choice == "2":
            return "intermediate"

        return ""

    def start_game(self, level: str) -> None:
        question = self._get_question(level)
        for letter in question:
            if letter == " ":
                self.hidden.append(" ")
            else:
                self.hidden.append("_")

        while self.life > 0:
            print(self.hidden, question, f"life:  {self.life}")
            letter_input = input("> ")
            self._letter_in_question(question, letter_input)

    def _get_question(self, level: str) -> str:
        if level == "basic":
            return random.choice(self.word_list)

        return random.choice(self.phrase_list)

    def _letter_in_question(self, question: str, letter_input: str) -> None:
        if letter_input not in question:
            self.life -= 1
            return

        for letter_idx in range(len(question)):
            if question[letter_idx] == letter_input:
                self.hidden[letter_idx] = letter_input
