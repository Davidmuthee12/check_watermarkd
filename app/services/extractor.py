from pathlib import Path
import asyncio
import json

from app.core.constants import (
    FRAME_DIR,
    FRAME_WIDTH,
    MAX_EXTRACTED_FRAMES,
    MIN_FRAME_INTERVAL_SECONDS,
)


class FrameExtractor:
    async def get_duration(
        self,
        video_path: Path,
    ) -> float:

        process = await asyncio.create_subprocess_exec(
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            str(video_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(stderr.decode())

        metadata = json.loads(stdout)

        return float(metadata["format"]["duration"])

    async def extract(
        self,
        video_path: Path,
    ) -> list[Path]:

        duration = await self.get_duration(video_path)

        interval = max(
            duration / MAX_EXTRACTED_FRAMES,
            MIN_FRAME_INTERVAL_SECONDS,
        )
        output_pattern = FRAME_DIR / f"{video_path.stem}_%03d.jpg"
        video_filter = (
            f"fps=1/{interval},"
            f"scale={FRAME_WIDTH}:-2:force_original_aspect_ratio=decrease,"
            "format=gray"
        )

        process = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(video_path),
            "-vf",
            video_filter,
            "-frames:v",
            str(MAX_EXTRACTED_FRAMES),
            "-q:v",
            "2",
            str(output_pattern),
            "-y",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(stderr.decode())

        frames = sorted(FRAME_DIR.glob(f"{video_path.stem}_*.jpg"))

        if not frames:
            raise RuntimeError("ffmpeg did not extract any frames")

        return frames
