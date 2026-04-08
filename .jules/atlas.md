# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-05-18 - Environment Variables Documentation Drift
**Learning:** Configuration environment variables drift easily when documented via manually maintained markdown tables (e.g. README.md missed Redis, Email, Storage settings added to Settings model).
**Action:** Replace handwritten tables with an auto-generated table bracketed by HTML markers, driven by a `scripts/check_doc_env_vars.py` script that parses pydantic `Settings.model_fields` and its `Field(description=...)` metadata.
