from pydantic import BaseModel


class Video(BaseModel):
    video_url: str
