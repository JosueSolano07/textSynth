from app.engine.classifier import Intent
from app.services.chat_service import ChatService
from app.services.document_service import DocumentService
from app.services.education_service import EducationService
from app.services.multimodal_service import MultimodalService


class EngineRouter:
    """
    Enruta cada intención al servicio correspondiente.
    """

    def __init__(self):

        self.chat = ChatService()

        self.documents = DocumentService()

        self.education = EducationService()

        self.multimodal = MultimodalService()

    # ---------------------------------------------------------

    async def dispatch(
        self,
        intent: Intent,
        question: str,
        history: list | None = None,
    ):

        history = history or []

        match intent:

            case Intent.CHAT:

                return await self.chat.chat(
                    message=question,
                    history=history,
                )

            case Intent.RAG:

                return await self.chat.ask(
                    question=question,
                    history=history,
                )

            case Intent.EDUCATION:

                return await self.education.process(
                    question=question,
                    history=history,
                )

            case Intent.MULTIMODAL:

                return await self.multimodal.process(
                    question=question,
                    history=history,
                )

            case _:

                return await self.chat.chat(
                    message=question,
                    history=history,
                )