import unittest
from unittest.mock import mock_open, patch
from src.read_json import ReadJson


class TestReadJson(unittest.TestCase):
    """
    Unit test for the 'get_data.read' function from the 'src.get_data' module.

    Tests both successful JSON file read and handling a missing file.
    """

    def setUp(self) -> None:
        self.reader = ReadJson()

    def test_get(self) -> None:
        """
        Test that `get_data.read` correctly reads a JSON file when it exists.

        Uses `unittest.mock` to simulate a file containing a JSON object with
        "words" and "phrases", does NOT require real file exists. Checks that
        returned tuple matches the expected data.
        """
        data = '{"words": ["food"], "phrases": ["hello world"]}'
        with patch("builtins.open", mock_open(read_data=data)):
            result = self.reader.get_data("data.json")
            self.assertEqual(result, (["food"], ["hello world"]))
        self.assertIsInstance(result, tuple)

    def test_not_found(self) -> None:
        """
        Test that `get_data.read` returns None when the file does not exist.
        """
        result = self.reader.get_data("none.json")
        self.assertIs(result, None)

if __name__ == "__main__":
    unittest.main()
