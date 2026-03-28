# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-28 - Drift prevention for configuration documentation
**Learning:** Hardcoded documentation for configuration options drifts away from the actual `BaseSettings` over time, leading to missing or incorrectly described options.
**Action:** Use Pydantic's `Field(..., description="...")` in the code, and extract `model_fields` to automatically generate the documentation table using markers (e.g. `<!-- CONFIG_TABLE_START -->`). Safely check for `PydanticUndefinedType` as Pydantic uses it for missing defaults.
