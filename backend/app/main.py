from fastapi import FastAPI
from app.core.config import settings

from app.api.middleware import register_middlewares
from app.api.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

register_middlewares(app)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "status": "running",
        "application": "TextSynth"
    }