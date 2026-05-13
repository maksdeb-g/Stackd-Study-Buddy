import httpx

from app.core.config import settings
from app.models.schemas import Resource


GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"


def infer_difficulty_from_categories(categories: list[str]) -> str:
    text = " ".join(categories).lower()

    advanced_keywords = [
        "computer science",
        "engineering",
        "mathematics",
        "data science",
        "artificial intelligence",
        "machine learning",
        "programming",
        "technology",
        "science",
        "research",
    ]

    beginner_keywords = [
        "juvenile",
        "children",
        "introductory",
        "beginner",
        "basic",
        "education",
        "study aids",
        "self-help",
    ]

    if any(keyword in text for keyword in advanced_keywords):
        return "advanced"

    if any(keyword in text for keyword in beginner_keywords):
        return "beginner"

    return "intermediate"


async def search_books(query: str, max_results: int = 4) -> list[Resource]:
    params = {
        "q": query,
        "maxResults": max_results,
        "printType": "books",
        "orderBy": "relevance",
    }

    if settings.GOOGLE_BOOKS_API_KEY:
        params["key"] = settings.GOOGLE_BOOKS_API_KEY

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.get(GOOGLE_BOOKS_URL, params=params)
            response.raise_for_status()
            data = response.json()
        except Exception:
            return []

    results: list[Resource] = []

    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})

        title = volume_info.get("title", "Untitled Book")
        authors = volume_info.get("authors", [])
        description = volume_info.get("description", "")
        categories = volume_info.get("categories", [])
        image_links = volume_info.get("imageLinks", {})

        author_text = ", ".join(authors) if authors else "Unknown author"

        thumbnail = (
            image_links.get("thumbnail")
            or image_links.get("smallThumbnail")
            or ""
        )

        link = (
            volume_info.get("previewLink")
            or volume_info.get("infoLink")
            or ""
        )

        if not link:
            continue

        results.append(
            Resource(
                title=title,
                source="book",
                description=(
                    f"By {author_text}. {description[:250]}"
                    if description
                    else f"By {author_text}. Google Books result."
                ),
                thumbnail=thumbnail,
                link=link,
                difficulty=infer_difficulty_from_categories(categories),
            )
        )

    return results