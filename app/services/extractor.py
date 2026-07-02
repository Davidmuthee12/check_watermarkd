from pathlib import Path
import asyncio
import json

from app.core.constants import FRAME_DIR


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

    async def extract_frame(
        self,
        video_path: Path,
        second: float,
        output: Path,
    ) -> Path:

        process = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-ss",
            str(second),
            "-i",
            str(video_path),
            "-frames:v",
            "1",
            "-q:v",
            "1",
            str(output),
            "-y",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(stderr.decode())

        return output

    async def extract(
        self,
        video_path: Path,
    ) -> list[Path]:

        duration = await self.get_duration(video_path)

        positions = [
            duration * 0.10,
            duration * 0.50,
            duration * 0.90,
        ]

        outputs = [FRAME_DIR / f"{video_path.stem}_{i}.jpg" for i in range(3)]

        tasks = [
            self.extract_frame(
                video_path,
                second,
                output,
            )
            for second, output in zip(
                positions,
                outputs,
            )
        ]

        return await asyncio.gather(*tasks)
