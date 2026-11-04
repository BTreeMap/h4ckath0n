# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-10-16 - FastAPI nested routes hiding in drift checks

**Learning:** When enumerating endpoints in FastAPI 0.115+, routes nested within an `_IncludedRouter` are not flattened in `app.routes`. Iterating over `app.routes` only finds root-level endpoints and misses the nested ones, leading to false negatives in route-verification scripts.
**Action:** When extracting all active HTTP routes from a FastAPI app, generate the OpenAPI schema using `app.openapi().get("paths", {})` and iterate through its path keys, rather than relying on `app.routes`.
