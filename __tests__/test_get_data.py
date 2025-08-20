import unittest
from unittest.mock import mock_open, patch
from src import get_data


class TestGetData(unittest.TestCase):
    """
    Unit test for the 'get_data.read' function from the 'src.get_data' module.

    Tests both successful JSON file read and handling a missing file.
    """

    def test_read_file_exists(self) -> None:
        """
        Test that `get_data.read` correctly reads a JSON file when it exists.

        Uses `unittest.mock` to simulate a file containing a JSON object with
        "words" and "phrases", does NOT require real file exists. Checks that
        returned tuple matches the expected data.
        """
        data = '{"words": ["food"], "phrases": ["hello world"]}'
        with patch("builtins.open", mock_open(read_data=data)):
            result = get_data.read("data.json")
            self.assertEqual(result, (["food"], ["hello world"]))

    def test_read_file_not_found(self) -> None:
        """
        Test that `get_data.read` returns None when the file does not exist.
        """
        result = get_data.read("none.json")
        self.assertIs(result, None)


if __name__ == "__main__":
    unittest.main()
