class Game:
    def __init__(self, word_list: list[str], phrase_list: list[str]) -> None:
        self.word_list = word_list
        self.phrase_list = phrase_list

    def _center_text_helper(self, width: int, text: str) -> str:
        return text.center(width)

    def game_menu(self) -> None:
        choice = input("> ")
        print(self._game_menu_helper(choice))

    def _game_menu_helper(self, choice: str) -> str:
        if choice == "1":
            return "Basic level"
        elif choice == "2":
            return "Intermediate level"
        elif choice == "3":
            return "Quit"
        else:
            return "Try again"

    def game_loop(self) -> None:
        pass
