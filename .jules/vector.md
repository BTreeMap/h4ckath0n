## 2025-05-07 - Extract parse_scopes and format_scopes pure functions
**Learning:** The codebase had duplicated and ad-hoc logic for normalizing and de-duplicating comma-separated string `scopes` across `src/h4ckath0n/cli.py`, `src/h4ckath0n/auth/session_router.py`, and `src/h4ckath0n/auth/dependencies.py`.
**Action:** Extract the scope parsing and formatting logic into pure functional helpers `parse_scopes` and `format_scopes` in `h4ckath0n.auth.schemas` to provide a single, deterministic source of truth.
