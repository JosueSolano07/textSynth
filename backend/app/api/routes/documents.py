from fastapi import APIRouter

from app.services.document_service import DocumentService

router = APIRouter()

document_service = DocumentService()


@router.get("")
async def list_documents():
    return await document_service.list_documents()


@router.get("/{document_id}")
async def get_document(document_id: str):
    return await document_service.get_document(document_id)


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    return await document_service.delete_document(document_id)