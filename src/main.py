import sys

from src.scanner import scan_directory
from src.search import search_file


def main():
    if len(sys.argv) != 3:
        print("Usage: python -m src.main <query> <directory>")
        return

    query = sys.argv[1]
    directory = sys.argv[2]

    files = scan_directory(directory)

    total_matches = 0

    for file_path in files:
        matches = search_file(file_path, query)

        for line_number, line in matches:
            print(f"{file_path}:{line_number}")
            print(f"    {line}")
            print()

            total_matches += 1

    print(f"Found {total_matches} matches")


if __name__ == "__main__":
    main()