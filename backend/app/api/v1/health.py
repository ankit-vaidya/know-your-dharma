from fastapi import APIRouter
from sqlalchemy import text

from backend.app.db.session import engine

router = APIRouter()


@router.get("/database")
async def database_health() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "service": "postgresql",
    }