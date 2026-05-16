from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

import shutil
import pdfplumber
import numpy as np
import re
import hashlib
import faiss
import requests

from sentence_transformers import SentenceTransformer

app = FastAPI()

# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# CONFIG
# ----------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ----------------------------
# MEMORY LIGHT STORAGE
# ----------------------------
texts = []
embeddings_list = []
index = None

# ----------------------------
# LAZY MODEL (IMPORTANTE)
# ----------------------------
embedding_model = None

def get_model():
    global embedding_model
    if embedding_model is None:
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return embedding_model


# ----------------------------
# ROOT
# ----------------------------
@app.get("/")
def root():
    return {"status": "TextSynth Production Ready 🚀"}


# ----------------------------
# UTILS
# ----------------------------
def clean_text(text: str):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def make_hash(text: str):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def chunk_text(text: str, max_words=100):
    sentences = re.split(r"\. |\n", text)
    chunks = []
    current = []

    for s in sentences:
        s = s.strip()
        if not s:
            continue

        current.append(s)

        if len(" ".join(current).split()) >= max_words:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


# ----------------------------
# FAISS BUILD (LIGHT)
# ----------------------------
def build_faiss():
    global index

    if len(embeddings_list) == 0:
        return

    vectors = np.array(embeddings_list).astype("float32")

    faiss.normalize_L2(vectors)

    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)


# ----------------------------
# UPLOAD PDF
# ----------------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + " "

    text = clean_text(text)
    chunks = chunk_text(text)

    model = get_model()
    embeddings = model.encode(chunks)

    seen = set()
    added = 0

    for i, chunk in enumerate(chunks):

        if len(chunk) < 40:
            continue

        h = make_hash(chunk)
        if h in seen:
            continue

        seen.add(h)

        texts.append(chunk)
        embeddings_list.append(embeddings[i])

        added += 1

    build_faiss()

    return {
        "chunks_added": added,
        "total_documents": len(texts)
    }


# ----------------------------
# ASK
# ----------------------------
@app.post("/ask")
async def ask(data: dict = Body(...)):

    if index is None:
        return {"error": "No hay documentos cargados"}

    question = data.get("question", "").strip().lower()

    model = get_model()

    q_emb = model.encode(question).astype("float32")
    q_emb = np.array([q_emb])
    faiss.normalize_L2(q_emb)

    scores, ids = index.search(q_emb, 3)

    top = []

    for i, idx in enumerate(ids[0]):
        if idx == -1:
            continue

        top.append({
            "chunk": texts[idx],
            "similarity": float(scores[0][i])
        })

    context = "\n".join([t["chunk"][:300] for t in top])

    prompt = f"""
Responde SOLO en español, breve.

CONTEXTO:
{context}

PREGUNTA:
{question}

RESPUESTA:
"""

    if not GROQ_API_KEY:
        return {"error": "Falta GROQ_API_KEY"}

    try:
        response = requests.post(
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

        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return {"error": str(e)}

    return {
        "question": question,
        "answer": result,
        "sources": top
    }