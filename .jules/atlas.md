# Atlas Journal: Critical Learnings

## 2026-03-01 - Prevent config doc drift by generating from source

**Learning:** Configuration documentation in READMEs often drifts from the actual settings loaded by the application (e.g., missing env vars, incorrect defaults). Hand-maintained tables are prone to failure.

**Action:** Centralise configuration in `pydantic-settings` (`config.py`), document fields using `pydantic.Field(description="...")`, and use a script (`scripts/generate_doc_config.py`) to generate the markdown table and inject it between `<!-- CONFIG_TABLE_START -->` and `<!-- CONFIG_TABLE_END -->` markers. Run the script with `--check` in CI to fail builds if the documentation is out-of-sync.

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
