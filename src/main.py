import get_data
import sys
from game import Game


def main() -> None:
    data_filename = "data.json"
    data = get_data.read(data_filename)
    if not data:
        print(f"File {data_filename} not found")
        sys.exit()
    word_list, phrase_list = data

    game = Game(word_list, phrase_list)
    game.game_menu()


if __name__ == "__main__":
    main()
