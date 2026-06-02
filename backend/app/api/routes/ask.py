from fastapi import APIRouter
from app.domain.schemas import AskRequest
from app.rag.query.ask import ask_question

router = APIRouter()


@router.post("")
async def ask(data: AskRequest):

    question = data.question.strip()

    if not question:
        return {"error": "question is required"}

    return ask_question(
        question=question,
        history=data.history
    )