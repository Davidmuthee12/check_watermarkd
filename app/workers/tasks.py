from app.workers.celery import celery

from app.services.video import VideoService

from app.api.schemas.video import VideoRequest


@celery.task
def process_video(url: str):

    import asyncio

    service = VideoService()

    return asyncio.run(
        service.check_watermarked(
            VideoRequest(
                video_url=url,
            )
        )
    ).model_dump()
