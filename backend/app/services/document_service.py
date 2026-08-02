from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.rag.ingestion.ingest import IngestionPipeline
from app.services.base_service import BaseService


class DocumentService(BaseService):
    """
    Servicio encargado de gestionar documentos.

    Casos de uso:

    - Subir documentos
    - Ingerir documentos
    - Reindexar
    - Eliminar
    - Listar documentos
    """

    def __init__(self):

        super().__init__()

        self.pipeline = IngestionPipeline()

    # ---------------------------------------------------------
    # Upload
    # ---------------------------------------------------------

    async def upload(
        self,
        file: UploadFile,
    ) -> dict:

        extension = Path(file.filename).suffix.lower()

        filename = f"{uuid4().hex}{extension}"

        filepath = self.uploads / filename

        with open(filepath, "wb") as buffer:
            buffer.write(await file.read())

        result = await self.pipeline.ingest(filepath)

        result.update(
            {
                "original_filename": file.filename,
                "stored_filename": filename,
            }
        )

        return result

    # ---------------------------------------------------------
    # Reindex
    # ---------------------------------------------------------

    async def reindex(
        self,
        filename: str,
    ) -> dict:

        filepath = self.uploads / filename

        if not filepath.exists():

            return {
                "success": False,
                "message": "Documento no encontrado.",
            }

        return await self.pipeline.ingest(filepath)

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    async def delete(
        self,
        filename: str,
    ) -> dict:

        filepath = self.uploads / filename

        if not filepath.exists():

            return {
                "success": False,
                "message": "Documento no encontrado.",
            }

        filepath.unlink()

        return {
            "success": True,
            "message": "Documento eliminado.",
        }

    # ---------------------------------------------------------
    # Exists
    # ---------------------------------------------------------

    async def exists(
        self,
        filename: str,
    ) -> bool:

        return (self.uploads / filename).exists()

    # ---------------------------------------------------------
    # List
    # ---------------------------------------------------------

    async def list_documents(self) -> list[str]:

        return sorted(

            file.name

            for file in self.uploads.iterdir()

            if file.is_file()

        )