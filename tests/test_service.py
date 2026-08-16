import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.service import SearchService


class TestSearchService(unittest.TestCase):

    def test_search(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "example.py"

            file_path.write_text(
                "def hello():\n"
                "    print('hello')\n"
            )

            service = SearchService()

            results = service.search(
                directory=temp_dir,
                query="hello",
            )

            self.assertEqual(len(results), 2)

    def test_max_results(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "example.py"

            file_path.write_text(
                "hello\n"
                "hello\n"
                "hello\n"
            )

            service = SearchService()

            results = service.search(
                directory=temp_dir,
                query="hello",
                max_results=2,
            )

            self.assertEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()