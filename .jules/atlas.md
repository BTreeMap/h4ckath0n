# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2025-01-01 - OpenAPI for generated route documentation

**Learning:** In FastAPI versions 0.115+ and 0.138+, `app.routes` obfuscates endpoints nested within `_IncludedRouter` or mounted sub-applications. Relying on `app.routes` for route discovery in drift-prevention scripts leads to false negatives. Furthermore, hand-written route lists are highly prone to drift.

**Action:** When enumerating routes programmatically (e.g., for drift-prevention scripts) or generating documentation, always use `app.openapi().get("paths", {})` rather than manually iterating through `app.routes` to reliably capture all endpoints and their metadata. Replace hand-written route lists with dynamically generated sections delimited by markers (e.g., `<!-- BEGIN ROUTES -->`).
