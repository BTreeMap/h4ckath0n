# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2023-10-27 - Using strict typing in generator scripts
**Learning:** Type checkers (like mypy) run in the CI pipeline will fail if generic python functions (like `any`) are used as type hints. The proper type hint from the `typing` module (e.g., `typing.Any`) must be used.
**Action:** Always use strict typing imports, and double check type hints when creating or modifying generation scripts like `check_doc_env.py` to prevent mypy CI failures.
