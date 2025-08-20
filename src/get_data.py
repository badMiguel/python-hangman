import json


def read(filename: str) -> None | tuple[list[str], list[str]]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return None

    return data["words"], data["phrases"]
