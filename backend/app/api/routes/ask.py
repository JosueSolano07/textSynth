from fastapi import APIRouter, Body
from app.rag.pipeline import ask_question

router = APIRouter()


@router.post("/ask")
async def ask(data: dict = Body(...)):

    question = data.get("question", "").strip()

    if not question:
        return {"error": "question is required"}

    return ask_question(question)