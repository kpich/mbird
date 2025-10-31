from pydantic import BaseModel, Field


class MbirdNode(BaseModel):
    id: str
    properties: dict = Field(default_factory=dict)
    children: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
