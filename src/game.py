import shutil
import os
import platform


class Game:
    def __init__(self, word_list: list[str], phrase_list: list[str]) -> None:
        self.word_list = word_list
        self.phrase_list = phrase_list
        self.clear_type: str = "cls"
        if platform.system() == "Linux":
            self.clear_type = "clear"

    def _center_text_helper(self, width: int, text: str) -> str:
        return text.center(width)

    def game_menu(self) -> None:
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
        pass
