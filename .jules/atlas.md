# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Env var docs drift prevention using Pydantic Settings

**Learning:** Environment variable documentation frequently drifts because it's handwritten in the README, while the actual implementation lives in a Pydantic `BaseSettings` class (e.g., `src/h4ckath0n/config.py`).
**Action:** Replace handwritten env var lists with a script (like `generate_env_docs.py`) that introspects the Pydantic Settings fields (via `model_fields` and `pydantic.Field` descriptions) to automatically generate the markdown table. Inject this table between HTML comment markers (`<!-- BEGIN ENV VARS -->` and `<!-- END ENV VARS -->`) and add a `--check` flag to the script. Enforce this check in the CI pipeline to completely eliminate config documentation drift.
