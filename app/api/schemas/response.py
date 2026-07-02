from pydantic import BaseModel


class WatermarkResponse(BaseModel):
    watermarked: bool
    detected_platforms: list[str]
    processing_time: float
