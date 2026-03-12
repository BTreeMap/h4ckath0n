"""Pydantic schemas for uploads."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: str
    original_filename: str
    content_type: str
    byte_size: int
    sha256: str
    extraction_job_id: str | None = None
    created_at: datetime
