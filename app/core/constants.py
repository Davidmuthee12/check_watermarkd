from enum import Enum
from pathlib import Path

BASE_DIR = Path("storage")

VIDEO_DIR = BASE_DIR / "videos"
FRAME_DIR = BASE_DIR / "frames"

VIDEO_DIR.mkdir(parents=True, exist_ok=True)
FRAME_DIR.mkdir(parents=True, exist_ok=True)


class FramePosition(str, Enum):
    START = "start"
    MIDDLE = "middle"
    END = "end"


WATERMARK_IDENTIFIERS = [
    "tiktok",
    "capcut",
    "instagram",
    "likee",
    "youtube",
    "reel",
    "snapchat",
]
