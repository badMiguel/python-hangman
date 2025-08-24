"""Utility module for reading JSON files"""

import json


class ReadJson:
    """
    Simple JSON file reader that either read game settings or word/phrase list
    """

    def get_data(self, filename: str) -> None | tuple[list[str], list[str]]:
        """Reads a JSON file and return word and phrase list

        Parameters:
            - filename : str
                Path to the JSON file

        Returns:
            - `tupple[list[str], list[str]]` | None
                Returns tuple of two lists (words, phrases) when file specified
                with file is present. Returns `None` if file does not exist.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return None

        return data["words"], data["phrases"]

    def get_settings(self, filename: str) -> None | dict[str, str]:
        """Reads a JSON file and return game settings

        Parameters:
            - filename : str
                Path to the JSON file

        Returns:
            - `dict[str, str]` | None
                Returns the parsed JSON object as a dictionary, or `None` if
                the file does not exist.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return None

        return data
