import redis

from backend.app.core.config import get_settings

settings = get_settings()

redis_client = redis.Redis(
    host="127.0.0.1",
    port=6379,
    password=settings.redis_password,
    decode_responses=True,
)