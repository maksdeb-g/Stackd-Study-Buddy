from fastapi import FastAPI
from app.services.wikipedia_service import search_wikipedia
from app.models.schemas import Resource

app = FastAPI(
    title="Stackd - Study Buddy API",
    version="1.0.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Stackd API"}

@app.get("/search/wikipedia", response_model=list[Resource])
async def search_wikipedia_endpoint(query: str, max_results: int = 4):
    """Search Wikipedia for learning resources."""
    return await search_wikipedia(query, max_results)

