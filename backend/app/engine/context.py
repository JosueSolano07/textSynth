from dataclasses import dataclass, field
from typing import Any

from app.engine.classifier import Intent
from app.engine.state import EngineState


@dataclass
class EngineContext:
    """
    Contexto compartido durante todo el ciclo de vida
    de una petición dentro del Engine.

    Este objeto viaja entre el classifier, router,
    servicios, RAG, LLM y cualquier otro componente.
    """

    # ==========================
    # Entrada
    # ==========================

    question: str

    history: list = field(default_factory=list)

    session_id: str | None = None

    user_id: str | None = None

    # ==========================
    # Estado del Engine
    # ==========================

    state: EngineState = EngineState.IDLE

    intent: Intent = Intent.UNKNOWN

    # ==========================
    # Contexto documental (RAG)
    # ==========================

    documents: list = field(default_factory=list)

    sources: list = field(default_factory=list)

    # ==========================
    # Respuesta
    # ==========================

    answer: str = ""

    # ==========================
    # Información adicional
    # ==========================

    metadata: dict[str, Any] = field(default_factory=dict)

    success: bool = True

    error: str | None = None

    # ==========================
    # Utilidades
    # ==========================

    def set_state(self, state: EngineState) -> None:
        """
        Actualiza el estado actual del Engine.
        """
        self.state = state

    def set_intent(self, intent: Intent) -> None:
        """
        Guarda la intención detectada.
        """
        self.intent = intent

    def add_documents(self, documents: list) -> None:
        """
        Agrega documentos recuperados por el RAG.
        """
        self.documents.extend(documents)

    def add_sources(self, sources: list) -> None:
        """
        Agrega las fuentes utilizadas.
        """
        self.sources.extend(sources)

    def set_answer(self, answer: str) -> None:
        """
        Guarda la respuesta generada.
        """
        self.answer = answer

    def set_error(self, error: str) -> None:
        """
        Marca el contexto como fallido.
        """
        self.success = False
        self.error = error
        self.state = EngineState.ERROR

    def to_dict(self) -> dict:
        """
        Convierte el contexto en un diccionario
        serializable.
        """
        return {
            "question": self.question,
            "history": self.history,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "state": self.state.value,
            "intent": self.intent.value,
            "documents": self.documents,
            "sources": self.sources,
            "answer": self.answer,
            "metadata": self.metadata,
            "success": self.success,
            "error": self.error,
        }