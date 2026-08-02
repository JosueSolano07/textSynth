from fastapi import APIRouter

from app.services.chat_service import ChatService

router = APIRouter()

chat_service = ChatService()


@router.get("")
async def list_chats():
    return await chat_service.list_chats()


@router.get("/{chat_id}")
async def get_chat(chat_id: str):
    return await chat_service.get_chat(chat_id)


@router.post("")
async def create_chat():
    return await chat_service.create_chat()


@router.delete("/{chat_id}")
async def delete_chat(chat_id: str):
    return await chat_service.delete_chat(chat_id)