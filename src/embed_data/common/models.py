from pydantic import BaseModel

class MgoBlogContentEmbedding(BaseModel):
    id: str
    url: str
    text: str
    embedding: list[float]