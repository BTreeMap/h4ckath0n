# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-05-18 - Replacing hand-written API endpoints in README
**Learning:** Hand-written API endpoints in `README.md` can easily cause documentation drift and false positives when they duplicate endpoints or are manually formatted.
**Action:** Extracting live routes from FastAPI's OpenAPI schema (`app.openapi().get('paths', {})`) and generating a markdown table enclosed in HTML comments (like `<!-- route-table-start -->` and `<!-- route-table-end -->`) prevents documentation drift.
