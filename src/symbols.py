import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Symbol:
    name: str
    symbol_type: str
    line_number: int


def extract_symbols(file_path: Path) -> list[Symbol]:
    try:
        source = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    symbols = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            symbols.append(
                Symbol(
                    name=node.name,
                    symbol_type="function",
                    line_number=node.lineno,
                )
            )

        elif isinstance(node, ast.AsyncFunctionDef):
            symbols.append(
                Symbol(
                    name=node.name,
                    symbol_type="async_function",
                    line_number=node.lineno,
                )
            )

        elif isinstance(node, ast.ClassDef):
            symbols.append(
                Symbol(
                    name=node.name,
                    symbol_type="class",
                    line_number=node.lineno,
                )
            )

    return symbols