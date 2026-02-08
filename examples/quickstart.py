"""Minimal h4ckrth0n example application.

Run with:
    uv run uvicorn examples.quickstart:app --reload
"""

from h4ckrth0n import create_app
from h4ckrth0n.auth import require_admin, require_scopes, require_user

app = create_app()


@app.get("/me")
def me(user=require_user()):
    """Return the current user's profile."""
    return {"id": user.id, "email": user.email, "role": user.role}


@app.get("/admin/dashboard")
def admin_dashboard(user=require_admin()):
    """Admin-only endpoint."""
    return {"ok": True, "admin": user.email}


@app.post("/billing/refund")
def refund(claims=require_scopes("billing:refund")):
    """Requires the ``billing:refund`` scope."""
    return {"status": "queued"}


@app.get("/llm-demo")
def llm_demo():
    """Demonstrate the LLM wrapper (requires OPENAI_API_KEY)."""
    try:
        from h4ckrth0n.llm import llm

        client = llm()
        resp = client.chat(
            system="You are a helpful assistant.",
            user="Say hello in one sentence.",
        )
        return {"text": resp.text}
    except RuntimeError as exc:
        return {"error": str(exc)}
