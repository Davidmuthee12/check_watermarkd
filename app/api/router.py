from fastapi import APIRouter

from .routers import video

master_router = APIRouter()

master_router.include_router(video.router)
