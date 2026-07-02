import time

from app.api.schemas.video import VideoRequest
from app.api.schemas.response import WatermarkResponse

from app.services.cleanup import CleanupService
from app.services.detector import WatermarkDetector
from app.services.downloader import VideoDownloader
from app.services.extractor import FrameExtractor


class VideoService:
    def __init__(self):

        self.downloader = VideoDownloader()

        self.extractor = FrameExtractor()

        self.detector = WatermarkDetector()

        self.cleanup = CleanupService()

    async def check_watermarked(
        self,
        request: VideoRequest,
    ) -> WatermarkResponse:

        started = time.perf_counter()

        try:
            video_path = await self.downloader.download(str(request.video_url))

            frame_paths = await self.extractor.extract(video_path)

            detections = [
                self.detector.detect(frame)
                for frame in frame_paths
            ]

            detected_platforms = sorted(
                {platform for result in detections for platform in result}
            )

            finished = time.perf_counter()
        finally:
            self.cleanup.cleanup()

        return WatermarkResponse(
            watermarked=len(detected_platforms) > 0,
            detected_platforms=detected_platforms,
            processing_time=round(
                finished - started,
                2,
            ),
        )
