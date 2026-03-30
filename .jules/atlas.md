# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Prevent documentation drift for configuration
**Learning:** Environment variables documented in README.md can easily fall out of sync with the actual `pydantic-settings` model.
**Action:** Generate the configuration table directly from code (e.g., using `pydantic.Field` descriptions) and inject it into markdown files via HTML comment markers. Pair this with a CI check (`--check`) to fail builds if the documentation is out-of-sync.
