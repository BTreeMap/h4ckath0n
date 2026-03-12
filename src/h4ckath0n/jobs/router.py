"""Jobs API router."""

from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import h4ckath0n.jobs.handlers  # noqa: F401 – ensure built-in handlers are loaded
from h4ckath0n.auth.dependencies import get_auth_context, require_user
from h4ckath0n.auth.models import User
from h4ckath0n.jobs.models import Job
from h4ckath0n.jobs.queue import enqueue_job
from h4ckath0n.jobs.registry import public_kinds
from h4ckath0n.jobs.schemas import EnqueueJobRequest, JobResponse
from h4ckath0n.realtime.auth import AuthContext

jobs_router = APIRouter(prefix="/jobs", tags=["jobs"])


async def _db_dep(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.async_session_factory() as db:
        yield db


def _job_to_response(job: Job) -> JobResponse:
    return JobResponse(
        id=job.id,
        kind=job.kind,
        queue=job.queue,
        status=job.status,
        progress=job.progress,
        result_json=job.result_json,
        error=job.error,
        created_at=job.created_at,
        started_at=job.started_at,
        finished_at=job.finished_at,
    )


@jobs_router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enqueue a job",
    description="Create a new background job.",
)
async def create_job(
    body: EnqueueJobRequest,
    request: Request,
    user: User = require_user(),
    ctx: AuthContext = Depends(get_auth_context),
    db: AsyncSession = Depends(_db_dep),
) -> JobResponse:
    if body.kind not in public_kinds():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown job kind: {body.kind}",
        )
    settings = request.app.state.settings
    job = await enqueue_job(
        db,
        body.kind,
        body.payload,
        queue=body.queue,
        user_id=user.id,
        redis_url=settings.redis_url,
        inline=settings.jobs_inline_in_dev,
    )
    return _job_to_response(job)


@jobs_router.get(
    "",
    response_model=list[JobResponse],
    summary="List jobs",
    description="List recent jobs for the current user.",
)
async def list_jobs(
    user: User = require_user(),
    db: AsyncSession = Depends(_db_dep),
) -> list[JobResponse]:
    result = await db.execute(
        select(Job)
        .filter(Job.created_by_user_id == user.id)
        .order_by(Job.created_at.desc())
        .limit(50)
    )
    return [_job_to_response(j) for j in result.scalars()]


@jobs_router.get(
    "/{job_id}",
    response_model=JobResponse,
    summary="Get job",
    description="Get details of a specific job.",
)
async def get_job(
    job_id: str,
    user: User = require_user(),
    db: AsyncSession = Depends(_db_dep),
) -> JobResponse:
    result = await db.execute(select(Job).filter(Job.id == job_id))
    job = result.scalars().first()
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.created_by_user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return _job_to_response(job)
