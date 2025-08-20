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
        self.answer = ""

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

            action = self._game_menu_helper(choice)
            if action is None:
                pass 
            else:
                self.start_game(action)

            for line in menu_text:
                print(self._center_text_helper(width, line))
            choice = input(" " * (width // 2 - MENU_TEXT_WIDTH // 2) + "-> ")

    def _game_menu_helper(self, choice: str) -> str | None:
        if choice == "1":
            return "basic"

        if choice == "2":
            return "intermediate"

        return None

    def start_game(self, level: str) -> None:
        question = self._get_question(level)

        while self.life > 0:
            print(self.hidden, question, f"life:  {self.life}")
            letter_input = input("> ")
            self._letter_in_question(letter_input)

        self.life = 5
        self.hidden = []
        self.answer = ""

    def _get_question(self, level: str) -> None:
        if level == "basic":
            self.answer = random.choice(self.word_list)
        else:
            self.answer = random.choice(self.phrase_list)
        for letter in self.answer:
            if letter == " ":
                self.hidden.append(" ")
            else:
                self.hidden.append("_")

    def _letter_in_question(self, letter_input: str) -> None:
        if not letter_input or letter_input not in self.answer:
            self.life -= 1
            return

        for letter_idx in range(len(self.answer)):
            if self.answer[letter_idx] == letter_input:
                self.hidden[letter_idx] = letter_input
