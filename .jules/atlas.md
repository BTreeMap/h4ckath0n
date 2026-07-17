# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2025-02-14 - Replace manual endpoint lists with generated OpenAPI table
**Learning:** Documentation of API routes drifts reliably when hand-written. Replacing them with an OpenAPI-generated table wrapped in HTML comments, enforced by a CI script calling the generator with `--check`, prevents drift.
**Action:** Always prefer generating API endpoint documentation dynamically from the OpenAPI schema and enforce accuracy in CI.
