# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2025-04-11 - Generate environment variable docs from config
**Learning:** Configuration docs (like env vars) manually written in READMEs frequently drift from the actual source code. The `Settings` model in pydantic can store descriptions, which we can parse dynamically to auto-generate the README env var table.
**Action:** Add `Field(..., description="...")` to the `Settings` model, create a verification script (`check_doc_env_vars.py`), and use markdown markers in `README.md` to embed the auto-generated documentation. Add this verification step to the project's quality checks.
