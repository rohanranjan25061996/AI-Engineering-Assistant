import argparse

from src.scanner import scan_directory
from src.search import search_file


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Search source code files for a text query."
    )

    parser.add_argument(
        "query",
        help="Text to search for",
    )

    parser.add_argument(
        "directory",
        help="Directory to search",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        files = scan_directory(args.directory)
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}")
        return

    total_matches = 0

    for file_path in files:
        matches = search_file(file_path, args.query)

        for line_number, line in matches:
            print(f"{file_path}:{line_number}")
            print(f"    {line}")
            print()

            total_matches += 1

    print(f"Found {total_matches} matches")


if __name__ == "__main__":
    main()