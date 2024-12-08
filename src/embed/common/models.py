import dataclasses
@dataclasses.dataclass
class EmbeddedTextData:
    index: int
    text: str
    embedded_text: list[float]