# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-02-28 - Env vars drift check prevents forgotten configuration docs

**Learning:** When new configuration variables are added to a Pydantic `Settings` model, developers frequently forget to document them in `README.md` or `.env.example`. This leads to a severe drift between the repo's behavior and the documentation.
**Action:** Always maintain a docs drift check script (like `check_env_vars.py`) that parses the Pydantic `Settings` class and validates that every field is explicitly documented in the README table. Integrate this script into the CI pipeline to prevent regressions.
