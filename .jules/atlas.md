# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2025-04-27 - Generate env vars doc from config loader
**Learning:** Environment variables documented in README.md naturally drift from `pydantic-settings` classes. A generated approach parsing `pydantic.Field` properties with a CI `--check` mode enforces 100% parity and prevents outdated or missed documentation.
**Action:** Always parse configuration loaders directly to generate configuration documentation instead of manually copying the definitions to markdown files. Use explicit markers in README files and add CI steps to enforce validation.
