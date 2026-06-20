"""LLM API router with streaming support."""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
from starlette.responses import JSONResponse

from h4ckath0n.auth.dependencies import require_user
from h4ckath0n.auth.models import User
from h4ckath0n.llm.schemas import ChatRequest
from h4ckath0n.realtime.sse import sse_response

logger = logging.getLogger(__name__)

llm_router = APIRouter(prefix="/llm", tags=["llm"])


@llm_router.post(
    "/chat",
    response_model=None,
    summary="Chat completion",
    description="Non-streaming chat completion. Requires OpenAI API key.",
)
async def chat(
    body: ChatRequest, request: Request, user: User = require_user()
) -> JSONResponse | dict[str, Any]:
    settings = request.app.state.settings
    if not settings.openai_api_key:
        return JSONResponse({"detail": "OpenAI API key not configured"}, status_code=503)
    from h4ckath0n.llm.client import AsyncLLMClient

    client = AsyncLLMClient(api_key=settings.openai_api_key)
    resp = await client.chat(
        user=body.user,
        system=body.system or "You are a helpful assistant.",
        model=body.model,
    )
    return resp.model_dump()


@llm_router.post(
    "/chat/stream",
    response_model=None,
    summary="Streaming chat completion",
    description="Stream LLM tokens via SSE. Requires OpenAI API key.",
    responses={200: {"content": {"text/event-stream": {"schema": {"type": "string"}}}}},
)
async def chat_stream(
    body: ChatRequest, request: Request, user: User = require_user()
) -> JSONResponse | EventSourceResponse:
    settings = request.app.state.settings
    if not settings.openai_api_key:
        return JSONResponse({"detail": "OpenAI API key not configured"}, status_code=503)

    from h4ckath0n.llm.client import AsyncLLMClient

    client = AsyncLLMClient(api_key=settings.openai_api_key)

    async def generate() -> AsyncGenerator[dict[str, Any], None]:
        yield {
            "event": "start",
            "data": json.dumps({"model": body.model or "gpt-4o-mini"}),
        }
        try:
            async for token in client.stream_chat(
                user=body.user,
                system=body.system or "You are a helpful assistant.",
                model=body.model,
            ):
                if await request.is_disconnected():
                    return
                yield {"event": "token", "data": json.dumps({"token": token})}
            yield {"event": "done", "data": json.dumps({"ok": True})}
        except Exception as exc:
            logger.exception("LLM streaming failed")
            yield {"event": "error", "data": json.dumps({"error": str(exc)})}

    return sse_response(generate())
