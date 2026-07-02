# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2025-05-01 - Prevent Configuration Drift

**Learning:** Env vars and configuration tables in documentation easily drift from the source of truth (`pydantic` models). While `scripts/generate_env_docs.py` existed in my head, the actual script didn't exist in the repo.
**Action:** When updating config docs, use a generated table powered by the config loader or add a check in CI that generates and compares the docs to prevent drift.
