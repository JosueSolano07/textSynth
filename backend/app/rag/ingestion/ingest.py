import os

from app.rag.ingestion.pdf_loader import load_pdf
from app.rag.ingestion.chunker import chunk_text
from app.rag.ingestion.embedder import embed_text
from app.db.queries import insert_chunks


def ingest_document(path: str):
    pages = load_pdf(path)

    batch = []
    filename = os.path.basename(path)

    for page in pages:
        page_index = int(page["page"])
        text = page["content"]

        chunks = chunk_text(text)

        for chunk_index, chunk in enumerate(chunks):

            chunk = chunk.strip()
            if not chunk:
                continue

            embedding = embed_text(chunk)

            batch.append({
                "document_name": filename,
                "content": chunk,
                "embedding": embedding,
                "chunk_index": chunk_index,
                "page": page_index
            })

    if batch:
        insert_chunks(batch)

    return len(batch)