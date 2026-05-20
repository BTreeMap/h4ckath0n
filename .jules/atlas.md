# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-24 - Prevent documentation drift for configuration by generating it from code

**Learning:** Manual environment variable configuration tables in `README.md` are highly prone to drift. Generating them from `pydantic.Field` descriptions and using HTML comment markers (`<!-- CONFIG_TABLE_START -->`) to inject them provides an automated single source of truth.
**Action:** Prevent documentation drift for configuration by generating it directly from code (using `pydantic.Field` metadata) and injecting it into markdown files via HTML markers. Always pair this with a CI check (`--check`) to fail builds if the documentation is out-of-sync.
