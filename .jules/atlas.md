# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-07-12 - FastAPI nested routes hiding in older enumeration methods
**Learning:** Iterating over `app.routes` in FastAPI >= 0.115.0 misses routes added via `include_router` because they are nested inside `_IncludedRouter` objects. This causes false positives in documentation drift checks.
**Action:** To accurately enumerate all flattened API paths for drift checks, parse the generated OpenAPI schema (`app.openapi().get('paths', {})`) instead of `app.routes`.

## 2024-07-12 - Ensure Pydantic Settings drift prevention
**Learning:** Configuration defined in `pydantic-settings` `BaseSettings` classes frequently drifts from the `README.md` documentation when new settings are added without updating the docs.
**Action:** Implement a CI script that iterates over `Settings.model_fields`, constructs the expected environment variable names, and asserts their explicit presence in the documentation.
