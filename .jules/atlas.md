# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-05-01 - Replace handwritten API list with OpenAPI-generated docs

**Learning:** Manual API route lists drift easily from code, especially when using FastAPI's auto-generated paths. Parsing `app.openapi().get("paths", {})` is a reliable way to capture the true source of truth.
**Action:** Use OpenAPI path extraction combined with delimited markdown blocks (`<!-- BEGIN ROUTES -->`) in drift-prevention scripts rather than trying to parse `app.routes` directly or writing them by hand.
