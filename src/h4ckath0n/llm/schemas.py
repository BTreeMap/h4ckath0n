"""Pydantic schemas for LLM endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user: str = Field(..., description="User message.")
    system: str | None = Field(None, description="Optional system prompt.")
    model: str | None = Field(None, description="Optional model override.")
