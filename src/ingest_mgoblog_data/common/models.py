from pydantic import BaseModel

class MgoblogContentLandingDataSchema(BaseModel):
    url: str
    raw_html: str
    collected_ts: int

class MgoblogContentProcessedDataSchema(BaseModel):
    url: str
    raw_html: str
    collected_ts: str
    tags: list[str]
    title: str
    author: str
    body: str
    date_written: str

class MgoBlogContentEmbedding(BaseModel):
    id: str
    url: str
    text: str
    embedding: list[float]