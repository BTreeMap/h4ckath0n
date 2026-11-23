# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Avoid internal app.routes for OpenAPI parity
**Learning:** Parsing FastAPI's `app.routes` internally misses routes added via specific router configurations or conditionally evaluated endpoint decorators, meaning it fails to document all exposed APIs. Relying on `app.routes` directly is brittle.
**Action:** Extract routes directly from `app.openapi().get("paths", {})` when checking API route documentation parity to ensure an exact match with what FastAPI actually exposes to the outside world.
