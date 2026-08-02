from fastapi import APIRouter

from app.services.document_service import DocumentService

router = APIRouter()

document_service = DocumentService()


@router.post("/{document_id}")
async def ingest(document_id: str):
    return await document_service.ingest(document_id)