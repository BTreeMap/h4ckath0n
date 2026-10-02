# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2023-10-24 - Drift-prevention for OpenAPI routes
**Learning:** Checking for routes based on substrings and hardcoded scripts is prone to false positives/negatives. Directly pulling `paths` from `app.openapi()` and generating a markdown table to assert against `README.md` is a much more robust verification technique.
**Action:** When verifying API route documentation, use `app.openapi()` to read metadata and use full string matches instead of regex substrings. Use `<!-- START ... -->` markers in Markdown for reliable replacement scripts.
