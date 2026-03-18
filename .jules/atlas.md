# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Environment variable configuration drift is preventable

**Learning:** Manually keeping a markdown table of environment variables in sync with an app's configuration model (`src/h4ckath0n/config.py`) is error-prone and leads to missing or inaccurate settings descriptions. By defining `pydantic` fields (`Field(default=..., description="...")`), the codebase itself acts as the single source of truth.

**Action:** Add drift-prevention scripts (e.g. `scripts/generate_doc_config.py --check`) to verify configuration documentation against `pydantic-settings` classes. Use markers like `<!-- CONFIG_TABLE_START -->` to safely generate and inject documentation automatically.
