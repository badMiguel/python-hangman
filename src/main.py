import sys
import threading
from read_json import ReadJson
from game import Game
from assets import Assets

SETTINGS_FILENAME = "settings.json"

def main() -> None:
    reader = ReadJson()

    settings = reader.get_settings(SETTINGS_FILENAME)
    if not settings:
        print(f"File {SETTINGS_FILENAME} not found")
        sys.exit()

    data = reader.get_data(settings["data_filename"])
    if not data:
        print(f"File {settings["data_filename"]} not found")
        sys.exit()
    word_list, phrase_list = data

    game = Game(settings, Assets(), word_list, phrase_list)
    game.game_menu()


if __name__ == "__main__":
    main()
