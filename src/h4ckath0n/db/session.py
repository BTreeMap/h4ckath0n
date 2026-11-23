"""Session dependency for FastAPI."""

from __future__ import annotations

from collections.abc import AsyncGenerator, Callable, Generator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker


def get_db_dependency(
    session_factory: sessionmaker[Session],
) -> Callable[[], Generator[Session, None, None]]:
    """Return a FastAPI ``Depends``-compatible generator."""

    def _get_db() -> Generator[Session, None, None]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    return _get_db


def get_async_db_dependency(
    session_factory: async_sessionmaker[AsyncSession],
) -> Callable[[], AsyncGenerator[AsyncSession, None]]:
    """Return a FastAPI ``Depends``-compatible async generator."""

    async def _get_async_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    return _get_async_db


# Populated at app startup.
get_db = get_db_dependency


async def get_async_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that returns an async database session."""
    async with request.app.state.async_session_factory() as session:
        yield session
