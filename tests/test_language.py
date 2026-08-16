import unittest
from pathlib import Path

from src.language import detect_language


class TestDetectLanguage(unittest.TestCase):

    def test_python(self):
        result = detect_language(
            Path("example.py")
        )

        self.assertEqual(
            result,
            "python",
        )

    def test_typescript(self):
        result = detect_language(
            Path("example.ts")
        )

        self.assertEqual(
            result,
            "typescript",
        )

    def test_javascript(self):
        result = detect_language(
            Path("example.js")
        )

        self.assertEqual(
            result,
            "javascript",
        )

    def test_unknown_extension(self):
        result = detect_language(
            Path("example.xyz")
        )

        self.assertEqual(
            result,
            "unknown",
        )


if __name__ == "__main__":
    unittest.main()