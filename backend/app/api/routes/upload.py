from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.rag.ingestion.pdf_loader import load_pdf
from app.rag.ingestion.ingest import ingest_document

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks_inserted = ingest_document(path)

    return {
        "message": "uploaded successfully",
        "chunks_inserted": chunks_inserted
    }