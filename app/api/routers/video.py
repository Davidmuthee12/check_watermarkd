from celery.result import AsyncResult
from fastapi import APIRouter

from app.api.schemas.video import VideoRequest
from app.workers.celery import celery
from app.workers.tasks import process_video

router = APIRouter()


@router.post("/video")
async def upload(
    request: VideoRequest,
):

    task = process_video.delay(str(request.video_url))

    return {
        "job_id": task.id,
    }


@router.get("/video/{job_id}")
async def status(
    job_id: str,
):

    task = AsyncResult(
        job_id,
        app=celery,
    )

    return {
        "status": task.status,
        "result": task.result,
    }
