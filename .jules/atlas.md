# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - OpenAPI schema generation prevents duplicate doc drift
**Learning:** Scattered handwritten lists of API endpoints in the README (e.g., separate sections for Passkeys, Password auth, and built-in routes) invariably drift from the actual code.
**Action:** Consolidate API endpoint documentation into a single markdown section generated directly from the live OpenAPI schema, using script markers and a `--fix` drift prevention check to guarantee parity.
