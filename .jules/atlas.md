# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-02 - Hand-written route lists are prone to drift

**Learning:** Hand-written lists of API routes in the README are highly susceptible to documentation drift, especially as routes change, get added, or removed.

**Action:** Replace hand-written API route lists in markdown files with dynamically generated lists delimited by HTML comments (e.g., `<!-- BEGIN ROUTES -->`), populated programmatically via `app.openapi().get('paths', {})` to prevent documentation drift.
