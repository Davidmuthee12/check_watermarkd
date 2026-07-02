from pathlib import Path
from uuid import uuid4

import yt_dlp

from app.core.constants import VIDEO_DIR


class VideoDownloader:
    def __init__(self):
        self.download_dir = VIDEO_DIR

    async def download(self, url: str) -> Path:

        filename = str(uuid4())

        output_template = str(self.download_dir / f"{filename}.%(ext)s")

        ydl_opts = {
            "outtmpl": output_template,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "quiet": True,
            "noprogress": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return self.download_dir / f"{filename}.mp4"
