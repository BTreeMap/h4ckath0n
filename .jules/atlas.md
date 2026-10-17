# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-03-01 - FastAPI nested routes and app.routes drift

**Learning:** When using FastAPI 0.115+, endpoints nested within `_IncludedRouter` are not fully flattened in `app.routes`. This causes drift prevention scripts that iterate over `app.routes` to miss many API routes, resulting in false negatives.
**Action:** Use `app.openapi().get("paths", {})` instead of `app.routes` to reliably extract all endpoints. Be sure to filter the OpenAPI schema keys for valid HTTP methods.
