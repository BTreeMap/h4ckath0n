"""Passkey (WebAuthn) business logic – challenge lifecycle, credential management."""

from __future__ import annotations

import json
import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from h4ckath0n.auth.models import User, WebAuthnChallenge, WebAuthnCredential
from h4ckath0n.auth.passkeys.ids import new_key_id
from h4ckath0n.auth.passkeys.webauthn import (
    base64url_to_bytes,
    bytes_to_base64url,
    make_authentication_options,
    make_registration_options,
    verify_authentication,
    verify_registration,
)
from h4ckath0n.config import Settings


class LastPasskeyError(Exception):
    """Raised when attempting to revoke the last active passkey, which would prevent user login."""


# ---------------------------------------------------------------------------
# Challenge helpers
# ---------------------------------------------------------------------------


def _new_flow_id() -> str:
    return secrets.token_urlsafe(32)


def _new_challenge() -> bytes:
    return secrets.token_bytes(32)


async def _lock_user(db: AsyncSession, user_id: str) -> None:
    """Acquire a per-user row lock used as a mutex for credential mutations.

    SQLite ignores FOR UPDATE, which is acceptable for dev and tests that run on SQLite.
    """
    await db.execute(select(User.id).where(User.id == user_id).with_for_update())


async def _get_valid_flow(db: AsyncSession, flow_id: str, kind: str) -> WebAuthnChallenge:
    """Fetch and validate an unconsumed, non-expired flow.

    Uses row-level locking to prevent double-consumption under concurrent submissions.
    """
    result = await db.execute(
        select(WebAuthnChallenge).where(WebAuthnChallenge.id == flow_id).with_for_update()
    )
    flow = result.scalars().first()
    if flow is None:
        raise ValueError("Unknown flow")
    if flow.kind != kind:
        raise ValueError("Flow kind mismatch")
    if flow.consumed_at is not None:
        raise ValueError("Flow already consumed")
    exp = flow.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=UTC)
    if exp < datetime.now(UTC):
        raise ValueError("Flow expired")
    return flow


async def _consume_flow(db: AsyncSession, flow: WebAuthnChallenge) -> None:
    flow.consumed_at = datetime.now(UTC)
    await db.flush()


# ---------------------------------------------------------------------------
# Registration (unauthenticated, creates a new account)
# ---------------------------------------------------------------------------


async def start_registration(
    db: AsyncSession,
    settings: Settings,
) -> tuple[str, dict]:
    """Begin passkey registration, create user + flow, return (flow_id, options_dict)."""
    rp_id = settings.effective_rp_id()
    origin = settings.effective_origin()

    challenge_bytes = _new_challenge()
    flow_id = _new_flow_id()

    async with db.begin():
        user = User()
        db.add(user)
        await db.flush()

        flow = WebAuthnChallenge(
            id=flow_id,
            challenge=bytes_to_base64url(challenge_bytes),
            user_id=user.id,
            kind="register",
            expires_at=datetime.now(UTC) + timedelta(seconds=settings.webauthn_ttl_seconds),
            rp_id=rp_id,
            origin=origin,
        )
        db.add(flow)

    options = make_registration_options(
        rp_id=rp_id,
        rp_name=rp_id,
        user_id=user.id.encode("utf-8"),
        user_name=user.id,
        user_display_name=user.id,
        challenge=challenge_bytes,
        settings=settings,
    )
    return flow_id, options


async def finish_registration(
    db: AsyncSession,
    flow_id: str,
    credential_json: dict,
    settings: Settings,
) -> User:
    """Complete passkey registration, verify attestation, store credential, return user."""
    async with db.begin():
        flow = await _get_valid_flow(db, flow_id, "register")

        challenge_bytes = base64url_to_bytes(flow.challenge)
        cred_id_bytes, public_key, sign_count, aaguid = verify_registration(
            credential_json=credential_json,
            expected_challenge=challenge_bytes,
            expected_rp_id=flow.rp_id,
            expected_origin=flow.origin,
        )

        await _consume_flow(db, flow)

        transports = credential_json.get("response", {}).get("transports")
        cred = WebAuthnCredential(
            id=new_key_id(),
            user_id=flow.user_id,  # type: ignore[arg-type]
            credential_id=bytes_to_base64url(cred_id_bytes),
            public_key=public_key,
            sign_count=sign_count,
            aaguid=aaguid,
            transports=json.dumps(transports) if transports else None,
        )
        db.add(cred)

        user_result = await db.execute(select(User).where(User.id == flow.user_id))
        user = user_result.scalars().first()
        if user is None:
            raise ValueError("User not found")

    return user


# ---------------------------------------------------------------------------
# Authentication (unauthenticated, username-less)
# ---------------------------------------------------------------------------


async def start_authentication(
    db: AsyncSession,
    settings: Settings,
) -> tuple[str, dict]:
    """Begin passkey login, return (flow_id, options_dict)."""
    rp_id = settings.effective_rp_id()
    origin = settings.effective_origin()

    challenge_bytes = _new_challenge()
    flow_id = _new_flow_id()

    async with db.begin():
        flow = WebAuthnChallenge(
            id=flow_id,
            challenge=bytes_to_base64url(challenge_bytes),
            user_id=None,
            kind="authenticate",
            expires_at=datetime.now(UTC) + timedelta(seconds=settings.webauthn_ttl_seconds),
            rp_id=rp_id,
            origin=origin,
        )
        db.add(flow)

    options = make_authentication_options(
        rp_id=rp_id,
        challenge=challenge_bytes,
        settings=settings,
    )
    return flow_id, options


async def finish_authentication(
    db: AsyncSession,
    flow_id: str,
    credential_json: dict,
    settings: Settings,
) -> User:
    """Complete passkey login, verify assertion, update counters, return user."""
    async with db.begin():
        flow = await _get_valid_flow(db, flow_id, "authenticate")

        raw_id = credential_json.get("rawId") or credential_json.get("id", "")
        result = await db.execute(
            select(WebAuthnCredential)
            .where(
                WebAuthnCredential.credential_id == raw_id,
                WebAuthnCredential.revoked_at.is_(None),
            )
            .with_for_update()
        )
        stored = result.scalars().first()
        if stored is None:
            raise ValueError("Unknown or revoked credential")

        challenge_bytes = base64url_to_bytes(flow.challenge)
        _cred_id, new_sign_count = verify_authentication(
            credential_json=credential_json,
            expected_challenge=challenge_bytes,
            expected_rp_id=flow.rp_id,
            expected_origin=flow.origin,
            credential_public_key=stored.public_key,
            credential_current_sign_count=stored.sign_count,
        )

        await _consume_flow(db, flow)

        stored.sign_count = new_sign_count
        stored.last_used_at = datetime.now(UTC)

        user_result = await db.execute(select(User).where(User.id == stored.user_id))
        user = user_result.scalars().first()
        if user is None:
            raise ValueError("User not found")

    return user


# ---------------------------------------------------------------------------
# Add credential (authenticated)
# ---------------------------------------------------------------------------


async def start_add_credential(
    db: AsyncSession,
    user: User,
    settings: Settings,
) -> tuple[str, dict]:
    """Begin adding a passkey for an already-authenticated user."""
    rp_id = settings.effective_rp_id()
    origin = settings.effective_origin()

    # Build excludeCredentials from user's existing active credentials
    result = await db.execute(
        select(WebAuthnCredential).where(
            WebAuthnCredential.user_id == user.id,
            WebAuthnCredential.revoked_at.is_(None),
        )
    )
    existing = result.scalars().all()
    from webauthn.helpers.structs import PublicKeyCredentialDescriptor

    exclude = [
        PublicKeyCredentialDescriptor(id=base64url_to_bytes(c.credential_id)) for c in existing
    ]

    challenge_bytes = _new_challenge()
    flow_id = _new_flow_id()

    async with db.begin():
        flow = WebAuthnChallenge(
            id=flow_id,
            challenge=bytes_to_base64url(challenge_bytes),
            user_id=user.id,
            kind="add_credential",
            expires_at=datetime.now(UTC) + timedelta(seconds=settings.webauthn_ttl_seconds),
            rp_id=rp_id,
            origin=origin,
        )
        db.add(flow)

    options = make_registration_options(
        rp_id=rp_id,
        rp_name=rp_id,
        user_id=user.id.encode("utf-8"),
        user_name=user.id,
        user_display_name=user.id,
        challenge=challenge_bytes,
        settings=settings,
        exclude_credentials=exclude,
    )
    return flow_id, options


async def finish_add_credential(
    db: AsyncSession,
    flow_id: str,
    credential_json: dict,
    current_user: User,
    settings: Settings,
) -> WebAuthnCredential:
    """Complete adding a passkey, verify attestation, store credential."""
    async with db.begin():
        flow = await _get_valid_flow(db, flow_id, "add_credential")
        if flow.user_id != current_user.id:
            raise ValueError("Flow does not belong to current user")

        # Per-user mutex so add and revoke serialize for a given user.
        await _lock_user(db, current_user.id)

        challenge_bytes = base64url_to_bytes(flow.challenge)
        cred_id_bytes, public_key, sign_count, aaguid = verify_registration(
            credential_json=credential_json,
            expected_challenge=challenge_bytes,
            expected_rp_id=flow.rp_id,
            expected_origin=flow.origin,
        )

        await _consume_flow(db, flow)

        transports = credential_json.get("response", {}).get("transports")
        cred = WebAuthnCredential(
            id=new_key_id(),
            user_id=current_user.id,
            credential_id=bytes_to_base64url(cred_id_bytes),
            public_key=public_key,
            sign_count=sign_count,
            aaguid=aaguid,
            transports=json.dumps(transports) if transports else None,
        )
        db.add(cred)
        await db.flush()
        await db.refresh(cred)

    return cred


# ---------------------------------------------------------------------------
# List and revoke
# ---------------------------------------------------------------------------


async def list_passkeys(db: AsyncSession, user: User) -> list[WebAuthnCredential]:
    """List all credentials (active and revoked) for a user."""
    result = await db.execute(
        select(WebAuthnCredential)
        .where(WebAuthnCredential.user_id == user.id)
        .order_by(WebAuthnCredential.created_at)
    )
    return list(result.scalars().all())


async def revoke_passkey(db: AsyncSession, user: User, key_id: str) -> None:
    """Revoke a credential by its internal key id.

    Raises LastPasskeyError if this is the user's last active passkey.
    Uses a per-user row lock for transactional safety in Postgres.
    """
    async with db.begin():
        # Per-user mutex. In SQLite, FOR UPDATE is ignored, which is fine for dev.
        await _lock_user(db, user.id)

        result = await db.execute(
            select(WebAuthnCredential)
            .where(
                WebAuthnCredential.id == key_id,
                WebAuthnCredential.user_id == user.id,
            )
            .with_for_update()
        )
        cred = result.scalars().first()
        if cred is None:
            raise ValueError("Credential not found")
        if cred.revoked_at is not None:
            raise ValueError("Credential already revoked")

        # Safe under the per-user mutex. Do not use FOR UPDATE with aggregates on Postgres.
        active_count = await db.scalar(
            select(func.count())
            .select_from(WebAuthnCredential)
            .where(
                WebAuthnCredential.user_id == user.id,
                WebAuthnCredential.revoked_at.is_(None),
            )
        )
        if active_count is not None and active_count <= 1:
            raise LastPasskeyError(
                "Cannot revoke the last active passkey. "
                "Add another passkey via POST /auth/passkey/add/start first."
            )

        cred.revoked_at = datetime.now(UTC)


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------


async def cleanup_expired_challenges(db: AsyncSession) -> int:
    """Delete expired and consumed challenges. Returns count deleted."""
    from sqlalchemy import delete

    now = datetime.now(UTC)
    async with db.begin():
        result = await db.execute(
            delete(WebAuthnChallenge).where(WebAuthnChallenge.expires_at < now)
        )
        count: int = result.rowcount  # type: ignore[attr-defined]
    return count
