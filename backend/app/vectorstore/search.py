from app.db.supabase_client import supabase


def insert_chunks(batch):
    if batch:
        supabase.table("documents").insert(batch).execute()