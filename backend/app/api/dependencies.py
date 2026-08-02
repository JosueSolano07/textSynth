from functools import lru_cache

from app.services.chat_service import ChatService
from app.services.document_service import DocumentService
from app.services.settings_service import SettingsService


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService()


@lru_cache
def get_document_service() -> DocumentService:
    return DocumentService()


@lru_cache
def get_settings_service() -> SettingsService:
    return SettingsService()