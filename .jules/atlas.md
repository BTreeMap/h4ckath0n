# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Route drift checks fail with FastAPI 0.115+ nested routers

**Learning:** In FastAPI 0.115+, endpoints nested inside `_IncludedRouter` are not flattened into `app.routes`. Scripts that iterate over `app.routes` will silently skip most of the application's endpoints, leading to severe false negatives in documentation drift checks. Furthermore, framework paths like `/openapi.json` and `/docs` are automatically excluded from the generated OpenAPI schema.

**Action:** Always parse `app.openapi().get("paths", {})` instead of `app.routes` to reliably enumerate all active API routes in FastAPI applications. Do not manually exclude framework paths, as the OpenAPI generator handles it automatically.
