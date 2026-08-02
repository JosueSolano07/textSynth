from fastapi import APIRouter, File, UploadFile

from app.services.document_service import DocumentService

router = APIRouter()

document_service = DocumentService()


@router.post("")
async def upload_document(file: UploadFile = File(...)):
    return await document_service.upload(file)