# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Config field drift without automation

**Learning:** Environment variables and settings drift silently when not programmatically synced with documentation. Checking whether a Pydantic `Settings` model's fields are documented prevents configuration options from becoming "hidden knowledge".

**Action:** Always generate or explicitly check Pydantic model configuration fields against their documentation counterparts using a CI script.
