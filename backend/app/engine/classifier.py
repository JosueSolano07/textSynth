from enum import Enum
import re


class Intent(str, Enum):
    CHAT = "chat"
    RAG = "rag"
    EDUCATION = "education"
    MULTIMODAL = "multimodal"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class QueryClassifier:
    """
    Clasifica la intención de una consulta.

    Por ahora utiliza reglas simples.
    En el futuro podrá utilizar un LLM o un modelo local.
    """

    CHAT_PATTERNS = [
        r"\bhola\b",
        r"\bhey\b",
        r"\bhi\b",
        r"\bqué tal\b",
        r"\bcomo estas\b",
        r"\bquien eres\b",
        r"\bgracias\b",
    ]

    RAG_PATTERNS = [
        r"\bresume\b",
        r"\bresumen\b",
        r"\bsegún\b",
        r"\bsegun\b",
        r"\bdocumento\b",
        r"\bpdf\b",
        r"\barchivo\b",
        r"\btexto\b",
        r"\bcapítulo\b",
        r"\bcapitulo\b",
        r"\bexplica el documento\b",
    ]

    EDUCATION_PATTERNS = [
        r"\benséñame\b",
        r"\benseñame\b",
        r"\baprender\b",
        r"\bcurso\b",
        r"\blección\b",
        r"\bleccion\b",
        r"\bejercicio\b",
        r"\bquiz\b",
        r"\bflashcards\b",
        r"\broadmap\b",
    ]

    MULTIMODAL_PATTERNS = [
        r"\bgenera una imagen\b",
        r"\bgenera imagen\b",
        r"\bvideo\b",
        r"\baudio\b",
        r"\bnarración\b",
        r"\bnarracion\b",
        r"\bvoz\b",
        r"\banimación\b",
        r"\banimacion\b",
    ]

    SYSTEM_PATTERNS = [
        r"\bconfiguración\b",
        r"\bconfiguracion\b",
        r"\bsettings\b",
        r"\bmodelo\b",
        r"\bprovider\b",
        r"\bproveedor\b",
    ]

    @classmethod
    def classify(cls, question: str) -> Intent:
        """
        Devuelve la intención principal de la consulta.
        """

        if not question:
            return Intent.UNKNOWN

        text = question.lower().strip()

        if cls._matches(text, cls.SYSTEM_PATTERNS):
            return Intent.SYSTEM

        if cls._matches(text, cls.MULTIMODAL_PATTERNS):
            return Intent.MULTIMODAL

        if cls._matches(text, cls.EDUCATION_PATTERNS):
            return Intent.EDUCATION

        if cls._matches(text, cls.RAG_PATTERNS):
            return Intent.RAG

        if cls._matches(text, cls.CHAT_PATTERNS):
            return Intent.CHAT

        return Intent.CHAT

    @staticmethod
    def _matches(text: str, patterns: list[str]) -> bool:
        """
        Comprueba si el texto coincide con alguno
        de los patrones definidos.
        """

        return any(re.search(pattern, text) for pattern in patterns)