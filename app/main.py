from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from supabase import create_client
import os
import pdfplumber
import requests
import shutil
import re

# ----------------------------
# LOAD ENV
# ----------------------------
load_dotenv()

# ----------------------------
# APP
# ----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# STORAGE
# ----------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------------------
# SUPABASE
# ----------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------
# GROQ
# ----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ----------------------------
# MODEL (LAZY LOAD - CRÍTICO)
# ----------------------------
model = None

def get_model():
    global model
    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

# ----------------------------
# CONFIG (RENDER SAFE)
# ----------------------------
MAX_PAGES = 15
MIN_CHUNK_SIZE = 40
BATCH_SIZE = 10

# ----------------------------
# UTILS
# ----------------------------
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text: str, max_words=100, overlap=20):
    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + max_words]))
        i += max_words - overlap

    return chunks

# ----------------------------
# ROOT
# ----------------------------
@app.get("/")
def root():
    return {"status": "TextSynth RAG running 🚀"}

# ----------------------------
# UPLOAD PDF → SUPABASE
# ----------------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    inserted = 0
    batch = []

    with pdfplumber.open(path) as pdf:

        for page_index, page in enumerate(pdf.pages):

            if page_index >= MAX_PAGES:
                break

            extracted = page.extract_text()
            if not extracted:
                continue

            text = clean_text(extracted)
            chunks = chunk_text(text)

            for chunk_index, chunk in enumerate(chunks):

                if len(chunk) < MIN_CHUNK_SIZE:
                    continue

                embedding = get_model().encode(chunk).tolist()

                batch.append({
                    "content": chunk,
                    "embedding": embedding,
                    "page": page_index,
                    "chunk_index": chunk_index
                })

                inserted += 1

                # batch insert
                if len(batch) >= BATCH_SIZE:
                    supabase.table("documents").insert(batch).execute()
                    batch = []

    # flush final batch
    if batch:
        supabase.table("documents").insert(batch).execute()

    return {
        "message": "uploaded successfully",
        "chunks_inserted": inserted
    }

# ----------------------------
# ASK → RAG + GROQ
# ----------------------------
@app.post("/ask")
async def ask(data: dict = Body(...)):

    question = data.get("question", "")

    if not question:
        return {"error": "question is required"}

    q_embedding = get_model().encode(question).tolist()

    response = supabase.rpc("match_documents", {
        "query_embedding": q_embedding,
        "match_count": 3
    }).execute()

    matches = response.data or []

    context = "\n".join([m["content"] for m in matches])

    prompt = f"""
Eres un asistente experto en documentos.

Responde SOLO en español, de forma clara y breve.

CONTEXTO:
{context}

PREGUNTA:
{question}
"""

    try:
        res = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1
            },
            timeout=60
        )

        res.raise_for_status()
        answer = res.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return {"error": str(e)}

    return {
        "question": question,
        "answer": answer,
        "sources": matches
    }