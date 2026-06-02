from fastapi import APIRouter

from app.api.routes import ask, chat, ingest, upload

api_router = APIRouter()

api_router.include_router(ask.router, prefix="/ask", tags=["ask"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])