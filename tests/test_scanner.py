import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.scanner import scan_directory


class TestScanDirectory(unittest.TestCase):

    def test_finds_supported_files(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            (root / "main.py").write_text("print('hello')")
            (root / "app.js").write_text("console.log('hello')")
            (root / "README.md").write_text("# Hello")

            files = scan_directory(temp_dir)

            file_names = {file.name for file in files}

            self.assertIn("main.py", file_names)
            self.assertIn("app.js", file_names)
            self.assertNotIn("README.md", file_names)

    def test_ignores_directories(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            (root / "main.py").write_text("print('hello')")

            node_modules = root / "node_modules"
            node_modules.mkdir()
            (node_modules / "package.py").write_text("test")

            files = scan_directory(temp_dir)

            file_names = {file.name for file in files}

            self.assertIn("main.py", file_names)
            self.assertNotIn("package.py", file_names)

    def test_finds_files_in_subdirectories(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            src = root / "src"
            src.mkdir()

            file_path = src / "app.py"
            file_path.write_text("print('hello')")

            files = scan_directory(temp_dir)

            self.assertIn(file_path, files)

    def test_invalid_directory(self):
        with self.assertRaises(FileNotFoundError):
            scan_directory("/this/directory/does/not/exist")


if __name__ == "__main__":
    unittest.main()