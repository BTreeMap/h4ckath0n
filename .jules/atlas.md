# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Consolidate manual lists with auto-generated OpenAPI / Settings blocks
**Learning:** Hand-written tables for configuration vars and hand-written lists for API routes reliably drift as new fields are added or path summaries change. Basic grep-based drift checks are hard to maintain and still allow out-of-order or duplicate entries.
**Action:** Replace hand-written documentation lists with single, consolidated sections generated dynamically from the authoritative source (OpenAPI schema, config loader). Use structural markdown markers (e.g., `<!-- BEGIN API ROUTES -->`) and ensure the corresponding drift-check script includes a `--fix` flag to automatically populate and verify these sections.
