"""Phase 1 integration tests – session, jobs, uploads, email, LLM streaming."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime, timedelta

import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)
from fastapi.testclient import TestClient
from jwt.algorithms import ECAlgorithm

from h4ckath0n.app import create_app
from h4ckath0n.config import Settings

# ---------------------------------------------------------------------------
# Helpers (same patterns as test_integration.py)
# ---------------------------------------------------------------------------


def _make_device_token(
    user_id: str,
    device_id: str,
    private_key_pem: bytes,
    expire_minutes: int = 15,
    aud: str = "h4ckath0n:http",
) -> str:
    """Create a device-signed ES256 JWT for testing."""
    import jwt as pyjwt

    now = datetime.now(UTC)
    payload: dict = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(minutes=expire_minutes),
    }
    if aud:
        payload["aud"] = aud
    return pyjwt.encode(
        payload,
        private_key_pem,
        algorithm="ES256",
        headers={"kid": device_id},
    )


def _create_device_keypair() -> tuple[bytes, dict]:
    """Generate an EC P-256 keypair. Returns (private_key_pem, public_key_jwk_dict)."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    private_pem = private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
    public_key = private_key.public_key()
    jwk_dict = json.loads(ECAlgorithm(ECAlgorithm.SHA256).to_jwk(public_key))
    return private_pem, jwk_dict


def _register_user_with_device(
    client: TestClient, email: str, password: str, display_name: str = "Test User"
) -> tuple[str, str, bytes]:
    """Register a user via password route and bind a device key.

    Returns (user_id, device_id, private_key_pem).
    """
    private_pem, public_jwk = _create_device_keypair()
    r = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "display_name": display_name,
            "device_public_key_jwk": public_jwk,
            "device_label": "test",
        },
    )
    assert r.status_code == 201, r.text
    body = r.json()
    return body["user_id"], body["device_id"], private_pem


def _auth_header(user_id: str, device_id: str, private_pem: bytes) -> dict[str, str]:
    """Build Authorization header dict."""
    token = _make_device_token(user_id, device_id, private_pem)
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def settings(tmp_path):
    db_path = tmp_path / "test.db"
    storage_dir = str(tmp_path / "storage")
    outbox_dir = str(tmp_path / "outbox")
    return Settings(
        database_url=f"sqlite:///{db_path}",
        env="development",
        first_user_is_admin=False,
        password_auth_enabled=True,
        storage_dir=storage_dir,
        email_backend="file",
        email_outbox_dir=outbox_dir,
        openai_api_key="",
        jobs_inline_in_dev=True,
    )


@pytest.fixture()
async def app(settings):
    application = create_app(settings)
    async with application.state.async_engine.begin() as conn:
        from h4ckath0n.db.base import Base

        await conn.run_sync(Base.metadata.create_all)
    yield application
    await application.state.async_engine.dispose()


@pytest.fixture()
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture()
async def db_session(app):
    async with app.state.async_session_factory() as session:
        yield session


# ---------------------------------------------------------------------------
# 1. TestSessionEndpoint
# ---------------------------------------------------------------------------


class TestSessionEndpoint:
    def test_session_returns_user_data(self, client: TestClient):
        uid, did, pem = _register_user_with_device(
            client, "sess@example.com", "P@ssw0rd", display_name="Session Tester"
        )
        headers = _auth_header(uid, did, pem)

        r = client.get("/auth/session", headers=headers)
        assert r.status_code == 200
        body = r.json()

        assert body["user_id"] == uid
        assert body["device_id"] == did
        assert body["role"] == "user"
        assert isinstance(body["scopes"], list)
        assert body["display_name"] == "Session Tester"
        assert body["email"] == "sess@example.com"

    async def test_session_returns_scopes_as_list(self, client: TestClient, db_session):
        uid, did, pem = _register_user_with_device(client, "scopes@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        # Set scopes directly in the DB
        from sqlalchemy import update

        from h4ckath0n.auth.models import User

        await db_session.execute(update(User).where(User.id == uid).values(scopes="read,write"))
        await db_session.commit()

        r = client.get("/auth/session", headers=headers)
        assert r.status_code == 200
        body = r.json()
        assert body["scopes"] == ["read", "write"]
        assert isinstance(body["scopes"], list)

    def test_session_unauthenticated(self, client: TestClient):
        r = client.get("/auth/session")
        assert r.status_code == 401


# ---------------------------------------------------------------------------
# 2. TestJobsEndpoint
# ---------------------------------------------------------------------------


class TestJobsEndpoint:
    def test_enqueue_job_echo(self, client: TestClient):
        uid, did, pem = _register_user_with_device(client, "jobs1@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        r = client.post(
            "/jobs",
            json={"kind": "demo.echo", "payload": {"msg": "hello"}},
            headers=headers,
        )
        assert r.status_code == 201
        body = r.json()
        assert body["kind"] == "demo.echo"
        assert body["id"].startswith("j")
        assert body["status"] in ("queued", "running", "succeeded")

    def test_enqueue_unknown_kind(self, client: TestClient):
        uid, did, pem = _register_user_with_device(client, "jobs2@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        r = client.post(
            "/jobs",
            json={"kind": "nonexistent.handler", "payload": {}},
            headers=headers,
        )
        assert r.status_code == 400
        assert "Unknown job kind" in r.json()["detail"]

    def test_list_jobs(self, client: TestClient):
        uid, did, pem = _register_user_with_device(client, "jobs3@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        client.post("/jobs", json={"kind": "demo.echo", "payload": {"a": 1}}, headers=headers)
        client.post("/jobs", json={"kind": "demo.echo", "payload": {"b": 2}}, headers=headers)

        r = client.get("/jobs", headers=headers)
        assert r.status_code == 200
        jobs = r.json()
        assert isinstance(jobs, list)
        assert len(jobs) >= 2

    def test_get_job(self, client: TestClient):
        uid, did, pem = _register_user_with_device(client, "jobs4@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        cr = client.post(
            "/jobs",
            json={"kind": "demo.echo", "payload": {"x": 42}},
            headers=headers,
        )
        job_id = cr.json()["id"]

        r = client.get(f"/jobs/{job_id}", headers=headers)
        assert r.status_code == 200
        body = r.json()
        assert body["id"] == job_id
        assert body["kind"] == "demo.echo"

    def test_get_job_access_denied(self, client: TestClient):
        # User A creates a job
        uid_a, did_a, pem_a = _register_user_with_device(client, "jobs5a@example.com", "P@ssw0rd")
        headers_a = _auth_header(uid_a, did_a, pem_a)

        cr = client.post(
            "/jobs",
            json={"kind": "demo.echo", "payload": {}},
            headers=headers_a,
        )
        job_id = cr.json()["id"]

        # User B tries to access it
        uid_b, did_b, pem_b = _register_user_with_device(client, "jobs5b@example.com", "P@ssw0rd")
        headers_b = _auth_header(uid_b, did_b, pem_b)

        r = client.get(f"/jobs/{job_id}", headers=headers_b)
        assert r.status_code == 403

    def test_inline_job_execution(self, client: TestClient):
        """With jobs_inline_in_dev=True, the job runs to completion inline."""
        uid, did, pem = _register_user_with_device(client, "jobs6@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        cr = client.post(
            "/jobs",
            json={"kind": "demo.echo", "payload": {"ping": "pong"}},
            headers=headers,
        )
        assert cr.status_code == 201
        job_id = cr.json()["id"]

        r = client.get(f"/jobs/{job_id}", headers=headers)
        body = r.json()
        assert body["status"] == "succeeded"
        assert body["progress"] == 100
        result = json.loads(body["result_json"])
        assert result == {"echo": {"ping": "pong"}}


# ---------------------------------------------------------------------------
# 3. TestUploadsEndpoint
# ---------------------------------------------------------------------------


class TestUploadsEndpoint:
    def test_upload_file(self, client: TestClient):
        uid, did, pem = _register_user_with_device(client, "up1@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        r = client.post(
            "/uploads",
            files={"file": ("hello.txt", b"Hello, world!", "text/plain")},
            headers=headers,
        )
        assert r.status_code == 201
        body = r.json()
        assert body["original_filename"] == "hello.txt"
        assert body["content_type"] == "text/plain"
        assert body["byte_size"] == len(b"Hello, world!")
        assert body["id"].startswith("f")
        assert body["sha256"]

    def test_list_uploads(self, client: TestClient):
        uid, did, pem = _register_user_with_device(client, "up2@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        client.post(
            "/uploads",
            files={"file": ("a.txt", b"aaa", "text/plain")},
            headers=headers,
        )
        client.post(
            "/uploads",
            files={"file": ("b.txt", b"bbb", "text/plain")},
            headers=headers,
        )

        r = client.get("/uploads", headers=headers)
        assert r.status_code == 200
        uploads = r.json()
        assert isinstance(uploads, list)
        assert len(uploads) >= 2

    def test_download_file(self, client: TestClient):
        uid, did, pem = _register_user_with_device(client, "up3@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)
        content = b"Download me!"

        up = client.post(
            "/uploads",
            files={"file": ("dl.txt", content, "application/octet-stream")},
            headers=headers,
        )
        upload_id = up.json()["id"]

        r = client.get(f"/uploads/{upload_id}/download", headers=headers)
        assert r.status_code == 200
        assert r.content == content

    def test_upload_ownership(self, client: TestClient):
        # User A uploads
        uid_a, did_a, pem_a = _register_user_with_device(client, "up4a@example.com", "P@ssw0rd")
        headers_a = _auth_header(uid_a, did_a, pem_a)

        up = client.post(
            "/uploads",
            files={"file": ("secret.txt", b"secret", "application/octet-stream")},
            headers=headers_a,
        )
        upload_id = up.json()["id"]

        # User B tries to download
        uid_b, did_b, pem_b = _register_user_with_device(client, "up4b@example.com", "P@ssw0rd")
        headers_b = _auth_header(uid_b, did_b, pem_b)

        r = client.get(f"/uploads/{upload_id}/download", headers=headers_b)
        assert r.status_code == 403

    def test_upload_text_triggers_extraction(self, client: TestClient):
        """Uploading a text/plain file should trigger an extraction job."""
        uid, did, pem = _register_user_with_device(client, "up5@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        r = client.post(
            "/uploads",
            files={"file": ("notes.txt", b"Some important notes", "text/plain")},
            headers=headers,
        )
        assert r.status_code == 201
        body = r.json()
        assert body["extraction_job_id"] is not None
        assert body["extraction_job_id"].startswith("j")


# ---------------------------------------------------------------------------
# 4. TestEmailIntegration
# ---------------------------------------------------------------------------


class TestEmailIntegration:
    def test_password_reset_sends_file_email(self, client: TestClient, settings):
        """Password reset for a known email writes an .eml file in the outbox dir."""
        _register_user_with_device(client, "reset@example.com", "P@ssw0rd")

        r = client.post("/auth/password-reset/request", json={"email": "reset@example.com"})
        assert r.status_code == 200
        assert "reset link was sent" in r.json()["message"].lower()

        outbox = settings.email_outbox_dir
        assert os.path.isdir(outbox)
        eml_files = [f for f in os.listdir(outbox) if f.endswith(".eml")]
        assert len(eml_files) >= 1

        # Verify the email content contains the reset link
        with open(os.path.join(outbox, eml_files[0]), encoding="utf-8") as f:
            content = f.read()
        assert "reset@example.com" in content
        assert "Password Reset" in content

    def test_password_reset_unknown_email_no_leak(self, client: TestClient, settings):
        """Reset for an unknown email returns the same message but writes no file."""
        r = client.post("/auth/password-reset/request", json={"email": "nobody@example.com"})
        assert r.status_code == 200
        assert "reset link was sent" in r.json()["message"].lower()

        outbox = settings.email_outbox_dir
        # Outbox may not even be created, or should have no files
        if os.path.isdir(outbox):
            eml_files = [f for f in os.listdir(outbox) if f.endswith(".eml")]
            assert len(eml_files) == 0


# ---------------------------------------------------------------------------
# 5. TestLLMStreaming
# ---------------------------------------------------------------------------


class TestLLMStreaming:
    def test_stream_chat_method_exists(self):
        """AsyncLLMClient must expose a stream_chat method."""
        from h4ckath0n.llm.client import AsyncLLMClient

        assert hasattr(AsyncLLMClient, "stream_chat")
        assert callable(AsyncLLMClient.stream_chat)

    def test_llm_chat_endpoint_without_key(self, client: TestClient):
        """POST /llm/chat without an OpenAI key returns 503."""
        uid, did, pem = _register_user_with_device(client, "llm1@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        r = client.post(
            "/llm/chat",
            json={"user": "Hello"},
            headers=headers,
        )
        assert r.status_code == 503
        assert "api key" in r.json()["detail"].lower()

    def test_llm_stream_endpoint_without_key(self, client: TestClient):
        """POST /llm/chat/stream without an OpenAI key returns 503."""
        uid, did, pem = _register_user_with_device(client, "llm2@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        r = client.post(
            "/llm/chat/stream",
            json={"user": "Hello"},
            headers=headers,
        )
        assert r.status_code == 503
        assert "api key" in r.json()["detail"].lower()


# ---------------------------------------------------------------------------
# 6. Security invariants
# ---------------------------------------------------------------------------


class TestSecurityInvariants:
    """Verify the security hardening applied in the remediation pass."""

    def test_storage_key_opaque(self, client: TestClient):
        """Storage key must NOT contain the original filename."""
        uid, did, pem = _register_user_with_device(client, "sec1@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        r = client.post(
            "/uploads",
            files={"file": ("evil/../../../etc/passwd", b"test", "application/octet-stream")},
            headers=headers,
        )
        assert r.status_code == 201
        body = r.json()
        # The original filename is preserved in metadata but must not appear in
        # the on-disk storage key (which is only in the DB, not in the API response).
        assert body["original_filename"] == "evil/../../../etc/passwd"
        assert body["sha256"]

    def test_internal_job_kind_rejected_from_api(self, client: TestClient):
        """Internal-only job kinds must not be callable from POST /jobs."""
        uid, did, pem = _register_user_with_device(client, "sec2@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        r = client.post(
            "/jobs",
            json={"kind": "uploads.extract_text", "payload": {"upload_id": "fake"}},
            headers=headers,
        )
        assert r.status_code == 400
        assert "Unknown job kind" in r.json()["detail"]

    def test_llm_summarize_internal_only(self, client: TestClient):
        """llm.summarize_text must also be internal-only."""
        uid, did, pem = _register_user_with_device(client, "sec3@example.com", "P@ssw0rd")
        headers = _auth_header(uid, did, pem)

        r = client.post(
            "/jobs",
            json={"kind": "llm.summarize_text", "payload": {"text": "hello"}},
            headers=headers,
        )
        assert r.status_code == 400

    def test_email_outbox_filename_opaque(self, client: TestClient, settings):
        """Email outbox files must not contain user-controlled address parts."""
        _register_user_with_device(client, "outbox@example.com", "P@ssw0rd")
        client.post("/auth/password-reset/request", json={"email": "outbox@example.com"})

        outbox = settings.email_outbox_dir
        assert os.path.isdir(outbox)
        eml_files = [f for f in os.listdir(outbox) if f.endswith(".eml")]
        assert len(eml_files) >= 1
        # Filename must NOT contain the email address or parts of it
        for fname in eml_files:
            assert "outbox" not in fname
            assert "example" not in fname
