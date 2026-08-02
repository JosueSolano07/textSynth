from app.engine.context import EngineContext
from app.engine.workflow import EngineWorkflow


class EnginePipeline:
    """
    Ejecuta el flujo completo del Engine.

    El Pipeline es el encargado de recibir un EngineContext,
    recorrer el Workflow y devolver el contexto actualizado.
    """

    def __init__(self):
        self.workflow = EngineWorkflow()

    async def run(self, context: EngineContext) -> EngineContext:
        """
        Ejecuta el Workflow completo.
        """

        context = await self.workflow.execute(context)

        return context