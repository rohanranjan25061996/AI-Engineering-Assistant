import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.search import SearchResult, search_file


class TestSearchFile(unittest.TestCase):

    def test_finds_matching_line(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"

            file_path.write_text(
                "def hello():\n"
                "    print('Hello')\n"
            )

            results = search_file(file_path, "hello")

            self.assertIsInstance(results[0], SearchResult)
            self.assertEqual(results[0].line_number, 1)
            self.assertEqual(results[1].line_number, 2)

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
    def test_search_directory_respects_max_results(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            (root / "one.py").write_text(
                "def hello():\n"
                "    print('hello')\n"
            )

            (root / "two.py").write_text(
                "def hello_again():\n"
            )

            from src.search import search_directory

            results = search_directory(
                temp_dir,
                "hello",
                max_results=2,
            )

            self.assertEqual(len(results), 2)
    def test_search_returns_context(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"

            file_path.write_text(
                "line 1\n"
                "line 2\n"
                "find this\n"
                "line 4\n"
                "line 5\n"
            )

            results = search_file(
                file_path,
                "find this",
                context=1,
            )

            self.assertEqual(len(results), 1)

            result = results[0]

            self.assertEqual(result.line_number, 3)
            self.assertEqual(result.line, "find this")
            self.assertEqual(result.context_before, ["line 2"])
            self.assertEqual(result.context_after, ["line 4"])

    def test_handles_invalid_utf8_file(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "invalid.py"

            file_path.write_bytes(b"\xff\xfe\xfd")

            results = search_file(
                file_path,
                "hello",
            )

        self.assertEqual(results, [])

    def test_search_includes_language(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"

            file_path.write_text(
                "def hello():\n"
                "    return True\n"
            )

            results = search_file(
                file_path,
                "hello",
            )

            self.assertEqual(
                len(results),
                1,
            )

            result = results[0]

            self.assertEqual(
                result.language,
                "python",
            )

    def test_search_includes_symbol(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"

            file_path.write_text(
                "def hello():\n"
                "    return True\n"
            )

            results = search_file(
                file_path,
                "hello",
            )

            self.assertEqual(
                len(results),
                1,
            )

            result = results[0]

            self.assertEqual(
                result.symbol,
                "hello",
            )


if __name__ == "__main__":
    unittest.main()