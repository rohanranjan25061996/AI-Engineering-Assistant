from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.search import SearchResult, search_directory


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


class SearchResponse(BaseModel):
    query: str
    total: int
    results: list[SearchResultResponse]


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/search", response_model=SearchResponse)
def search(
    query: str,
    directory: str = ".",
    max_results: int = 50,
    context: int = 0,
):
    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty.",
        )

    if max_results <= 0:
        raise HTTPException(
            status_code=400,
            detail="max_results must be greater than 0.",
        )

    if context < 0:
        raise HTTPException(
            status_code=400,
            detail="context cannot be negative.",
        )

    try:
        results = search_directory(
            directory=directory,
            query=query,
            max_results=max_results,
            context=context,
        )

    except (FileNotFoundError, NotADirectoryError) as error:
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
        )
        for result in results
    ]

    return SearchResponse(
        query=query,
        total=len(response_results),
        results=response_results,
    )