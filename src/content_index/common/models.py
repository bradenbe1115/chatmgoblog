from pydantic import BaseModel
from typing import Optional


class MgoBlogContent(BaseModel):
    id: str
    url: str
    embedding: list[float]
    text: str

    def __hash__(self):
        return hash(self.id)
