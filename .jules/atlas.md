# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Centralize Pydantic V2 config documentation
**Learning:** Hardcoded environment variables in README.md drift out of sync with Pydantic BaseSettings.
**Action:** Centralize environment variable documentation in `Settings` using Pydantic's `Field(description="...")`. Create a generated markdown table bounded by markers (`<!-- CONFIG_START -->` and `<!-- CONFIG_END -->`) and run a drift check script in CI to enforce exact matching.
