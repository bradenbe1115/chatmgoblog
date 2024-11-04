from pydantic import BaseModel

class MgoblogContentLandingDataSchema(BaseModel):
    url: str
    raw_html: str
    date_collected: str
