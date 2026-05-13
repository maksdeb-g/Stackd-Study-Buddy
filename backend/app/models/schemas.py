from pydantic import BaseModel


class Resource(BaseModel):
    id: str | None = None
    title: str
    source: str
    description: str
    thumbnail: str = ""
    link: str
    difficulty: str = "beginner"