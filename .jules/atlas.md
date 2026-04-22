# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-04-22 - Automated env var docs from Pydantic config

**Learning:** Manual configuration tables in READMEs quickly fall out of sync with actual environment variable loading (in this case, Pydantic's `BaseSettings`). This causes painful onboarding for contributors unaware of undocumented settings (e.g., SMTP or Redis configuration fields added but not documented).
**Action:** Replace handwritten tables with a generated table driven by Pydantic's `Field(description="...")`. Add a CI step running a script like `scripts/generate_env_docs.py --check` to catch out-of-sync configuration docs on push.
