# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2023-10-25 - Environment variable documentation drift

**Learning:** Environment variables frequently drift from their documented state as new settings are added to configuration models (like Pydantic's `Settings`). This leads to incomplete documentation where required or optional configurations are not discoverable.
**Action:** Always use a drift prevention script that dynamically parses the configuration source of truth (e.g., `Settings.model_fields`), applies the relevant prefix, and enforces that the specific variable string enclosed in backticks exists in the README or appropriate documentation file.
