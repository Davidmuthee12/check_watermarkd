import json

import redis.asyncio as redis

from app.config import redis_settings


class RedisRepository:
    def __init__(self):

        self.client = redis.from_url(
            redis_settings.REDIS_URL(0),
            decode_responses=True,
        )

    async def save(
        self,
        key,
        value,
    ):

        await self.client.set(
            key,
            json.dumps(value),
        )

    async def get(
        self,
        key,
    ):

        value = await self.client.get(key)

        if value is None:
            return None

        return json.loads(value)
