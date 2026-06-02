from fastapi import APIRouter
from app.domain.chat.models import ChatRequest
from app.domain.chat.service import handle_chat

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

    return handle_chat(
        question=request.question,
        chat_id=request.chat_id
    )