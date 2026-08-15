from collections.abc import Generator

from backend.app.core.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

settings = get_settings()

engine = create_engine(
    settings.postgres_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()