from fastapi import APIRouter
from ..schemas.video import Video
from app.services.video import VideoService

router = APIRouter()


### Upload a watermarked video
@router.post("/video")
async def check_watermark(video: Video):
    service = VideoService()
    return await service.check_watermarked(video)
