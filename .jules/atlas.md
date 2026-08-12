# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - FastAPI nested router paths missing from app.routes
**Learning:** Iterating over `app.routes` in FastAPI does not yield routes nested within an `_IncludedRouter` correctly, leading to massive false negatives in drift-prevention checks. The true flat list of endpoints is available via OpenAPI schema generation (`app.openapi().get("paths", {})`).
**Action:** When validating or enumerating APIs in drift checks, use the generated OpenAPI schema rather than `app.routes`.
