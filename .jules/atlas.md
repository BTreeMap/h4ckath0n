# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-05 - Generate configuration documentation from source code
**Learning:** Hardcoding configuration env vars and their defaults in markdown causes them to drift over time. Relying on manually maintained tables in the README leads to inconsistencies where new or changed settings are not documented.
**Action:** Extract configuration fields directly from code (using `pydantic.Field` descriptions and defaults) and inject them into markdown files using markers (`<!-- CONFIG_TABLE_START -->`). Add a CI check to enforce parity.
