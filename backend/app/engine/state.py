from enum import Enum


class EngineState(str, Enum):
    """
    Estados internos del Engine.

    Permiten conocer en qué etapa del procesamiento
    se encuentra una petición.
    """

    IDLE = "idle"

    RECEIVED = "received"

    CLASSIFIED = "classified"

    ROUTED = "routed"

    RETRIEVING = "retrieving"

    GENERATING = "generating"

    COMPLETED = "completed"

    ERROR = "error"