from enum import Enum
from pathlib import Path

BASE_DIR = Path("storage")

VIDEO_DIR = BASE_DIR / "videos"
FRAME_DIR = BASE_DIR / "frames"
MIN_FRAME_INTERVAL_SECONDS = 1.0
FRAME_WIDTH = 960
OCR_CONFIDENCE_THRESHOLD = 0.30

VIDEO_DIR.mkdir(parents=True, exist_ok=True)
FRAME_DIR.mkdir(parents=True, exist_ok=True)


class FramePosition(str, Enum):
    START = "start"
    MIDDLE = "middle"
    END = "end"


PLATFORM_WATERMARKS = {
    "TikTok": [
        "tiktok",
        "tik tok",
        "douyin",
    ],
    "CapCut": [
        "capcut",
        "cap cut",
    ],
    "Instagram": [
        "instagram",
        "insta",
        "reel",
        "reels",
    ],
    "Likee": [
        "likee",
    ],
    "YouTube": [
        "youtube",
        "you tube",
        "shorts",
    ],
    "Snapchat": [
        "snapchat",
        "snap",
    ],
}

WATERMARK_IDENTIFIERS = [
    keyword for keywords in PLATFORM_WATERMARKS.values() for keyword in keywords
]
