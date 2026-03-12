"""Job queue - Redis backed with inline fallback."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from h4ckath0n.jobs.models import Job
from h4ckath0n.jobs.registry import get_handler

logger = logging.getLogger(__name__)


async def enqueue_job(
    db: AsyncSession,
    kind: str,
    payload: dict[str, Any] | None = None,
    *,
    queue: str = "default",
    user_id: str | None = None,
    redis_url: str = "",
    inline: bool = False,
) -> Job:
    """Create a job record and optionally push to Redis or run inline."""
    handler = get_handler(kind)
    if handler is None:
        raise ValueError(f"Unknown job kind: {kind}")

    job = Job(
        kind=kind,
        queue=queue,
        payload_json=json.dumps(payload or {}),
        created_by_user_id=user_id,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    if redis_url:
        try:
            import redis.asyncio as aioredis

            r = aioredis.from_url(redis_url)
            await r.lpush(f"h4ckath0n:jobs:{queue}", job.id)  # type: ignore[misc]
            await r.close()
            logger.info("Job %s enqueued to Redis queue %s", job.id, queue)
        except Exception:
            logger.exception("Failed to push job %s to Redis, falling back to inline", job.id)
            if inline:
                await _run_inline(db, job)
    elif inline:
        await _run_inline(db, job)

    return job


async def _run_inline(db: AsyncSession, job: Job) -> None:
    """Execute a job synchronously in the current process."""
    handler = get_handler(job.kind)
    if handler is None:
        job.status = "failed"
        job.error = f"No handler for kind: {job.kind}"
        job.finished_at = datetime.now(UTC)
        await db.commit()
        return

    job.status = "running"
    job.started_at = datetime.now(UTC)
    job.attempts += 1
    await db.commit()

    try:
        payload = json.loads(job.payload_json)
        result = await handler(payload)
        job.status = "succeeded"
        job.result_json = json.dumps(result)
        job.progress = 100
        job.finished_at = datetime.now(UTC)
    except Exception as exc:
        job.status = "failed"
        job.error = str(exc)
        job.finished_at = datetime.now(UTC)

    await db.commit()
