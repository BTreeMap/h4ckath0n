"""Job SQLAlchemy models."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from h4ckath0n.auth.passkeys.ids import random_base32
from h4ckath0n.db.base import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


def new_job_id() -> str:
    """Generate a job ID (32 chars, starts with 'j')."""
    s = random_base32()
    return "j" + s[1:]


class Job(Base):
    __tablename__ = "h4ckath0n_jobs"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_job_id)
    kind: Mapped[str] = mapped_column(String(100), nullable=False)
    queue: Mapped[str] = mapped_column(String(50), nullable=False, default="default")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="queued")
    payload_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    created_by_user_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )
