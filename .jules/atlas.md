# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Pydantic settings are prone to undocumented environment variables

**Learning:** Configuration drift commonly happens when fields are added to `Settings` (pydantic-settings) but are not added to `README.md`. It is crucial to have a drift prevention check that ensures all fields mapped to environment variables are explicitly mentioned in the documentation.
**Action:** Iterate over the `Settings.model_fields` dictionary to construct the expected environment variable names and ensure they appear in the markdown documentation.
