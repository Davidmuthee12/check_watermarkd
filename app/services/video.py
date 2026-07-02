import asyncio
import time
from pathlib import Path

from app.api.schemas.video import VideoRequest
from app.api.schemas.response import WatermarkResponse

from app.services.cleanup import CleanupService
from app.services.detector import WatermarkDetector
from app.services.downloader import VideoDownloader
from app.services.extractor import FrameExtractor

from app.core.constants import FramePosition


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

        video_path = await self.downloader.download(str(request.video_url))

        frame_tasks = [
            self.extractor.extract(
                video_path,
                FramePosition.START,
            ),
            self.extractor.extract(
                video_path,
                FramePosition.MIDDLE,
            ),
            self.extractor.extract(
                video_path,
                FramePosition.END,
            ),
        ]

        frame_paths = await asyncio.gather(*frame_tasks)

        detector_tasks = [
            asyncio.to_thread(
                self.detector.detect,
                frame,
            )
            for frame in frame_paths
        ]

        detections = await asyncio.gather(*detector_tasks)

        detected_platforms = sorted(
            {platform for result in detections for platform in result}
        )

        finished = time.perf_counter()

        self.cleanup.cleanup()

        return WatermarkResponse(
            watermarked=len(detected_platforms) > 0,
            detected_platforms=detected_platforms,
            processing_time=round(
                finished - started,
                2,
            ),
        )
