from app.db.supabase_client import supabase


def search_vectors(question_embedding):

    response = supabase.rpc("match_documents", {
        "query_embedding": question_embedding,
        "match_count": 5
    }).execute()

    return response.data or []