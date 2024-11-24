from pydantic import BaseModel
from typing import Optional

class MgoblogContentLandingDataSchema(BaseModel):
    url: str
    raw_html: str
    collected_ts: int

    def __hash__(self):
        return hash(self.url)

class MgoblogContentProcessedDataSchema(BaseModel):
    url: str
    raw_html: str
    collected_ts: int
    tags: Optional[list[str]] = []
    title: Optional[str] = None
    author: Optional[str] = None
    body: Optional[str] = None
    date_written: Optional[str] = None

    def __hash__(self):
        return hash(self.url)

class MgoBlogContentEmbedding(BaseModel):
    id: str
    url: str
    text: str
    embedding: list[float]