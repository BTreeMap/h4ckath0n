# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-10-01 - [FastAPI API routes documentation drift]
**Learning:** In recent FastAPI versions, endpoints nested within `_IncludedRouter` are not explicitly visible in `app.routes` as `APIRoute` instances but are wrapped or omitted. Using `app.routes` directly is unreliable for fetching all paths for drift verification.
**Action:** Use `app.openapi().get('paths', {})` to reliably list all registered endpoints for drift verification checks.
