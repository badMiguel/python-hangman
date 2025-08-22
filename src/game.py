import random
import shutil
import os, platform
import threading, time
import string


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
        self.letter_list: list[str] = []

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
        self._create_letter_was_typed()

        while self.life > 0 and self.correct_counter < len(self.answer):
            self._print_question()

            print()
            width = int(self.settings["gallows_width"])
            # *2-1 because of the additional space added when printing
            if len(self.hidden) * 2 - 1 > width:
                width = len(self.hidden) * 2 - 1
            letter_input = input(
                # -3 is from additional space from "-> "
                " " * (self.terminal_width // 2 - width // 2 - 3)
                + "-> "
            ).lower()

            self._letter_in_question(letter_input)

        self._reset_game()
        os.system(self.clear_type)

    def _create_letter_was_typed(self) -> None:
        letter_list: list[str] = []

        letters = string.ascii_lowercase
        for letter in letters:
            letter_list.append(letter)
            self.letter_was_typed[letter] = False

        self.letter_list = letter_list

    def _print_question(self) -> None:
        os.system(self.clear_type)
        print(self.answer)

        self._get_terminal_size()

        print(
            f"\033[{self.terminal_height//2 - len(self.assets.gallows_1)//2};1H",
            end="",
        )

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
            print(self._center_text_helper(self.terminal_width, line))

        print()
        print(self._center_text_helper(self.terminal_width, " ".join(self.hidden)))

        len_letter_list = len(self.letter_list)
        portion = len_letter_list // 3
        list_of_letter_list = [
            self.letter_list[:portion],
            self.letter_list[portion : len_letter_list - portion],
            self.letter_list[len_letter_list - portion : len_letter_list],
        ]

        for letter_list in list_of_letter_list:
            print(f"\n\033[{self.terminal_width//2-len(letter_list)+1}C", end="")
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

    def _reset_game(self) -> None:
        self.life = int(self.settings["start_life"])
        self.hidden = []
        self.answer = ""
        self.correct_counter = 0
        self._create_letter_was_typed()

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
        self.letter_was_typed[letter_input] = True
        if letter_input not in self.answer:
            self.life -= 1
            return

        if letter_input in self.hidden:
            return

        for idx, char in enumerate(self.answer):
            if self.answer[idx] == letter_input:
                self.hidden[idx] = char
                self.correct_counter += 1

    def create_timer(self) -> None:
        # # creates new thread for timer to avoid blocking whole program
        # self._start_timer_thread = threading.Timer(15, self._start_timer)
        # self._timer_display_thread = threading.Thread(target=self._timer_display)
        #
        # self._start_timer_thread.start()
        # self._timer_display_thread.start()
        pass

    def _start_timer(self) -> None:
        pass

    def _timer_display(self) -> None:
        pass
