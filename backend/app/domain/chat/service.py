from app.rag.query.ask import ask_question


def handle_chat(question: str, chat_id: str = None):

    result = ask_question(question)

    return {
        "chat_id": chat_id or "default",
        "answer": result["answer"],
        "sources": result["sources"]
    }