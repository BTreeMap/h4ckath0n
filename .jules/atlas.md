# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-04-19 - Generate Config Docs from Pydantic
**Learning:** Hardcoded environment variable lists in READMEs drift easily from the actual configuration fields.
**Action:** Use `Settings.model_fields` to programmatically extract descriptions and defaults, outputting them between markdown markers in the README, and add a CI step to enforce parity.
