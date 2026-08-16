import argparse

from src.search import search_directory


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

    parser.add_argument(
        "--max-results",
        type=int,
        default=50,
        help="Maximum number of search results.",
    )

    parser.add_argument(
        "--context",
        type=int,
        default=0,
        help="Number of context lines before and after each match.",
    )

    return parser.parse_args()


def validate_arguments(args):
    if not args.query.strip():
        raise ValueError("Search query cannot be empty.")

    if args.max_results <= 0:
        raise ValueError(
            "max-results must be greater than 0."
        )

    if args.context < 0:
        raise ValueError(
            "context cannot be negative."
        )


def main():
    args = parse_arguments()

    try:
        validate_arguments(args)

        results = search_directory(
            directory=args.directory,
            query=args.query,
            max_results=args.max_results,
            context=args.context,
        )

    except (
        ValueError,
        FileNotFoundError,
        NotADirectoryError,
    ) as error:
        print(f"Error: {error}")
        return

    for result in results:
        print(
            f"{result.file_path}:{result.line_number}"
        )

        if result.context_before:
            first_line_number = (
                result.line_number
                - len(result.context_before)
            )

            for offset, line in enumerate(
                result.context_before
            ):
                line_number = first_line_number + offset
                print(f"    {line_number} | {line}")

        print(
            f"    {result.line_number} | {result.line}"
        )

        for offset, line in enumerate(
            result.context_after,
            start=1,
        ):
            line_number = result.line_number + offset
            print(f"    {line_number} | {line}")

        print()

    print(f"Found {len(results)} matches")


if __name__ == "__main__":
    main()