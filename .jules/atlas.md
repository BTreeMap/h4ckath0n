# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-03-05 - Centralizing env var documentation in Pydantic models
**Learning:** Hardcoding environment variables in `README.md` without automated generation leads to documentation drift as variables are added or defaults change. Furthermore, having a single list of env vars makes it hard to generate `.env.example` consistently.
**Action:** Embed descriptions directly in the Pydantic `Settings` model using `Field(default, description='...')`. Use a script to automatically generate both the markdown documentation and `.env.example` files from the codebase, delimited by markers (`<!-- START_ENV -->` etc.), preventing drift.
