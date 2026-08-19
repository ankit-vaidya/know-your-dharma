import uuid
from datetime import datetime

from backend.app.db.base import Base
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class VerseContent(Base):
    __tablename__ = "verse_contents"

    __table_args__ = (
        UniqueConstraint(
            "verse_id",
            "edition_id",
            "content_type",
            "language",
            name="uq_verse_content_variant",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    verse_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("verses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    edition_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("editions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    content_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    language: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    source_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    verse: Mapped["Verse"] = relationship(
        back_populates="contents",
    )

    edition: Mapped["Edition"] = relationship(
        back_populates="verse_contents",
    )