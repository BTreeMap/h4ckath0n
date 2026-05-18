"""GET /auth/session – return the current authenticated session info."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from h4ckath0n.auth.dependencies import get_auth_context, require_user
from h4ckath0n.auth.models import User
from h4ckath0n.auth.schemas import SessionResponse
from h4ckath0n.realtime.auth import AuthContext
from h4ckath0n.scopes import parse_scopes

session_router = APIRouter(prefix="/auth", tags=["auth"])


@session_router.get(
    "/session",
    response_model=SessionResponse,
    summary="Current session",
    description="Return information about the currently authenticated session.",
)
async def get_session(
    user: User = require_user(),
    ctx: AuthContext = Depends(get_auth_context),
) -> SessionResponse:
    scopes = list(parse_scopes(user.scopes))
    return SessionResponse(
        user_id=user.id,
        device_id=ctx.device_id,
        role=user.role,
        scopes=scopes,
        display_name=user.display_name,
        email=user.email,
    )
