# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-06-04 - Environment Variable Doc Drift
**Learning:** Using Pydantic Settings model_fields and dynamically prepending the env_prefix is a reliable verification technique to catch undocumented environment variables in the repo.
**Action:** Ensure that any doc claim about available environment variables is verified against the actual configuration loader.
