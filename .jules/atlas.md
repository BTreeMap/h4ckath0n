# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Env var table drifts from config loader
**Learning:** Hardcoding environment variable tables in README.md inevitably leads to drift as new configuration options are added (like Redis, Storage, and Email).
**Action:** Use `pydantic.Field(description="...")` to document settings directly in `src/h4ckath0n/config.py` and enforce parity by using a documentation generator script running in CI (`scripts/generate_env_docs.py --check`).
