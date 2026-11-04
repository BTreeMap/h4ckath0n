# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-05-19 - OpenAPI Route Discovery
 **Learning:** When programmatically enumerating routes in recent FastAPI versions, iterating through `app.routes` directly misses endpoints nested within `_IncludedRouter`. `app.openapi().get('paths', {})` reliably retrieves all registered endpoints and their metadata.
 **Action:** Update `scripts/check_doc_routes.py` to use `app.openapi().get("paths", {})` instead of `app.routes`.
## 2024-05-19 - OpenAPI Route Discovery (Correction)
 **Learning:** I previously hallucinated that `app.routes` flattens all endpoints, but in FastAPI 0.115+, `app.routes` DOES indeed contain `_IncludedRouter` objects instead of flattened paths, meaning iterating it blindly misses nested routes. However, my proposed fix of using `app.openapi().get("paths", {})` and iterating over its keys caused a bug because OpenAPI path items can contain non-method keys like `summary`, `description`, etc.
 **Action:** The safest way to extract routes from `app.openapi()` is to filter keys by valid HTTP methods (`get`, `post`, `put`, `patch`, `delete`, `options`, `head`, `trace`).
