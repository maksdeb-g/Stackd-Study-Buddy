from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class Resource(BaseModel):
    id: str | None = None
    title: str
    source: str
    description: str
    thumbnail: str = ""
    link: str
    difficulty: str = "beginner"


# Folder
class FolderCreate(BaseModel):
    name: str
    color: Optional[str] = "#6366f1"

class Folder(BaseModel):
    id: str
    name: str
    color: Optional[str] = "#6366f1"
    created_at: Optional[datetime] = None

# Save Resource
class SaveResourceRequest(BaseModel):
    folder_id: str
    title: str
    source: str
    description: str
    thumbnail: Optional[str] = None
    link: str
    difficulty: str = "beginner"

# Progress
class ProgressUpdate(BaseModel):
    status: Literal["WANT_TO_LEARN", "IN_PROGRESS", "DONE"]

# Subtopics
class SubtopicRequest(BaseModel):
    topic: str

class SubtopicResponse(BaseModel):
    subtopics: list[str]

# Search History
class SearchHistoryItem(BaseModel):
    id: str
    query: str
    result_count: int
    created_at: datetime