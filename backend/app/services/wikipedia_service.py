import httpx

from app.core.config import settings
from app.models.schemas import Resource


async def search_wikipedia(query: str, max_results: int = 4) -> list[Resource]:
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": max_results,
        "format": "json",
        "srprop": "snippet|titlesnippet",
    }

    headers = {
        "User-Agent": "StackdStudyBuddy/1.0 (educational project)"
    }

    async with httpx.AsyncClient(timeout=15, headers=headers) as client:
        try:
            search_response = await client.get(
                settings.WIKI_BASE_URL,
                params=search_params,
            )
            search_response.raise_for_status()
            search_data = search_response.json()
        except Exception:
            return []

        pages = search_data.get("query", {}).get("search", [])
        results: list[Resource] = []

        for page in pages:
            title = page.get("title", "Untitled")
            page_id = page.get("pageid", "")

            snippet = (
                page.get("snippet", "")
                .replace('<span class="searchmatch">', "")
                .replace("</span>", "")
                .strip()
            )

            thumbnail = ""

            try:
                image_response = await client.get(
                    settings.WIKI_BASE_URL,
                    params={
                        "action": "query",
                        "pageids": page_id,
                        "prop": "pageimages",
                        "pithumbsize": 300,
                        "format": "json",
                    },
                )
                image_response.raise_for_status()
                image_data = image_response.json()

                thumbnail = (
                    image_data.get("query", {})
                    .get("pages", {})
                    .get(str(page_id), {})
                    .get("thumbnail", {})
                    .get("source", "")
                )
            except Exception:
                pass

            results.append(
                Resource(
                    title=title,
                    source="wikipedia",
                    description=snippet[:300] if snippet else "Wikipedia article.",
                    thumbnail=thumbnail,
                    link=f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                    difficulty="beginner",
                )
            )

        return results