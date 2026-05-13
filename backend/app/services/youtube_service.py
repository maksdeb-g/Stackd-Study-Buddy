import httpx

from app.core.config import settings
from app.models.schemas import Resource


YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def infer_difficulty(title: str, description: str) -> str:
    text = f"{title} {description}".lower()

    advanced_keywords = [
        "advanced",
        "expert",
        "deep dive",
        "research",
        "architecture",
        "optimization",
        "deployment",
        "production",
        "system design",
    ]

    beginner_keywords = [
        "beginner",
        "beginners",
        "introduction",
        "intro",
        "basics",
        "fundamentals",
        "learn",
        "getting started",
        "for beginners",
    ]

    intermediate_keywords = [
        "intermediate",
        "project",
        "build",
        "crash course",
        "complete course",
        "hands-on",
        "explained",
        "tutorial",
    ]

    if any(keyword in text for keyword in advanced_keywords):
        return "advanced"

    if any(keyword in text for keyword in beginner_keywords):
        return "beginner"

    if any(keyword in text for keyword in intermediate_keywords):
        return "intermediate"

    return "beginner"


async def search_youtube(query: str, max_results: int = 4) -> list[Resource]:
    if not settings.YOUTUBE_API_KEY:
        return []

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": settings.YOUTUBE_API_KEY,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.get(YOUTUBE_SEARCH_URL, params=params)
            response.raise_for_status()
            data = response.json()
        except Exception:
            return []

    results: list[Resource] = []

    for item in data.get("items", []):
        video_id = item.get("id", {}).get("videoId", "")
        snippet = item.get("snippet", {})

        title = snippet.get("title", "Untitled YouTube Video")
        description = snippet.get("description", "")
        thumbnails = snippet.get("thumbnails", {})

        thumbnail = (
            thumbnails.get("high", {}).get("url")
            or thumbnails.get("medium", {}).get("url")
            or thumbnails.get("default", {}).get("url")
            or ""
        )

        if not video_id:
            continue

        results.append(
            Resource(
                title=title,
                source="youtube",
                description=description[:300] if description else "YouTube video.",
                thumbnail=thumbnail,
                link=f"https://www.youtube.com/watch?v={video_id}",
                difficulty=infer_difficulty(title, description),
            )
        )

    return results