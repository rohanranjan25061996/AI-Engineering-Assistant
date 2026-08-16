from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel

from src.service import SearchService


app = FastAPI(
    title="AI Engineering Assistant",
    description="Code search API",
    version="1.0.0",
)


class SearchResultResponse(BaseModel):
    file_path: str
    line_number: int
    line: str
    context_before: list[str]
    context_after: list[str]
    language: str
    symbol: str | None


class SearchResponse(BaseModel):
    query: str
    total: int
    results: list[SearchResultResponse]


def get_search_service() -> SearchService:
    return SearchService()


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get(
    "/search",
    response_model=SearchResponse,
)
def search(
    query: str = Query(
        min_length=1,
        description="Text to search for",
    ),
    directory: str = Query(
        default=".",
        description="Directory to search",
    ),
    max_results: int = Query(
        default=50,
        ge=1,
        description="Maximum number of results",
    ),
    context: int = Query(
        default=0,
        ge=0,
        description="Context lines before and after a match",
    ),
    search_service: SearchService = Depends(
        get_search_service
    ),
):
    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty.",
        )

    try:
        results = search_service.search(
            directory=directory,
            query=query,
            max_results=max_results,
            context=context,
        )

    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    response_results = [
        SearchResultResponse(
            file_path=str(result.file_path),
            line_number=result.line_number,
            line=result.line,
            context_before=result.context_before,
            context_after=result.context_after,
            language=result.language,
            symbol=result.symbol,
        )
        for result in results
    ]

    return SearchResponse(
        query=query,
        total=len(response_results),
        results=response_results,
    )