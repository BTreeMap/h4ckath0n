# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Env var drift prevention via Settings.model_fields

**Learning:** Environment variables documented in READMEs often drift from the actual application configuration. Pydantic's `Settings.model_fields` is the source of truth for the config schema in this repository.

**Action:** Write scripts that extract all expected environment variables directly from `Settings.model_fields` and verify that they are mentioned in the `README.md` to guarantee documentation parity.
