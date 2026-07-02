from app.api.schemas.video import Video
from app.services.watermarkd import Watermarked


class VideoService(Watermarked):
    def __init__(self):
        pass

    async def check_watermarked(self, checkVideo: Video):
        return await self._check_if_watermarkd(checkVideo.video_url)
