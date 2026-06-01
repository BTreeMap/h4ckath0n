# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-03-01 - Generate Environment Variables Table in Docs
**Learning:** Configuration environment variables drift often between the code (e.g. `h4ckath0n/config.py`) and the README table. Pydantic Fields provide a way to store descriptions alongside the models.
**Action:** Implemented a `check_doc_env_vars.py` script running in CI to parse pydantic `Field` attributes and verify/update the `README.md` generated table automatically.
