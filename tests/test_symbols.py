import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.symbols import Symbol, extract_symbols


class TestExtractSymbols(unittest.TestCase):

    def test_extracts_function(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"

            file_path.write_text(
                "def hello():\n"
                "    return True\n"
            )

            symbols = extract_symbols(file_path)

            self.assertEqual(
                symbols,
                [
                    Symbol(
                        name="hello",
                        symbol_type="function",
                        line_number=1,
                    )
                ],
            )

    def test_extracts_class(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"

            file_path.write_text(
                "class UserService:\n"
                "    pass\n"
            )

            symbols = extract_symbols(file_path)

            self.assertEqual(
                symbols,
                [
                    Symbol(
                        name="UserService",
                        symbol_type="class",
                        line_number=1,
                    )
                ],
            )

    def test_extracts_class_and_method(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"

            file_path.write_text(
                "class UserService:\n"
                "    def authenticate(self):\n"
                "        return True\n"
            )

            symbols = extract_symbols(file_path)

            self.assertEqual(
                symbols,
                [
                    Symbol(
                        name="UserService",
                        symbol_type="class",
                        line_number=1,
                    ),
                    Symbol(
                        name="authenticate",
                        symbol_type="function",
                        line_number=2,
                    ),
                ],
            )

    def test_extracts_async_function(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"

            file_path.write_text(
                "async def fetch_user():\n"
                "    return None\n"
            )

            symbols = extract_symbols(file_path)

            self.assertEqual(
                symbols,
                [
                    Symbol(
                        name="fetch_user",
                        symbol_type="async_function",
                        line_number=1,
                    )
                ],
            )

    def test_invalid_python(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "invalid.py"

            file_path.write_text(
                "def broken(:\n"
            )

            symbols = extract_symbols(file_path)

            self.assertEqual(
                symbols,
                [],
            )

    def test_invalid_utf8(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "invalid.py"

            file_path.write_bytes(
                b"\xff\xfe\xfd"
            )

            symbols = extract_symbols(file_path)

            self.assertEqual(
                symbols,
                [],
            )


if __name__ == "__main__":
    unittest.main()