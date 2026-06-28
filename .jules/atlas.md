# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2025-06-28 - Generate env var docs from Pydantic config
**Learning:** Env vars drift heavily when Pydantic config adds/modifies attributes and manual tables are left unchanged (e.g. README configuration table was severely outdated with many missing variables like Redis, jobs, storage, email).
**Action:** When auditing configuration docs for drift, replace handwritten tables with generated blocks using a script that parses `Settings.model_fields`, accesses `pydantic.Field` descriptors for defaults/descriptions, and runs in CI as a `--check` flag.
