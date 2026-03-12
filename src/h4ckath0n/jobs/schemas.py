"""Pydantic schemas for jobs API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class EnqueueJobRequest(BaseModel):
    kind: str = Field(..., description="Registered job kind.")
    payload: dict = Field(default_factory=dict, description="Job payload.")
    queue: str = Field(default="default", description="Target queue name.")


class JobResponse(BaseModel):
    id: str
    kind: str
    queue: str
    status: str
    progress: int
    result_json: str | None = None
    error: str | None = None
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
