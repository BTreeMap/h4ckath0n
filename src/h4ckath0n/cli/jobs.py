"""Background job worker subcommand."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import UTC, datetime

from h4ckath0n.cli._common import EXIT_BAD_ARGS, EXIT_OK


def _cmd_jobs_worker(args: argparse.Namespace) -> int:
    """Run a background job worker.

    Polls a Redis queue (``brpop``) for job IDs, loads each job from the
    database, executes the registered handler, and updates the job status
    to ``succeeded`` or ``failed``.  Exits with ``EXIT_BAD_ARGS`` when no
    Redis URL is configured.
    """
    from h4ckath0n.config import Settings

    settings = Settings()
    queue = getattr(args, "queue", settings.jobs_default_queue)
    poll_interval = getattr(args, "poll_interval", 2)

    if not settings.redis_url:
        print(
            "No Redis URL configured. Set H4CKATH0N_REDIS_URL.",
            file=sys.stderr,
        )
        return EXIT_BAD_ARGS

    from sqlalchemy.ext.asyncio import async_sessionmaker

    import h4ckath0n.jobs.handlers  # noqa: F401 – ensure handlers registered
    from h4ckath0n.db.engine import create_async_engine_from_settings
    from h4ckath0n.jobs.models import Job
    from h4ckath0n.jobs.registry import get_handler

    print(f"Starting worker on queue '{queue}' (Redis: {settings.redis_url})")

    async def _worker_loop() -> None:
        import redis.asyncio as aioredis

        r = aioredis.from_url(settings.redis_url)
        engine = create_async_engine_from_settings(settings)
        session_factory = async_sessionmaker(engine, expire_on_commit=False)

        try:
            while True:
                raw = await r.brpop(  # type: ignore[misc]
                    [f"h4ckath0n:jobs:{queue}"],
                    timeout=int(poll_interval),
                )
                if raw is None:
                    continue
                _, job_id_bytes = raw
                job_id = job_id_bytes.decode()
                print(f"Processing job {job_id}")

                async with session_factory() as db:
                    job = await db.get(Job, job_id)
                    if not job:
                        print(f"Job {job_id} not found")
                        continue

                    handler = get_handler(job.kind)
                    if not handler:
                        job.status = "failed"
                        job.error = f"No handler for: {job.kind}"
                        job.finished_at = datetime.now(UTC)
                        await db.commit()
                        continue

                    job.status = "running"
                    job.started_at = datetime.now(UTC)
                    job.attempts += 1
                    await db.commit()

                    try:
                        payload = json.loads(job.payload_json)
                        handler_result = await handler(payload)
                        job.status = "succeeded"
                        job.result_json = json.dumps(handler_result)
                        job.progress = 100
                    except Exception as exc:
                        job.status = "failed"
                        job.error = str(exc)

                    job.finished_at = datetime.now(UTC)
                    await db.commit()
                    print(f"Job {job_id}: {job.status}")
        finally:
            await r.aclose()
            await engine.dispose()

    try:
        asyncio.run(_worker_loop())
    except KeyboardInterrupt:
        print("\nWorker stopped.")
    return EXIT_OK
