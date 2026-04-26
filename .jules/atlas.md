# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-05-24 - Env var documentation drift
**Learning:** The `README.md` file previously used a hand-written table to document environment variables defined in `src/h4ckath0n/config.py`. This manual process inevitably leads to drift when new settings are added or defaults changed.
**Action:** Add a generation script `scripts/generate_env_docs.py` to parse pydantic `Settings` and update `README.md`. Ensure `README.md` includes `<!-- GENERATED_ENV_VARS_START -->` and `<!-- GENERATED_ENV_VARS_END -->` markers. Add a CI step `uv run scripts/generate_env_docs.py --check` to enforce parity.
