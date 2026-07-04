# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2025-01-20 - Missing Configuration Documentation
**Learning:** Environment variables in Pydantic settings easily drift from the README. Validating env var names via introspection (Settings.model_fields) and regex matching against markdown prevents this.
**Action:** Enforce programmatic drift checks against README documentation for all Pydantic settings configurations by adding a check script in CI.
