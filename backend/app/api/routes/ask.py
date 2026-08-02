from fastapi import APIRouter

from app.engine.orchestrator import EngineOrchestrator
from app.schemas.ask import AskRequest

router = APIRouter()

orchestrator = EngineOrchestrator()


@router.post("")
async def ask(data: AskRequest):

    return await orchestrator.process(
        question=data.question,
        history=data.history,
    )