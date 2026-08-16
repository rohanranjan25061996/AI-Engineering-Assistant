from dataclasses import dataclass
from pathlib import Path


@dataclass
class SearchResult:
    file_path: Path
    line_number: int
    line: str


def search_file(file_path: Path, query: str) -> list[SearchResult]:
    matches = []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if query.lower() in line.lower():
                    matches.append(
                        SearchResult(
                            file_path=file_path,
                            line_number=line_number,
                            line=line.rstrip(),
                        )
                    )

    except (UnicodeDecodeError, PermissionError):
        return []

    return matches