# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-06-25 - FastAPI nested routers cause missed API routes in drift checks
**Learning:** `app.routes` in FastAPI includes nested `APIRouter` objects (represented internally as `_IncludedRouter`), which do not expose `.path` and `.methods` directly. Iterating over `app.routes` and skipping items without `.path` silently misses all endpoints mounted via nested routers (e.g. `/auth/passkey/*`).
**Action:** When validating or extracting API routes in FastAPI, always generate and inspect the OpenAPI schema (`app.openapi()["paths"]`) instead of recursively walking the internal routing tree, as it is a more reliable source of truth for the fully registered endpoints.
