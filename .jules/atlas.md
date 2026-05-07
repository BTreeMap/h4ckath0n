# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2025-05-07 - Generate env vars table from pydantic.Field
**Learning:** Environment variable descriptions in README.md quickly drift from the actual settings configuration in `src/h4ckath0n/config.py` when managed manually.
**Action:** Always prefer dynamically generating markdown tables of config properties by reading defaults and descriptions directly from Python type declarations and using explicit doc-generation scripts protected by CI drift checks.
