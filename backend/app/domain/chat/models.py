from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    chat_id: Optional[str]
    question: str


class ChatResponse(BaseModel):
    chat_id: str
    answer: str
    sources: list