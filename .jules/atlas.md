# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-05-18 - Environment variable table drift

**Learning:** Hand-written tables of environment variables in READMEs drift heavily from Pydantic config models, especially when new features (like Storage or Email) add new settings that the docs miss.
**Action:** Always generate environment variable markdown tables directly from `pydantic.Field` descriptions and add a CI check (`--check`) to ensure the README remains in sync with the source code.
