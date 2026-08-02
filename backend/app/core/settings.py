from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    # --------------------------------------------------
    # App
    # --------------------------------------------------

    APP_NAME: str = "TextSynth"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    # --------------------------------------------------
    # Storage
    # --------------------------------------------------

    STORAGE_FOLDER: str = "storage"

    UPLOAD_FOLDER: str = "storage/uploads"

    VECTOR_FOLDER: str = "storage/vectors"

    CACHE_FOLDER: str = "storage/cache"

    TEMP_FOLDER: str = "storage/temp"

    EXPORT_FOLDER: str = "storage/exports"

    MODEL_FOLDER: str = "storage/models"

    LOG_FOLDER: str = "storage/logs"

    # --------------------------------------------------
    # LLM
    # --------------------------------------------------

    LLM_PROVIDER: str = "ollama"

    LLM_MODEL: str = "llama3.1:8b"

    OLLAMA_URL: str = "http://localhost:11434"

    EMBEDDING_MODEL: str = "nomic-embed-text"

    # --------------------------------------------------
    # RAG
    # --------------------------------------------------

    TOP_K: int = 5

    CHUNK_SIZE: int = 800

    CHUNK_OVERLAP: int = 100

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @property
    def storage_path(self) -> Path:
        return Path(self.STORAGE_FOLDER)

    @property
    def upload_path(self) -> Path:
        return Path(self.UPLOAD_FOLDER)

    @property
    def vector_path(self) -> Path:
        return Path(self.VECTOR_FOLDER)


settings = Settings()