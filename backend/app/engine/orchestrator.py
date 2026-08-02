from app.engine.context import EngineContext
from app.engine.pipeline import EnginePipeline


class EngineOrchestrator:
    """
    Punto de entrada del Engine.

    El Orchestrator no contiene lógica de negocio.
    Su única responsabilidad es:

    - Crear el contexto inicial.
    - Ejecutar el Pipeline.
    - Devolver la respuesta final.
    """

    def __init__(self):
        self.pipeline = EnginePipeline()

    async def process(
        self,
        question: str,
        history: list | None = None,
        session_id: str | None = None,
        user_id: str | None = None,
    ) -> dict:

        question = question.strip()

        if not question:
            return {
                "success": False,
                "answer": "La pregunta está vacía.",
                "intent": "unknown",
            }

        context = EngineContext(
            question=question,
            history=history or [],
            session_id=session_id,
            user_id=user_id,
        )

        context = await self.pipeline.run(context)

        return context.to_dict()