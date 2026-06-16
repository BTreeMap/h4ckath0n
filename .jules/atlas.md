# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-05-04 - Env var documentation frequently drifts

**Learning:** Manually keeping `README.md` in sync with `src/h4ckath0n/config.py` environment variables leads to omitted variables (e.g., Redis, Email, Storage settings were missing). Pydantic allows defining descriptions on fields themselves using `Field(description="...")`.

**Action:** Treat the Pydantic `Settings` model as the source of truth for both code and documentation. Use `scripts/generate_env_docs.py` to parse Pydantic `Field` descriptions and automatically generate/check the `README.md` table in CI between `<!-- BEGIN ENV VARS -->` and `<!-- END ENV VARS -->` markers.
