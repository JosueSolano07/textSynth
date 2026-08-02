from pydantic import BaseModel, Field


class AskRequest(BaseModel):

    question: str = Field(..., min_length=1)

    history: list = Field(default_factory=list)


class AskResponse(BaseModel):

    answer: str

    sources: list = Field(default_factory=list)