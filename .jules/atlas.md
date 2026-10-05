# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-02-28 - Env var drift prevention via Pydantic

**Learning:** Environment variable documentation frequently drifts because descriptions and defaults exist only in Markdown, separate from the code.
**Action:** Use Pydantic's `Field(..., description="...")` in the `Settings` class to centralize the source of truth, and generate both README markdown and `.env.example` templates programmatically from the model.

## 2026-02-28 - FastAPI route enumeration

**Learning:** Iterating over `app.routes` in recent FastAPI versions can miss nested routes hidden behind `_IncludedRouter`.
**Action:** Always use `app.openapi().get("paths", {})` to reliably list all registered endpoints and their metadata.
