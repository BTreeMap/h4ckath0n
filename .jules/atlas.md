# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-08-10 - Replace hand-written API docs with OpenAPI generation
**Learning:** Hand-written API route documentation inevitably drifts. Simple substring checks or basic regexes often fail due to missing routes or changes in summaries. The most reliable verification technique is to parse the authoritative OpenAPI schema, use structural markdown markers (e.g., `<!-- BEGIN API ROUTES -->`), and inject the generated section directly.
**Action:** Replace manual API lists with consolidated, dynamically generated sections from OpenAPI and update drift-check scripts to include a `--fix` flag for automatic alignment.
