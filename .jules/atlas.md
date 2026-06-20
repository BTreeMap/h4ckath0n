# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Config docs drift prevention
**Learning:** Hardcoding config variables in a README markdown table leads to drift as the `Settings` class grows. For this repo, parsing `Settings.model_fields` and using `pydantic.Field` descriptions allows full generation of the config documentation.
**Action:** Use a script to extract env variables and default settings from `Settings.model_fields` in `src/h4ckath0n/config.py`. Enclose the README config section with HTML comments (`<!-- CONFIG_DOCS_START -->` and `<!-- CONFIG_DOCS_END -->`) and write the parsed content in between, then run this check in CI.
