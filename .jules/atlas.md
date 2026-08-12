# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - FastAPI Router Enumeration and Automated Route Docs
**Learning:** In FastAPI (v0.115+), nested routers hide their `.methods` and `.path` inside `_IncludedRouter` objects in `app.routes`, breaking manual iteration for doc drift checks. Additionally, hand-maintained route lists in README files frequently omit new routes.
**Action:** To reliably enumerate all fully registered endpoints, always generate and inspect the OpenAPI schema via `app.openapi().get('paths', {})`. Use this OpenAPI truth not only to check drift, but to directly generate and inject the route documentation into the README using delimited markers.
