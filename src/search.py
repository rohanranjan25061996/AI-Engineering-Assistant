from dataclasses import dataclass
from pathlib import Path

from src.language import detect_language
from src.symbols import extract_symbols


@dataclass
class SearchResult:
    file_path: Path
    line_number: int
    line: str
    context_before: list[str]
    context_after: list[str]
    language: str = "unknown"
    symbol: str | None = None


def search_file(
    file_path: Path,
    query: str,
    context: int = 0,
) -> list[SearchResult]:
    try:
        lines = file_path.read_text(
            encoding="utf-8"
        ).splitlines()
    except (UnicodeDecodeError, OSError):
        return []

    query_lower = query.lower()

    language = detect_language(file_path)
    symbols = extract_symbols(file_path)

    results = []

    for index, line in enumerate(lines):
        if query_lower not in line.lower():
            continue

        line_number = index + 1

        context_before = lines[
            max(0, index - context):index
        ]

        context_after = lines[
            index + 1:index + 1 + context
        ]

        matched_symbol = None

        for symbol in symbols:
            if symbol.line_number <= line_number:
                matched_symbol = symbol.name
            else:
                break

        results.append(
            SearchResult(
                file_path=file_path,
                line_number=line_number,
                line=line,
                context_before=context_before,
                context_after=context_after,
                language=language,
                symbol=matched_symbol,
            )
        )

    return results


def search_directory(
    directory: str | Path,
    query: str,
    max_results: int = 50,
    context: int = 0,
) -> list[SearchResult]:

    directory_path = Path(directory)

    if not directory_path.exists():
        raise FileNotFoundError(
            f"Directory does not exist: {directory}"
        )

    if not directory_path.is_dir():
        raise NotADirectoryError(
            f"Not a directory: {directory}"
        )

    results = []

    supported_extensions = {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".go",
        ".rs",
        ".cpp",
        ".c",
        ".cs",
        ".rb",
        ".php",
        ".swift",
        ".kt",
        ".md",
        ".json",
        ".yaml",
        ".yml",
    }

    for file_path in directory_path.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in supported_extensions:
            continue

        file_results = search_file(
            file_path,
            query,
            context=context,
        )

        results.extend(file_results)

        if len(results) >= max_results:
            return results[:max_results]

    return results