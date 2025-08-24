"""Entry point for the Hangman game.

This module locates configuration files, read settings and words/phrases data
from a json file, and starts the game loop by creating a `Game` instance.
"""

import sys
import os
from read_json import ReadJson
from game import Game
from assets import Assets

CURRENT_DIR = os.path.basename(os.getcwd())
SETTINGS_FILENAME = (
    "../settings.json" if CURRENT_DIR == "src" else "settings.json"
)


def main() -> None:
    """Start the application

    Loads the settings and data files, constructs a Game object, and enters
    the game menu.

    Exits the program with an error message if the settings or data file cannot
    be found.
    """
    reader = ReadJson()

    settings = reader.get_settings(SETTINGS_FILENAME)
    if not settings:
        print(f"File {SETTINGS_FILENAME} not found")
        sys.exit()

    data_filename = (
        f"../{settings["data_filename"]}"
        if CURRENT_DIR == "src"
        else settings["data_filename"]
    )
    data = reader.get_data(data_filename)
    if not data:
        print(f"File {settings["data_filename"]} not found")
        sys.exit()
    word_list, phrase_list = data

    game = Game(settings, Assets(), word_list, phrase_list)
    game.game_menu()


if __name__ == "__main__":
    main()
