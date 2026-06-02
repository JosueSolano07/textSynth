from app.rag.pipeline import ingest_document, ask_question


class RAGService:

    def ingest(self, file_path: str):
        return ingest_document(file_path)

    def ask(self, question: str):
        return ask_question(question)