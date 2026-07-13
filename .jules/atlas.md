# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Add drift check for settings environment variables

**Learning:** Environment variables in settings often drift because developers forget to document new config additions. Using Pydantic's `Settings.model_fields` provides an automated way to compare code expectations against README claims.
**Action:** Always write a check script iterating over `model_fields` to verify environment variable documentation parity when configuration uses Pydantic.
