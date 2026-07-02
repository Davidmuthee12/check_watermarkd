from celery import Celery

from app.config import redis_settings


celery = Celery(
    "watermark",
    broker=redis_settings.REDIS_URL(0),
    backend=redis_settings.REDIS_URL(1),
)

celery.conf.task_serializer = "json"

celery.conf.result_serializer = "json"

celery.conf.accept_content = ["json"]
