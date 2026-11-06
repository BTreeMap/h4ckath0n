"""FastAPI dependencies for endpoint protection.

All request authentication uses device-signed ES256 JWTs.  Authorization
(roles, scopes) is loaded from the database – the JWT carries no privilege
claims.

The core verification logic lives in :mod:`h4ckath0n.realtime.auth` so
that HTTP, WebSocket and SSE endpoints all share a single code path.
"""

from __future__ import annotations

from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from h4ckath0n.auth.authz import missing_scopes, parse_scopes
from h4ckath0n.auth.models import User
from h4ckath0n.db import get_async_session
from h4ckath0n.realtime.auth import AUD_HTTP, AuthContext, AuthError, verify_device_jwt

_bearer = HTTPBearer(
    scheme_name="DeviceJWT",
    description=(
        "Device-signed ES256 JWT minted by the client. The JWT header must include "
        "kid set to the device id, and the aud claim must be h4ckath0n:http."
    ),
)


async def get_auth_context(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: AsyncSession = Depends(get_async_session),
) -> AuthContext:
    """Public dependency that returns the current :class:`AuthContext`."""
    token = credentials.credentials
    try:
        return await verify_device_jwt(token, expected_aud=AUD_HTTP, db=db)
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.detail,
        ) from None


async def _get_current_user(
    ctx: AuthContext = Depends(get_auth_context),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    # Use primary-key lookup for the session identity map.
    if (user := await db.get(User, ctx.user_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


def require_user() -> Any:
    """Dependency that returns the current authenticated user."""
    return Depends(_get_current_user)


def require_admin() -> Any:
    """Dependency that requires the current user to be an admin."""

    async def _admin(user: User = Depends(_get_current_user)) -> User:
        if user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Admin required"
            )
        return user

    return Depends(_admin)


def require_scopes(*scopes: str) -> Any:
    """Dependency that requires the user to have specific scopes (from DB)."""

    needed = set(parse_scopes(scopes))

    async def _scoped(user: User = Depends(_get_current_user)) -> User:
        if missing := missing_scopes(parse_scopes(user.scopes), needed):
            missing_list = ", ".join(sorted(missing))
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing scope(s): {missing_list}",
            )
        return user

    return Depends(_scoped)
