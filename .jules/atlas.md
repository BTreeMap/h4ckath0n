# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Environment variable docs drifting from configuration schema
**Learning:** Hardcoded environment variable tables in READMEs quickly drift from the Pydantic `Settings` schema, especially when new defaults or properties are added. Several `h4ckath0n` specific fields (Redis, Storage, Email, Demo) were missing from the documentation.
**Action:** Embed documentation directly via `pydantic.Field(description="...")` in the `Settings` class and dynamically inject the markdown table into the README using `<!-- BEGIN/END ENV VARS -->` markers and an automated script.
