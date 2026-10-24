# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - OpenAPI generation for route documentation
**Learning:** Hardcoded API route lists in README drift quickly. The FastAPI `app.openapi()` method can be used to extract the source of truth for all routes (including optional ones depending on settings) and generate a markdown table.
**Action:** Replace hardcoded endpoint lists with generated markdown tables, and enforce this via an update/check script using `<!-- route-table-start -->` markers.
