import unittest
from argparse import Namespace

from src.main import validate_arguments


class TestValidateArguments(unittest.TestCase):

    def test_valid_arguments(self):
        args = Namespace(
            query="hello",
            directory=".",
            max_results=10,
            context=0,
        )

        validate_arguments(args)

    def test_empty_query(self):
        args = Namespace(
            query="",
            directory=".",
            max_results=10,
            context=0,
        )

        with self.assertRaises(ValueError):
            validate_arguments(args)

    def test_zero_max_results(self):
        args = Namespace(
            query="hello",
            directory=".",
            max_results=0,
            context=0,
        )

        with self.assertRaises(ValueError):
            validate_arguments(args)

    def test_negative_max_results(self):
        args = Namespace(
            query="hello",
            directory=".",
            max_results=-1,
            context=0,
        )

        with self.assertRaises(ValueError):
            validate_arguments(args)

    def test_negative_context(self):
        args = Namespace(
            query="hello",
            directory=".",
            max_results=10,
            context=-1,
        )

        with self.assertRaises(ValueError):
            validate_arguments(args)


if __name__ == "__main__":
    unittest.main()