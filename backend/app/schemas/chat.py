from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    message: str = Field(..., min_length=1)

    history: list = Field(default_factory=list)


class ChatResponse(BaseModel):

    answer: str