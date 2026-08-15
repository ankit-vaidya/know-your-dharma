from backend.app.db.session import engine
from backend.app.services.qdrant import qdrant_client
from backend.app.services.redis import redis_client
from fastapi import APIRouter
from sqlalchemy import text

router = APIRouter()


@router.get("/database")
async def database_health() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "service": "postgresql",
    }


@router.get("/redis")
async def redis_health() -> dict[str, str]:
    response = redis_client.ping()

    if not response:
        raise RuntimeError("Redis health check failed")

    return {
        "status": "healthy",
        "service": "redis",
    }

@router.get("/qdrant")
async def qdrant_health() -> dict[str, str]:
    qdrant_client.get_collections()

    return {
        "status": "healthy",
        "service": "qdrant",
    }