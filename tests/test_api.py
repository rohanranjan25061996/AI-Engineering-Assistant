import unittest

from fastapi.testclient import TestClient

from src.api import app


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

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["query"], "def")
        self.assertIn("total", data)
        self.assertIn("results", data)

    def test_empty_query(self):
        response = client.get(
            "/search",
            params={
                "query": "",
                "directory": ".",
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_invalid_max_results(self):
        response = client.get(
            "/search",
            params={
                "query": "def",
                "directory": ".",
                "max_results": 0,
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_negative_context(self):
        response = client.get(
            "/search",
            params={
                "query": "def",
                "directory": ".",
                "context": -1,
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_invalid_directory(self):
        response = client.get(
            "/search",
            params={
                "query": "def",
                "directory": "./does-not-exist",
            },
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()