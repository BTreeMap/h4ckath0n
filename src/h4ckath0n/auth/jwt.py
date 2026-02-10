"""JWT helpers for device-key (ES256) verification."""

from __future__ import annotations

from datetime import datetime

import jwt
from pydantic import BaseModel


class JWTClaims(BaseModel):
    """Typed representation of device-signed JWT payload.

    Contains only identity and time claims.  No privilege claims (role/scopes)
    are read from the JWT – authorization is computed server-side.
    """

    sub: str
    iat: datetime
    exp: datetime
    aud: str | None = None
    iss: str | None = None


def decode_device_token(
    token: str,
    *,
    public_key_pem: str,
) -> JWTClaims:
    """Decode an ES256 device-signed JWT using the device's public key."""
    payload = jwt.decode(
        token,
        public_key_pem,
        algorithms=["ES256"],
        options={"verify_aud": False},
    )
    return JWTClaims(**payload)


def get_unverified_kid(token: str) -> str | None:
    """Extract the kid from the JWT header without verification."""
    try:
        header = jwt.get_unverified_header(token)
        return header.get("kid")
    except jwt.InvalidTokenError:
        return None
