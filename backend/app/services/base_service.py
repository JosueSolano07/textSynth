from pathlib import Path

from app.core.config import settings


class BaseService:
    """
    Clase base para todos los servicios.

    Centraliza recursos compartidos del backend.
    """

    def __init__(self):

        self.settings = settings

        self.storage = Path(settings.STORAGE_FOLDER)

        self.uploads = Path(settings.UPLOAD_FOLDER)

        self.cache = Path(settings.CACHE_FOLDER)

        self.exports = Path(settings.EXPORT_FOLDER)

        self.logs = Path(settings.LOG_FOLDER)

        self.models = Path(settings.MODEL_FOLDER)

        self.temp = Path(settings.TEMP_FOLDER)

        self.vectors = Path(settings.VECTOR_FOLDER)

        for folder in (
            self.storage,
            self.uploads,
            self.cache,
            self.exports,
            self.logs,
            self.models,
            self.temp,
            self.vectors,
        ):

            folder.mkdir(
                parents=True,
                exist_ok=True,
            )