from pydantic import BaseModel

class MgoBlogContentEmbedding(BaseModel):
    url: str
    embedding: list[float]