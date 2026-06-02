from app.rag.retrieval.vector_search import search_vectors
from app.rag.retrieval.reranker import rerank
from app.rag.ingestion.embedder import embed_text
from app.services.llm_service import generate_answer
from app.utils.context import build_context, clean_sources


def ask_question(question: str, history: list = None):

    # 1. embedding de la pregunta
    query_embedding = embed_text(question)

    # 2. retrieval
    matches = search_vectors(query_embedding)

    # fallback si no hay resultados
    if not matches:
        return {
            "answer": "No encontré información relevante en los documentos cargados.",
            "sources": []
        }

    # 3. rerank
    matches = rerank(matches)

    # safety fallback
    if not matches:
        matches = search_vectors(query_embedding)

    # 4. limpiar fuentes
    unique_sources = clean_sources(matches)

    # 5. construir contexto
    context = build_context(unique_sources, max_chars=2500)

    # 6. generar respuesta con memoria
    answer = generate_answer(
        question=question,
        context=context,
        history=history
    )

    return {
        "answer": answer,
        "sources": unique_sources
    }