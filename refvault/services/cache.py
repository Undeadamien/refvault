import json
import logging
from typing import Any, Optional

from redis.asyncio import Redis

from refvault.config import settings

logger = logging.getLogger(__name__)

_client: Optional[Redis] = None
_available = False


def key(*parts: str) -> str:
    return ":".join(["refvault", *parts])


async def init() -> None:
    global _client, _available
    try:
        _client = Redis.from_url(settings.redis_url, decode_responses=True)
        await _client.ping()
        _available = True
        logger.info("Redis connected at %s", settings.redis_url)
    except Exception as e:
        _client = None
        _available = False
        logger.warning("Redis unavailable, cache disabled: %s", e)


async def close() -> None:
    global _client, _available
    if _client is not None:
        await _client.close()
    _client = None
    _available = False


async def get(key: str) -> Any:
    if not _available or _client is None:
        return None
    try:
        data = await _client.get(key)
        if data is None:
            return None
        return json.loads(data)
    except Exception as e:
        logger.warning("cache get error: %s", e)
        return None


async def set(key: str, value: Any, ttl: Optional[int] = None) -> None:
    if not _available or _client is None:
        return
    try:
        await _client.set(
            key, json.dumps(value, default=str), ex=ttl or settings.cache_ttl
        )
    except Exception as e:
        logger.warning("cache set error: %s", e)


async def delete(key: str) -> None:
    if not _available or _client is None:
        return
    try:
        await _client.delete(key)
    except Exception as e:
        logger.warning("cache delete error: %s", e)


async def delete_pattern(pattern: str) -> None:
    if not _available or _client is None:
        return
    try:
        cursor = 0
        while True:
            cursor, keys = await _client.scan(cursor, match=pattern, count=100)
            if keys:
                await _client.delete(*keys)
            if cursor == 0:
                break
    except Exception as e:
        logger.warning("cache delete_pattern error: %s", e)
