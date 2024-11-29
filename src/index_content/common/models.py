from pydantic import BaseModel

class EmbeddedTextData(BaseModel):
    index: int
    text: str
    embedded_text: list[float]