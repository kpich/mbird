from pydantic import BaseModel, Field


class MbirdNode(BaseModel):
    id: str
    children: list[str] = Field(default_factory=list)
