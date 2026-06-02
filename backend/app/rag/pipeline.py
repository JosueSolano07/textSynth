import os

from app.rag.ingestion.pdf_loader import load_pdf
from app.rag.ingestion.chunker import chunk_text
from app.rag.ingestion.embedder import embed_text

from app.rag.retrieval.vector_search import search_vectors
from app.rag.retrieval.reranker import rerank
from app.services.llm_service import generate_answer

from app.db.queries import insert_chunks


# =========================
# INGESTION
# =========================

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


# =========================
# HELPERS
# =========================

def build_context(chunks, max_chars=2500):
    context = ""
    used = 0

    for c in chunks:
        text = (c.get("content") or "").strip()
        if not text:
            continue

        if used + len(text) > max_chars:
            break

        context += text + "\n\n"
        used += len(text)

    return context.strip()


def clean_sources(chunks):
    seen = set()
    cleaned = []

    for c in chunks:
        content = (c.get("content") or "").strip()
        if not content:
            continue

        cid = c.get("id", "no-id")

        key = (cid, content[:120].lower())

        if key in seen:
            continue

        seen.add(key)

        cleaned.append({
            "id": cid,
            "content": content,
            "score": round(float(c.get("score", 0)), 4),
            "page": c.get("page"),
            "document_name": c.get("document_name")
        })

    return cleaned


# =========================
# PIPELINE PRINCIPAL
# =========================

def ask_question(question: str):

    query_embedding = embed_text(question)

    # 1. retrieval vectorial
    matches = search_vectors(query_embedding)

    print("MATCHES:", len(matches))

    if not matches:
        return {
            "question": question,
            "answer": "No se encontró información relevante en los documentos.",
            "sources": []
        }

    # =========================
    # 2. RERANK (IMPORTANTE)
    # =========================
    matches = rerank(matches)

    # seguridad: reranker nunca debe vaciar todo
    if not matches:
        matches = search_vectors(query_embedding)

    # =========================
    # 3. SOURCES LIMPIAS
    # =========================
    unique_sources = clean_sources(matches)

    print("UNIQUE:", len(unique_sources))

    # =========================
    # 4. CONTEXTO
    # =========================
    context = build_context(unique_sources)

    print("CONTEXT SAMPLE:", context[:300])

    # =========================
    # 5. GENERACIÓN
    # =========================
    answer = generate_answer(question, context)

    return {
        "question": question,
        "answer": answer,
        "sources": unique_sources
    }