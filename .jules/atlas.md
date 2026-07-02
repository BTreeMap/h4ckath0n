# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-06-02 - Pydantic settings env var drift check
**Learning:** Pydantic `Settings` environment variables can easily drift from the documentation table in README.md. Substring matching the README may fail if variable names overlap.
**Action:** Always write a drift script using `Settings.model_fields` and strictly verify exact variable names using backticks (e.g. \`VARIABLE_NAME\`). Handle environment prefixes explicitly.
