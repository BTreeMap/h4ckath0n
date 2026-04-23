# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Env var drift check

**Learning:** Environment variables documented in README.md quickly fall out of sync with Settings in src/h4ckath0n/config.py. Parsing README markdown tables for fields is fragile.
**Action:** Instead of manually keeping README.md env vars up-to-date, add descriptions to `pydantic.Field` properties inside `Settings` and write a generation script (`scripts/generate_env_docs.py`) to keep the source of truth entirely in python code, which generates markdown inside `<!-- GENERATED_ENV_VARS_START -->` blocks. Use `--check` flags in CI to prevent drift.
