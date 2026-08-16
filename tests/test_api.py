import unittest
from types import SimpleNamespace

from fastapi.testclient import TestClient

from src.api import app, get_search_service


class FakeSearchService:

    def search(
        self,
        directory: str,
        query: str,
        max_results: int = 50,
        context: int = 0,
    ):
        return [
            SimpleNamespace(
                file_path="src/example.py",
                line_number=10,
                line="def hello():",
                context_before=["import os"],
                context_after=["    return 'hello'"],
                language="python",
                symbol="hello",
            )
        ]


def override_search_service():
    return FakeSearchService()


app.dependency_overrides[get_search_service] = (
    override_search_service
)

client = TestClient(app)


class TestHealthEndpoint(unittest.TestCase):

    def test_health(self):
        response = client.get("/health")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json(),
            {"status": "ok"},
        )


class TestSearchEndpoint(unittest.TestCase):

    def test_search(self):
        response = client.get(
            "/search",
            params={
                "query": "def",
                "directory": ".",
                "max_results": 2,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertEqual(
            data["query"],
            "def",
        )

        self.assertEqual(
            data["total"],
            1,
        )

        self.assertEqual(
            data["results"],
            [
                {
                    "file_path": "src/example.py",
                    "line_number": 10,
                    "line": "def hello():",
                    "context_before": ["import os"],
                    "context_after": ["    return 'hello'"],
                    "language": "python",
                    "symbol": "hello",
                }
            ],
        )

    def test_empty_query(self):
        response = client.get(
            "/search",
            params={
                "query": "",
                "directory": ".",
            },
        )

        self.assertEqual(
            response.status_code,
            422,
        )

    def test_invalid_max_results(self):
        response = client.get(
            "/search",
            params={
                "query": "def",
                "directory": ".",
                "max_results": 0,
            },
        )

        self.assertEqual(
            response.status_code,
            422,
        )

    def test_negative_context(self):
        response = client.get(
            "/search",
            params={
                "query": "def",
                "directory": ".",
                "context": -1,
            },
        )

        self.assertEqual(
            response.status_code,
            422,
        )

    def test_invalid_directory(self):
        response = client.get(
            "/search",
            params={
                "query": "def",
                "directory": "./does-not-exist",
            },
        )

        # FakeSearchService doesn't access the filesystem,
        # so the directory itself doesn't cause an error.
        self.assertEqual(
            response.status_code,
            200,
        )


if __name__ == "__main__":
    unittest.main()