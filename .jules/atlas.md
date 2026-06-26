# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-06-26 - Generate config documentation from Pydantic models
**Learning:** Hard-coded configuration tables in `README.md` drift quickly from the single source of truth in `src/h4ckath0n/config.py` as settings are added or modified.
**Action:** Use Pydantic V2's `Field(default=..., description="...")` inside the `BaseSettings` class, and run a script to dynamically generate the markdown table and inject it between markers (`<!-- CONFIG_START -->`) in the `README.md`. Add a CI step that regenerates the docs and fails (`git diff --exit-code`) if drift is detected.
