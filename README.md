# AI Engineering Assistant

A small Python-based code search tool built as the first milestone of my AI Engineering learning journey.

## Features

- Recursively scans source-code files
- Supports multiple programming languages
- Ignores common directories such as `.git`, `.venv`, and `node_modules`
- Case-insensitive text search
- Maximum result limit
- Context lines around matches
- Input validation
- Automated tests

## Project Structure

```text
ai-engineering-assistant/
├── src/
│   ├── __init__.py
│   ├── scanner.py
│   ├── search.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_scanner.py
│   ├── test_search.py
│   └── test_main.py
├── requirements.txt
├── README.md
└── .gitignore