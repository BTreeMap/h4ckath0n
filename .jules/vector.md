## 2024-04-19 - Centralize scope parsing/formatting helper
**Learning:** String parsing logic for comma-separated tokens (like `user.scopes.split(",")`) is duplicated and manually reimplemented across `auth/dependencies.py`, `auth/session_router.py`, and `cli.py`, violating DRY and increasing the risk of subtle divergence in trim/filter/deduplication behavior.
**Action:** Extract a `parse_scopes`, `format_scopes`, and `iter_scopes` into a new `src/h4ckath0n/auth/scopes.py` helper to create a pure, composable single source of truth that avoids scattered mutation and inconsistent list comps.
