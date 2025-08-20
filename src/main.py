import get_data
import sys


class GameLoop:
    def __init__(self) -> None:
        pass


def main() -> None:
    data_filename = "data.json"
    data = get_data.read(data_filename)
    if not data:
        print(f"File {data_filename} not found")
        sys.exit()
    word_list, phrase_list = data

    print(word_list, phrase_list)


if __name__ == "__main__":
    main()
