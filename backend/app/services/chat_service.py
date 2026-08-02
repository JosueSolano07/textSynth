from app.llm.manager import LLMManager
from app.llm.prompt_builder import PromptBuilder
from app.services.rag_service import RAGService


class ChatService:
    """
    Servicio principal de conversación.

    Coordina:
    - Recuperación de contexto (RAG)
    - Construcción del prompt
    - Consulta al LLM
    """

    def __init__(self):

        self.rag = RAGService()

        self.llm = LLMManager()

    # ---------------------------------------------------------

    async def ask(
        self,
        question: str,
        history: list | None = None,
    ) -> dict:

        history = history or []

        context = await self.rag.build_context(question)

        messages = PromptBuilder.build_chat_messages(
            question=question,
            context=context,
            history=history,
        )

        answer = await self.llm.chat(messages)

        return {

            "success": True,

            "question": question,

            "answer": answer,

            "context_found": bool(context),

            "sources": [],

        }

    # ---------------------------------------------------------

    async def chat(
        self,
        message: str,
        history: list | None = None,
    ) -> dict:

        return await self.ask(
            question=message,
            history=history,
        )