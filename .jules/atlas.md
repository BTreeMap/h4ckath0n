# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-03-01 - Auto-generate environment tables from Pydantic config

**Learning:** Manually maintained environment variable tables in `README.md` are highly prone to drift. Pydantic `Field` definitions can act as the sole source of truth for variables, defaults, descriptions, and aliases, provided we manage `AliasChoices` effectively.
**Action:** Inject `<!-- START_ENV_VARS -->` markers into the README and use an automated Python script to dump `Settings.model_fields` metadata directly into the document, enforcing drift prevention within CI.
