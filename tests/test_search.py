import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.search import search_file


class TestSearchFile(unittest.TestCase):

    def test_finds_matching_line(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"

            file_path.write_text(
                "def hello():\n"
                "    print('Hello')\n"
            )

            results = search_file(file_path, "hello")

            self.assertEqual(len(results), 2)
            self.assertEqual(results[0][0], 1)
            self.assertEqual(results[1][0], 2)

    def test_search_is_case_insensitive(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"

            file_path.write_text(
                "def Hello():\n"
            )

            results = search_file(file_path, "hello")

            self.assertEqual(len(results), 1)

    def test_returns_empty_when_no_match(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"

            file_path.write_text(
                "def hello():\n"
            )

            results = search_file(file_path, "python")

            self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()