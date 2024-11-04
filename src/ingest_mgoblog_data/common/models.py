from pydantic import BaseModel

class MgoblogContentLandingDataSchema(BaseModel):
    url: str
    raw_html: str
    collected_ts: int
