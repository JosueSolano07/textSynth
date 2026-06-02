from fastapi import APIRouter, UploadFile, File
from app.rag.ingestion.ingest import ingest_document

router = APIRouter()


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):

    path = f"uploads/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    count = ingest_document(path)

    return {
        "message": "documento indexado",
        "chunks": count
    }