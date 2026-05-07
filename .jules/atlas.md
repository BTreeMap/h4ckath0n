# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-05-24 - Configuration Docs Drift Prevention
**Learning:** Environment-driven configuration managed via `pydantic-settings` in `src/h4ckath0n/config.py` easily drifts from the manually maintained configuration table in `README.md` (e.g., missing 10+ settings like `storage_backend` and `redis_url`).
**Action:** Prevent documentation drift by generating configuration tables directly from `pydantic.Field` descriptions and injecting them into `README.md` via HTML comment markers (`<!-- CONFIG_TABLE_START -->` and `<!-- CONFIG_TABLE_END -->`). Always pair this with a CI check (`--check`) to fail builds if the documentation is out-of-sync.
