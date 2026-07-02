from fastapi import APIRouter

router = APIRouter()


### Upload a watermarked video
@router.post("/video")
async def check_watermark():
    pass
