# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2025-04-07 - Generate Env Vars Documentation from Pydantic Fields
**Learning:** Hardcoded environment variables in README.md are a recurring source of drift. Descriptions and default values get out of sync with `src/h4ckath0n/config.py`.
**Action:** Use `pydantic.Field` to colocate descriptions with configuration properties in `Settings`. Use `scripts/check_doc_env_vars.py` to generate the markdown table dynamically and enforce parity in CI using `<!-- BEGIN ENV VARS -->` markers.
