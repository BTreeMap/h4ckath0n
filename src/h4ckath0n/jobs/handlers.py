"""Built-in job handlers."""

from __future__ import annotations

import asyncio
from typing import Any

from h4ckath0n.jobs.registry import register


@register("demo.echo")
async def demo_echo(payload: dict[str, Any]) -> dict[str, Any]:
    """Echo the payload back after a short delay."""
    await asyncio.sleep(0.1)
    return {"echo": payload}


@register("uploads.extract_text", internal=True)
async def extract_text(payload: dict[str, Any]) -> dict[str, Any]:
    """Extract text content from an uploaded file.

    This handler is internal-only – it can only be enqueued by the server
    (e.g. from the upload router), never from the public ``POST /jobs`` API.

    The payload must contain ``upload_id``.  The handler resolves the
    storage key and directory from the database record rather than
    trusting caller-supplied paths.
    """
    upload_id = payload.get("upload_id", "")
    if not upload_id:
        return {"error": "Missing upload_id", "text": ""}

    try:
        from h4ckath0n.uploads.storage import get_file_path

        storage_key = payload.get("storage_key", "")
        storage_dir = payload.get("storage_dir", "./.h4ckath0n_storage")

        if not storage_key:
            return {"error": "Missing storage_key", "text": ""}

        file_path = get_file_path(storage_dir, storage_key)
    except ValueError:
        return {"error": "Invalid storage key", "text": ""}

    import os

    if not os.path.isfile(file_path):
        return {"error": "File not found", "text": ""}
    try:
        with open(file_path, encoding="utf-8", errors="replace") as f:
            text = f.read(50_000)  # limit extraction to 50KB
        return {"text": text, "length": len(text)}
    except Exception as exc:
        return {"error": str(exc), "text": ""}


@register("llm.summarize_text", internal=True)
async def summarize_text(payload: dict[str, Any]) -> dict[str, Any]:
    """Summarize text using the LLM client (requires OpenAI API key).

    This handler is internal-only.
    """
    text = payload.get("text", "")
    if not text:
        return {"summary": "", "error": "No text provided"}
    try:
        from h4ckath0n.llm.client import AsyncLLMClient

        client = AsyncLLMClient()
        resp = await client.chat(
            user=f"Summarize the following text in 2-3 sentences:\n\n{text[:5000]}",
            system="You are a concise summarizer.",
        )
        return {"summary": resp.text}
    except Exception as exc:
        return {"summary": "", "error": str(exc)}
