# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Environment variable documentation drift
**Learning:** It is easy for the configuration table in README.md to drift from the actual `Settings` model in `src/h4ckath0n/config.py`.
**Action:** Implement a drift check script that dynamically parses `Settings.model_fields` and verifies that every field (with the appropriate env prefix) is explicitly documented in backticks in the README.
