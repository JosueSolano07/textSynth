from fastapi import APIRouter

from app.services.settings_service import SettingsService

router = APIRouter()

settings_service = SettingsService()


@router.get("")
async def get_settings():
    return await settings_service.get_settings()


@router.put("")
async def update_settings(data: dict):
    return await settings_service.update_settings(data)