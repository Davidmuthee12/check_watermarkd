from fastapi import APIRouter
from ..schemas.video import Video

router = APIRouter()


### Upload a watermarked video
@router.post("/video")
async def check_watermark(video: Video):
    pass
