from dataclasses import dataclass
from pathlib import Path


@dataclass
class SearchResult:
    file_path: Path
    line_number: int
    line: str
    context_before: list[str]
    context_after: list[str]


def search_file(
    file_path: Path,
    query: str,
    context: int = 0,
) -> list[SearchResult]:
    try:
        lines = file_path.read_text(encoding="utf-8").splitlines()

    except (UnicodeDecodeError, PermissionError, OSError):
        return []

    matches = []

    for index, line in enumerate(lines):
        if query.lower() not in line.lower():
            continue

        start = max(0, index - context)
        end = min(len(lines), index + context + 1)

        matches.append(
            SearchResult(
                file_path=file_path,
                line_number=index + 1,
                line=line,
                context_before=lines[start:index],
                context_after=lines[index + 1:end],
            )
        )

    return matches


def search_directory(
    directory: str,
    query: str,
    max_results: int = 50,
    context: int = 0,
) -> list[SearchResult]:
    from src.scanner import scan_directory

    files = scan_directory(directory)

    results = []

    for file_path in files:
        matches = search_file(
            file_path=file_path,
            query=query,
            context=context,
        )

        for match in matches:
            results.append(match)

            if len(results) >= max_results:
                return results

    return results