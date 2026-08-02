from app.engine.context import EngineContext
from app.engine.classifier import QueryClassifier
from app.engine.router import EngineRouter
from app.engine.state import EngineState


class EngineWorkflow:
    """
    Define el flujo completo de ejecución del Engine.

    Cada petición sigue siempre el mismo proceso:

        1. Recibir pregunta
        2. Clasificar intención
        3. Seleccionar servicio
        4. Ejecutar servicio
        5. Guardar respuesta
        6. Finalizar
    """

    def __init__(self):
        self.router = EngineRouter()

    async def execute(self, context: EngineContext) -> EngineContext:

        try:

            # -----------------------------
            # 1. Pregunta recibida
            # -----------------------------

            context.set_state(EngineState.RECEIVED)

            # -----------------------------
            # 2. Clasificar intención
            # -----------------------------

            intent = QueryClassifier.classify(context.question)

            context.set_intent(intent)

            context.set_state(EngineState.CLASSIFIED)

            # -----------------------------
            # 3. Seleccionar servicio
            # -----------------------------

            context.set_state(EngineState.ROUTED)

            result = await self.router.dispatch(
                intent=context.intent,
                question=context.question,
                history=context.history,
            )

            # -----------------------------
            # 4. Guardar respuesta
            # -----------------------------

            if isinstance(result, dict):

                context.answer = result.get("answer", "")

                context.sources = result.get("sources", [])

                context.documents = result.get("documents", [])

                context.metadata.update(
                    result.get("metadata", {})
                )

            else:

                context.answer = str(result)

            # -----------------------------
            # 5. Finalizar
            # -----------------------------

            context.set_state(EngineState.COMPLETED)

        except Exception as e:

            context.set_error(str(e))

        return context