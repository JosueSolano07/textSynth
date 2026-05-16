from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

import os
import shutil
import pdfplumber
import numpy as np
import re
import hashlib
import requests
import faiss
import json

from sentence_transformers import SentenceTransformer

# ----------------------------
# ENV
# ----------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# print("GROQ:", "OK" if GROQ_API_KEY else "MISSING")

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
# CONFIG
# ----------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"

# ----------------------------
# STORAGE
# ----------------------------
texts = []
embeddings_list = []
index = None

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


def chunk_text(text: str, max_words=120):
    sentences = re.split(r'(?<=[.!?])\s+', text)

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
# FAISS
# ----------------------------
def build_faiss():
    global index

    if not embeddings_list:
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
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "

    text = clean_text(text)
    chunks = chunk_text(text)
    embeddings = embedding_model.encode(chunks)

    seen = set()
    added = 0

    for i, chunk in enumerate(chunks):
        if len(chunk) < 30:
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
# ASK (NORMAL)
# ----------------------------
@app.post("/ask")
async def ask(data: dict = Body(...)):

    question = data.get("question", "").strip().lower()

    if index is None:
        return {"error": "No hay documentos cargados"}

    if not GROQ_API_KEY:
        return {"error": "Falta GROQ_API_KEY"}

    q_emb = embedding_model.encode(question).astype("float32")
    q_emb = np.array([q_emb])
    faiss.normalize_L2(q_emb)

    scores, ids = index.search(q_emb, 8)

    top = []
    for i, idx in enumerate(ids[0]):
        if idx == -1:
            continue
        top.append(texts[idx])

    context = "\n".join([t for t in top])

    prompt = f"""
        Eres un sistema de recuperación de información (RAG).

        REGLAS ESTRICTAS:
        - NO eres un asistente conversacional
        - NO inventes información
        - NO respondas fuera del contexto
        - NO des opiniones ni interpretaciones
        - Responde SOLO usando el contexto proporcionado
        - Si la respuesta no está en el contexto: responde exactamente "No encontrado"

        FORMATO:
        - Respuestas cortas
        - Directas
        - Sin explicaciones adicionales

        CONTEXTO:
        {context}

        PREGUNTA:
        {question}

        RESPUESTA:
        """.strip()

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
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

# ----------------------------
# ASK STREAM (CHATGPT STYLE)
# ----------------------------
@app.post("/ask-stream")
async def ask_stream(data: dict = Body(...)):

    question = data.get("question", "").strip().lower()

    if index is None:
        return {"error": "No hay documentos cargados"}

    if not GROQ_API_KEY:
        return {"error": "Falta GROQ_API_KEY"}

    q_emb = embedding_model.encode(question).astype("float32")
    q_emb = np.array([q_emb])
    faiss.normalize_L2(q_emb)

    scores, ids = index.search(q_emb, 8)

    top = [
        texts[idx] for idx in ids[0] if idx != -1
    ]

    context = "\n".join([t[:200] for t in top[:2]])

    prompt = f"""
Eres un asistente experto en documentos.

CONTEXTO:
{context}

PREGUNTA:
{question}

RESPUESTA:
""".strip()

    def generate():
        try:
            response = requests.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "stream": True
                },
                stream=True
            )

            for line in response.iter_lines():
                if line:
                    yield line.decode("utf-8") + "\n"

        except Exception as e:
            yield json.dumps({"error": str(e)})

    return StreamingResponse(generate(), media_type="text/plain")