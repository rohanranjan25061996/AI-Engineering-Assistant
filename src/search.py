from pathlib import Path


def search_file(file_path: Path, query: str) -> list[tuple[int, str]]:
    matches = []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if query.lower() in line.lower():
                    matches.append((line_number, line.rstrip()))

    except (UnicodeDecodeError, PermissionError):
        return []

    return matches