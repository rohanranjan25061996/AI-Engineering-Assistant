from src.search import SearchResult, search_directory


class SearchService:

    def search(
        self,
        directory: str,
        query: str,
        max_results: int = 50,
        context: int = 0,
    ) -> list[SearchResult]:

        return search_directory(
            directory=directory,
            query=query,
            max_results=max_results,
            context=context,
        )