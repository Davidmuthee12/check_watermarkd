from functools import lru_cache

from app.services.video import VideoService


@lru_cache
def get_video_service():

    return VideoService()
