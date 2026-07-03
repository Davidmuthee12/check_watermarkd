from pathlib import Path
from uuid import uuid4

import yt_dlp
from yt_dlp.utils import DownloadError

from app.core.constants import VIDEO_DIR


class VideoDownloader:
    def __init__(self):
        self.download_dir = VIDEO_DIR

    async def download(self, url: str) -> Path:

        filename = str(uuid4())

        output_template = str(self.download_dir / f"{filename}.%(ext)s")

        ydl_opts = {
            "outtmpl": output_template,
            "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best",
            "merge_output_format": "mp4",
            "noplaylist": True,
            "retries": 3,
            "fragment_retries": 3,
            "socket_timeout": 30,
            "quiet": True,
            "noprogress": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded = Path(ydl.prepare_filename(info))
        except DownloadError as exc:
            raise RuntimeError(f"Unable to download video: {exc}") from exc

        merged = self.download_dir / f"{filename}.mp4"

        if merged.exists():
            return merged

        if downloaded.exists():
            return downloaded

        raise FileNotFoundError(f"Downloaded video was not found for {url}")
